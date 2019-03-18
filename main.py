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
        self.content=self.clean_file()
        self.data = self.GetInBetween(".data\n",".text\n")
        self.code = self.GetInBetween(".text\n",".data\n")

        self.code_labels = self.get_code_labels()
        self.data_labels = self.get_data_labels()

        machine_code = self.assemble_data()
        data_file.write(machine_code)

        machine_code = self.assemble_code()
        code_file.write(machine_code)

        mips_file.close()
        mips_file.close()
        data_file.close()
        code_file.close()
    def GetInBetween(self,first,second):
        data=[]
        dOffset=-1
        cOffset=-1

        while True:

            if first in self.content[dOffset+1:len(self.content)]:
                dOffset=self.content[dOffset+1:len(self.content)].index(first)+dOffset+1
                if dOffset==-1 :
                    dOffset=0

                if second in self.content[dOffset + 1:len(self.content)]:
                    cOffset = self.content[dOffset + 1:len(self.content)].index(second) + dOffset + 1
                else:
                    cOffset = len(self.content)

                if first in self.content[dOffset + 1:len(self.content)]:
                    cOffset = min(cOffset,self.content[dOffset + 1:len(self.content)].index(first) + dOffset + 1)
                print(dOffset," ",cOffset)
                data+=self.content[dOffset+1:cOffset]
            else:
                break
        print(len(data))
        print(data)
        return data





    def clean_file(self):
        output = []
        for i in self.content:
            i = i.split("#")[0]
            if re.search(r"\w", i):
                output.append(i.strip() + "\n")
        return output

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
            if match:
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
            if match:
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
                machine_code += instructions.get(match[0])(i[match.start():])
        return machine_code

    def Get_R_Operands(self, instruction_line):
        line = re.split(r"\s*,\s*|\s", instruction_line)

        rd = self.registers.index(str(line[1]).strip())
        rs = self.registers.index(str(line[2]).strip())
        rt = self.registers.index(str(line[3]).strip())

        return rs, rt, rd

    def R_Machine_Code(self,instruction_line, func):
        rs, rt, rd = self.Get_R_Operands(instruction_line)
        R_machinecode = bin(0).replace("0b", "").zfill(6) + bin(rs).replace("0b", "").zfill(5) + \
                 bin(rt).replace("0b", "").zfill(5) + bin(rd).replace("0b", "").zfill(5) + \
                 bin(0).replace("0b", "").zfill(5) + bin(func).replace("0b", "").zfill(6) + "\n"
        return R_machinecode

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


Assembler("MIPS.asm", "data.txt", "code.txt")
