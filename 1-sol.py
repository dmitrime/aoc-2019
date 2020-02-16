def calc(n):
    return n / 3 - 2;

def rec(n):
    x = calc(n)
    if x <= 0: return 0
    return x + rec(x)

if __name__ == '__main__':
    # sol 1
    total = 0
    with open('inputs/1-input') as f:
        for line in f:
            total += calc(int(line))
    print(total)

    # sol 2
    total = 0
    with open('inputs/1-input') as f:
        for line in f:
            fuel = calc(int(line))
            total += fuel + rec(fuel)

    print(total)
