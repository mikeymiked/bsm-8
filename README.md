# BSM-8

A toy 8-bit stack machine I built to learn how CPUs and virtual machines work. I have no computer science background and do not really know what I am doing. This is just a passion project.

## What is it

It is a made up computer. It has 256 bytes of RAM, a stack, a heap for storing variables, and 12 instructions. Values wrap around at 255 like a real 8-bit machine. There is also a basic assembler so you can write programs with named labels instead of raw memory addresses.

## Files

- `main.py` -- the VM itself. Loads and runs a program file.
- `assembler.py` -- converts `.asm` files with named labels into a program file the VM can load.

## How to run

Write a program in a `.asm` file, assemble it, then run it:

```
python3 assembler.py myprogram.asm myprogram.txt
python3 main.py myprogram.txt
```

## Example program

This counts down from 5 to 0 and prints each value:

```
PUSH 5
loop:
JM0  done
DUP
PRINT
PUSH 1
SUB
JMP  loop
done:
HALT
```

Labels like `loop:` and `done:` are resolved by the assembler so you do not have to count memory addresses by hand.

## Instructions

| Instruction | What it does                          |
|-------------|---------------------------------------|
| `PUSH n`    | Put a value on the stack              |
| `POP`       | Throw away the top value              |
| `DUP`       | Copy the top value                    |
| `ADD`       | Add the top two values                |
| `SUB`       | Subtract the top two values           |
| `MUL`       | Multiply the top two values           |
| `JMP n`     | Jump to a label or address            |
| `JM0 n`     | Jump if the top of the stack is zero  |
| `STORE n`   | Save the top value to a variable slot |
| `LOAD n`    | Load a variable slot onto the stack   |
| `PRINT`     | Print the top value                   |
| `HALT`      | Stop                                  |

## Memory layout

```
Slots   0 - 127 : program
Slots 128 - 191 : heap (variables)
Slots 192 - 255 : stack
```

## Requirements

Just Python 3. No libraries.
