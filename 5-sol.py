def add(x, a, b, c):
    x[c] = x[a] + x[b]

def mul(x, a, b, c):
    x[c] = x[a] * x[b]

def read(x, a, val):
    x[a] = val

def write(x, a):
    return x[a]

def jmp_true(x, a, b, pos):
    if x[a] != 0:
        return x[b]
    return pos+3

def jmp_false(x, a, b, pos):
    if x[a] == 0:
        return x[b]
    return pos+3

def less(x, a, b, c):
    if x[a] < x[b]:
        x[c] = 1
    else:
        x[c] = 0

def eq(x, a, b, c):
    if x[a] == x[b]:
        x[c] = 1
    else:
        x[c] = 0

def run(x, input_instruction):
    pos = 0
    while True:
        ins = f"{x[pos]:05}"

        _, b, c = ins[:3]
        op = ins[3:]

        if op == "99":
            break

        pc = x[pos+1] if c == '0' else pos+1
        pb = x[pos+2] if b == '0' else pos+2

        if op == "01":
            add(x, pc, pb, x[pos+3])
            pos += 4
        elif op == "02":
            mul(x, pc, pb, x[pos+3])
            pos += 4
        elif op == "03":
            read(x, x[pos+1], input_instruction)
            pos += 2
        elif op == "04":
            print(write(x, pc))
            pos += 2
        elif op == "05":
            pos = jmp_true(x, pc, pb, pos)
        elif op == "06":
            pos = jmp_false(x, pc, pb, pos)
        elif op == "07":
            less(x, pc, pb, x[pos+3])
            pos += 4
        elif op == "08":
            eq(x, pc, pb, x[pos+3])
            pos += 4

if __name__ == '__main__':
    inp = []
    with open('inputs/5-input') as f:
        for n in f.read().strip().split(','):
            inp.append(int(n))
    # sol 1
    # run(inp, 1)

    run(inp, 5)
