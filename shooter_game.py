
from pygame import *
from random import randint
window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
game = True
finish = False
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound  = mixer.Sound('fire.ogg')


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y))       
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
        
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 700:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top,15, 20,  -15)
        bullets.add(bullet)
player = Player('rocket.png',300, 400,60, 60, 10)

score = 0
lost = 0
max_lost = 3
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost += 1
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

            
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy ('ufo.png', randint(60, 620), 0,60, 60, randint(2,7))
    monsters.add(monster)
    
bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(80,800 - 80), -40, 80, 50, randint(1,5))
    asteroids.add(asteroid)
font.init()
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN', True, (255, 255, 255))
lose = font.render('YOU LOSE', True,(220, 220, 220))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
        
    if not finish:
        window.blit(background,(0,0))
        text_lose = font.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        score_lose = font.render('Счёт:' + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))
        window.blit(score_lose,(10,80))
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy ('ufo.png', randint(60, 620), 0,60, 60, randint(2,7))
            monsters.add(monster)
        if score >= 10:
            finish = True
            window.blit(win,(200,200))
        if sprite.spritecollide(player,monsters,False) or lost >= 3:
            finish = True
            window.blit(lose,(200,200))
    else:
        finish = False
        if sprite.spritecollide(player, asteroids, False ) or lost >= max_lost:
            finish = True
            window.blit(lose,(200, 200))
        score = 0
        lost = 0
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        for asteroid in asteroids:
            asteroid.kill()
        time.delay(60)
        for i in range(1,6):
            monster = Enemy ('ufo.png', randint(60, 620), 0,60, 60, randint(2,7))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy('asteroid.png', randint(80,800 - 80), -40, 80, 50, randint(1,5))
            asteroids.add(asteroid)
    display.update()
    time.delay(50)