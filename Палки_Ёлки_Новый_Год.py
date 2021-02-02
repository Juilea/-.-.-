import pygame
import sys
import os
import random

pygame.init()
size = width, height = 962, 591
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()
running = True


def load_image(name, colorkey=None):
    fullname = os.path.join('картинки', name)
    try:
        image = pygame.image.load(fullname).convert()
    except:
        print('Файл не найден')
        exit()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Sprites(pygame.sprite.Sprite):
    def __init__(self, im, x, y, classs):
        image = load_image(im, -1)
        super().__init__(classs)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def start_screen(count, n=1, sound=None):

    komiks = pygame.transform.scale(load_image(count), (width, height))

    if sound:
        pygame.mixer.Channel(n).play(pygame.mixer.Sound(sound))

    screen.blit(komiks, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if sound:
                    pygame.mixer.stop()
                return

        pygame.display.flip()
        clock.tick(FPS)


def dragging_sticks(eve):
    if eve.type == pygame.MOUSEBUTTONDOWN and eve.button == 1:
        for brunch in sticks_list:
            if brunch[0].rect.collidepoint(eve.pos) and brunch[2] and brunch[3]:
                brunch[1] = True

                for x in sticks_list:
                    x[2] = False
    elif eve.type == pygame.MOUSEBUTTONUP and eve.button == 1:
        for brunch in sticks_list:
            if brunch[1]:
                brunch[1] = False
                if brunch[4][0] + 3 >= eve.pos[0] >= brunch[4][0] - 3 and \
                        brunch[4][1] + 3 >= eve.pos[1] >= brunch[4][1] - 3:
                    brunch[0].rect.center = brunch[4]
                    brunch[3] = False
                else:
                    brunch[0].rect.x = brunch[5][0]
                    brunch[0].rect.y = brunch[5][1]
                for x in sticks_list:
                    x[2] = True
    elif eve.type == pygame.MOUSEMOTION and eve.buttons[0]:
        for brunch in sticks_list:
            if brunch[1]:
                brunch[0].rect.center = eve.pos


count = 0
name_list = [('v1.png', True), ('v2.png', True), ('v3.png', True),
             ('пл22.png', False), ('пл2.png', False), ('пл3.png', False)]
virysyatki_list = []
virysyatki = pygame.sprite.Group()
group = pygame.sprite.Group()
Sprites("полоска3игра1.png", 2.5, 536, group)
Sprites("полоска3игра2.png", 0, 0, group)


def restart_first():
    global count
    virysyatki_list.clear()
    virysyatki.empty()
    count = 0
    for _ in range(random.randrange(20, 40)):
        random_pil_or_vir = random.choice(name_list)
        vid = Sprites(random_pil_or_vir[0], random.randrange(0, 5) * 142 + 145, -160, virysyatki)
        virysyatki_list.append([vid, False, False, random.randrange(30, 100), random_pil_or_vir[1]])
    virysyatki_list[0][1] = True


def moving_first():
    for i in virysyatki_list:
        if i[1]:
            i[0].rect.y += 4
            if i[0].rect.y >= 550:
                i[1] = False
                if not i[4]:
                    restart_first()
                    break
            if i[0].rect.y >= i[3]:
                if virysyatki_list.index(i) < len(virysyatki_list) - 1:
                    virysyatki_list[virysyatki_list.index(i) + 1][1] = True
                    virysyatki_list[virysyatki_list.index(i)][2] = True


def killing(cor):
    global count
    for i in virysyatki_list:
        if i[0].rect.collidepoint(cor):
            if i[4]:
                restart_first()
            else:
                count += 1
                i[0].kill()
                virysyatki_list.remove(i)


fon = pygame.transform.scale(load_image('fon1.jpg'), (width, height))
start_screen('комикс1.png', 1, 'ком1.wav')
start_screen('комикс2.png', 2, 'ком2.wav')
start_screen('комикс3.png', 3, 'ком3.wav')

pygame.mixer.music.load('минус.mp3')
pygame.mixer.music.set_volume(0.04)
pygame.mixer.music.play(-1)

sticks = pygame.sprite.Group()
s = [('П1П.png', (640, 290), (352, 390)), ('П2П.png', (690, 290), (397, 391)), ('П3П.png', (750, 310), (375, 424)),
     ('П1В.xcf', (640, 50), (347, 174)), ('П2В.png', (750, 180), (402, 174)), ('П3В.png', (670, 400), (375, 198)),
     ('П1С.png', (700, 180), (412, 239)), ('П2С.png', (670, 50), (335, 241)), ('П3С.png', (650, 450), (375, 279)),
     ('П1Н.png', (710, 60), (329, 319)), ('П2Н.png', (630, 180), (423, 317)), ('П3Н.png', (630, 500), (375, 357))]
sticks_list = []

for i in s:
    stick = Sprites(i[0], i[1][0], i[1][1], sticks)
    sticks_list.append([stick, False, True, True, i[2], i[1]])

filling = pygame.sprite.Group()
filling_up = Sprites('Заливка.png', 282, 149, filling)
f = [True, False]

start_screen('komdo1game.png')

while running:
    fon = pygame.transform.scale(load_image('фон2.xcf'), (width, height))
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not f[0] and not f[1]:
                f[0] = True
            if not f[0] and f[1]:
                running = False
    if f[0] and not f[1]:
        dragging_sticks(pygame.event.wait())
        sticks.draw(screen)
    if not any(list(map(lambda i: i[3], sticks_list))):
        filling.draw(screen)
        sticks.draw(screen)
        f = [False, True]
    pygame.display.flip()

    clock.tick(60)

start_screen('kompast1game.png')

start_screen('до2игры.png')

all_sprites = pygame.sprite.Group()
fon = pygame.transform.scale(load_image('фониградва.png'), (width, height))
Sprites("полоска3игра2.png", 0, 0, all_sprites)

name = [('ш1.png', 0), ('ш2.png', 1), ('ш3.png', 2), ('ш4.png', 3)]
ball_list = []
ball = pygame.sprite.Group()

for i in name:
    for j in range(5):
        ball_mov = Sprites(i[0], random.randrange(0, 4) * 144 + 150, -160, ball)
        ball_list.append([ball_mov, True, False, i[1]])

random.shuffle(ball_list)

count = 0


def moving_second():
    global count
    if any(list(map(lambda x: x[1], ball_list))):
        while not ball_list[0][1]:
            ball_list.pop(0)
        ball_list[0][2] = True
    else:
        return True
    if not pygame.sprite.collide_mask(ball_list[0][0], maska4) and \
            not pygame.sprite.collide_mask(ball_list[0][0], maska5) and \
            not pygame.sprite.collide_mask(ball_list[0][0], maska6):
        ball_list[0][0].rect.y += 5
        if ball_list[0][0].rect.y - ball_list[0][0].image.get_rect().y >= 450:
            if ball_list[0][3] == 0:
                if not (120 < ball_list[0][0].rect.x < 235):
                    ball_list[0][0].rect.y = -160
                    ball_list[0][2] = False
                    a = ball_list.pop(0)
                    ball_list.append(a)
                else:
                    ball_list[0][1] = False
                    ball_list[0][2] = False
                    count += 1
            if ball_list[0][3] == 1:
                if not (310 < ball_list[0][0].rect.x < 415):
                    ball_list[0][0].rect.y = -160
                    ball_list[0][2] = False
                    a = ball_list.pop(0)
                    ball_list.append(a)
                else:
                    ball_list[0][1] = False
                    ball_list[0][2] = False
                    count += 1
            if ball_list[0][3] == 2:
                if not (488 < ball_list[0][0].rect.x < 596):
                    ball_list[0][0].rect.y = -160
                    ball_list[0][2] = False
                    a = ball_list.pop(0)
                    ball_list.append(a)
                else:
                    ball_list[0][1] = False
                    ball_list[0][2] = False
                    count += 1
            if ball_list[0][3] == 3:
                if not (590 < ball_list[0][0].rect.x < 775):
                    ball_list[0][0].rect.y = -160
                    ball_list[0][2] = False
                    a = ball_list.pop(0)
                    ball_list.append(a)
                else:
                    ball_list[0][1] = False
                    ball_list[0][2] = False
                    count += 1
    else:
        ball_list[0][0].rect.y = -160
        ball_list[0][2] = False
        a = ball_list.pop(0)
        ball_list.append(a)
    return False


def vector(k):
    for i in ball_list:
        if i[2]:
            if k[pygame.K_LEFT]:
                if i[0].rect.left - 10 >= 142:
                    i[0].rect.left -= 10
                else:
                    i[0].rect.left = 142
            if k[pygame.K_RIGHT]:
                if i[0].rect.left + 10 <= 765:
                    i[0].rect.left += 10
                else:
                    i[0].rect.left = 765


maska4 = Sprites("перегородка.png", 313, 434, all_sprites)
maska4.mask = pygame.mask.from_surface(maska4.image)

maska5 = Sprites("перегородка.png", 494, 434, all_sprites)
maska5.mask = pygame.mask.from_surface(maska5.image)

maska6 = Sprites("перегородка.png", 673, 434, all_sprites)
maska6.mask = pygame.mask.from_surface(maska6.image)

clock = pygame.time.Clock()

f = False
flag = False

running = True
while running:
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and f:
            running = False

    font = pygame.font.Font(None, 45)
    text = font.render("Счёт: {}".format(count), True, (255, 255, 255))
    screen.blit(text, (2, 100))

    key = pygame.key.get_pressed()
    vector(key)
    f = moving_second()

    ball.draw(screen)
    all_sprites.draw(screen)
    clock.tick(25)
    pygame.display.flip()

start_screen('после2игры.png')

start_screen('до3игры.png')

restart_first()
running = True

while running:
    fon = pygame.transform.scale(load_image('фон_игра3_2.png'), (width, height))
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            killing(event.pos)

    font = pygame.font.Font(None, 45)
    text = font.render("Счёт: {}".format(count), True, (255, 255, 255))

    screen.blit(text, (2, 70))
    moving_first()
    virysyatki.draw(screen)
    group.draw(screen)

    if not any((list(map(lambda x: x[1], virysyatki_list)))):
        running = False

    clock.tick(35)
    pygame.display.flip()

start_screen('после3игры.png')


def killing(cor):
    for i in star_list:
        if i[0].rect.collidepoint(cor) and i[3] < 30:
            star.empty()
            predskazanie = Sprites('зв_{}.png'.format(random.randrange(1, 28)), 235, 45.5, star)
            star_list.clear()
            star_list.append([predskazanie, False, False, 30, False])


name_star = [('зв_м.png', False), ('зв_с.png', False), ('зв_б.png', False)]
star_list = []
star = pygame.sprite.Group()

for _ in range(30):
    random_size_of_the_stars = random.choice(name_star)
    star_fall = Sprites(random_size_of_the_stars[0], random.randrange(0, 7) * 125 + 55, -160, star)
    star_list.append([star_fall, False, False, random.randrange(1, 20), random_size_of_the_stars[1]])

star_list[0][1] = True
running = True

while running:
    fon = pygame.transform.scale(load_image('fon1.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if star_list[0][3] == 30:
                running = False
            killing(event.pos)

    for i in star_list:
        if i[1]:
            i[0].rect.y += 9
            if i[0].rect.y >= 600:
                i[1] = False
                i[0].rect.y = -160

            if i[0].rect.y >= i[3]:
                if star_list.index(i) < len(star_list) - 1:
                    star_list[star_list.index(i) + 1][1] = True
                    star_list[star_list.index(i)][2] = True
                else:
                    star_list[0][1] = True

    star.draw(screen)
    clock.tick(35)
    pygame.display.flip()

start_screen('ending.png')

pygame.quit()
sys.exit()