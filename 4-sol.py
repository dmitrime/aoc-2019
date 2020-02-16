def conditions1(pw):
    repeated, non_dec = False, True
    for i in range(1, 6):
        if pw[i-1] == pw[i]:
            repeated = True
        if pw[i-1] > pw[i]:
            non_dec = False
    return repeated and non_dec

def conditions2(pw):
    repeated, non_dec = False, True
    dg = 0
    for i in range(1, 6):
        if pw[i-1] == pw[i] and pw[i] != dg:
            if i+1 < 6 and pw[i+1] == pw[i]:
                dg = pw[i]
            else:
                repeated = True
        if pw[i-1] > pw[i]:
            non_dec = False
    return repeated and non_dec


if __name__ == '__main__':
    start = 183564
    end = 657474

    # sol 1
    count = sum([1 for r in range(start, end+1) if conditions1(str(r))])
    print(count)

    # sol 2
    count = sum([1  for r in range(start, end+1) if conditions2(str(r))])
    print(count)
