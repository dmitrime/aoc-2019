from collections import defaultdict

class State:
    def __init__(self, prog, instructions):
        self.mem = defaultdict(int)
        self.mem.update({k:v for k,v in enumerate(prog)})
        self.instructions = instructions
        self.ip = 0
        self.output = None
        self.base = 0
        self.stop = False

    def nextOp(self):
        return self.mem[self.ip] % 100

    def mode(self):
        code = self.mem[self.ip] 
        return code // 100 % 10, code // 1000 % 10, code // 10000

    def _read(self, i, mode):
        if mode == 1: # immediate
            return self.mem[i]
        addr = self.mem[i]
        if mode == 2: # relative
            addr += self.base
        return self.mem[addr]

    def _write(self, i, mode, val):
        addr = self.mem[i]
        if mode == 2: # relative
            addr += self.base
        self.mem[addr] = val

    def _arg(self, i,  m):
        return self._read(self.ip + i, m)

    def add(self, m1, m2, m3):
        a, b = self._arg(1, m1), self._arg(2, m2)
        self._write(self.ip + 3, m3, a + b)
        self.ip += 4

    def mul(self, m1, m2, m3):
        a, b = self._arg(1, m1), self._arg(2, m2)
        self._write(self.ip + 3, m3, a * b)
        self.ip += 4

    def set(self, m1, _, __):
        self._write(self.ip + 1, m1, self.instructions.pop(0))
        self.ip += 2

    def out(self, m1, _, __):
        self.output = self._arg(1, m1)
        self.ip += 2

    def jmp(self, m1, m2, _):
        if self._arg(1, m1) != 0:
            self.ip = self._arg(2, m2)
        else:
            self.ip += 3

    def jnz(self, m1, m2, _):
        if self._arg(1, m1) == 0:
            self.ip = self._arg(2, m2)
        else:
            self.ip += 3

    def lss(self, m1, m2, m3):
        if self._arg(1, m1) < self._arg(2, m2):
            self._write(self.ip + 3, m3, 1)
        else:
            self._write(self.ip + 3, m3, 0)
        self.ip += 4

    def eql(self, m1, m2, m3):
        if self._arg(1, m1) == self._arg(2, m2):
            self._write(self.ip + 3, m3, 1)
        else:
            self._write(self.ip + 3, m3, 0)
        self.ip += 4

    def adj(self, m1, _, __):
        self.base += self._arg(1, m1)
        self.ip += 2

    def halt(self, _, __, ___):
        self.stop = True
        self.ip += 1

    def execute(self):
        self.output = None
        operations = {
                1: lambda state, mode: state.add(*mode),
                2: lambda state, mode: state.mul(*mode),
                3: lambda state, mode: state.set(*mode),
                4: lambda state, mode: state.out(*mode),
                5: lambda state, mode: state.jmp(*mode),
                6: lambda state, mode: state.jnz(*mode),
                7: lambda state, mode: state.lss(*mode),
                8: lambda state, mode: state.eql(*mode),
                9: lambda state, mode: state.adj(*mode),
                99: lambda state, mode: state.halt(*mode)
        }
        operations[self.nextOp()](self, self.mode())

def turn(d, turn):
    if d == 'up':
        return 'left' if turn == 0 else 'right'
    elif d == 'down':
        return 'right' if turn == 0 else 'left'
    elif d == 'left':
        return 'down' if turn == 0 else 'up'
    elif d == 'right':
        return 'up' if turn == 0 else 'down'

def move(d, pos):
    x, y = pos
    if d == 'up':
        y += -1
    elif d == 'down':
        y += 1
    elif d == 'right':
        x += 1
    elif d == 'left':
        x -= 1
    return (x, y)


def update(world, pair):
    paint, trn = pair
    # print('paint =', paint, ' turn =', trn)
    # paint
    pos = world['pos']
    world['map'][pos] = '#' if paint == 1 else '.'
    # turn
    d = world['dir'] = turn(world['dir'], trn)
    # move
    newpos = world['pos'] = move(d, pos)
    # 1 if over white, 0 if over black
    if newpos in world['map'] and world['map'][newpos] == '#':
        return 1
    else:
        return 0

def visual(world):
    m = world['map']
    minx = min(m.keys(), key=lambda x: x[0])[0]
    maxx = max(m.keys(), key=lambda x: x[0])[0]
    miny = min(m.keys(), key=lambda x: x[1])[1]
    maxy = max(m.keys(), key=lambda x: x[1])[1]

    for y in range(miny, maxy+1, 1):
        for x in range(minx, maxx+1, 1):
            if (x, y) in m:
                print(m[(x, y)], end='')
            else:
                print('.', end='')
        print()

def run(prog, instructions):
    state = State(prog, instructions)

    world = {'map': dict(), 'dir': 'up', 'pos': (0, 0)}
    pair = []
    while not state.stop:
        if state.output is not None:
            pair.append(state.output)
        if len(pair) == 2:
            state.instructions.append(update(world, pair))
            pair = []

        state.execute()
    return world


if __name__ == '__main__':
    prog = []
    with open('inputs/11-input') as f:
        prog.extend(map(int, f.read().strip().split(',')))

    # sol 1
    world = run(prog, [0])
    print(len(world['map']))

    # sol 2
    world = run(prog, [1])
    visual(world)
