import re

class Instruction:
    def __init__(self, label, action, goto_true=None, goto_false=None):
        self.label = label
        self.action = action
        self.goto_true = goto_true
        self.goto_false = goto_false

    @classmethod
    def parse(cls, line):
        line = line.split("#")[0].strip()  # remove comentários
        if not line:
            return None

        m = re.match(r"(\d+):\s*(.*)", line)
        if not m:
            raise ValueError(f"Sintaxe inválida: {line}")

        label = int(m.group(1))
        expr = m.group(2)

        # Teste if zero(a) goto X else goto Y
        if expr.startswith("if"):
            m = re.match(r"if\s+zero\((\w)\)\s+goto\s+(\d+)\s+else\s+goto\s+(\d+)", expr)
            if not m:
                raise ValueError(f"Sintaxe inválida em teste: {expr}")
            return cls(label, ("if_zero", m.group(1)), int(m.group(2)), int(m.group(3)))

        # Ação add(a) goto X, sub(a) goto X ou macro
        m = re.match(r"(\w+)\(([\w, ]*)\)\s+goto\s+(\d+)", expr)
        if not m:
            raise ValueError(f"Sintaxe inválida em ação: {expr}")
        name = m.group(1)
        args = [x.strip() for x in m.group(2).split(",") if x.strip()]
        return cls(label, (name, args), int(m.group(3)))
