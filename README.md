# BSM-8

A toy 8-bit stack machine I built to learn how CPUs and virtual machines work. I have no computer science background and do not really know what I am doing. This is just a passion project.

## What is it

It is a made up computer. It has 256 bytes of RAM, a stack, a heap for storing variables, and 17 instructions. Values wrap around at 255 like a real 8-bit machine. There is also a basic assembler so you can write programs with named labels instead of raw memory addresses.

## Files

- `bsm8.py` -- the VM itself. Can be run directly as a script or imported as a library into other Python programs.
- `assembler.py` -- converts `.asm` files with named labels into a program file the VM can load.

## Requirements

Python 3 and pygame. Install pygame with:

```
pip install pygame
```

## How to run

Write a program in a `.asm` file, assemble it, then run it:

```
python3 assembler.py myprogram.asm myprogram.txt
python3 bsm8.py myprogram.txt
```

You can also import the VM into your own Python code:

```python
from bsm8 import BSM8

vm = BSM8()
vm.load_program('myprogram.txt')
while True:
    result = vm.step()
    if result is True:
        break
    elif result is False:
        break
    elif result == 'DSP':
        pass  # handle display output
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

This program prints the larger of two values using `CMP` and `JEQ`:

```
PUSH 7
PUSH 10
CMP
JM0  equal
JEQ  2 ten_wins
seven_wins:
PUSH 7
PRINT
JMP  done
ten_wins:
PUSH 10
PRINT
JMP  done
equal:
PUSH 10
PRINT
done:
HALT
```

`CMP` pops both values and pushes a result: 0 if equal, 1 if the top was less, 2 if the top was greater. `JEQ 2 ten_wins` then jumps to `ten_wins` if that result is 2, meaning 10 was the larger value.

## Instructions

| Instruction  | What it does                                              |
|--------------|-----------------------------------------------------------|
| `PUSH n`     | Put a value on the stack                                  |
| `POP`        | Throw away the top value                                  |
| `DUP`        | Copy the top value                                        |
| `ADD`        | Add the top two values                                    |
| `SUB`        | Subtract the top two values                               |
| `MUL`        | Multiply the top two values                               |
| `CMP`        | Compare the top two values, push 0 (equal), 1 (a < b), or 2 (a > b)                   |
| `JMP n`      | Jump to a label or address                                |
| `JM0 n`      | Jump if the top of the stack is zero                      |
| `JG0 n`      | Jump if the top of the stack is greater than zero         |
| `JEQ v n`    | Jump to address n if the top of the stack equals v        |
| `CALL n`     | Push the return address and jump to a subroutine          |
| `RET`        | Pop the return address and jump back to the caller        |
| `STORE n`    | Save the top value to a variable slot                     |
| `LOAD n`     | Load a variable slot onto the stack                       |
| `PRINT`      | Print the top value                                       |
| `DSP`        | Signal the runner to render the display (reads heap slot 0) |
| `HALT`       | Stop                                                      |

## Memory layout

```
Slots   0 - 127 : program
Slots 128 - 191 : heap (variables)
Slots 192 - 255 : stack
```

