"""
--- Part Two ---

In order to determine the timing window for your underflow exploit, you also need an upper bound:

What is the lowest non-negative integer value for register 0 that causes the program to halt after executing the most instructions? (The program must actually halt; running forever does not count as halting.)
"""
x, a, b, c, d, e = (1, 0, 0, 0, 0, 0)
c = 0  # 5

a = c | 65536
c = 10373714

values = []
while True:
    c += a & 255
    c &= 16777215
    c *= 65899
    c &= 16777215

    if a < 256:
        # What we essentially want is the last unique value of c.
        if c not in values:
            values.append(c)
        else:
            print('EXIT()', values[-1])
            exit()

        if c == x:
            print('EXIT()', c)
            exit()
        else:
            a = c | 65536
            c = 10373714
            continue

    else:
        a = int(a / 256)
