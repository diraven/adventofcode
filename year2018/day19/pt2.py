"""
--- Part Two ---

A new background process immediately spins up in its place. It appears identical, but on closer inspection, you notice that this time, register 0 started with the value 1.

What value is left in register 0 when this new background process halts?
"""
from collections import namedtuple
from typing import List

Instruction = namedtuple("Instruction", ('op', 'a', 'b', 'c'))
Registers = List[int]  # registers


def apply(inst: Instruction, registers: Registers):
    registers[inst.c] = ops[inst.op](inst, registers)


ops = {
    # x: instruction, y: data
    'addr': lambda x, y: y[x.a] + y[x.b],
    'addi': lambda x, y: y[x.a] + x.b,
    'mulr': lambda x, y: y[x.a] * y[x.b],
    'muli': lambda x, y: y[x.a] * x.b,
    'banr': lambda x, y: y[x.a] & y[x.b],
    'bani': lambda x, y: y[x.a] & x.b,
    'borr': lambda x, y: y[x.a] | y[x.b],
    'bori': lambda x, y: y[x.a] | x.b,
    'setr': lambda x, y: y[x.a],
    'seti': lambda x, y: x.a,
    'gtir': lambda x, y: 1 if x.a > y[x.b] else 0,
    'gtri': lambda x, y: 1 if y[x.a] > x.b else 0,
    'gtrr': lambda x, y: 1 if y[x.a] > y[x.b] else 0,
    'eqir': lambda x, y: 1 if x.a == y[x.b] else 0,
    'eqri': lambda x, y: 1 if y[x.a] == x.b else 0,
    'eqrr': lambda x, y: 1 if y[x.a] == y[x.b] else 0,
}

with open("./input.txt") as f:
    # Load data.
    data = f.read().splitlines()

    ip = int(data[0].replace('#ip ', ''))
    ipv = 0

    instructions = []  # type: List[Instruction]

    for line in data[1:]:
        splitted = line.split(' ')
        splitted[1:] = [int(x) for x in splitted[1:]]

        instruction = Instruction(*splitted)
        instructions.append(instruction)

    registers = [1] + [0] * 5

    counter = 0
    for i in range(100):
        # while True:
        counter += 1
        print(registers[ip], instructions[registers[ip]])
        apply(instructions[registers[ip]], registers)
        if registers[ip] > len(instructions) - 2:
            break
        registers[ip] += 1
        print(registers, "\n")
        # if counter >= 10000000:
        # counter = 0
        # print(registers[ip], instructions[registers[ip]])
        # print(registers, "\n")

    print(registers)

# Done manually. The idea is to figure out what exactly does the
# program do and then calcualte the answer. Program calculates the sum
# of all the divisors of the number contained in registers[5] after
# initialization.
