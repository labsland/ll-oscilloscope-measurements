import os
import glob
import json
import matplotlib.pyplot as plt

for filename in glob.glob('*.csv'):
    times = []
    chan0 = []
    chan1 = []

    with open(filename, "r") as waveform_file:
        for line in waveform_file.readlines():
            if line.startswith("sep="):
                continue
            if line.startswith("Time"):
                continue
            if not line.strip():
                continue

            line_split = line.split()
            times.append(float(line_split[0]))
            chan0.append(float(line_split[1]))
            chan1.append(float(line_split[2]))

    figure = plt.figure()
    plt.plot(chan0)
    plt.plot(chan1)
    figure.savefig(filename.replace('.csv', '.png'))

    json_content = json.dumps({'ch0': chan0, 'ch1': chan1}, indent=4)
    with open(filename.replace('.csv', '.json'), 'w') as fout:
        fout.write(json_content)
