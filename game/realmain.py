# some content from kids can code: http://kidscancode.org/blog/ (collision, movement, sprites)
# sprites from https://opengameart.org/content/space-shooter-redux
# space invaders using pygame

# from platform import platform

# design
'''
Innovation:
Unlimited fire rate and ammo; customization for many things, homing bullets

Goals, rules, feedback, freedom:
Kill all the enemies, lose all lives and you die; kill all enemies and you win, lives and score displayed, move around freely; shoot as much as you want
'''

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from settings import *
from os import path

# vectors
vec = pg.math.Vector2

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Invaders by Andrew Perevoztchikov")
clock = pg.time.Clock()

# loading filepaths for the sprite images
img_dir1 = path.join(path.dirname(__file__), r'C:\githubstuff\intro_to_programming\videogameFall2022\game\images')

# function to draw text on the screen
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# random color generator
def colorbyte():
    return random.randint(0,255)

# get images for sprites and assign to variables
background = pg.image.load(path.join(img_dir1, 'black.png')).convert()
background = pg.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pg.image.load(path.join(img_dir1, "playerShip1_orange.png")).convert()
enemy_img = pg.image.load(path.join(img_dir1, "enemyGreen3.png")).convert()
bullet_img = pg.image.load(path.join(img_dir1, "laserRed16.png")).convert()
boss_img = pg.image.load(path.join(img_dir1, "enemyBlue2.png")).convert()

player_bullets = 0
# player class
class Player(Sprite):
    def __init__(self):
        # defines player sprite parameters
        Sprite.__init__(self)
        self.image = pg.Surface((50, 38))
        self.image = player_img
        self.image = pg.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT-10)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    # what happens when a key gets pressed: horizontal movement and shooting
    def controls(self):
        global player_bullets
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -2.5
            # print(self.vel)
        if keys[pg.K_RIGHT]:
            self.acc.x = 2.5
        # times the bullet shooting
        if keys[pg.K_SPACE]:
            if FRAME % PLAYER_FIRERATE == 0:
                for i in range(PIERCE):    
                    self.shoot()
                    # player_bullets += 1
        if keys[pg.K_a]:
            if FRAME % 1 == 0:
                for i in range(AIMBOT_DELAY):
                    self.aimbot()
                    # player_bullets += 1
        if keys[pg.K_d]:
            if FRAME % 5 == 0:
                for i in range(1):
                    self.home()
                    # player_bullets += 1
        
    # shoot function creates a bullet at player coordinates
    def shoot(self):
        global player_bullets
        x = self.rect.x + 25
        y = self.rect.y - 10
        w = int(PLAYER_FIRERATE)/2
        h = int(w)*3
        movey = -5
        movex = 0
        e = Bullet(x, y, RED, w, h, movex, movey, "player")
        all_sprites.add(e)
        bullets.add(e)
        player_bullets += 1
    # homing bullet that follows enemy
    def home(self):
        global player_bullets
        x = self.rect.x + 25
        y = self.rect.y - 10
        w = 15
        h = 15
        movey = -5
        movex = 0
        e = Bullet(x, y, RED, w, h, movex, movey, "aimbot")
        all_sprites.add(e)
        bullets.add(e)
        player_bullets += 1
    # bullet aimed directly at random enemy
    def aimbot(self):
        global enemy_list, player_bullets
        try:
            x = self.rect.x + 25
            y = self.rect.y + 15
            w = 5
            h = 5
            enemy = random.randint(0,len(enemy_list)-1)
            movey = ((enemy_list[enemy].rect.y + enemy_list[enemy].h/2) - self.rect.y - 19)/60
            movex = ((enemy_list[enemy].rect.x + enemy_list[enemy].w/2) - self.rect.x - 25)/60
            e = Bullet(x, y, RED, w, h, movex, movey, "player")
            all_sprites.add(e)
            bullets.add(e)
            player_bullets += 1
        except:
            pass
    # updating all movement and acceleration and gravity
    def update(self):
        self.acc = vec(0, 0)
        self.controls()
        self.acc.x += self.vel.x * -0.3
        self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
    
# enemy class        
class Enemy(Sprite):
    # initialize enemy class
    def __init__(self, x, y, color, w, h, movex, movey, cooldown, hp):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.w = w
        self.h = h
        self.image = pg.Surface((self.w, self.h))
        self.image = enemy_img
        self.image = pg.transform.scale(enemy_img, (30, 22))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.x, self.y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.movex = movex
        self.movey = movey
        self.cooldown = cooldown
        self.hp = hp
    # updates movement at a set interval and shoots
    def update(self):
        self.rect.x += self.movex 
        if FRAME % 30 == 0:
            self.rect.y += self.movey
        if FRAME % random.randint(120, self.cooldown) == 0:
            x = self.rect.x + 15
            y = self.rect.y + 50
            movey = 5
            movex = 0  
            e = Bullet(x, y, RED, 5, 15, movex, movey, "enemy")
            all_sprites.add(e)
            bullets.add(e)
        # if self.hp <= 0:
        #     self.kill()

# bullet class
class Bullet(Sprite):
    def __init__(self, x, y, color, w, h, movex, movey, side):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.w = w
        self.h = h
        self.image = pg.Surface((self.w, self.h))
        self.image = bullet_img
        self.image = pg.transform.scale(bullet_img, (w, h))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.x, self.y)
        self.movey = movey
        self.movex = movex
        self.side = side
        self.timer = 0
    def aimbot(self):
        try:
            if self.side == "aimbot":
                # x = self.rect.x + 25
                # y = self.rect.y + 15
                self.w = 15
                self.h = 15
                enemy = (len(enemy_list)-1)
                self.movey = ((enemy_list[enemy].rect.y + 11) - self.rect.y)/5
                self.movex = ((enemy_list[enemy].rect.x + 15) - self.rect.x)/5
                # e = Bullet(x, y, RED, w, h, movex, movey, "player")
                # all_sprites.add(e)
                # bullets.add(e)
        except:
            pass
    # collisions of bullet with enemy/player/boss and movement
    def update(self):
        global SCORE, LIVES, BOSS_HP, player_bullets
        keys = pg.key.get_pressed()
        if keys[pg.K_s]:
            self.aimbot()
        self.rect.y += self.movey
        self.rect.x += self.movex
        # end of game confetti
        if self.side == "confetti":
            pass
        # for homing bullets
        if self.side == "aimbot":
            hits = pg.sprite.spritecollide(self, enemies, True)
            if hits:
                SCORE += 1
                enemy_list.remove(hits[0])
                # self.kill()
                hits[0].hp -= 1
            hits1 = pg.sprite.spritecollide(self, bosses, False)
            if hits1:
                SCORE += 5 
                hits1[0].hp -= 1
                # self.kill()
        # player bullets
        if self.side == "player":
            hits = pg.sprite.spritecollide(self, enemies, True)
            if hits:
                SCORE += 1
                enemy_list.remove(hits[0])
                self.kill()
                hits[0].hp -= 1
                player_bullets -= 1
            hits1 = pg.sprite.spritecollide(self, bosses, False)
            if hits1:
                SCORE += 5 
                hits1[0].hp -= 1
                self.kill()
                player_bullets -= 1
        # enemy bullets
        if self.side == "enemy":
            hits = pg.sprite.spritecollide(self, players, False)
            if hits:
                LIVES -= 1
                self.kill()
        # kill bullet after timer ends to conserve memory
        if self.timer >= 150:
            self.kill()
            if self.side == "player":
                player_bullets -= 1
            elif self.side == "aimbot":
                player_bullets -= 1
            else:
                pass
        self.timer += 1

# boss class
class Boss(Sprite):
    def __init__(self, x, y, color, w, h, movex, movey, cooldown, damage):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.w = w
        self.h = h
        self.image = pg.Surface((self.w, self.h))
        self.image = boss_img
        self.image = pg.transform.scale(boss_img, (60, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.x, self.y)
        self.movey = movey
        self.movex = movex
        self.hp = BOSS_HP
        self.cooldown = cooldown
        self.damage = damage
    # move boss and shooting function and health counter
    def update(self):
        if FRAME % 5 == 0:
            self.rect.x += self.movex
        if FRAME % random.randint(120, self.cooldown) == 0:
            for i in range(self.damage):
                x = self.rect.x + 30
                y = self.rect.y + 50
                movey = 5
                movex = 0
                e = Bullet(x, y, RED, 10, 30, movex, movey, "enemy")
                all_sprites.add(e)
                bullets.add(e)
        if self.hp <= 0:
            enemy_list.remove(self)
            self.kill()


# create a group for all sprites
all_sprites = pg.sprite.Group()
players = pg.sprite.Group()
enemies = pg.sprite.Group()
bullets = pg.sprite.Group()
bosses = pg.sprite.Group()

# instantiate the player class
player = Player()
players.add(player)

count = 1

# spacing for enemies
spacingx = WIDTH/20
spacingy = HEIGHT/30


enemy_list = []
# spawns enemies in with correct spacing based off of screen dimensions
for i in range((ROWS*19)):
    cooldown = random.randint(120, ENEMY_FIRERATE)
    x = spacingx
    y = spacingy
    movey = 5
    movex = 0
    e = Enemy(x, y, RED, 30, 22, movex, movey, cooldown, ENEMY_HP)
    all_sprites.add(e)
    enemies.add(e)
    enemy_list.append(e)
    # print(e)
    spacingx += WIDTH/20
    if count % 19 == 0:
        spacingy += HEIGHT/15
        spacingx = WIDTH/20  
    count += 1

# add player to all sprites group
all_sprites.add(player)


win = False
# Game loop
running = True
# gameover = False
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    # get pygame events to check
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        # if event.type == pg.KEYDOWN:
        #     if event.key == 
    
    # when to spawn boss and where to spawn it
    if FRAME % BOSS_SPAWN == 0:
        cooldown = random.randint(120, BOSS_FIRERATE)
        x = random.choice([-5, (WIDTH + 5)])
        y = 50
        movey = 0
        if x < 0:
            movex = 5
        else:
            movex = -5
        e = Boss(x, y, BLUE, 60, 30, movex, movey, cooldown, BOSS_DAMAGE)
        all_sprites.add(e)
        enemy_list.append(e)
        bosses.add(e)
    
    
    ############ Update ##############
    # update all sprites
    all_sprites.update()

    ############ Draw ################
    # draw the background screen
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    # draw all sprites
    all_sprites.draw(screen)
    
    # draw score and lives on screen
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    draw_text("LIVES: " + str(LIVES), 22, WHITE, WIDTH / 2 - 100, HEIGHT / 24)
    draw_text("FRAMES: " + str(FRAME), 22, WHITE, WIDTH / 2 + 150, HEIGHT / 24)
    draw_text("ENEMIES: " + str(len(enemy_list)), 22, WHITE, WIDTH / 2 - 250, HEIGHT / 24)
    draw_text("BULLETS: " + str(player_bullets), 22, WHITE, WIDTH / 2 - 400, HEIGHT / 24)
    
    # check if you win
    if len(enemies) == 0:
        win = True
        
    if win == True:
        PLAYER_FIRERATE = 6
        # print("YOU WIN!!!")
        if FRAME % 15 == 0:
            for i in range(50):
                x = random.randint(0,WIDTH)
                y = random.randint(0,HEIGHT)
                movey = 2
                movex = 0
                e = Bullet(x, y, (colorbyte(), colorbyte(), colorbyte()), 2, 4, movex, movey, "confetti")
                all_sprites.add(e)
                bullets.add(e)
        if FRAME % 1 == 0:
            cooldown = random.randint(120, BOSS_FIRERATE)
            x = random.choice([-5, (WIDTH + 5)])
            y = 50
            movey = 0
            if x < 0:
                movex = 10
            else:
                movex = -10
            e = Boss(x, y, BLUE, 60, 30, movex, movey, cooldown, BOSS_DAMAGE)
            all_sprites.add(e)
            enemy_list.append(e)
            bosses.add(e)
            
            cooldown = random.randint(120, ENEMY_FIRERATE)
            x = random.randint(0,WIDTH)
            y = random.randint(0,HEIGHT)
            movey = 5
            movex = 0
            e = Enemy(x, y, RED, 30, 22, movex, movey, cooldown, ENEMY_HP)
            all_sprites.add(e)
            enemies.add(e)
            enemy_list.append(e)
                # print(e)
        draw_text("YOU WIN!!!", 144, YELLOW, WIDTH / 2, HEIGHT / 2)
            # gameover = True
        
    # check if you lose
    if LIVES <= 0:
        if win == False:
            player.kill()
            # print("GAME OVER")
            draw_text("GAME OVER", 144, RED, WIDTH / 2, HEIGHT / 2)

    # buffer - after drawing everything, flip display
    pg.display.flip()
    FRAME += 1

pg.quit()
