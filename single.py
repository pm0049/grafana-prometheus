motOpCode = {
    "MOV": 1, "A": 2, "S": 3, "M": 4, "D": 5, "AN": 6, "O": 7,
    "ADD": 8, "SUB": 9, "MUL": 10, "DIV": 11, "AND": 12, "OR": 13,
    "LOAD": 14, "STORE": 15, "DCR": 16, "INC": 17, "JMP": 18,
    "JNZ": 19, "HALT": 20
}

motSize = {
    "MOV": 1, "A": 1, "S": 1, "M": 1, "D": 1, "AN": 1, "O": 1,
    "ADD": 1, "SUB": 2, "MUL": 2, "DIV": 2, "AND": 2, "OR": 2,
    "LOAD": 3, "STORE": 3, "DCR": 1, "INC": 1, "JMP": 3, "JNZ": 3,
    "HALT": 1
}

l = []
relativeAddress = []
machineCode = []
RA = 0

n = int(input("Enter the number of instruction lines: "))

for i in range(n):
    instructions = input("Enter instruction line {}: ".format(i + 1))
    if not instructions.strip():
        print("Error: Instruction line cannot be empty.")
        exit(1)
    l.append(instructions.upper())

for instr in l:
    parts = instr.split()
    opcode = parts[0]
    if opcode in motOpCode:
        size = motSize[opcode]
        relativeAddress.append(RA)
        RA += size
        machineCode.append(str(motOpCode[opcode]))
        if len(parts) > 1:
            operand = ','.join(parts[1:])
            machineCode[-1] += ',' + operand
    else:
        print("Instruction '{}' is not in Op Code Table.".format(instr))
        exit(1)

print("Relative Address Instruction OpCode")
for i in range(n):
    instr = l[i]
    if ',' in machineCode[i]:
        opcode, operand = machineCode[i].split(',', 1)
        print("{:<16} {:<12} {}".format(relativeAddress[i], instr, opcode + ' ' + operand))
    else:
        print("{:<16} {:<12} {}".format(relativeAddress[i], instr, machineCode[i]))
#Enter the number of instruction lines: 3
#Enter instruction line 1: MOV A,B
#Enter instruction line 2: ADD C
#Enter instruction line 3: HALT
#Relative Address Instruction OpCode
#0                MOV A,B      1 A,B
#1                ADD C        8 C
#2                HALT         20
