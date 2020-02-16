def dist(pos):
    return abs(pos[0]) + abs(pos[1])

def parse(cmds, times):
    x, y = 0, 0
    time = 0
    positions = []
    for cmd in cmds:
        for n in range(int(cmd[1:])):
            time += 1
            if cmd[0] == 'R':
                x += 1
            elif cmd[0] == 'L':
                x -= 1
            elif cmd[0] == 'U':
                y += 1
            elif cmd[0] == 'D':
                y -= 1
            positions.append((x, y))
            times[(x, y)] = time
    return positions


if __name__ == '__main__':
    map1, map2 = {}, {}
    with open('inputs/3-input') as f:
        for c, line in enumerate(f):
            inp = line.strip().split(',')
            if c == 0:
                line1 = set(parse(inp, map1))
            if c == 1:
                line2 = set(parse(inp, map2))

    sect = line1.intersection(line2)
    distances = [dist(s) for s in sect]
    # sol 1
    print(min(distances))

    #sol 2
    print(min([map1[s] + map2[s] for s in sect]))


