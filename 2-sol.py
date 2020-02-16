def add(x, a, b, c):
    x[c] = x[a] + x[b]

def mul(x, a, b, c):
    x[c] = x[a] * x[b]

def run(x):
    pos = 0
    while True:
        if x[pos] == 99:
            break
        if x[pos] == 1:
            add(x, x[pos+1], x[pos+2], x[pos+3])
        elif x[pos] == 2:
            mul(x, x[pos+1], x[pos+2], x[pos+3])
        pos += 4

if __name__ == '__main__':
    inp = []
    with open('inputs/2-input') as f:
        for n in f.read().strip().split(','):
            inp.append(int(n))
    # sol 1

    # replace
    #inp[1] = 12
    #inp[2] = 2

    #run(inp)
    #print(inp[0])

    #sol 2

    for i in range(0, 100):
        for j in range(0, 100):
            x = inp[:]
            x[1] = i
            x[2] = j
            run(x)
            if x[0] == 19690720:
                print(x[1], x[2])
                break
