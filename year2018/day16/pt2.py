"""
--- Part Two ---
Using the samples you collected, work out the number of each opcode and execute the test program (the second section of your puzzle input).

What value is contained in register 0 after executing the test program?
"""
import copy
import timeit
from typing import List

Instruction = List[int]

def addr(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = data[a] + data[b]

    return data


def addi(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = data[a] + b

    return data


def mulr(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = data[a] * data[b]

    return data


def muli(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = data[a] * b

    return data


def banr(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = data[a] & data[b]

    return data


def bani(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = data[a] & b

    return data


def borr(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = data[a] | data[b]

    return data


def bori(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = data[a] | b

    return data


def setr(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = data[a]

    return data


def seti(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    data[c] = a

    return data


def gtir(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    if a > data[b]:
        data[c] = 1
    else:
        data[c] = 0

    return data


def gtri(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    if data[a] > b:
        data[c] = 1
    else:
        data[c] = 0

    return data


def gtrr(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    if data[a] > data[b]:
        data[c] = 1
    else:
        data[c] = 0

    return data


def eqir(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    if a == data[b]:
        data[c] = 1
    else:
        data[c] = 0

    return data


def eqri(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    if data[a] == b:
        data[c] = 1
    else:
        data[c] = 0

    return data


def eqrr(inst: Instruction, data: Instruction) -> Instruction:
    opnum, a, b, c = inst

    if data[a] == data[b]:
        data[c] = 1
    else:
        data[c] = 0

    return data


ops = {
    'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr,
}


def run() -> None:
    """
    Main function.
    """
    with open("./input1.txt") as f:
        # Load data.
        data = f.read().splitlines()

        sequences = []
        sequence = []
        for row in data:
            if row.startswith("Before: "):
                row = row.replace("Before:", "").strip().lstrip("[")
                row = row.rstrip("]")
                sequence.append([int(x) for x in row.split(", ")])
            elif row.startswith("After: "):
                row = row.replace("After:", "").strip().lstrip("[")
                row = row.rstrip("]")
                sequence.append([int(x) for x in row.split(", ")])
                sequences.append(sequence)
                sequence = []
            elif row != "":
                sequence.append([int(x) for x in row.split(" ")])

        opname_to_opnum = {}
        for sequence in sequences:
            for opname, op in ops.items():
                seq = copy.deepcopy(sequence)
                if seq[2] == op(seq[1], seq[0]):
                    if opname not in opname_to_opnum:
                        opname_to_opnum[opname] = set()
                    opname_to_opnum[opname].add(seq[1][0])

        while [name for name, nums in opname_to_opnum.items() if
               len(nums) > 1]:
            for name, nums in opname_to_opnum.items():
                if len(nums) == 1:
                    for name2, nums2 in opname_to_opnum.items():
                        if len(nums2) != 1:
                            try:
                                nums2.remove(list(nums)[0])
                            except KeyError:
                                pass

        opnum_to_opname = {list(y)[0]: x for x, y in opname_to_opnum.items()}

        with open("./input2.txt") as f:
            data = f.read().splitlines()
            registers = [0, 0, 0, 0]

            for row in data:
                instr = [int(x) for x in row.split(" ")]
                ops[opnum_to_opname[instr[0]]](instr, registers)

            print(registers[0])
        # [print(f"{num}: {name}") for name, num in opnum_to_opname.items()]


print(f"{timeit.timeit(run, number=1)} sec")
