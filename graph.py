import pickle
import math
import matplotlib.pyplot as plt
plt.style.use('dark_background')

color = ["", "", "red", "green"]

for solution in range(1, 4):
    radius = 200
    with open(f"./pickle_data/s{solution}_y_data.pickle","rb") as fr:
        y1 = pickle.load(fr)

    mid_lines = 0
    for i in y1:
        mid_lines += i

    measure = 1
    domain = int((1/measure)*(radius*2+1))
    x = [i*measure for i in range(domain)]
    y2 = [i/mid_lines for i in y1]

    probability = 0
    for i in range(len(y2)):
        if i >= radius*math.sqrt(3):
            probability += y2[i]
    print(probability)

    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Length")
    ax1.set_ylabel("Count")
    ax1.plot(x, y1, color[solution])

    ax2 = ax1.twinx()
    ax2.set_ylabel("Probability")
    ax2.plot(x, y2, color[solution])

    show_mean_graph = False
    if show_mean_graph:
        mean_len = 5
        mean = []
        mean_x = [(mean_len/2)+mean_len*i for i in range(len(y1)//mean_len)]
        for i in range(len(y1)//mean_len):
            sum = 0
            for j in range(mean_len):
                sum += y1[mean_len*i+j]
            mean.append(sum / mean_len)
        ax3 = ax1.twiny()
        ax3.plot(mean_x, mean, color="white")

    plt.title(f"solution{solution}")
    plt.show()