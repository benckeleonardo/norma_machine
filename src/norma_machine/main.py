import string
from program_loader import load_program
from macro import MacroLoader
from machine import Machine

if __name__ == "__main__":
    # Carrega programa principal e macros
    program = load_program("programs/example2.nm")
    macros = MacroLoader.load_macros("macros")

    # Pergunta número de registradores
    num_regs = int(input("Quantos registradores? "))
    num_regs = min(num_regs, 26)

    print()  # linha em branco após perguntar número de registradores

    # Pergunta valor inicial de cada registrador
    registers_init = {}
    for reg in string.ascii_lowercase[:num_regs]:
        while True:
            val = input(f"Valor inicial do registrador {reg} (pressione Enter para 0): ").strip()
            if val == "":
                registers_init[reg] = 0
                break
            elif val.isdigit():
                registers_init[reg] = int(val)
                break
            else:
                print("Por favor, digite um número inteiro ou pressione Enter.")

    print()  # linha em branco após todos os registradores

    # Cria máquina e atualiza registradores
    m = Machine(num_regs, program, macros)
    m.registers.update(registers_init)

    # Executa
    m.run()