# Helicopter in Python!
import random

import pygame

pygame.init()

HEIGHT = 600
WIDTH = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Helicopter in Python!')
font = pygame.font.Font('freesansbold.ttf', 20)
fps = 60
timer = pygame.time.Clock()
new_map = True
map_rects = []
rect_width = 10
total_rects = WIDTH // rect_width
spacer = 10
player_x = 100
player_y = 300
flying = False
y_speed = 0
gravity = 0.3
map_speed = 2
score = 0
high_score = 0
active = True
heli = pygame.transform.scale(pygame.image.load('helicopter.png'), (60, 60))


def generate_new():
    global player_y
    rects = []
    top_height = random.randint(0, 300)
    player_y = top_height + 150
    for i in range(total_rects):
        top_height = random.randint(top_height - spacer, top_height + spacer)
        if top_height < 0:
            top_height = 0
        elif top_height > 300:
            top_height = 300
        top_rect = pygame.draw.rect(screen, 'green', [i * rect_width, 0, rect_width, top_height])
        bot_rect = pygame.draw.rect(screen, 'green', [i * rect_width, top_height + 300, rect_width, HEIGHT])
        rects.append(top_rect)
        rects.append(bot_rect)
    return rects


def draw_map(rects):
    for i in range(len(rects)):
        pygame.draw.rect(screen, 'green', rects[i])
    pygame.draw.rect(screen, 'dark gray', [0, 0, WIDTH, HEIGHT], 12)


def draw_player():
    # draw player hit box as circle, and player helicopter image
    player = pygame.draw.circle(screen, 'black', (player_x, player_y), 20)
    screen.blit(heli, (player_x - 40, player_y - 30))
    return player


def move_player(y_pos, speed, fly):
    if fly:
        speed += gravity
    else:
        speed -= gravity
    y_pos -= speed
    return y_pos, speed


def move_rects(rects):
    global score
    for i in range(len(rects)):
        rects[i] = (rects[i][0] - map_speed, rects[i][1], rect_width, rects[i][3])
        if rects[i][0] + rect_width < 0:
            rects.pop(1)
            rects.pop(0)
            top_height = random.randint(rects[-2][3] - spacer, rects[-2][3] + spacer)
            if top_height < 0:
                top_height = 0
            elif top_height > 300:
                top_height = 300
            rects.append((rects[-2][0] + rect_width, 0, rect_width, top_height))
            rects.append((rects[-2][0] + rect_width, top_height + 300, rect_width, HEIGHT))
            score += 1
    return rects


def check_collision(rects, circle, act):
    for i in range(len(rects)):
        if circle.colliderect(rects[i]):
            act = False
    return act


run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    if new_map:
        map_rects = generate_new()
        new_map = False
    draw_map(map_rects)
    player_circle = draw_player()
    if active:
        player_y, y_speed = move_player(player_y, y_speed, flying)
        map_rects = move_rects(map_rects)
    active = check_collision(map_rects, player_circle, active)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flying = True
            if event.key == pygame.K_RETURN:
                if not active:
                    new_map = True
                    active = True
                    y_speed = 0
                    map_speed = 2
                    if score > high_score:
                        high_score = score
                    score = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                flying = False
    map_speed = 2 + score//50
    spacer = 10 + score//100

    screen.blit(font.render(f'Score: {score}', True, 'black'), (20, 15))
    screen.blit(font.render(f'High Score: {high_score}', True, 'black'), (20, 565))
    if not active:
        screen.blit(font.render('Press Enter to Restart', True, 'black'), (300, 15))
        screen.blit(font.render('Press Enter to Restart', True, 'black'), (300, 565))
    pygame.display.flip()
pygame.quit()
