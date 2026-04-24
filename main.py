#!/usr/bin/env python3

import sys

# =============================================================================
# OLD VERSION (flat stack, separate heap, unbounded memory)
# =============================================================================

# opcodes = ['PUSH', 'POP', 'DUP', 'ADD', 'SUB', 'MUL', 'JMP', 'JM0', 'HALT', 'PRINT']
# memory  = []
# stack   = []
# heap    = [0] * 256
# PC      = 0

# with open(sys.argv[1], 'r') as file:
#     content = file.read().split()
#     for token in content:
#         if token.isdigit():
#             memory.append(int(token))
#         else:
#             memory.append(token)

# while True:
#     if PC < len(memory):
#         instruction = memory[PC]
#         PC += 1
#         if instruction == 'PRINT':
#             print(stack.pop())
#         elif instruction == 'PUSH':
#             stack.append(memory[PC])
#             PC += 1
#         elif instruction == 'POP':
#             if len(stack) > 0:
#                 stack.pop()
#         elif instruction == 'DUP':
#             stack.append(stack[-1])
#         elif instruction == 'ADD':
#             a = stack.pop()
#             b = stack.pop()
#             c = a + b
#             stack.append(c)
#         elif instruction == 'SUB':
#             a = stack.pop()
#             b = stack.pop()
#             c = b - a
#             stack.append(c)
#         elif instruction == 'MUL':
#             a = stack.pop()
#             b = stack.pop()
#             c = a * b
#             stack.append(c)
#         elif instruction == 'JMP':
#             n = memory[PC]
#             PC = n
#         elif instruction == 'JM0':
#             if stack[-1] == 0:
#                 n = memory[PC]
#                 PC = n
#             else:
#                 PC += 1
#         elif instruction == 'HALT':
#             exit(0)
#         elif instruction == 'STORE':
#             heap[memory[PC]] = stack.pop()
#             PC += 1
#         elif instruction == 'LOAD':
#             stack.append(heap[memory[PC]])
#             PC += 1
#         else:
#             print(f'Unknown operation: {instruction}')
#             break


# =============================================================================
# New Version
# BSM-8 -- 8-bit Stack Machine (flat RAM, real stack pointer, heap offset addressing)
# =============================================================================

# BoundedMemory is a custom list that enforces the 8-bit limit of the BSM-8.
# On a real 8-bit machine, each memory slot can only hold a value between 0 and 255.
# Python does not enforce this on its own, so we wrap the built-in list in a class
# that automatically applies the limit every time something is written to memory.
# If a value exceeds 255 it wraps back around to 0 and counts up from there --
# the same way a car odometer rolls over from 999999 back to 0.
# This class behaves exactly like a normal list from the outside. The rest of the
# VM code does not need to know or care that the limit is being enforced here.
class BoundedMemory():
    def __init__(self):
        self.data = [0] * 256

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if isinstance(value, int):
            value = value % 256
        self.data[index] = value

# Create the BSM-8's RAM -- 256 slots of bounded 8-bit memory.
# Every piece of data on this machine lives here: the program, variables, and the stack.
RAM = BoundedMemory()

# The 256 slots are divided into three regions. These numbers are just the
# starting address of each region. Think of them as street addresses.
#
#   Slots   0 - 127 : program space  (instructions and their arguments live here)
#   Slots 128 - 191 : heap           (variables stored with STORE/LOAD live here)
#   Slots 192 - 255 : stack          (temporary working values live here)
PROGRAM_START = 0
HEAP_START    = 128
STACK_START   = 255

# PC (Program Counter) -- a number that tracks which instruction to run next.
# It starts at 0 (the first slot in RAM) and moves forward as the program runs.
# Jump instructions can change it to anything, which is how loops and branches work.
PC = 0

# SP (Stack Pointer) -- a number that tracks the top of the stack.
# The stack grows DOWNWARD, so SP starts at 255 (the top of RAM) and decreases
# as values are pushed onto the stack. Think of it as a finger pointing to the
# last used slot -- the next free slot is always one below where SP is pointing.
SP = STACK_START

# Load the program from the file passed on the command line.
# Each token (word or number) in the file gets written into RAM one slot at a time,
# starting at slot 0. Numbers are stored as integers, everything else as strings.
with open(sys.argv[1], 'r') as file:
    content = file.read().split()
    addr = PROGRAM_START
    for token in content:
        if token.isdigit():
            RAM[addr] = int(token)
        else:
            RAM[addr] = str(token)
        addr += 1

# The main loop. This runs forever until HALT is hit or something goes wrong.
# Each iteration is one full instruction cycle: fetch, decode, execute.
while True:

    # Only run if PC is still inside the program region (below the heap).
    if PC < HEAP_START:

        # FETCH -- read the instruction sitting at the current PC position.
        # Then immediately advance PC by 1 so it points at the next thing.
        # (If the instruction has an argument, PC now points at that argument.)
        instruction = RAM[PC]
        PC += 1

        # DECODE + EXECUTE -- figure out what the instruction is and do it.

        if instruction == 'PRINT':
            # Pop the top value off the stack and print it.
            # SP + 1 is the top of the stack because SP points one below the last pushed value.
            SP += 1
            print(RAM[SP])

        elif instruction == 'PUSH':
            # Read the argument (the value to push) from the next slot in RAM.
            # Write it to the current top of the stack, then move SP down.
            RAM[SP] = RAM[PC]
            PC += 1   # skip past the argument so the next fetch lands on the next instruction
            SP -= 1   # stack grows downward, so pushing moves SP down

        elif instruction == 'POP':
            # Discard the top value. Moving SP up one slot "uncovers" the value below it,
            # making the previous value the new top. The discarded value is still physically
            # in RAM but SP has moved past it so nothing can reach it anymore.
            SP += 1

        elif instruction == 'DUP':
            # Read the top value (SP + 1) and push a second copy of it onto the stack.
            RAM[SP] = RAM[SP + 1]
            SP -= 1

        elif instruction == 'ADD':
            # Pop two values, add them, push the result.
            # We pop by moving SP up (SP += 1) then reading from RAM[SP].
            SP += 1
            a = RAM[SP]   # first popped value (was on top)
            SP += 1
            b = RAM[SP]   # second popped value (was below the top)
            c = a + b
            RAM[SP] = c   # overwrite the second value's slot with the result
            SP -= 1       # push: move SP back down one to account for the result we just wrote

        elif instruction == 'SUB':
            # Same pattern as ADD but subtracts. b - a keeps the order intuitive:
            # if you pushed 5 then 1, you get 5 - 1 = 4, not 1 - 5 = -4.
            SP += 1
            a = RAM[SP]
            SP += 1
            b = RAM[SP]
            c = b - a
            RAM[SP] = c
            SP -= 1

        elif instruction == 'MUL':
            # Same pattern as ADD but multiplies.
            SP += 1
            a = RAM[SP]
            SP += 1
            b = RAM[SP]
            c = a * b
            RAM[SP] = c
            SP -= 1

        elif instruction == 'JMP':
            # Unconditional jump. Read the target address from the next slot in RAM
            # and set PC to it. The next instruction fetched will be at that address.
            n = RAM[PC]
            PC = n

        elif instruction == 'JM0':
            # Conditional jump. Check the top of the stack (without consuming it).
            # If it is zero, jump to the target address. Otherwise skip past the argument.
            if RAM[SP + 1] == 0:
                n = RAM[PC]   # read the jump target from the program
                PC = n        # jump to it
            else:
                PC += 1       # not zero, skip past the argument and continue

        elif instruction == 'HALT':
            # Stop the VM cleanly.
            exit(0)

        elif instruction == 'STORE':
            # Save a value from the stack into the heap (variable storage).
            # The argument tells us which heap slot to write to (0, 1, 2...).
            # We add HEAP_START to convert that relative slot number into a real RAM address.
            # Example: STORE 0 writes to RAM[128], STORE 1 writes to RAM[129], etc.
            addr = RAM[PC]
            PC += 1
            SP += 1           # pop: move SP up to expose the top value
            data = RAM[SP]    # read the top value
            RAM[HEAP_START + addr] = data

        elif instruction == 'LOAD':
            # Load a value from the heap onto the stack.
            # The argument tells us which heap slot to read from (0, 1, 2...).
            # Same HEAP_START offset as STORE.
            addr = RAM[PC]
            data = RAM[HEAP_START + addr]
            RAM[SP] = data    # write to the current top of stack
            PC += 1
            SP -= 1           # push: move SP down to account for the new value

        else:
            print(f'Unknown operation: {instruction}')
            break
