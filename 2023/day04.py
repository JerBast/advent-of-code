from aocd import get_data


data = get_data(year=2023, day=4).splitlines()

tot_score = 0
for line in data:
    score = 0
    winning, own = line.split(': ')[1].split(' | ')
    winning = set(map(int, winning.split()))
    own = set(map(int, own.split()))
    for o in own:
        if o in winning:
            if score == 0:
                score = 1
            else:
                score *= 2
    tot_score += score

print(tot_score)

cards = [0] * len(data)
for idx, line in enumerate(data):
    winning, own = line.split(': ')[1].split(' | ')
    winning = set(map(int, winning.split()))
    own = set(map(int, own.split()))
    next = 1
    cards[idx] += 1
    for o in own:
        if o in winning:
            cards[idx + next] += cards[idx]
            next += 1

print(sum(cards))
