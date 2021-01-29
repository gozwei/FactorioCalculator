from FactorySizing import InputMaterial, OutputMaterial, IntermediateMaterial, Process, SizeFactory

# Create the list of materials
MaterialsList = [
    InputMaterial('Crude Oil'),
    InputMaterial('Water'),
    InputMaterial('Copper Plates'),
    InputMaterial('Iron Plates'),
    IntermediateMaterial('Heavy Oil'),
    IntermediateMaterial('Light Oil'),
    IntermediateMaterial('Petroleum Gas'),
    OutputMaterial('Sulfur', DesiredOutputRate=500/60),
    OutputMaterial('Sulfuric Acid', DesiredOutputRate=5000/60),
    OutputMaterial('Lubricant', DesiredOutputRate=500/60),
    OutputMaterial('Batteries', DesiredOutputRate=250/60),
]

# Create the corresponding dictionary of materials
Materials = dict()
for m in MaterialsList:
    Materials[m.Name] = m

# Create the list of processes
ProcessList = [
    Process(
        Name = 'Battery Production',
        Equipment = 'Chemical Plant',
        Inputs = {
            'Sulfuric Acid'     :   20,
            'Iron Plates'       :   1,
            'Copper Plates'     :   1,
        },
        Outputs = {
            'Batteries'         :   1
        },
        Time = 4
    ),
    Process(
        Name = 'Sulfuric Acid Production',
        Equipment = 'Chemical Plant',
        Inputs = {
            'Iron Plates'       :   1,
            'Sulfur'            :   5,
            'Water'             :   100,
        },
        Outputs = {
            'Sulfuric Acid'     :   50,
        },
        Time = 1
    ),
    Process(
        Name = 'Sulfur Production',
        Equipment = 'Chemical Plant',
        Inputs = {
            'Water'         :   30,
            'Petroleum Gas' :   30,
        },
        Outputs = {
            'Sulfur'        :   2,
        },
        Time = 1
    ),
    Process(
        Name = 'Advanced Oil Processing',
        Equipment = 'Refinery',
        Inputs = {
            'Crude Oil'     :   100,
            'Water'         :   50,
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
            'Heavy Oil'     :   40,
            'Water'         :   30,
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
            'Light Oil'     :   30,
            'Water'         :   30,
        },
        Outputs = {
            'Petroleum Gas' :   20,
        },
        Time = 2
    ),
    Process(
        Name = 'Lubricant Production',
        Equipment = 'Chemical Plant',
        Inputs = {
            'Heavy Oil'     :   10,
        },
        Outputs = {
            'Lubricant'     :   10,
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