from instruction import Instruction

def load_program(path):
    with open(path) as f:
        lines = f.readlines()
    instructions = {i.label: i for i in (Instruction.parse(l) for l in lines) if i}
    return instructions