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


def main():
    mips_file = open("MIPS.s", "r")
    data_file = open("data.txt", "w+")
    code_file = open("code.txt", "w+")
    content = mips_file.read()
    labels = get_labels(content)

    parts = re.split(".data|.text", content)
    data = parts[1].strip().split("\n")
    code = parts[2].strip().split("\n")
    for i in data:
        data_file.write(assemble_data(i))
    for i in code:
        if assemble_code(i) is not None:
            code_file.write(assemble_code(i))
    mips_file.close()
    data_file.close()
    code_file.close()


def get_labels(content):
    labels = dict()
    # TODO: get labels and store it in dictionary key = label name, value = address and return it
    return labels


def assemble_data(instruction_line):
    # TODO
    return example_function(instruction_line)


def assemble_code(instruction_line):
    instructions = {
        "ex": example_function(instruction_line),
        # "add": add_assemble(instruction_line),
        # "and": and_assemble(instruction_line),
        # "sub": sub_assemble(instruction_line),
        # "nor": nor_assemble(instruction_line),
        # "or": or_assemble(instruction_line),
        # "slt": slt_assemble(instruction_line),
        # "addi": addi_assemble(instruction_line),
        # "lw": lw_assemble(instruction_line),
        # "sw": sw_assemble(instruction_line),
        # "beq": beq_assemble(instruction_line),
        # "bne": bne_assemble(instruction_line),
        # "j" : j_assemble(instruction_line),
    }
    instruction_line = re.split("#", instruction_line)[0]
    match = re.search("[a-z]+(?= )", instruction_line)
    if match:
        return instructions.get(match.group(0))
    return None


def example_function(instruction_line):
    machine_code = instruction_line
    return machine_code


if __name__ == '__main__':
    main()
