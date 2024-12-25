from aocd import get_data
from collections import defaultdict


DATA = get_data(year=2024, day=24).split('\n\n')
EXPR = {}
MEM = defaultdict(lambda: None)

for expr in DATA[1].splitlines():
    inp, out = expr.split(' -> ')
    EXPR[out] = inp.split()

for inp in DATA[0].splitlines():
    k, v = inp.split(': ')
    MEM[k] = int(v)


def solve(expr: dict[str, tuple]) -> int:
    stack = [k for k in expr if k[0] == 'z']
    mem = MEM.copy()

    while len(stack):
        v = stack.pop()
        lhs, op, rhs = expr[v]
        l, r = mem[lhs], mem[rhs]

        if l is None and r is None:
            stack.extend((v, lhs, rhs))
            continue

        match op:
            case 'OR':
                if l == 1 or r == 1:
                    mem[v] = 1
                elif l == 0 and r == 0:
                    mem[v] = 0
                else:
                    stack.extend((v, lhs if l is None else rhs))
            case 'XOR':
                if l is not None and r is not None:
                    mem[v] = l ^ r
                else:
                    stack.extend((v, lhs if l is None else rhs))
            case 'AND':
                if l == 0 or r == 0:
                    mem[v] = 0
                elif l == 1 and r == 1:
                    mem[v] = 1
                else:
                    stack.extend((v, lhs if l is None else rhs))

    zs = sorted([k for k in mem if k[0] == 'z'], reverse=True)
    return int(''.join(str(mem[z]) for z in zs), 2)


def part1():
    print(solve(EXPR))


def part2():
    def investigate(out: str, depth: int = 0) -> None:
        if out not in EXPR:
            return
        lhs, op, rhs = EXPR[out]
        lhs, rhs = sorted([lhs, rhs])
        if lhs in EXPR and EXPR[lhs][1] == 'XOR':
            lhs, rhs = rhs, lhs
        elif rhs in EXPR and EXPR[rhs][1] == 'AND' and EXPR[rhs][0][0] in 'xy':
            lhs, rhs = rhs, lhs
        print('  ' * depth + out, '=', lhs, op, rhs)
        investigate(lhs, depth + 1)
        investigate(rhs, depth + 1)

    def swap(fst: str, snd: str) -> None:
        EXPR[fst], EXPR[snd] = EXPR[snd], EXPR[fst]

    swap('dwp', 'kfm')
    swap('z31', 'jdr')
    swap('z22', 'gjh')
    swap('z08', 'ffj')
    for k in sorted([k for k in EXPR if k[0] == 'z'], reverse=True):
        investigate(k)
        print('-' * 50)
        input()


if __name__ == '__main__':
    part1()
    part2()
