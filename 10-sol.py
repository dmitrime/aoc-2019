from math import atan2
from collections import defaultdict

def sights(point, lines):
    si, sj = point
    direct = set()
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if (i, j) != (si, sj) and lines[i][j] == '#':
                direct.add(atan2(i-si, j-sj))
    return len(direct)

def solve(lines):
    result = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == '#':
                asteroids = sights((i,j), lines)
                if result < asteroids:
                    result = asteroids
                    pos = (i, j)
    return result, pos

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def position(point, pos):
    y, x = point
    sy, sx = pos
    l = atan2(y-sy, x-sx)
    if y < sy and x >= sx:
        return ('q1', l)
    elif y >= sy and x >= sx:
        return ('q2', l)
    elif y >= sy and x < sx:
        return ('q3', l)
    elif y < sy and x <= sx:
        return ('q4', l)


def rotate(pos, lines):
    si, sj = pos
    seen = set([pos])
    count = 0 
    total = sum([x.count('#') for x in lines]) - 1
    while count < min(total, 200):
        halves = defaultdict(dict)
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                point = (i, j)
                if lines[i][j] == '#' and point not in seen:
                    m = manhattan(point, pos)
                    save = (m, point)
                    key, l = position(point, pos)
                    halves[key][l] = min(save, halves[key].get(l, save))

        for q in ['q1', 'q2', 'q3', 'q4']:
            h = sorted(halves[q].items())
            for _, x in h: seen.add(x[1])
            count += len(h)
            if count > 200:
                count -= len(h)
                for _, x in h:
                    count += 1
                    if count == 200:
                        return x[1]
    return None


if __name__ == '__main__':
    # sol 1
    lines = []
    with open('inputs/10-input') as f:
        for line in f:
            lines.append(line.strip())
    
    result, pos = solve(lines)
    print(result)
    print(pos)

    # sol 2
    ry, rx = rotate(pos, lines)
    print(rx*100 + ry)
