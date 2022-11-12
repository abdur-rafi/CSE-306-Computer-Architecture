inst_type = {
    "sll": ("S", "0000"),
    "lw": ("I", "0001"),
    "andi": ("I", "0010"),
    "subi": ("I", "0011"),
    "addi": ("I", "0100"),
    "and": ("R", "0101"),
    "add": ("R", "0110"),
    "ori": ("I", "0111"),
    "sw": ("I", "1000"),
    "j": ("J", "1001"),
    "beq": ("I", "1010"),
    "or": ("R", "1011"),
    "bneq": ("I", "1100"),
    "nor": ("R", "1101"),
    "sub": ("R", "1110"),
    "srl": ("S", "1111")
}
reg_map = {
    "$zero": "0000",
    "$t0": "0001",
    "$t1": "0010",
    "$t2": "0011",
    "$t3": "0100",
    "$t4": "0101", 
    "$sp": "0110"
}
labels=dict()

def bin_to_hex(*argv):
    res=''
    for arg in argv:
        res += hex(int(arg, 2))[2:]
    return res

def handle_IRS_type(inst_sep, fmt, i)->str:
    inst_name, r1 = inst_sep[0].split(' ')
    inst_name = inst_name.strip()
    if inst_name == 'lw' or inst_name == 'sw':
        return handle_lwsw(inst_sep)

    opcode = inst_type.get(inst_name)[1]
    r1 = reg_map.get(r1.strip())
    r2 = reg_map.get(inst_sep[1].strip())
    r3 = inst_sep[2].strip()

    if fmt == 'R':
        r3 = reg_map.get(r3)
        return bin_to_hex(opcode, r2, r3, r1)
    if inst_name == 'beq' or inst_name == 'bneq':
        jmp_to = labels.get(r3)
        if i < jmp_to:
            r3 = jmp_to - i - 1
        else:
            r3 = i - jmp_to - 1
            r3 = 1 << 4 - r3 #twos complement
    r3 = int(r3)
    r3 = bin(r3)[2:].zfill(4)

    return bin_to_hex(opcode, r2, r1, r3)

def handle_lwsw(inst_sep)->str:
    # print(inst_sep)
    inst_name, r2 = inst_sep[0].split(' ')
    inst_name = inst_name.strip()

    opcode = inst_type.get(inst_name)[1]
    r2 = reg_map.get(r2.strip())
    r1 = inst_sep[1].strip()
    start = r1.find('(')
    end = r1.find(')')
    shmt = int(r1[:start])
    shmt = bin(shmt)[2:].zfill(4)
    r1 = reg_map.get(r1[start+1:end])
    return bin_to_hex(opcode, r1, r2, shmt)

def handle_J_type(inst_sep, i)->str:
    inst_name, jmpaddr = inst_sep[0].split(' ')
    inst_name = inst_name.strip()
    jmpaddr = labels.get(jmpaddr.strip())

    opcode = inst_type.get(inst_name)[1]
    # jmpaddr = bin(jumpaddr)[2:].zfill(8)
    return bin_to_hex(opcode) + hex(jmpaddr)[2:].zfill(2) + '0'

def mips_to_machine(inst:str, i)->str:
    comma_sep = inst.split(',')
    inst_name = comma_sep[0].split(' ')[0].strip()
    if inst_name not in inst_type:
        print('Invalid instruction: ' + inst_name)
        exit(1)
    fmt, opcode = inst_type.get(inst_name)
    if fmt=='R' or fmt=='I' or fmt=='S':
        return handle_IRS_type(comma_sep, fmt, i)
    else:
        return handle_J_type(comma_sep, i)


try:
    asm_input = open('inst.asm', 'r')
except:
    print('\033[91m' + "inst.asm file not found" + '\033[0m')
    exit(1)

fout = open('out.hex', 'w')
fout.write('v2.0 raw\n')
mips_code = asm_input.readlines()

#find labels
for i, line in enumerate(mips_code):
    if line=="":
        continue
    line = line.strip()
    colon = line.find(':')
    if colon!=-1:
        labels[line[:colon]] = i

for i, line in enumerate(mips_code):
    if line == "" or line.find(':')!=-1:
        continue
    cmnt = line.find(';')
    if cmnt!=-1:
        line = line[:cmnt].strip()
    print(line, end= '' if line.endswith('\n') else '\n')
    xcode = mips_to_machine(line, i)
    print("Machine code: " + xcode, end='\n\n')
    fout.write(xcode + '\n')
fout.close()
asm_input.close()
