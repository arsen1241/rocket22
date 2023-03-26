from pygame import *
from random import randint

win = display.set_mode((700, 500))
win_height = 500
win_width = 700
display.set_caption('Шутер')
win = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

font.init()
font2 = font.SysFont('Times New Roman', 36)

speed = 3

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg') 


img_rocket = 'rocket.png'
img_enemy = 'asteroid.png'
img_bullet = 'bullet.png'

FPS = 60
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

monsters = sprite.Group()
for i in range (1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

rocket = Player(img_rocket, 5, win_height-100, 80, 100, 10)
finish = False
game = True
score = 0
lost = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()

    if not finish:
        win.blit(background, (0,0))
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        win.blit(text, (10,20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        win.blit(text_lose, (10,50))
        rocket.update()
        monsters.update()
        rocket.reset()
        monsters.draw(win)
        
        bullets.update()
        bullets.draw(win)
        display.update()
    clock.tick(FPS)