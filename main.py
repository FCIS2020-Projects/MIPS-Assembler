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
        data_index = self.content.index(".data\n")
        code_index = self.content.index(".text\n")
        self.data = self.content[data_index + 1:code_index]
        self.code = self.content[code_index + 1:]
        self.code_labels = self.get_code_labels()
        self.data_labels = self.get_data_labels()

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

    def get_data_labels(self):
        labels = {}
        line = 0
        regex = r"([a-zA-Z_][a-zA-Z0-9_]*):"
        for item in self.data:
            if re.findall(regex, item):
                matches = re.findall(regex, item)
                for match in matches:
                    if match in labels.keys():
                        print("Label %s already Exist" % match)
                    else:
                        labels[match] = line
            match = re.search(r"(\.\w+) (.*)", item)

            if match[1] == ".word":
                line += 4 * len(match[2].split(","))
            elif match[1] == ".space":
                line += 4 * int(match[2])

        return labels

    def get_code_labels(self):
        labels = {}
        line = 0
        regex = r"([a-zA-Z_][a-zA-Z0-9_]*):"
        for item in self.code:
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
            match = re.search(r"(\.\w+) (.*)", i)
            if match[1] == ".word":
                values = match[2].split(",")
                for j in range(0, len(values)):
                    machine_code += bin(int(values[j])).replace("0b", "").zfill(32) + "\n"
            elif match[1] == ".space":
                for j in range(0, int(match[2])):
                    machine_code += "".ljust(32, "X") + "\n"
        return machine_code

    def assemble_code(self):
        instructions = {
            "add": self.add_assemble,
            "and": self.and_assemble,
            "sub": self.sub_assemble,
            "nor": self.nor_assemble,
            "or": self.or_assemble,
            "slt": self.slt_assemble,
            "lw": self.lw_assemble,
            "sw": self.sw_assemble,
            "addi": self.addi_assemble,
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
                machine_code += instructions.get(match[0])(i[match.start():])
        return machine_code

    def Get_R_Operands(self, instruction_line):
        line = re.split(r"\s*,\s*|\s", instruction_line)

        rd = self.registers.index(str(line[1]).strip())
        rs = self.registers.index(str(line[2]).strip())
        rt = self.registers.index(str(line[3]).strip())
        return rs, rt, rd

    def Get_I_Operands(self, instruction_line):
        line = {}
        line = re.split(r" |\s*,\s*|[()]", instruction_line)
        while '' in line: line.remove('')
        #line = re.search(r'(lw|sw)\s*(\$\w*)\s*,\s*(\w*)[(](\$\w*)[)]\n', instruction_line)
        if(line[0] == 'addi'):line[3], line[2] = line[2], line[3]
        dict = self.get_data_labels()
        if line[2] in dict:
            line[2] = dict.get(line[2])
        rs = self.registers.index(str(line[3]).strip())
        rt = self.registers.index(str(line[1]).strip())
        im = int(str(line[2]).strip())
        return rs, rt, im

    def R_Machine_Code(self,instruction_line, func):
        rs, rt, rd = self.Get_R_Operands(instruction_line)
        R_machinecode = bin(0).replace("0b", "").zfill(6) + bin(rs).replace("0b", "").zfill(5) + \
                 bin(rt).replace("0b", "").zfill(5) + bin(rd).replace("0b", "").zfill(5) + \
                 bin(0).replace("0b", "").zfill(5) + bin(func).replace("0b", "").zfill(6) + "\n"
        return R_machinecode

    def I_Machine_Code(self,instruction_line, func):
        rs, rt, im = self.Get_I_Operands(instruction_line)
        I_machinecode = bin(func).replace("0b", "").zfill(6) + bin(rs).replace("0b", "").zfill(5) + bin(rt).replace("0b", "").zfill(5) + bin(im).replace("0b", "").zfill(16) + "\n"
        return I_machinecode

    def add_assemble(self,instruction_line):
        add_machinecode = self.R_Machine_Code(instruction_line, 32)
        return add_machinecode

    def and_assemble(self,instruction_line):
        and_machinecode = self.R_Machine_Code(instruction_line, 36)
        return and_machinecode

    def sub_assemble(self,instruction_line):
        sub_machinecode = self.R_Machine_Code(instruction_line, 34)
        return sub_machinecode

    def nor_assemble(self,instruction_line):
        nor_machinecode = self.R_Machine_Code(instruction_line, 39)
        return nor_machinecode

    def or_assemble(self,instruction_line):
        or_machinecode = self.R_Machine_Code(instruction_line, 37)
        return or_machinecode

    def slt_assemble(self,instruction_line):
        slt_machinecode = self.R_Machine_Code(instruction_line, 42)
        return slt_machinecode

    def lw_assemble(self,instruction_line):
        lw_machinecode = self.I_Machine_Code(instruction_line, 35)
        return lw_machinecode

    def sw_assemble(self,instruction_line):
        sw_machinecode = self.I_Machine_Code(instruction_line, 43)
        return sw_machinecode

    def addi_assemble(self,instruction_line):
        addi_machinecode = self.I_Machine_Code(instruction_line, 8)


Assembler("MIPS.asm", "data.txt", "code.txt")
