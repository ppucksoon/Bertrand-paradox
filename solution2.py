from functools import cache
import pygame
import random
import math
import pickle
import time

pygame.init()
pygame.display.set_caption("solution2")

WHITE = (255, 255, 255)
BLUE = (0, 200, 255, 200)
RED = (255, 50, 50, 200)
GRAY = (200, 200, 200, 200)
BLACK = (0, 0 ,0)
FPS = 1000
size = (1500, 800)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

def left_relat_coord(absol_coord):
    return (absol_coord[0] + size[0]//4 - 100, absol_coord[1] + size[1]//2)
def mid_relat_coord(absol_coord):
    return (absol_coord[0] + size[0]*2//4, absol_coord[1] + size[1]//2)
def right_relat_coord(absol_coord):
    return (absol_coord[0] + size[0]*3//4 + 100, absol_coord[1] + size[1]//2)

class line():
    def __init__(self, pos, color, length):
        self.start_pos = pos[0]
        self.end_pos = pos[1]
        self.mid_pos = ((pos[0][0]+pos[1][0])/2, (pos[0][1]+pos[1][1])/2)
        self.color = color
        self.length = length
    
    def draw(self, pos):
        if pos == "left":
            pygame.draw.line(screen, self.color, left_relat_coord(self.start_pos), left_relat_coord(self.end_pos), 1)
        if pos == "mid":
            pygame.draw.line(screen, self.color, mid_relat_coord(self.start_pos), mid_relat_coord(self.end_pos), 1)
        if pos == "right":
            pygame.draw.circle(screen, self.color, right_relat_coord(self.mid_pos), 1)

@cache
def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)

radius = 200
tri_length = radius*math.sqrt(3)
left_lines = []
mid_lines = []
right_lines = []
count = [0, 0] # [긴 경우, 전체]

start_t = time.time()

while not done:
    clock.tick(FPS)
    screen.fill(BLACK)

    theta = math.radians(random.uniform(0, 360))
    length = random.uniform(0, radius)

    intersection_point = ((radius*math.cos(theta + math.acos(length/radius)), radius*math.sin(theta + math.acos(length/radius))), \
                        (radius*math.cos(theta - math.acos(length/radius)), radius*math.sin(theta - math.acos(length/radius))))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    line_length = math.sqrt(math.pow(intersection_point[0][0] - intersection_point[1][0], 2) + \
                            math.pow(intersection_point[0][1] - intersection_point[1][1], 2))

    count[1] += 1
    if line_length >= tri_length:
        left_lines.append(line(intersection_point, RED, None))
        count[0] += 1
    else:
        left_lines.append(line(intersection_point, BLUE, None))
    mid_lines.append(line(intersection_point, GRAY, line_length))
    right_lines.append(line(intersection_point, GRAY, line_length))

    for i in left_lines:
        i.draw("left")
    for i in mid_lines:
        i.draw("mid")
    for i in right_lines:
        i.draw("right")
    pygame.draw.line(screen, WHITE, left_relat_coord(intersection_point[0]), left_relat_coord(intersection_point[1]), 3)
    pygame.draw.circle(screen, WHITE, left_relat_coord((0, 0)), radius, 3)
    pygame.draw.circle(screen, WHITE, mid_relat_coord((0, 0)), radius, 3)
    pygame.draw.circle(screen, WHITE, right_relat_coord((0, 0)), radius, 3)

    probability_txt = font(50).render(f"{count[0]/count[1]:.2f}", True, WHITE)
    probability_txt_center = probability_txt.get_rect()
    probability_txt_center.center = (size[0]//2, size[1]//8)
    screen.blit(probability_txt, probability_txt_center)

    pygame.display.update()

pygame.quit()

update_data = False

if update_data:
    measure = 1
    domain = int((1/measure)*(radius*2+1))
    x = [i*measure for i in range(domain)]
    y = [0 for i in range(domain)]
    for i in mid_lines:
        for j in range(len(x)):
            if round(i.length, int(abs(math.log10(measure)))) <= (j+1)*measure:
                y[j] += 1
                break

    with open("./pickle_data/s2_y_data.pickle","wb") as fw:
        pickle.dump(y, fw)