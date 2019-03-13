import re

registers = ["$zero",
             "$at",
             "$v0", "$v1",
             "$a0", "$a1", "$a2", "$a3",
             "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
             "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
             "$t8", "$t9",
             "$k0", "$k1",
             "$gp",
             "$sp",
             "$fp",
             "$ra"]

labels = {}


def main():
    mips_file = open("MIPS.s", "r")
    data_file = open("data.txt", "w+")
    code_file = open("code.txt", "w+")
    content = mips_file.read()
    get_labels(content)

    parts = re.split(".data|.text", content)
    data = parts[1].split("\n")
    code = parts[2].split("\n")
    for i in data:
        machine_code = assemble_data(i)
        if machine_code is not None:
            data_file.write(machine_code)
    for i in code:
        machine_code = assemble_code(i)
        if machine_code is not None:
            code_file.write(machine_code)
    mips_file.close()
    data_file.close()
    code_file.close()


def get_labels(content):
    # TODO: fill labels dictionary
    pass


def assemble_data(instruction_line):
    instruction_line = re.split("#", instruction_line)[0]
    # TODO
    return example_function(instruction_line)


def assemble_code(instruction_line):
    instruction_line = re.split("#", instruction_line)[0]
    instructions = {
        "add": example_function,
        # "add": add_assemble,
        # "and": and_assemble,
        # "sub": sub_assemble,
        # "nor": nor_assemble,
        # "or": or_assemble,
        # "slt": slt_assemble,
        # "addi": addi_assemble,
        # "lw": lw_assemble,
        # "sw": sw_assemble,
        # "beq": beq_assemble,
        # "bne": bne_assemble,
        # "j" : j_assemble,
    }
    match = None
    for i in instructions.keys():
        match = re.search(i + "(?= )", instruction_line)
        if match is not None:
            break
    if match:
        return instructions.get(match.group(0))(instruction_line[match.start():])
    return None


def example_function(instruction_line):
    machine_code = instruction_line.strip() + "\n"
    return machine_code


if __name__ == '__main__':
    main()
