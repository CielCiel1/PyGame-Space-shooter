import pygame, sys
import random
import json
import time
import os

pygame.init()
pygame.mixer.init() 
width = 400
height = 600
screen = pygame.display.set_mode([width,height])
shot= pygame.mixer.Sound('Game/pew.wav')
shotdie= pygame.mixer.Sound('Game/expl6.wav')
shotdiem= pygame.mixer.Sound('Game/expl3.wav')
class Ship(pygame.sprite.Sprite):
        def __init__(self,x,y,blood,score):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('Game/Ship.png')
            self.rect = self.image.get_rect()
            self.rect.center = [x,y]
            self.blood_start = blood
            self.blood_remaining = blood
            self.change = 2
            self.last_shot = pygame.time.get_ticks()
            self.score = score
            
        def update(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT] and self.rect.x < 350:
                self.rect.x += self.change
                x =self.rect.x
            if key[pygame.K_LEFT]and self.rect.x> 0:
                self.rect.x -= self.change
                x =self.rect.x
            if key[pygame.K_UP] and self.rect.y >0:
                self.rect.y -= self.change
                y =self.rect.y
            if key[pygame.K_DOWN] and self.rect.y < 490:
                self.rect.y += self.change
                y =self.rect.y
            time_now = pygame.time.get_ticks()
            cooldown = 300
            if key[pygame.K_SPACE]:
                if time_now - self.last_shot >cooldown:
                    bullets = Bullet(self.rect.x+30,self.rect.y)
                    bullet_group.add(bullets)
                    self.last_shot = time_now
                    shot.play()
            pygame.draw.rect(screen,(255,0,0),(self.rect.x,(self.rect.bottom),self.rect.width,5))
            if self.blood_remaining>0:
                pygame.draw.rect(screen,(0,255,0),(self.rect.x,(self.rect.bottom),int(self.rect.width*(self.blood_remaining / self.blood_start)),5))
            if pygame.sprite.spritecollide(self, meto_group,True):
                spaceship.blood_remaining = 0
class Monster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.list_monster=['m1','m2','m3','m4','m5','m6']
        self.image = pygame.image.load("Game/" +random.choice(self.list_monster) +".png")
        self.rect = self.image.get_rect()
        self.rect.x= random.choice(range(1,350,10))
        self.rect.y = 10
        self.speed = -1
        self.move = 1
        self.move_count =0
    def update(self):
        self.rect.y -=self.speed
       
        if pygame.sprite.spritecollide(self, ship_group,False):
            self.kill()
            shotdie.play()
            spaceship.blood_remaining -=10

class Bullet(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('Game/bullet1.png')
            self.rect = self.image.get_rect()
            self.rect.bottom = y 
            self.rect.x = x 
            self.speed = -10
        def update(self):
            self.rect.y += self.speed
            if self.rect.bottom < 100:
                self.kill()  
            if pygame.sprite.spritecollide(self, monster_group,True):
                spaceship.score +=1
                shotdie.play()
                self.kill()
                
            
class Meto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Game/metoer.png')
        self.rect = self.image.get_rect()
        self.rect.x= random.choice(range(1,300,10))
        self.rect.y = -30
        self.speed = -3
    def update(self):
        self.rect.y -=self.speed
class MonsterBullet(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('Game/monbullet.png')
            self.rect = self.image.get_rect()
            self.rect.x= random.choice(range(1,300,10))
            self.rect.y = -30
            self.speed = -3
        def update(self):
            self.rect.y -=self.speed
            if self.rect.bottom > height:
                self.kill()
            if pygame.sprite.spritecollide(self, ship_group,False):
                shotdie.play()
                self.kill()
                spaceship.blood_remaining -= 10

    
ship_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
meto_group = pygame.sprite.Group()
monsterbullet_group = pygame.sprite.Group()


spaceship = Ship(width/2,height-110,100,0)
ship_group.add(spaceship)


class Space_shooter:
    def __init__(self):
        
        self.clock = pygame.time.Clock()
        
        self.x =  width/2
        self.y = height-110
        
        pygame.display.set_caption("Space Shooter")
        self.font = pygame.font.SysFont("comicsansms", 25)
        self.surface = pygame.image.load('Game/back_ground.jpg')
        self.surfaceend = pygame.image.load('Game/endgame.png').convert()
        self.surfaceend = pygame.transform.scale(self.surfaceend,(400,600))
        self.image = pygame.image.load('Game/Ship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]
        
        
        
        self.last_shot1 = pygame.time.get_ticks()
        self.have_meto = pygame.time.get_ticks()
        self.have_monster = pygame.time.get_ticks()
        
        
        self.run_block = 10
        self.last_shot = pygame.time.get_ticks()
        self.my = 10
        self.over= pygame.mixer.Sound('Game/end.wav')
        pygame.mixer.music.load('Game/Bg.wav')
        pygame.mixer.music.play(15)

    def gameOver(self):
        check = (spaceship.blood_remaining == 0)
        return check
    def score(self):
        value = self.font.render(f"Your score: {spaceship.score}",True, (255,255,255))
        screen.blit(value,[0,0])
    
    def run(self):
        change =2
        
        listc = [ i for i in range(20,50,5)]
        coolmeto = (random.choice(listc))*70
        coolmonster = (random.choice(listc))*50
        coolmonbul = (random.choice(listc))*40
        game_over = False
        run = True
        
        while run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                key = pygame.key.get_pressed()
                if key[pygame.K_RIGHT] and self.x < 300:
                    self.x += change
                    x =self.rect.x
                if key[pygame.K_LEFT]and self.x> 0:
                    self.x -= change
                    x =self.x
                if key[pygame.K_UP] and self.y >0:
                    self.y -= change
                    y =self.rect.y
                if key[pygame.K_DOWN] and self.y < 490:
                    self.y += change
                    y =self.y
            
            screen.blit(self.surface,(0,0)) 
            self.score()
                
            time_now0 = pygame.time.get_ticks()
            if time_now0 - self.last_shot1 >coolmonbul:
                monbullets = MonsterBullet()
                monsterbullet_group.add(monbullets)
                self.last_shot1 = time_now0   
                
            time_now1 = pygame.time.get_ticks()
            if time_now1 - self.have_meto >coolmeto:
                metos = Meto()
                meto_group.add(metos)
                self.have_meto = time_now1
                
            time_now2 = pygame.time.get_ticks()
            if time_now1 - self.have_monster >coolmonster:
                monsters = Monster()
                monster_group.add(monsters)
                self.have_monster = time_now1
            
           
            
            monsterbullet_group.draw(screen)
            bullet_group.draw(screen)
            monster_group.draw(screen)
            ship_group.draw(screen)
            meto_group.draw(screen)
           
            
            ship_group.update()
          
            monster_group.update()
            bullet_group.update()
            meto_group.update()
            monsterbullet_group.update()
            
            
            pygame.time.delay(3)
            
            pygame.display.flip()
            game_over = self.gameOver()
            while game_over:
                pygame.mixer.music.stop()
               
                self.over.play(30)
                screen.blit(self.surfaceend,(0,0)) 
                message = f"""You Lost! your score is {spaceship.score} """
                value = self.font.render(message,True, (255,255,255))
                screen.blit(value,[50, height//2])
                message2 = 'Enter SPACE to quit screen'
                value2 = self.font.render(message2,True, (255,255,255))
                screen.blit(value2,[50, height//2+40])
                pygame.display.update()
                for event in pygame.event.get():
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE] :
                        pygame.quit()
                        sys.exit()
        
                
            

player=Space_shooter()
player.run()