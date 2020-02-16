import itertools


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

def run(x, inputs, start_pos=0):
    pos = start_pos
    out = -1
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
            if len(inputs) == 0:
                return (pos, out)
            read(x, x[pos+1], inputs.pop(0))
            pos += 2
        elif op == "04":
            out = write(x, pc)
            # print(out)
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

    return (pos, out)

class Amp:
    def __init__(self, idx, inp):
        self.idx = idx
        self.pos = 0
        self.instr = 0
        self.inp = inp

    def dump(self):
        return ' '.join(['Amp ', str(self.idx), 'pos =', str(self.pos), 'instr =', str(self.instr)])


if __name__ == '__main__':
    inp = []
    with open('inputs/7-input') as f:
        for n in f.read().strip().split(','):
            inp.append(int(n))
    # sol 1
    values = []
    for phases in itertools.permutations(range(5)):
        instruction = 0
        for phase in phases:
            _, instruction = run(inp, [phase, instruction])
        values.append((instruction, phases))
    print(max(values))

    # sol 2
    values = []
    for phases in itertools.permutations(range(5, 10)):
        instruction = 0
        count = 0
        # create amps
        amps = [Amp(i, inp[:]) for i in range(5)]
        # init amps with a phase input
        for i in range(len(amps)):
            amps[i].pos, _ = run(amps[i].inp, [phases[i]])

        while True:
            a, b = count % 5, (count+1) % 5
            # run current amp and update current amp position after
            amps[a].pos, new_instr = run(amps[a].inp, [amps[a].instr], amps[a].pos)

            # end of code
            if new_instr == -1:
                break

            # update next amp input instruction
            amps[b].instr = new_instr

            count += 1


        # print('\n'.join([amp.dump() for amp in amps]))

        values.append((amps[0].instr, phases))

    print(max(values))

