import string


class Machine:
    def __init__(self, num_registers, program, macros):
        # inicializa registradores (a, b, c, ...) com 0
        self.registers = {ch: 0 for ch in string.ascii_lowercase[:num_registers]}
        self.program = program
        self.macros = {m.name: m for m in macros}
        self.stack = []

    def run(self):
        pc = 1  # programa principal sempre começa no rótulo 1

        while True:
            # Determina contexto atual (programa principal ou macro)
            if not self.stack:
                instr_set = self.program
                pc_key = pc
                context = f"{pc}"
                param_map = None
            else:
                top = self.stack[-1]
                instr_set = top['macro'].instructions
                pc_key = top['pc']
                context = f"{top['macro'].name}:{pc_key}"
                param_map = top['param_map']

            # Se rótulo não existe
            if pc_key not in instr_set:
                if self.stack:
                    # finaliza macro
                    finished = self.stack.pop()
                    print(
                        f"({finished['caller_context']}, {format_registers(self.registers)}) "
                        f"Finalizou a macro {finished['macro'].name}({', '.join(finished['param_map'].values())}) "
                        f"e desviou para {finished['return_pc']}"
                    )
                    # volta para o rótulo de retorno
                    if self.stack:
                        self.stack[-1]['pc'] = finished['return_pc']
                    else:
                        pc = finished['return_pc']
                    continue
                else:
                    print(f"({pc}, {format_registers(self.registers)}) Execução finalizada")
                    break

            instr = instr_set[pc_key]
            action = instr.action

            # Se instrução é teste if zero
            if action[0] == "if_zero":
                reg = action[1]
                real_reg = param_map[reg] if param_map else reg
                if self.registers[real_reg] == 0:
                    print(
                        f"({context}, {format_registers(self.registers)}) "
                        f"Como {reg} == 0 desviou para {instr.goto_true}"
                    )
                    next_pc = instr.goto_true
                else:
                    print(
                        f"({context}, {format_registers(self.registers)}) "
                        f"Como {reg} <> 0 desviou para {instr.goto_false}"
                    )
                    next_pc = instr.goto_false

            else:
                name, args = action
                # mapeia argumentos para registradores reais
                real_args = [param_map[a] if param_map else a for a in args]

                if name == "add":
                    print(
                        f"({context}, {format_registers(self.registers)}) "
                        f"Adicionou no registrador {real_args[0]} e desviou para {instr.goto_true}"
                    )
                    self.registers[real_args[0]] += 1
                    next_pc = instr.goto_true

                elif name == "sub":
                    print(
                        f"({context}, {format_registers(self.registers)}) "
                        f"Subtraiu do registrador {real_args[0]} e desviou para {instr.goto_true}"
                    )
                    self.registers[real_args[0]] -= 1
                    next_pc = instr.goto_true

                elif name in self.macros:
                    macro = self.macros[name]
                    if len(real_args) != len(macro.params):
                        raise ValueError(f"Número de parâmetros incorreto na macro {name}")
                    # Cria contexto da macro
                    self.stack.append({
                        'macro': macro,
                        'param_map': dict(zip(macro.params, real_args)),
                        'return_pc': instr.goto_true,
                        'pc': 1,
                        'caller_context': context  # <- guarda o contexto atual (main:2, teste:2, etc.)
                    })
                    print(
                        f"({context}, {format_registers(self.registers)}) "
                        f"Iniciou a macro {name}({', '.join(real_args)})"
                    )
                    next_pc = 1  # inicia macro no rótulo 1
                else:
                    raise ValueError(f"Instrução desconhecida: {name}")

            # atualiza PC
            if self.stack:
                self.stack[-1]['pc'] = next_pc
            else:
                pc = next_pc

def format_registers(registers):
    """Formata os registradores de forma amigável."""
    vals = list(registers.values())
    if len(vals) == 1:
        return f"({vals[0]})"
    return str(tuple(vals))