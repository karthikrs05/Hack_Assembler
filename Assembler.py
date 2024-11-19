import os                                                                                                                                                                                                                                                                                                                                                                                                                                   

# Define computation, destination, and jump dictionaries
comp = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101"
}

dest = {
    "null": "000", "M": "001", "D": "010", "A": "100",
    "MD": "011", "AM": "101", "AD": "110", "AMD": "111"
}

jmp = {
    "null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

# Initialize symbol table
table = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}
for i in range(0, 16): #R0,R1,R2,R3,R4..R15
    key = "R" + str(i)
    table[key] = i

# Remove whitespace and comments from the input file
name = input("Enter the name of the file: ")
f = open(name + '.asm', "r")
fw = open("wc.asm", "w") #new file wc
for line in f:
    line = line.strip()  # Remove leading and trailing whitespace
    comment_index = line.find('//')
    if comment_index != -1:
        line = line[:comment_index]  # Remove comments
    if line:
        fw.write(line + '\n')  # Write non-empty lines
f.close()
fw.close()

# Format C instructions into proper equation form
f = open("wc.asm", "r")
fw = open("norm.asm", "w")
for line in f:
    if line.startswith('@') or line.startswith('('):
        fw.write(line)  # Write A and label instructions as is
        continue
    else:
        if "=" not in line:
            line = "null=" + line #if dest is missing
        if ";" not in line:
            line = line.strip() + ";null\n" #removes leading and trailing spaces and addes null value as jmp
        fw.write(line)  # Ensure every C instruction has both destination and jump
f.close()
fw.close()

# First pass: add labels to symbol table
f = open("norm.asm", "r")
line_no = 0
for line in f:
    if not line.startswith('('):
        line_no += 1
        continue
    else:
        label = line[1:-2].strip()  # Extract label
        table[label] = line_no
f.close()

# Second pass: add variables and symbols
f = open("norm.asm", "r")
pos = 16
for line in f:
    if line.startswith('@'):
        label = line[1:-1].strip()  # Extract variable
        if label.isalpha() and label not in table: #Check if the label consists of alphabetic characters and if it's not already in the symbol table
            table[label] = pos
            pos += 1
f.close()

# Translate instructions to binary
f = open("norm.asm", "r")
fw = open(name + ".hack", "w")
for line in f:
    if line.startswith('@'):
        label = line[1:].strip()  # Extract label or variable removing @
        if label in table:
            value = table[label]
            binvalue = format(value, '016b')
            fw.write(str(binvalue) + "\n")
        else:
            label = int(line[1:-1])  # Convert label to integer
            binvalue = format(label, '016b')
            fw.write(binvalue + "\n")
    elif line.startswith('('):
        label = line[1:-2].strip()  # Extract label
        if label in table:
            value = table[label]
            binvalue = format(value, '016b')
            fw.write(str(binvalue) + "\n")
    else:
        dest_comp_jump = line.split("=")  # Split destination and computation+jump
        destination = dest[dest_comp_jump[0]]  # Get destination code
        comp_jump = dest_comp_jump[1].split(";")
        computation = comp[comp_jump[0]]  # Get computation code
        jump = jmp[comp_jump[1].strip()]  # Get jump code
        fw.write("111" + computation + destination + jump + "\n")  # Write binary instruction
f.close()
fw.close()
