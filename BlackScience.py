from FactorySizing import InputMaterial, OutputMaterial, IntermediateMaterial, Process, SizeFactory

# Create the list of materials
MaterialsList = [
    InputMaterial('Stone'),
    InputMaterial('Coal'),
    InputMaterial('Iron Plates'),
    InputMaterial('Copper Plates'),
    InputMaterial('Steel Plates'),
    IntermediateMaterial('Stone Brick'),
    IntermediateMaterial('Wall'),
    IntermediateMaterial('Grenade'),
    IntermediateMaterial('Piercing Rounds'),
    IntermediateMaterial('Firearm Magazine'),
    OutputMaterial('Black Science', DesiredOutputRate=250/60),  # 250 per minute
]

# Create the corresponding dictionary of materials
Materials = dict()
for m in MaterialsList:
    Materials[m.Name] = m

# Create the list of processes
ProcessList = [
    Process(
        Name = 'Firearm Magazine Production',
        Equipment = 'Assembly Machine',
        Inputs = {
            'Iron Plates'     :   4,
        },
        Outputs = {
            'Firearm Magazine'     :   1,
        },
        Time = 1
    ),
    Process(
        Name = 'Piercing Rounds Production',
        Equipment = 'Assembly Machine',
        Inputs = {
            'Firearm Magazine'      :   1,
            'Copper Plates'         :   5,
            'Steel Plates'          :   1,
        },
        Outputs = {
            'Piercing Rounds'     :   1,
        },
        Time = 3
    ),
    Process(
        Name = 'Grenade Production',
        Equipment = 'Assembly Machine',
        Inputs = {
            'Iron Plates'     :   5,
            'Coal'            :   10,
        },
        Outputs = {
            'Grenade'     :   1,
        },
        Time = 8
    ),
    Process(
        Name = 'Stone Brick Production',
        Equipment = 'Electric Furnace',
        Inputs = {
            'Stone'     :   2,
        },
        Outputs = {
            'Stone Brick'     :   1,
        },
        Time = 3.2
    ),
    Process(
        Name = 'Wall Production',
        Equipment = 'Assembly Machine',
        Inputs = {
            'Stone Brick'     :   5,
        },
        Outputs = {
            'Wall'     :   1,
        },
        Time = 0.5
    ),
    Process(
        Name = 'Black Science Production',
        Equipment = 'Assembly Machine',
        Inputs = {
            'Wall'              :   2,
            'Grenade'           :   1,
            'Piercing Rounds'   :   1
        },
        Outputs = {
            'Black Science'     :   1,
        },
        Time = 10
    ),
]

# Translate the list of processes into a dictionary
Processes = dict()
for p in ProcessList:
    Processes[p.Name] = p

# Size the factory
SizeFactory(Materials, Processes)