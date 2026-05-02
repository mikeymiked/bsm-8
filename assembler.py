#!/usr/bin/env python3

import sys

labels = {}
# opcodes = ['PUSH', 'POP', 'DUP', 'ADD', 'SUB', 'MUL', 'CMP', 'JMP', 'JM0', 'JG0', 'JEQ', 'CALL', 'RET', 'HALT', 'STORE', 'LOAD', 'PRINT', 'DSP']
opcodes = {
    'PUSH': 0x11, 'POP': 0x12, 'DUP': 0x13, 
    'ADD': 0x21, 'SUB': 0x22, 'MUL': 0x23, 'CMP': 0x24,
    'JMP': 0x31, 'JM0': 0x32, 'JG0': 0x33, 'JEQ': 0x34, 'CALL': 0x35, 'RET': 0x36, 'HALT': 0x37,
    'STORE': 0x41, 'LOAD': 0x42,
    'PRINT': 0x51, 'DSP': 0x52
}

with open(sys.argv[1], 'r') as file:
    content = []
    for line in file:
        content.extend(line.split(';')[0].split())

    counter = 0

    for token in content:
        if token.endswith(':'):
            labels[token.replace(':', '')] = counter
        else:
            counter += 1

new_content = []

for token in content:
    if token.endswith(':'):
        pass
    elif token in labels:
        token = labels[token]
        new_content.append(token)
    elif token.isdigit():
        new_content.append(int(token))
    elif token in opcodes:
        new_content.append(opcodes[token])
    else:
        new_content.append(str(token))


with open(sys.argv[2], 'w') as file:
    for token in new_content:
        if token in opcodes.values():
            file.write(hex(token) + "\n")
        else:
            file.write(str(token) + "\n")