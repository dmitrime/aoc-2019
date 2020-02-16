from collections import defaultdict

def traverse(G):
    count = 0
    keys = set(G.keys())
    for a, _ in G.items():
        start = a
        while start in keys:
            count += 1
            start = G[start][0]
    return count

def transfers(G):
    start1 = 'YOU'
    mem = {}
    keys = set(G.keys())
    count = 0

    while start1 in keys:
        count += 1
        start1 = G[start1][0]
        mem[start1] = count

    count = 0
    start2 = 'SAN'
    while start2 in keys:
        count += 1
        start2 = G[start2][0]
        if start2 in mem:
            break

    return count + mem[start2] - 2


if __name__ == '__main__':
    G = defaultdict(list)
    with open('inputs/6-input') as f:
        for line in f:
            a, b = line.strip().split(')') 
            G[b].append(a)

    # sol 1
    print(traverse(G))

    # sol 2
    print(transfers(G))
