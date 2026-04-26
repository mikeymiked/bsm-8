#!/usr/bin/env python3

import sys

labels = {}
opcodes = ['PUSH', 'POP', 'DUP', 'ADD', 'SUB', 'MUL', 'CMP', 'JMP', 'JM0', 'JG0', 'JEQ', 'CALL', 'RET', 'HALT', 'STORE', 'LOAD', 'PRINT', 'DSP']

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
        new_content.append(str(token))
    else:
        new_content.append(str(token))


with open(sys.argv[2], 'w') as file:
    for token in new_content:
        file.write(str(token) + "\n")