from ortools.linear_solver import pywraplp

# Define the material class
class Material():

    def __init__(self, Name, Type):

        self.Name = Name
        self.Type = Type # Input, Output, or Intermediate
        self.NetProductionRate = None # This will be an OR-Tools decision variable representing the net production rate of this material expressed in units per second.

class InputMaterial(Material):

    def __init__(self, Name):
        
        super().__init__(Name, 'Input')

class OutputMaterial(Material):

    def __init__(self, Name, DesiredOutputRate):
        
        super().__init__(Name, 'Output')
        self.DesiredOutputRate = DesiredOutputRate # Expressed in units per second

class IntermediateMaterial(Material):

    def __init__(self, Name):
        
        super().__init__(Name, 'Intermediate')

# Define the process class
class Process():

    def __init__(self, Name, Equipment, Inputs, Outputs, Time):

        self.Name = Name
        self.Equipment = Equipment
        self.Time = Time # the time required to complete the process, in seconds.

        # Make sure all of the input materials are valid
        for m in Inputs:
            if m not in Materials:
                raise Exception('Error: the input %s is not recognized as a valid material.' % m)

        self.Inputs = Inputs # a dictionary mapping material names to quantities

        # Make sure all of the output materials are valid
        for m in Outputs:
            if m not in Materials:
                raise Exception('Error: the output %s is not recognized as a valid material.' % m)

        self.Outputs = Outputs # a dictionary mapping material names to quantities

        self.Number = None # This will be an OR-Tools decision variable representing the number of machines that will be assigned to this process.

# Create the list of materials
MaterialsList = [
    InputMaterial('Crude Oil'),
    InputMaterial('Water'),
    InputMaterial('Coal'),
    IntermediateMaterial('Petroleum Gas'),
    IntermediateMaterial('Heavy Oil'),
    IntermediateMaterial('Light Oil'),
    OutputMaterial('Plastic', DesiredOutputRate=78)
]

# Create the corresponding dictionary of materials
Materials = dict()
for m in MaterialsList:
    Materials[m.Name] = m

# Create the list of processes
ProcessList = [
    Process(
        Name = 'Advanced Oil Processing',
        Equipment = 'Refinery',
        Inputs = {
            'Crude Oil' :   100,
            'Water'     :   50,
        },
        Outputs = {
            'Petroleum Gas' :   55,
            'Heavy Oil'     :   25,
            'Light Oil'     :   45,
        },
        Time = 5
    ),
    Process(
        Name = 'Heavy Oil Cracking',
        Equipment = 'Chemical Plant',
        Inputs = {
            'Heavy Oil' :   40,
            'Water'     :   30,
        },
        Outputs = {
            'Light Oil'     :   30,
        },
        Time = 2
    ),
    Process(
        Name = 'Light Oil Cracking',
        Equipment = 'Chemical Plant',
        Inputs = {
            'Light Oil' :   30,
            'Water'     :   30,
        },
        Outputs = {
            'Petroleum Gas'     :   20,
        },
        Time = 2
    ),
    Process(
        Name = 'Plastic Production',
        Equipment = 'Chemical Plant',
        Inputs = {
            'Petroleum Gas'     :   20,
            'Coal'              :   1,
        },
        Outputs = {
            'Plastic'     :   2,
        },
        Time = 1
    ),
]

# Translate the list of processes into a dictionary
Processes = dict()
for p in ProcessList:
    Processes[p.Name] = p

# Initalize model
Model = pywraplp.Solver.CreateSolver('gurobi')

# Create a decision variable for each process
for p in Processes.values():
    p.Number = Model.IntVar(0, Model.infinity(), p.Name)

# Create a decision variable for the net production rate of each material
for m in Materials.values():
    m.NetProductionRate = Model.NumVar(-Model.infinity(), Model.infinity(), '%s Production Rate (units/s)' % m.Name)

# Create a constraint defining the net production rate for each material
for m in Materials.values():
    Model.Add(
        sum(
            p.Outputs.get(m.Name, 0) / p.Time
            *
            p.Number
            for p in Processes.values()
        )
        -
        sum(
            p.Inputs.get(m.Name, 0) / p.Time
            *
            p.Number
            for p in Processes.values()
        )
        ==
        m.NetProductionRate
    )

# Create a constraint specifying the net production rate of each Output material must be above some specification
for m in Materials.values():
    if m.Type == 'Output':
        Model.Add(
            m.NetProductionRate >= m.DesiredOutputRate
        )

# Create a constraint specifying the net production rate of each Intermediate material must be zero
for m in Materials.values():
    if m.Type == 'Intermediate':
        Model.Add(
            m.NetProductionRate == 0
        )

# Add the objective of minimizing the total number machines
Model.Minimize(
    sum(
        p.Number
        for p in Processes.values()
    )
)

# Enable output
Model.EnableOutput()

# Solve the model
Model.Solve()

# Print the number of machines that should be devoted to each process
print('Process Counts:')
for p in Processes.values():
    print('%s: %d' % (p.Name, p.Number.solution_value()))

# Print the net production rate for each material
print('Net Material Production (units/s):')
for m in Materials.values():
    print('%s: %f' % (m.Name, m.NetProductionRate.solution_value()))