from FactorySizing import InputMaterial, OutputMaterial, IntermediateMaterial, Process, SizeFactory

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

# Size the factory
SizeFactory(Materials, Processes)