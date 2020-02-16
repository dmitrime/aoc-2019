def decode(N, M, im):
    out = ['2']*(M*N)

    for i in range(len(out)):
        for start in range(0, len(im), M*N):
            if im[start+i] != '2':
                out[i] = ' ' if im[start+i] == '0' else '#'
                break

    return out

if __name__ == '__main__':
    # sol 1
    N, M = 25, 6
    image = -1
    with open('inputs/8-input') as f:
        image = f.read().strip()

    layers = [image[i:i+N*M] for i in range(0, len(image), N*M)]
    zeros = map(lambda l: (l.count('0'), l), layers)
    _, l = min(zeros)
    print(l.count('1') * l.count('2'))

    # sol 2
    im = decode(N, M, image)
    for i in range(0, len(im), N):
        print(''.join(im[i:i+N]))
