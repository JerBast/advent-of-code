import re

from aocd import get_data


DATA = get_data(year=2024, day=17).split('\n\n')
REGISTERS = list(map(int, re.findall(r'\d+', DATA[0])))
PROGRAM = list(map(int, re.findall(r'\d+', DATA[1])))
STEPS = list(zip(PROGRAM[::2], PROGRAM[1::2]))


def resolve_combo(a: int, b: int, c: int, combo: int) -> int:
    match combo:
        case 4: return a
        case 5: return b
        case 6: return c
    return combo


def run(a: int, b: int, c: int) -> str:
    ip = 0
    out = ''
    while ip < len(STEPS):
        literal, combo = STEPS[ip]
        rc = resolve_combo(a, b, c, combo)
        match literal:
            case 0: a //= 2 ** rc
            case 1: b ^= rc
            case 2: b = rc % 8
            case 3: ip = ip if a == 0 else rc - 1
            case 4: b ^= c
            case 5: out += str(rc % 8)
            case 6: b = a // 2 ** rc
            case 7: c = a // 2 ** rc
        ip += 1
    return out


def part1():
    print(*run(*REGISTERS), sep=',')


def part2():
    _, b, c = REGISTERS
    queue = list('01234567')
    prog_str = ''.join(map(str, PROGRAM))
    while len(queue) != 0:
        a = queue.pop(0)
        if prog_str.endswith(run(int(a, 8), b, c)):
            if len(a) == len(prog_str):
                print(int(a, 8))
                break
            for i in '01234567':
                queue.append(a + i)


if __name__ == '__main__':
    part1()
    part2()
