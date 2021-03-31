import pygame
from pygame.locals import *
import os
import sys
import math
import random
global level1
level1=0

while True:
    if level1==0:
        pygame.init()
        x=1
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        win=pygame.display.set_mode((800,600))
        bg = pygame.image.load('introo.jpg')
        win.blit(bg,(0,0))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            level1+=1
            pygame.time.delay(1000)

    if level1==1:
        pygame.init()

        win = pygame.display.set_mode((800,447))
        bg1 = pygame.image.load('intro11.png')
        win.blit(bg1,(0,0))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            
            pygame.display.set_caption("Zaviour")

            walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
            walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

            char = pygame.image.load('standing.png')

            clock = pygame.time.Clock()

            bg = pygame.image.load(os.path.join('bg.png')).convert()
            bgX = 0
            bgX2 = bg.get_width()

            bulletSound = pygame.mixer.Sound('bullet.mp3')
            hitSound = pygame.mixer.Sound('hit6.wav')
            collision=pygame.mixer.Sound('collision.wav')

            music = pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.play(-1)

            score = 0

            class player(object):
                def __init__(self,x,y,width,height):
                    self.x = x
                    self.y = y
                    self.width = width
                    self.height = height
                    self.vel = 5
                    self.isJump = False
                    self.left = False
                    self.right = False
                    self.walkCount = 0
                    self.jumpCount = 10
                    self.standing = True
                    self.hitbox = (self.x + 17, self.y + 11, 29, 52)
                    self.health=15
                    

                def draw(self, win):
                    if self.walkCount + 1 >= 27:
                        self.walkCount = 0

                    if not(self.standing):
                        if self.left:
                            win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                            self.walkCount += 1
                        elif self.right:
                            win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                            self.walkCount +=1
                    else:
                        if self.left:
                            win.blit(walkLeft[0], (self.x, self.y))
                        else:
                            win.blit(walkRight[0], (self.x, self.y))
                    self.hitbox = (self.x + 17, self.y + 11, 29, 52)
                    pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 75, 10))
                    pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 75 - (5 * (15 - self.health)), 10))
                    #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

                def hit(self):
                    self.isJump = False
                    self.jumpCount = 10
                    #self.x = 10
                    self.y = 311
                    self.walkCount = 0
                    if self.health > 0:
                        self.health -= 1
                    font1 = pygame.font.SysFont('comicsans', 100)
                    text = font1.render('-5', 1, (255,0,0))
                    win.blit(text, (250 - (text.get_width()/2),200))
                    pygame.display.update()
                    i = 0
                    while i < 10:
                        pygame.time.delay(10)
                        i += 1
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                i = 11
                                pygame.quit()

            class saw(object):
                rotate = [pygame.image.load(os.path.join('images', 'SAW0.PNG')),pygame.image.load(os.path.join('images', 'SAW1.PNG')),pygame.image.load(os.path.join('images', 'SAW2.PNG')),pygame.image.load(os.path.join('images', 'SAW3.PNG'))]
                def __init__(self,x,y,width,height):
                    self.x = x
                    self.y = y
                    self.width = width
                    self.height = height
                    self.rotateCount = 0
                    self.vel = 1.4
                    self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)

                def draw(self,win):
                    # Defines the accurate hitbox for our character 
                    #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
                    if self.rotateCount >= 8:  # This is what will allow us to animate the saw
                        self.rotateCount = 0
                    win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (64,64)), (self.x,self.y))  # scales our image down to 64x64 before drawing
                    self.rotateCount += 1
                    self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)                


            class projectile(object):
                def __init__(self,x,y,radius,color,facing):
                    self.x = x
                    self.y = y
                    self.radius = radius
                    self.color = color
                    self.facing = facing
                    self.vel = 8 * facing

                def draw(self,win):
                    pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

            class enemy(object):
                walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
                walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

                def __init__(self, x, y, width, height, end):
                    self.x = x
                    self.y = y
                    self.width = width
                    self.height = height
                    self.end = end
                    self.path = [0, self.end]
                    self.walkCount = 0
                    self.vel = 3
                    self.hitbox = (self.x + 17, self.y + 2, 31, 57)
                    self.health = 10
                    self.visible = True

                def draw(self,win):
                    self.move()
                    if self.visible:
                        if self.walkCount + 1 >= 33:
                            self.walkCount = 0

                        if self.vel > 0:
                            win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                            self.walkCount += 1
                        else:
                            win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                            self.walkCount += 1

                        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
                        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
                        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

                def move(self):
                    if self.vel > 0:
                        if self.x + self.vel < self.path[1]:
                            self.x += self.vel
                        else:
                            self.vel = self.vel * -1
                            self.walkCount = 0
                    else:
                        if self.x - self.vel > self.path[0]:
                            self.x += self.vel
                        else:
                            self.vel = self.vel * -1
                            self.walkCount = 0

                def hit(self):
                    if self.health > 0:
                        self.health -= 1
                    else:
                        self.visible = False
                    
            run = True
            speed = 30  # NEW

            def redrawGameWindow():
                win.blit(bg, (bgX, 0))  
                win.blit(bg, (bgX2, 0))  
                text = font.render('Score: ' + str(score), 1, (0,0,0))
                win.blit(text, (350, 10))
                man.draw(win)                          
                for bullet in bullets:
                    bullet.draw(win)
                for e in enemies:
                    e.draw(win)
                for o in objects:
                    o.draw(win)    

                pygame.display.update()    
                
            #mainloop
            font = pygame.font.SysFont('comicsans', 30, True)
            man = player(200, 310, 64,64)
            shootLoop = 0
            bullets = []
            enemies=[]
            objects=[]
            run = True
            pygame.time.set_timer(USEREVENT+2, random.randrange(2000, 3500))
            while run:
                clock.tick(speed)  # NEW
                bgX -= 1.4  # Move both background images back
                bgX2 -= 1.4

                if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
                    bgX = bg.get_width()
                
                if bgX2 < bg.get_width() * -1:
                    bgX2 = bg.get_width()

                for obstacle in objects: 
                    obstacle.x -= 1.4
                    if obstacle.x < obstacle.width * -1: # If our obstacle is off the screen we will remove it
                        objects.pop(objects.index(obstacle))        

                for event in pygame.event.get():  
                    if event.type == pygame.QUIT: 
                        run = False    
                        pygame.quit() 
                        quit()
                    if event.type == USEREVENT+2:
                        r = random.randrange(0,2)
                        if r == 0 :
                            enemies.append(enemy(random.randrange(780,800), 313, 64, 64, 800))
                            #else:
                                #enemies.append(enemy(random.randrange(740,750), 313, 64, 64, 800))                   
                        else:
                                objects.append(saw(780, 310, 64, 64))
                                pygame.time.delay(100)
                                x=1                                               

                #if goblin.visible == True:
                for e in enemies:
                    if man.hitbox[1] < e.hitbox[1] + e.hitbox[3] and man.hitbox[1] + man.hitbox[3] > e.hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2] > e.hitbox[0] and man.hitbox[0] < e.hitbox[0] + e.hitbox[2]:
                            man.hit()
                            enemies.remove(e)
                            collision.play()
                            score -= 5
                            
                for x in objects:
                    if man.hitbox[1] < x.hitbox[1] + x.hitbox[3] and man.hitbox[1] + man.hitbox[3] > x.hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2] > x.hitbox[0] and man.hitbox[0] < x.hitbox[0] + x.hitbox[2]:
                            man.hit()
                            collision.play()
                            score -= 5
                            objects.pop(objects.index(x)) 



                if shootLoop > 0:
                    shootLoop += 1
                if shootLoop > 3:
                    shootLoop = 0
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    
                for bullet in bullets.copy():
                    for e in enemies.copy():
                        if bullet.y - bullet.radius < e.hitbox[1] + e.hitbox[3] and bullet.y + bullet.radius > e.hitbox[1]:
                            if bullet.x + bullet.radius > e.hitbox[0] and bullet.x - bullet.radius < e.hitbox[0] + e.hitbox[2]:
                                hitSound.play()
                                e.hit()
                                score += 1
                                if(bullet in bullets):
                                    bullets.pop(bullets.index(bullet))            
                            if not(e.visible):
                                enemies.pop(enemies.index(e))
                                                    
                for bullet in bullets:            
                    if bullet.x < 800 and bullet.x > 0:
                        bullet.x += bullet.vel
                    else:
                        bullets.pop(bullets.index(bullet))

                keys = pygame.key.get_pressed()

                if keys[pygame.K_SPACE] and shootLoop == 0:
                    
                    if man.left:
                        facing = -1
                    else:
                        facing = 1
                        
                    if len(bullets) < 6:
                        bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (153,0,0), facing))
                        bulletSound.play()

                    shootLoop = 1

                if keys[pygame.K_a] and man.x > man.vel:
                    man.x -= man.vel
                    man.left = True
                    man.right = False
                    man.standing = False
                elif keys[pygame.K_d] and man.x < 800 - man.width - man.vel:
                    man.x += man.vel
                    man.right = True
                    man.left = False
                    man.standing = False
                else:
                    man.standing = True
                    man.walkCount = 0
                    
                if not(man.isJump):
                    if keys[pygame.K_w]:
                        man.isJump = True
                        man.right = False
                        man.left = False
                        man.walkCount = 0
                else:
                    if man.jumpCount >= -10:
                        neg = 1
                        if man.jumpCount < 0:
                            neg = -1
                        man.y -= (man.jumpCount ** 2) * 0.5 * neg
                        man.jumpCount -= 1
                    else:
                        man.isJump = False
                        man.jumpCount = 10
                if(score==300):
                    level1+=1
                    font2 = pygame.font.SysFont('comicsans', 50)
                    text1 = font2.render('You have succesfully passed Level 1!', 1, (255,0,0))
                    win.blit(text1, (100,200))
                    pygame.display.update()    
                    pygame.time.delay(4000)
                    break                    
                redrawGameWindow()
                if(man.health==0):
                    level1=5
                    pygame.time.delay(1500)
                    break

            pygame.quit()











    if level1==2:
        pygame.font.init()
        pygame.init()
        win = pygame.display.set_mode((750,750))
        pygame.display.set_caption("Zaviour")
        bg1 = pygame.image.load('intro22.jpg')
        win.blit(bg1,(0,0))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            WIDTH, HEIGHT = 750, 750
            WIN = pygame.display.set_mode((WIDTH, HEIGHT))
            

            # Load images
            RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
            GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
            BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

            # Player player
            YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

            # Lasers
            RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
            GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
            BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
            YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

            # Background
            BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
            #Sound
            music=pygame.mixer.music.load('level2.mp3')
            pygame.mixer.music.play(-1)
            class Laser:
                def __init__(self, x, y, img):
                    self.x = x
                    self.y = y
                    self.img = img
                    self.mask = pygame.mask.from_surface(self.img)

                def draw(self, window):
                    window.blit(self.img, (self.x, self.y))

                def move(self, vel):
                    self.y += vel

                def off_screen(self, height):
                    return not(self.y <= height and self.y >= 0)

                def collision(self, obj):
                    return collide(self, obj)


            class Ship:
                COOLDOWN = 30

                def __init__(self, x, y, health=100):
                    self.x = x
                    self.y = y
                    self.health = health
                    self.ship_img = None
                    self.laser_img = None
                    self.lasers = []
                    self.cool_down_counter = 0

                def draw(self, window):
                    window.blit(self.ship_img, (self.x, self.y))
                    for laser in self.lasers:
                        laser.draw(window)

                def move_lasers(self, vel, obj):
                    self.cooldown()
                    for laser in self.lasers:
                        laser.move(vel)
                        if laser.off_screen(HEIGHT):
                            self.lasers.remove(laser)
                        elif laser.collision(obj):
                            obj.health -= 10
                            self.lasers.remove(laser)

                def cooldown(self):
                    if self.cool_down_counter >= self.COOLDOWN:
                        self.cool_down_counter = 0
                    elif self.cool_down_counter > 0:
                        self.cool_down_counter += 1

                def shoot(self):
                    if self.cool_down_counter == 0:
                        laser = Laser(self.x, self.y, self.laser_img)
                        self.lasers.append(laser)
                        self.cool_down_counter = 1

                def get_width(self):
                    return self.ship_img.get_width()

                def get_height(self):
                    return self.ship_img.get_height()


            class Player(Ship):
                def __init__(self, x, y, health=100):
                    super().__init__(x, y, health)
                    self.ship_img = YELLOW_SPACE_SHIP
                    self.laser_img = YELLOW_LASER
                    self.mask = pygame.mask.from_surface(self.ship_img)
                    self.max_health = health

                def move_lasers(self, vel, objs):
                    self.cooldown()
                    for laser in self.lasers:
                        laser.move(vel)
                        if laser.off_screen(HEIGHT):
                            self.lasers.remove(laser)
                        else:
                            for obj in objs:
                                if laser.collision(obj):
                                    objs.remove(obj)
                                    if laser in self.lasers:
                                        self.lasers.remove(laser)

                def draw(self, window):
                    super().draw(window)
                    self.healthbar(window)

                def healthbar(self, window):
                    pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
                    pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


            class Enemy(Ship):
                COLOR_MAP = {
                            "red": (RED_SPACE_SHIP, RED_LASER),
                            "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                            "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                            }

                def __init__(self, x, y, color, health=100):
                    super().__init__(x, y, health)
                    self.ship_img, self.laser_img = self.COLOR_MAP[color]
                    self.mask = pygame.mask.from_surface(self.ship_img)

                def move(self, vel):
                    self.y += vel

                def shoot(self):
                    if self.cool_down_counter == 0:
                        laser = Laser(self.x-20, self.y, self.laser_img)
                        self.lasers.append(laser)
                        self.cool_down_counter = 1


            def collide(obj1, obj2):
                offset_x = obj2.x - obj1.x
                offset_y = obj2.y - obj1.y
                return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

            def main():
                run = True
                FPS = 60
                level=0
                lives = 5
                main_font = pygame.font.SysFont("comicsans", 50)
                lost_font = pygame.font.SysFont("comicsans", 60)

                enemies = []
                wave_length = 5
                enemy_vel = 1

                player_vel = 7
                laser_vel = 7

                player = Player(300, 630)

                clock = pygame.time.Clock()

                lost = False
                lost_count = 0

                def redraw_window():
                    WIN.blit(BG, (0,0))
                    # draw text
                    lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
                    level_label = main_font.render(f"Wave: {level}", 1, (255,255,255))

                    WIN.blit(lives_label, (10, 10))
                    WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

                    for enemy in enemies:
                        enemy.draw(WIN)

                    player.draw(WIN)

                    

                    pygame.display.update()

                while run:
                    clock.tick(FPS)
                    redraw_window()

                    if lives <= 0 or player.health <= 0:
                        lost = True
                        lost_count += 1



                    if lost:
                        list1=globals()
                        list1['level1']=4
                        run = False
                        

                    if len(enemies) == 0:
                        level+= 1
                        if(level==4 ):
                            break

                        wave_length += 6
                        
                        for i in range(wave_length):
                            enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                            enemies.append(enemy)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_a] and player.x - player_vel > 0: # left
                        player.x -= player_vel
                    if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
                        player.x += player_vel
                    if keys[pygame.K_w] and player.y - player_vel > 0: # up
                        player.y -= player_vel
                    if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
                        player.y += player_vel
                    if keys[pygame.K_SPACE]:
                        player.shoot()

                    for enemy in enemies[:]:
                        enemy.move(enemy_vel)
                        enemy.move_lasers(laser_vel, player)

                        if random.randrange(0, 2*60) == 1:
                            enemy.shoot()

                        if collide(enemy, player):
                            player.health -= 10
                            enemies.remove(enemy)
                        elif enemy.y + enemy.get_height() > HEIGHT:
                            lives -= 1
                            enemies.remove(enemy)

                    player.move_lasers(-laser_vel, enemies)

            def main_menu():
                title_font = pygame.font.SysFont("comicsans", 70)
                run = True
                global level
                level=0 
                while run:
                    WIN.blit(BG, (0,0))
                    title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
                    WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if level==4:
                            run=False
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            main()
                            run=False
                            



                pygame.quit()
            main_menu()
            level1+=1







    if level1==3:
        pygame.init()
        global level2
        level2=0
        gray=(119,118,110)
        black=(0,0,0)
        red=(255,0,0)
        green=(0,200,0)
        blue=(0,0,200)
        bright_red=(255,0,0)
        bright_green=(0,255,0)
        bright_blue=(0,0,255)
        display_width=800
        display_height=600
        import time
        import random
        global hel
        hel=3
        


        gamedisplays=pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption("Zaviour")
        clock=pygame.time.Clock()
        carimg=pygame.image.load('car1.jpg')
        backgroundpic=pygame.image.load("download12.jpg")
        yellow_strip=pygame.image.load("yellow strip.jpg")
        strip=pygame.image.load("strip.jpg")
        intro_background=pygame.image.load("background.jpg")
        instruction_background=pygame.image.load("background2.jpg")
        car_width=56
        pause=False

        def intro_loop():
            intro=True
            while intro:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
                        sys.exit()
                gamedisplays.blit(intro_background,(0,0))
                largetext=pygame.font.Font('freesansbold.ttf',115)
                TextSurf,TextRect=text_objects("LEVEL 3",largetext)
                TextRect.center=(400,100)
                gamedisplays.blit(TextSurf,TextRect)
                button("START",150,520,100,50,green,bright_green,"play")
                button("QUIT",550,520,100,50,red,bright_red,"quit")
                button("INSTRUCTION",300,520,200,50,blue,bright_blue,"intro")
                pygame.display.update()
                clock.tick(50)
                list2=globals()
                if list2['hel']<=0:
                    break
                if list2['level2']==3:
                    break


                


        def button(msg,x,y,w,h,ic,ac,action=None):
            mouse=pygame.mouse.get_pos()
            click=pygame.mouse.get_pressed()
            if x+w>mouse[0]>x and y+h>mouse[1]>y:
                pygame.draw.rect(gamedisplays,ac,(x,y,w,h))
                if click[0]==1 and action!=None:
                    if action=="play":
                        countdown()
                    elif action=="quit":
                        pygame.quit()
                        quit()
                        sys.exit()
                    elif action=="intro":
                        introduction()
                    elif action=="menu":
                        intro_loop()
                    elif action=="pause":
                        paused()
                    elif action=="unpause":
                        unpaused()


            else:
                pygame.draw.rect(gamedisplays,ic,(x,y,w,h))
            smalltext=pygame.font.Font("freesansbold.ttf",20)
            textsurf,textrect=text_objects(msg,smalltext)
            textrect.center=((x+(w/2)),(y+(h/2)))
            gamedisplays.blit(textsurf,textrect)


        def introduction():
            introduction=True
            while introduction:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
                        sys.exit()
                gamedisplays.blit(instruction_background,(0,0))
                largetext=pygame.font.Font('freesansbold.ttf',80)
                smalltext=pygame.font.Font('freesansbold.ttf',20)
                mediumtext=pygame.font.Font('freesansbold.ttf',40)
                textSurf,textRect=text_objects("Our hero has reached earth and now he has to defuse the bomb using the ",smalltext)
                textRect.center=((400),(200))
                textSurf2,textRect2=text_objects("cube as soon as possible but there is heavy traffic on the way :). ",smalltext)
                textRect2.center=((350),(220))
                textSurf3,textRect3=text_objects("You need to score 300 points to save the Earth only 3 crashes allowed",smalltext)
                textRect3.center=((350),(240))
                TextSurf,TextRect=text_objects("INSTRUCTION",largetext)
                TextRect.center=((400),(100))

                gamedisplays.blit(TextSurf,TextRect)
                gamedisplays.blit(textSurf,textRect)
                gamedisplays.blit(textSurf2,textRect2)
                gamedisplays.blit(textSurf3,textRect3)
                stextSurf,stextRect=text_objects("ARROW LEFT : LEFT TURN",smalltext)
                stextRect.center=((150),(400))
                hTextSurf,hTextRect=text_objects("ARROW RIGHT : RIGHT TURN" ,smalltext)
                hTextRect.center=((150),(450))
                atextSurf,atextRect=text_objects("A : ACCELERATOR",smalltext)
                atextRect.center=((150),(500))
                rtextSurf,rtextRect=text_objects("B : BRAKE ",smalltext)
                rtextRect.center=((150),(550))
                ptextSurf,ptextRect=text_objects("P : PAUSE  ",smalltext)
                ptextRect.center=((150),(350))
                sTextSurf,sTextRect=text_objects("CONTROLS",mediumtext)
                sTextRect.center=((350),(300))
                gamedisplays.blit(sTextSurf,sTextRect)
                gamedisplays.blit(stextSurf,stextRect)
                gamedisplays.blit(hTextSurf,hTextRect)
                gamedisplays.blit(atextSurf,atextRect)
                gamedisplays.blit(rtextSurf,rtextRect)
                gamedisplays.blit(ptextSurf,ptextRect)
                button("BACK",600,450,100,50,blue,bright_blue,"menu")
                pygame.display.update()
                clock.tick(30)

        def paused():
            global pause

            while pause:
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            pygame.quit()
                            quit()
                            sys.exit()
                    gamedisplays.blit(instruction_background,(0,0))
                    largetext=pygame.font.Font('freesansbold.ttf',115)
                    TextSurf,TextRect=text_objects("PAUSED",largetext)
                    TextRect.center=((display_width/2),(display_height/2))
                    gamedisplays.blit(TextSurf,TextRect)
                    button("CONTINUE",150,450,150,50,green,bright_green,"unpause")
                    button("RESTART",350,450,150,50,blue,bright_blue,"play")
                    button("MAIN MENU",550,450,200,50,red,bright_red,"menu")
                    pygame.display.update()
                    clock.tick(30)

        def unpaused():
            global pause
            pause=False


        def countdown_background():
            font=pygame.font.SysFont(None,25)
            x=(display_width*0.45)
            y=(display_height*0.8)
            gamedisplays.blit(backgroundpic,(0,0))
            gamedisplays.blit(backgroundpic,(0,200))
            gamedisplays.blit(backgroundpic,(0,400))
            gamedisplays.blit(backgroundpic,(700,0))
            gamedisplays.blit(backgroundpic,(700,200))
            gamedisplays.blit(backgroundpic,(700,400))
            gamedisplays.blit(yellow_strip,(400,100))
            gamedisplays.blit(yellow_strip,(400,200))
            gamedisplays.blit(yellow_strip,(400,300))
            gamedisplays.blit(yellow_strip,(400,400))
            gamedisplays.blit(yellow_strip,(400,100))
            gamedisplays.blit(yellow_strip,(400,500))
            gamedisplays.blit(yellow_strip,(400,0))
            gamedisplays.blit(yellow_strip,(400,600))
            gamedisplays.blit(strip,(120,200))
            gamedisplays.blit(strip,(120,0))
            gamedisplays.blit(strip,(120,100))
            gamedisplays.blit(strip,(680,100))
            gamedisplays.blit(strip,(680,0))
            gamedisplays.blit(strip,(680,200))
            gamedisplays.blit(carimg,(x,y))
            text=font.render("DODGED: 0",True, black)
            score=font.render("SCORE: 0",True,red)
            gamedisplays.blit(text,(0,50))
            gamedisplays.blit(score,(0,30))
            button("PAUSE",650,0,150,50,blue,bright_blue,"pause")

        def countdown():
            countdown=True

            while countdown:
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            pygame.quit()
                            quit()
                            sys.exit()
                    gamedisplays.fill(gray)
                    countdown_background()
                    largetext=pygame.font.Font('freesansbold.ttf',115)
                    TextSurf,TextRect=text_objects("3",largetext)
                    TextRect.center=((display_width/2),(display_height/2))
                    gamedisplays.blit(TextSurf,TextRect)
                    pygame.display.update()
                    clock.tick(1)
                    gamedisplays.fill(gray)
                    countdown_background()
                    largetext=pygame.font.Font('freesansbold.ttf',115)
                    TextSurf,TextRect=text_objects("2",largetext)
                    TextRect.center=((display_width/2),(display_height/2))
                    gamedisplays.blit(TextSurf,TextRect)
                    pygame.display.update()
                    clock.tick(1)
                    gamedisplays.fill(gray)
                    countdown_background()
                    largetext=pygame.font.Font('freesansbold.ttf',115)
                    TextSurf,TextRect=text_objects("1",largetext)
                    TextRect.center=((display_width/2),(display_height/2))
                    gamedisplays.blit(TextSurf,TextRect)
                    pygame.display.update()
                    clock.tick(1)
                    gamedisplays.fill(gray)
                    countdown_background()
                    largetext=pygame.font.Font('freesansbold.ttf',115)
                    TextSurf,TextRect=text_objects("GO!!!",largetext)
                    TextRect.center=((display_width/2),(display_height/2))
                    gamedisplays.blit(TextSurf,TextRect)
                    pygame.display.update()
                    clock.tick(1)
                    game_loop()
                    countdown=False

        def obstacle(obs_startx,obs_starty,obs):
            if obs==0:
                obs_pic=pygame.image.load("car.jpg")
            elif obs==1:
                obs_pic=pygame.image.load("car1.jpg")
            elif obs==2:
                obs_pic=pygame.image.load("car2.jpg")
            elif obs==3:
                obs_pic=pygame.image.load("car4.jpg")
            elif obs==4:
                obs_pic=pygame.image.load("car5.jpg")
            elif obs==5:
                obs_pic=pygame.image.load("car6.jpg")
            elif obs==6:
                obs_pic=pygame.image.load("car7.jpg")
            gamedisplays.blit(obs_pic,(obs_startx,obs_starty))

        def score_system(passed,score):
            font=pygame.font.SysFont(None,25)
            text=font.render("Passed"+str(passed),True,black)
            score=font.render("Score"+str(score),True,red)
            gamedisplays.blit(text,(0,50))
            gamedisplays.blit(score,(0,30))


        def text_objects(text,font):
            textsurface=font.render(text,True,black)
            return textsurface,textsurface.get_rect()

        def message_display(text):
            largetext=pygame.font.Font("freesansbold.ttf",80)
            textsurf,textrect=text_objects(text,largetext)
            textrect.center=((display_width/2),(display_height/2))
            gamedisplays.blit(textsurf,textrect)
            pygame.display.update()
            time.sleep(3)
            game_loop()


        def crash():
            list2=globals()
            list2['hel']-=1
            message_display("YOU CRASHED")


        def background():
            gamedisplays.blit(backgroundpic,(0,0))
            gamedisplays.blit(backgroundpic,(0,200))
            gamedisplays.blit(backgroundpic,(0,400))
            gamedisplays.blit(backgroundpic,(700,0))
            gamedisplays.blit(backgroundpic,(700,200))
            gamedisplays.blit(backgroundpic,(700,400))
            gamedisplays.blit(yellow_strip,(400,0))
            gamedisplays.blit(yellow_strip,(400,100))
            gamedisplays.blit(yellow_strip,(400,200))
            gamedisplays.blit(yellow_strip,(400,300))
            gamedisplays.blit(yellow_strip,(400,400))
            gamedisplays.blit(yellow_strip,(400,500))
            gamedisplays.blit(strip,(120,0))
            gamedisplays.blit(strip,(120,100))
            gamedisplays.blit(strip,(120,200))
            gamedisplays.blit(strip,(680,0))
            gamedisplays.blit(strip,(680,100))
            gamedisplays.blit(strip,(680,200))

        def car(x,y):
            gamedisplays.blit(carimg,(x,y))

        def game_loop():
            global pause
            x=(display_width*0.45)
            y=(display_height*0.8)
            x_change=0
            obstacle_speed=11
            obs=0
            y_change=0
            obs_startx=random.randrange(200,(display_width-200))
            obs_starty=-750
            obs_width=56
            obs_height=125
            passed=0
            
            score=0
            y2=7
            fps=120
            pygame.mixer.music.load('racing01.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1, 0.0)

            bumped=False
            while not bumped:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()

                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_LEFT:
                            x_change=-5
                        if event.key==pygame.K_RIGHT:
                            x_change=5
                        if event.key==pygame.K_a:
                            obstacle_speed+=2
                        if event.key==pygame.K_b:
                            obstacle_speed-=2
                    if event.type==pygame.KEYUP:
                        if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                            x_change=0

                x+=x_change
                pause=True
                gamedisplays.fill(gray)

                rel_y=y2%backgroundpic.get_rect().width
                gamedisplays.blit(backgroundpic,(0,rel_y-backgroundpic.get_rect().width))
                gamedisplays.blit(backgroundpic,(700,rel_y-backgroundpic.get_rect().width))
                if rel_y<800:
                    gamedisplays.blit(backgroundpic,(0,rel_y))
                    gamedisplays.blit(backgroundpic,(700,rel_y))
                    gamedisplays.blit(yellow_strip,(400,rel_y))
                    gamedisplays.blit(yellow_strip,(400,rel_y+100))
                    gamedisplays.blit(yellow_strip,(400,rel_y+200))
                    gamedisplays.blit(yellow_strip,(400,rel_y+300))
                    gamedisplays.blit(yellow_strip,(400,rel_y+400))
                    gamedisplays.blit(yellow_strip,(400,rel_y+500))
                    gamedisplays.blit(yellow_strip,(400,rel_y-100))
                    gamedisplays.blit(strip,(120,rel_y-200))
                    gamedisplays.blit(strip,(120,rel_y+20))
                    gamedisplays.blit(strip,(120,rel_y+30))
                    gamedisplays.blit(strip,(680,rel_y-100))
                    gamedisplays.blit(strip,(680,rel_y+20))
                    gamedisplays.blit(strip,(680,rel_y+30))

                y2+=obstacle_speed

                
                list2=globals()
                if list2['hel']<=0:
                    break

                obs_starty-=(obstacle_speed/4)
                obstacle(obs_startx,obs_starty,obs)
                obs_starty+=obstacle_speed
                car(x,y)
                score_system(passed,score)
                if x>690-car_width or x<110:
                    pygame.mixer.music.stop()
                    crash()
                if x>display_width-(car_width+110) or x<110:
                    pygame.mixer.music.stop()
                    crash()
                if obs_starty>display_height:
                    obs_starty=0-obs_height
                    obs_startx=random.randrange(170,(display_width-170))
                    obs=random.randrange(0,7)
                    passed=passed+1
                    score=passed*10
                    

                    if int(passed)%10==0:
                        list2['level2']=list2['level2']+1
                        if(list2['level2']==3):
                            break
                        obstacle_speed+=2
                        largetext=pygame.font.Font("freesansbold.ttf",80)
                        textsurf,textrect=text_objects("WAVE "+str(list2['level2']),largetext)
                        textrect.center=((display_width/2),(display_height/2))
                        gamedisplays.blit(textsurf,textrect)
                        pygame.display.update()
                        time.sleep(3)


                if y<obs_starty+obs_height:
                    if x > obs_startx and x < obs_startx + obs_width or x+car_width > obs_startx and x+car_width < obs_startx+obs_width:
                        pygame.mixer.music.stop()
                        crash()
                button("Pause",650,0,150,50,blue,bright_blue,"pause")
                pygame.display.update()
                clock.tick(60)
        intro_loop()
        level1+=1
        list2=globals()
        if list2['hel']<=0:
            level1=5
        
    if level1==4:
        pygame.init()
        win=pygame.display.set_mode((800,600))
        bg = pygame.image.load('win.jpg')
        winsound=pygame.mixer.Sound('mix1.wav')
        winsound.play()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(bg,(0,0))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            level1=0
            pygame.time.delay(1000)
            continue 
        elif keys[pygame.K_q]:
            level1=6
            break
    
    if level1==5:
        pygame.init()
        win=pygame.display.set_mode((800,600))
        bg = pygame.image.load('over1.jpg')
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()       
        oversound=pygame.mixer.Sound('mix2.wav')
        if x==1:
            oversound.play()
            x+=1
        win.blit(bg,(0,0))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            level1=0
            pygame.time.delay(1000)
        elif keys[pygame.K_q]:
            level1=6
            break

               

