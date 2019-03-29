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

    instructions = {"add": ["R", 0, 32],
                    "and": ["R", 0, 36],
                    "sub": ["R", 0, 34],
                    "nor": ["R", 0, 39],
                    "or": ["R", 0, 37],
                    "slt": ["R", 0, 42],
                    "addi": ["I", 8],
                    "lw": ["I", 35],
                    "sw": ["I", 43],
                    "beq": ["I", 4],
                    "bne": ["I", 5],
                    "j": ["J", 2]}

    data_labels = {}
    code_labels = {}

    pc = 0

    def __init__(self, mips_file_path, data_file_path, code_file_path):
        mips_file = open(mips_file_path, "r")
        data_file = open(data_file_path, "w+")
        code_file = open(code_file_path, "w+")

        self.content = mips_file.readlines()
        self.clean_file()

        self.data = self.GetInBetween(".data\n", ".text\n")
        self.code = self.GetInBetween(".text\n", ".data\n")

        Assembler.code_labels = self.get_code_labels()
        Assembler.data_labels = self.get_data_labels()

        machine_code = self.assemble_data()
        data_file.write(machine_code)

        machine_code = self.assemble_code()
        code_file.write(machine_code)

        mips_file.close()
        data_file.close()
        code_file.close()

    def GetInBetween(self, first, second):
        data = []
        dOffset = -1
        cOffset = -1

        while True:

            if first in self.content[dOffset + 1:len(self.content)]:
                dOffset = self.content[dOffset + 1:len(self.content)].index(first) + dOffset + 1
                if dOffset == -1:
                    dOffset = 0

                if second in self.content[dOffset + 1:len(self.content)]:
                    cOffset = self.content[dOffset + 1:len(self.content)].index(second) + dOffset + 1
                else:
                    cOffset = len(self.content)

                if first in self.content[dOffset + 1:len(self.content)]:
                    cOffset = min(cOffset, self.content[dOffset + 1:len(self.content)].index(first) + dOffset + 1)

                data += self.content[dOffset + 1:cOffset]
            else:
                break

        return data

    def clean_file(self):
        output = []
        for i in self.content:
            i = str(i).lower()
            i = i.split("#")[0]
            if re.search(r"\w", i):
                output.append(i.strip() + "\n")
        self.content = output

    def get_data_labels(self):
        labels = {}
        line = 0
        regex = r"([a-zA-Z_][a-zA-Z0-9_]*):"
        for item in self.data:
            match = re.search(regex, item)
            if match:
                if match[1] in labels.keys():
                    print("Label %s already Exist" % match)
                else:
                    labels[match[1]] = line

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
            match = re.search(regex, item)
            if match:
                if match[1] in labels.keys():
                    print("Label %s already Exist" % match)
                else:
                    labels[match[1]] = line
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
        machine_code = ""
        for i in self.code:
            match = None
            for j in Assembler.instructions.keys():
                match = re.search(j + "(?= )", i)
                if match is not None:
                    break

            if match:
                instruction_type = Assembler.instructions[match[0]][0]
                instruction = None

                if instruction_type == "R":
                    instruction = R(i[match.start():], self.pc)
                elif instruction_type == "I":
                    instruction = I(i[match.start():], self.pc)
                elif instruction_type == "J":
                    instruction = J(i[match.start():], self.pc)

                if instruction.get_operands():
                    machine_code += instruction.machine_code()
            else:
                print("Compilation Error on line %d: invalid instruction" % self.pc)

            self.pc += 1
        return machine_code


class Instruction:

    def __init__(self, instruction_line, line_no):
        self.instruction_line = instruction_line
        self.line_no = line_no

    def get_operands(self):
        pass

    def machine_code(self):
        pass


class R(Instruction):

    def __init__(self, instruction_line, line_no):
        super().__init__(instruction_line, line_no)
        self.op_code = 0
        self.rd = 0
        self.rs = 0
        self.rt = 0
        self.func = 0

    def get_operands(self):
        line = re.split(r"\s*,\s*|\s", self.instruction_line)
        if line[1] not in Assembler.registers:
            print("Compilation Error on line %d: invalid rd" % self.line_no)
            return False
        if line[2] not in Assembler.registers:
            print("Compilation Error on line %d: invalid rs" % self.line_no)
            return False

        if line[3] not in Assembler.registers:
            print("Compilation Error on line %d: invalid rt" % self.line_no)
            return False
        self.op_code = Assembler.instructions[line[0]][1]
        self.rd = Assembler.registers.index(str(line[1]).strip())
        self.rs = Assembler.registers.index(str(line[2]).strip())
        self.rt = Assembler.registers.index(str(line[3]).strip())
        self.func = Assembler.instructions[line[0]][2]
        return True

    def machine_code(self):
        machine_code = bin(self.op_code).replace("0b", "").zfill(6) + bin(self.rs).replace("0b", "").zfill(5) + \
                       bin(self.rt).replace("0b", "").zfill(5) + bin(self.rd).replace("0b", "").zfill(5) + \
                       bin(0).replace("0b", "").zfill(5) + bin(self.func).replace("0b", "").zfill(6) + "\n"
        return machine_code


class I(Instruction):

    def __init__(self, instruction_line, line):
        super().__init__(instruction_line, line)
        self.op_code = 0
        self.rs = 0
        self.rt = 0
        self.im = 0

    def get_operands(self):
        line = re.split(r"\s|\s*,\s*|[()]", self.instruction_line)
        while '' in line: line.remove('')
        if line[0] == 'sw' or line[0] == 'lw': line[3], line[2] = line[2], line[3]
        if line[0] == 'beq' or line[0] == 'bne': line[1], line[2] = line[2], line[1]
        if line[2] not in Assembler.registers:
            print("Compilation Error on line %d: invalid rs" % self.line_no)
            return False

        if line[1] not in Assembler.registers:
            print("Compilation Error on line %d: invalid rt" % self.line_no)
            return False

        if line[3] not in Assembler.data_labels and line[3] not in Assembler.code_labels:
            try:
                self.im = int(line[3])
            except ValueError:
                print("Compilation Error on line %d: invalid immediate" % self.line_no)
                return False
        else:
            if line[0] == 'beq' or line[0] == 'bne':
                self.im = Assembler.code_labels.get(line[3]) - (self.line_no + 1)
            else:
                self.im = Assembler.data_labels.get(line[3])

        self.op_code = Assembler.instructions[line[0]][1]
        self.rs = Assembler.registers.index(str(line[2]).strip())
        self.rt = Assembler.registers.index(str(line[1]).strip())
        return True

    def machine_code(self):
        machine_code = bin(self.op_code).replace("0b", "").zfill(6) + bin(self.rs).replace("0b", "").zfill(5) + \
                       bin(self.rt).replace("0b", "").zfill(5) +\
                       bin(self.im if self.im >= 0 else self.im + (1 << 16)).replace("0b", "").zfill(16) + "\n"
        return machine_code


class J(Instruction):

    def __init__(self, instruction_line, line_no):
        super().__init__(instruction_line, line_no)
        self.op_code = 0
        self.address = 0

    def get_operands(self):
        line = re.split(r"\s", self.instruction_line)
        if line[1] not in Assembler.code_labels:
            print("Compilation Error on line %d: invalid label" % self.line_no)
            return False
        self.op_code = Assembler.instructions[line[0]][1]
        self.address = Assembler.code_labels.get(line[1])
        return True

    def machine_code(self):
        machine_code = bin(self.op_code).replace("0b", "").zfill(6) +\
                       bin(self.address).replace("0b", "").zfill(26) + "\n"
        return machine_code


Assembler("MIPS.asm", "data.txt", "code.txt")
