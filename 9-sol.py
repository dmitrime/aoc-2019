from collections import defaultdict

class State:
    def __init__(self, prog, instruction):
        self.mem = defaultdict(int)
        self.mem.update({k:v for k,v in enumerate(prog)})
        self.instruction = instruction
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
        self._write(self.ip + 1, m1, self.instruction.pop(0))
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
        return self


def run(prog, instruction):
    state = State(prog, [instruction])

    while not state.stop:
        state = state.execute()
        if state.output:
            print(state.output, end=' ')
    print()


if __name__ == '__main__':
    prog = []
    with open('inputs/9-input') as f:
        prog.extend(map(int, f.read().strip().split(',')))

    # sol 1
    run(prog, 1)

    # sol 2
    run(prog, 2)

