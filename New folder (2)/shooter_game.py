#Create your own shooter


from pygame import *
from random import randint
from time import time as timer 


win_width = 700
win_height = 500
lost = 0
SCORE = 0 
bullet_speed = - 10
num_fire = 0

bullets = sprite.Group()

window = display.set_mode((win_width, win_height))
display.set_caption("shooter game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_w, player_h , player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(player_w,player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and (self.rect.x > 10):
            self.rect.x -= self.speed
        if keys[K_RIGHT] and (self.rect.x < win_width-90):
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15,20, bullet_speed)
        bullets.add(bullet)

        
class enemy(GameSprite):

    def update(self):
        global lost
        if self.rect.y >= win_height:
            lost = lost + 1

            self.rect.y = 0
            self.rect.x = randint(100,600)
        else:
            self.rect.y += speed
    
class Bullet(GameSprite):
    def  update(self):

        self.rect.y += self.speed
        if self.rect.y < 0:
            self .kill()


font.init()
style = font.SysFont("Arial", 36)
win = style.render("WIN", True, (255,255,255))
loss = style.render("LOSE", True, (120,0,0))
reloadFont = font.SysFont("Arial", 30)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()


clock = time.Clock()
FPS = 60
game = True
speed = 2


player = Player("rocket.png", 350, 400, 65, 65, 10)
    


enemys = sprite.Group()
enemys.add(enemy("ufo.png", 100, 0, 65, 65, 50))
enemys.add(enemy("ufo.png", 370, 120,65, 65, 100))
enemys.add(enemy("ufo.png", 490, 50,65, 65, 70))
enemys.add(enemy("ufo.png", 500, 20,65, 65, 75))
enemys.add(enemy("ufo.png", 600, 50,65, 65, 90))

rocks = sprite.Group()
rocks.add(enemy("asteroid.png", 120, 50, 65, 65, 70))


fireSFX = mixer.Sound("fire.ogg")

Finish = False
timer()

rel_timer = False
curTime = 0
stopTime = 0

while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_timer == False:
                    player.fire()
                    fireSFX.play()
                    num_fire += 1
                if num_fire >= 5 and rel_timer  == False:
                    rel_timer = True
                    stopTime = timer()
                
    
    if Finish != True:
        text_lose = style.render("Missed:" +str(lost),1,(255,255,255))
        window.blit(background,(0,0))
        window.blit(text_lose, (10,10))
        player.update()
        enemys.update()
        bullets.update()
        rocks.update()

        bullets.draw(window)
        player.reset()
        enemys.draw(window)
        rocks.draw(window)


        if rel_timer == True:
            curTime = timer()
            if (curTime-stopTime) < 3: 
                reload = reloadFont.render("Reloading...", True, (255, 0, 0))
                window.blit(reload,(300, 400))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(enemys, bullets, True, True)


        for c in collides:
            SCORE += 1
            enemy1 = enemy("ufo.png", 100, 0, 65, 65, 50)
            enemys.add(enemy1)

        if (sprite.spritecollide(player, enemys or rocks, False)) or lost >= 5 :
            Finish  = True
            window.blit(loss, (200, 200))

        if SCORE >= 10:
            Finish = True
            window.blit(win,(200,200))


    display.update()
    clock.tick(FPS)




