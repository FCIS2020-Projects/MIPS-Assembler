import re


class Assembler:
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

    def __init__(self, mips_file_path, data_file_path, code_file_path):
        mips_file = open(mips_file_path, "r")
        data_file = open(data_file_path, "w+")
        code_file = open(code_file_path, "w+")

        self.content = mips_file.readlines()
        self.clean_file()
        self.labels = self.get_labels()
        data_index = self.content.index(".data\n")
        code_index = self.content.index(".text\n")
        self.data = self.content[data_index + 1:code_index]
        self.code = self.content[code_index + 1:]

        machine_code = self.assemble_data()
        data_file.write(machine_code)

        machine_code = self.assemble_code()
        code_file.write(machine_code)
        mips_file.close()
        data_file.close()
        code_file.close()

    def clean_file(self):
        output = []
        for i in self.content:
            i = i.split("#")[0]
            if re.search(r"\w", i):
                output.append(i.strip() + "\n")
        self.content = output

    def get_labels(self):
        labels = {}
        line = 0
        regex = r"([a-zA-Z_][a-zA-Z0-9_]*):"
        for item in self.content:
            # print(line,"\t",item)
            if re.findall(regex, item):
                matches = re.findall(regex, item)
                for match in matches:
                    if match in labels.keys():
                        print("Label %s already Exist" % match)
                    else:
                        labels[match] = line
            line += 1
        return labels

    def assemble_data(self):
        machine_code = ""
        for i in self.data:
            machine_code += i
        return machine_code

    def assemble_code(self):
        instructions = {
            "add": self.add_assemble,
            "and": self.and_assemble,
            # "sub": self.sub_assemble,
            # "nor": self.nor_assemble,
            # "or": self.or_assemble,
            # "slt": self.slt_assemble,
            # "addi": self.addi_assemble,
            # "lw": self.lw_assemble,
            # "sw": self.sw_assemble,
            # "beq": self.beq_assemble,
            # "bne": self.bne_assemble,
            # "j" : self.j_assemble,
        }
        machine_code = ""
        for i in self.code:
            match = None
            for j in instructions.keys():
                match = re.search(j + "(?= )", i)
                if match is not None:
                    break

            if match:
                machine_code += instructions.get(match.group(0))(i[match.start():])
        return machine_code

    def rs_rt_rd(self, instruction_line):
        add_line = re.split(r",\s*|\s", instruction_line)

        rd = self.registers.index(str(add_line[1]).strip())
        rs = self.registers.index(str(add_line[2]).strip())
        rt = self.registers.index(str(add_line[3]).strip())

        return rs, rt, rd

    def add_assemble(self, instruction_line):

        rs, rt, rd = self.rs_rt_rd(instruction_line)
        mc_ode = bin(0).replace("0b", "").zfill(6) + bin(rs).replace("0b", "").zfill(5) + \
                 bin(rt).replace("0b", "").zfill(5) + bin(rd).replace("0b", "").zfill(5) + \
                 bin(0).replace("0b", "").zfill(5) + bin(32).replace("0b", "").zfill(6) + "\n"
        return mc_ode

    def and_assemble(self, instruction_line):
        rs, rt, rd = self.rs_rt_rd(instruction_line)

        mc_ode = bin(0).replace("0b", "").zfill(6) + bin(rs).replace("0b", "").zfill(5) + \
                 bin(rt).replace("0b", "").zfill(5) + bin(rd).replace("0b", "").zfill(5) + \
                 bin(0).replace("0b", "").zfill(5) + bin(34).replace("0b", "").zfill(6) + "\n"
        return mc_ode


Assembler("MIPS.asm", "data.txt", "code.txt")
