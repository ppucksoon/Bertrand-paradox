import random
import math
import pickle
import time

def save_data(mid_lines, solution):
    start_t = time.time()

    x = [i for i in range(401)]
    y = [0 for i in range(401)]
    for i in range(len(mid_lines)):
        for j in range(401):
            if round(mid_lines[i], 0) <= (j+1):
                y[j] += 1
                break

    with open(f"./pickle_data/s{solution}_y_data.pickle","wb") as fw:
        pickle.dump(y, fw)

    print(f"데이터 저장 소요시간 : {time.time() - start_t}초")

def solution(num):
    radius = 200
    mid_lines = []
    count = 0
    stop_num = 10000000

    def sol_1():
        intersection_point = []

        for i in range(2):
            theta = math.radians(random.uniform(0, 360))
            intersection_point.append((radius*math.cos(theta), radius*math.sin(theta)))
        return intersection_point

    def sol_2():
        theta = math.radians(random.uniform(0, 360))
        length = random.uniform(0, radius)

        intersection_point = ((radius*math.cos(theta + math.acos(length/radius)), radius*math.sin(theta + math.acos(length/radius))), \
                            (radius*math.cos(theta - math.acos(length/radius)), radius*math.sin(theta - math.acos(length/radius))))
        return intersection_point

    def sol_3():
        while True:
            mid_point = (random.uniform(-radius, radius), random.uniform(-radius, radius))
            length = math.sqrt(math.pow(mid_point[0], 2) + math.pow(mid_point[1], 2))
            if length <= radius:
                break
        theta = math.acos(mid_point[0]/length)
        if mid_point[1] < 0:
            theta += math.pi

        th_len = math.sqrt(math.pow(radius, 2) - math.pow(length, 2))
        intersection_point = ((length*math.cos(theta) + th_len*math.sin(theta), length*math.sin(theta) - th_len*math.cos(theta)), \
                            (length*math.cos(theta) - th_len*math.sin(theta), length*math.sin(theta) + th_len*math.cos(theta)))
        return intersection_point

    start_t = time.time()

    while True:
        match num:
            case 1:
                intersection_point = sol_1()
            case 2:
                intersection_point = sol_2()
            case 3:
                intersection_point = sol_3()

        line_length = math.sqrt(math.pow(intersection_point[0][0] - intersection_point[1][0], 2) + \
                                math.pow(intersection_point[0][1] - intersection_point[1][1], 2))

        count += 1
        mid_lines.append(line_length)

        if count >= stop_num:
            print(f"3번 풀이법 실험 소요시간 : {time.time() - start_t}초")
            return mid_lines

# for i in range(1, 4):
#     save_data(solution(i), i)