import os
import re
from instruction import Instruction

class Macro:
    def __init__(self, name, params, instructions):
        self.name = name
        self.params = params
        self.instructions = instructions  # dict de rótulo -> Instruction

    @classmethod
    def parse(cls, path):
        with open(path) as f:
            lines = f.readlines()

        lines = [l.split("#")[0].strip() for l in lines if l.strip() and not l.strip().startswith("#")]
        if not lines:
            raise ValueError(f"Macro vazia: {path}")
        header = lines[0]
        m = re.match(r"(\w+)\(([\w, ]*)\)", header)
        if not m:
            raise ValueError(f"Macro inválida: {header}")

        name = m.group(1)
        params = [x.strip() for x in m.group(2).split(",") if x.strip()]
        instructions = {i.label: i for i in (Instruction.parse(l) for l in lines[1:]) if i}
        return cls(name, params, instructions)


class MacroLoader:
    @staticmethod
    def load_macros(path="macros"):
        macros = []
        if not os.path.exists(path):
            return macros
        for fn in os.listdir(path):
            if fn.endswith(".nm"):
                macros.append(Macro.parse(os.path.join(path, fn)))
        return macros