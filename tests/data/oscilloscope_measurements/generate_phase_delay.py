for filename in ("sine_1vpp_1khz.csv", "square_1vpp_1khz.csv"):
    for n in (5, 10, 15, 20):
        lines = list(open(filename).readlines())
        additional_lines = []

        target = 500 - n

        while len(lines) > target:
            additional_lines.append(lines.pop(target))

        for line in additional_lines[::-1]:
            lines.insert(2, line)

        open(filename.replace('.csv', f'_delayed_{n}.csv'), 'w').write(''.join(lines))

for filename in ("sine_1vpp_200hz.csv", "square_1vpp_200hz.csv"):
    for n in (25, 50, 62, 75, 100, 125):
        lines = list(open(filename).readlines())
        additional_lines = []

        target = 500 - n

        while len(lines) > target:
            additional_lines.append(lines.pop(target))

        for line in additional_lines[::-1]:
            lines.insert(2, line)

        open(filename.replace('.csv', f'_delayed_{n}.csv'), 'w').write(''.join(lines))


