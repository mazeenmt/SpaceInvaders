import pygame
import random
from pygame.locals import *
from pygame.sprite import *
from pygame import mixer
#import os

#os.chdir(r'C:\Users\LENOVO\Documents\Python\Games\SpaceInvaders')

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#define fps
clock = pygame.time.Clock()
fps = 60

#create window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders')


#define game variables
rows = 5
cols = 5
game_over = 0
alien_cooldown = 1000
last_alien_shot =  pygame.time.get_ticks()

#define colours 
red =(255,0,0)
blue =(0,0,255)



#load image
bg= pygame.image.load("img/bg.png")
restart_img = pygame.image.load(r'img\Restart.jpg')
restart_image = pygame.transform.scale(restart_img, (400,269))
youwin_img = pygame.image.load(r'img\YouWin.jpg')
youwin_image = pygame.transform.scale(youwin_img, (600,320))

#load sounds
invader_killed_fx = pygame.mixer.Sound(r'img\invader_killed_fx.wav')
invader_killed_fx.set_volume(0.5)
#game_over_fx = pygame.mixer.Sound(r'img\game_over_fx.wav')
#game_over_fx.set_volume(0.5)
shoot_fx = pygame.mixer.Sound(r'img\shoot_fx.wav')
shoot_fx.set_volume(0.5)
alien_bullet_fx = pygame.mixer.Sound(r'img\alien_bullet_fx.wav')
alien_bullet_fx.set_volume(0.5)
explosion_fx = pygame.mixer.Sound(r'img\explosion_fx.wav')
explosion_fx.set_volume(0.5)
begin_fx = pygame.mixer.Sound(r'img\begin_fx.mp3')
begin_fx.set_volume(0.5)
win_fx = pygame.mixer.Sound(r'img\win_fx.mp3')
win_fx.set_volume(0.5)
exploded_spaceship_fx = pygame.mixer.Sound(r'img\exploded_spaceship_fx.wav')
exploded_spaceship_fx.set_volume(0.5)

def draw_bg():
    screen.blit(bg, (0,0))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect =self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouse over and clicked conditions 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)

        return action

#create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        self.reset(x, y, health)

    def update(self, game_over):
        #set movement speed
        speed = 5
        #set a cooldown variable
        cooldown = 500 #ms
        if game_over == 0:
            #get key press
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
            if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += speed
            #record current time
            time_now = pygame.time.get_ticks()
            #shoot 
            if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
                bullet = Bullets(self.rect.centerx,self.rect.top)
                Bullet_group.add(bullet)
                self.last_shot = time_now
                if game_over == 0:
                    shoot_fx.play()

            #draw health bar 
            pygame.draw.rect(screen, red , (self.rect.x, (self.rect.bottom +10),self.rect.width,15))
            if self.health_remaining >0:
                pygame.draw.rect(screen, blue , (self.rect.x, (self.rect.bottom +10),int(self.rect.width * (self.health_remaining / self.health_start)),15))
            
            #Death
            if self.health_remaining <= 0:
                game_over = -1
                exploded_spaceship_fx.play()
                pygame.mixer.music.stop()
        elif game_over == -1:
            self.image = self.exploded_spaceship

        return game_over
    
    def reset(self, x, y, health):
        pygame.mixer.music.load(r'img\fxBg.mp3')
        pygame.mixer.music.play(-1, 0.5, 5000)
        pygame.sprite.Sprite.__init__(self)
        begin_fx.play()
        Alien_group.empty()
        Alien_Bullet_group.empty()
        Bullet_group.empty()
        #draw_bg()
        create_aliens()
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        exploded_spaceship = pygame.image.load(r'img\exploded_spaceship.png')
        self.exploded_spaceship = pygame.transform.scale(exploded_spaceship, (100,100))

#create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0 : # ki tfout screen m3ach famma bullets
            self.kill()



#create Aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1,5))+".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move_counter = 0
        self.move_direction = 1
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75 :
            self.move_direction *= -1 
            self.move_counter /= self.move_direction

        
#create  Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > SCREEN_HEIGHT: # ki tfout screen m3ach famma bullets
            self.kill()        

#create sprite groups
Spaceship_group = pygame.sprite.Group()
Bullet_group = pygame.sprite.Group()
Alien_group = pygame.sprite.Group()
Alien_Bullet_group = pygame.sprite.Group()

#create aliens
def create_aliens() :
    #generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100,100 + row * 70 )
            Alien_group.add(alien)

create_aliens()

#create player 
spaceship = Spaceship(( SCREEN_WIDTH / 2 ), SCREEN_HEIGHT - 100,5)
Spaceship_group.add(spaceship)

#create buttons
restart_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, restart_image )
youwin_button = Button(0, SCREEN_HEIGHT // 2 - 200, youwin_image )


#game loop
#inside the while loop gonna be executed
run = True
while run:
    clock.tick(fps)
    #draw background
    draw_bg()


    #create random alien bullets
    #record current time
    time_now = pygame.time.get_ticks()
    #shoot
    if time_now - last_alien_shot > alien_cooldown and len(Alien_Bullet_group ) <5 and len(Alien_group) >0 and game_over == 0:
        attacking_alien = random.choice(Alien_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        Alien_Bullet_group.add(alien_bullet)
        last_alien_shot = time_now
        alien_bullet_fx.play()


    #event Handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #update spaceship
    game_over = spaceship.update(game_over)
    
    if game_over == 0:
        #update sprite groups
        Alien_Bullet_group.update()
        Bullet_group.update()
        Alien_group.update()

    #draw sprite groups
    Spaceship_group.draw(screen)
    Bullet_group.draw(screen)
    Alien_group.draw(screen)
    Alien_Bullet_group.draw(screen)
    
    #Collision of the spaceship with the alien bullet
    if pygame.sprite.spritecollide(spaceship, Alien_Bullet_group, False):
        spaceship.health_remaining -= 1
        explosion_fx.play()
    #killing the alien bullet colided with the spaceship
    for bullet in pygame.sprite.spritecollide(spaceship, Alien_Bullet_group, True):
        bullet.kill()
    #killing the alien colided with the bullet
    for bullet in Bullet_group:
        collisions = pygame.sprite.spritecollide(bullet, Alien_group, True)
        if collisions:
            invader_killed_fx.play()
            bullet.kill()
    #killing the alien bullet collided with the spaceship bullet
    for albullet in Alien_Bullet_group:
        collisions = pygame.sprite.spritecollide(albullet, Bullet_group, True)
        if collisions:
            albullet.kill()

    if len(Alien_group) == 0:
        game_over = 1
        win_fx.play()

    game_over = spaceship.update(game_over)

    #if spaceship has died
    if game_over == -1:
        if restart_button.draw():
            spaceship.reset(( SCREEN_WIDTH / 2 ), SCREEN_HEIGHT - 100, 5)
            game_over = 0
            #score = 0
    #WIN
    if game_over == 1:
        pygame.mixer.music.stop()
        if youwin_button.draw():
            win_fx.stop()
            spaceship.reset(( SCREEN_WIDTH / 2 ), SCREEN_HEIGHT - 100, 5)
            game_over = 0
            #score = 0
    
    pygame.display.update()


pygame.quit()