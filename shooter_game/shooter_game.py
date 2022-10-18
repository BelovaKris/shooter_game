from pygame import *
from time import sleep
from time import time as timer
from random import randint
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, pl_y, pl_x, pl_speed, size_x, size_y):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale(image.load(pl_image), (self.size_x, self.size_y))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        key1 = key.get_pressed()
        if key1[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key1[K_RIGHT] and self.rect.x < win_width - self.size_x:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.top, self.rect.centerx - 10, 15, 20, 50)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global f
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(10, win_width - 70)
            f += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

font2 = font.SysFont('Arial', 40)
font1 = font.SysFont('Arial', 80)
font3 = font.SysFont('Arial', 20)
win_width = 900
win_height = 650
t = 0
f = 0
display.set_caption('pygame window')
window = display.set_mode((win_width, win_height))
clock = time.Clock()
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
FPS = 80
kill1 = 0
num_fire = 0
life = 10
r1 = Player('rocket.png', win_height - 150, win_width/2, 10, 100, 150)
game = True
finish = True
rel_time = False
asteroids = sprite.Group()
mixer.init()
mx = mixer.Sound('fire.ogg')
# mixer.music.load('space.ogg')
# mixer.music.play()
monsters = sprite.Group()
bullets = sprite.Group()
for m in range(5):
    monster = Enemy('ufo.png', 0, randint(10, win_width), randint(2, 7), 70, 50)
    monsters.add(monster)
for n in range(3):
    asteroid = Enemy('asteroid.png', 0, randint(10, win_width), randint(1, 3), 70, 50)
    asteroids.add(asteroid)
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN and i.key == K_SPACE:
            if num_fire <= 10 and rel_time == False:
                r1.fire()
                num_fire += 1
                mx.play()
            if num_fire >= 10 and rel_time == False:
                rel_time = True
                start_time = timer()
        
    if finish:
        window.blit(background, (0, 0))
        r1.reset()
        r1.update()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        asteroids.update()
        bullets.update()
        monsters.update()
        sprite_collide = sprite.groupcollide(monsters, bullets, True, True)
        if sprite.spritecollide(r1, asteroids, True):
            life -= 1
        for i in sprite_collide:
            kill1 += 1
            monster = Enemy('ufo.png', 0, randint(10, win_width), randint(2, 7), 70, 50)
            monsters.add(monster)
        if kill1 >= 10:
            text_3 = font1.render('YOU WIN!', 1, (255, 255, 255))
            window.blit(text_3, (330, 325))
            finish = False
        if f >= 150 or life <= 0:
            text_4 = font1.render('YOU LOSE!', 1, (255, 255, 255))
            window.blit(text_4, (330, 325))
            finish = False
        if rel_time == True:
            end_time = timer()
            now_time = end_time - start_time
            if now_time >= 2:
                num_fire = 0
                rel_time = False
            else:
                text_6 = font3.render('Перезарядка...' + str(round(now_time, 1)), 1, (255, 255, 255))
                window.blit(text_6, (r1.rect.left, r1.rect.centery))
        text_1 = font2.render('Пропущено: ' + str(f), 1, (255, 255, 255))
        text_2 = font2.render('Счёт: ' + str(kill1), 1, (255, 255, 255))
        text_5 = font2.render('Жизни: ' + str(life), 1, (255, 255, 255))
        window.blit(text_1, (20, 55))
        window.blit(text_5, (750, 55))
        window.blit(text_2, (20, 20))
        display.update()
    else:
        sleep(3)
        finish = True
        f = 0
        num_fire = 0
        rel_time = False
        kill1 = 0
        life = 10
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        for m in range(5):
            monster = Enemy('ufo.png', 0, randint(10, win_width), randint(2, 7), 70, 50)
            monsters.add(monster)
        for n in range(3):
            asteroid = Enemy('asteroid.png', 0, randint(10, win_width), randint(1, 3), 70, 50)
            asteroids.add(asteroid)
    clock.tick(FPS)

