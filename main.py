# Zhan Xiang Zheng ODD 1
import pygame
pygame.init()

# set up game window and caption
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Mario Rip-off Edition")

# list of animation for player
walk_right = [pygame.image.load('Images/MR1.png'), pygame.image.load('Images/MR2.png'), pygame.image.load('Images/MR3.png'), pygame.image.load('Images/MR4.png'), pygame.image.load('Images/MR5.png'), pygame.image.load('Images/MR6.png'), pygame.image.load('Images/MR7.png')]
walk_left = [pygame.image.load('Images/ML1.png'), pygame.image.load('Images/ML2.png'), pygame.image.load('Images/ML3.png'), pygame.image.load('Images/ML4.png'), pygame.image.load('Images/ML5.png'), pygame.image.load('Images/ML6.png'), pygame.image.load('Images/ML7.png')]

# background image and music and initial character image
char = pygame.image.load('Images/MR1.png')
background = pygame.image.load('Images/background.jpg')
background = pygame.transform.scale(background, (1000, 500))
music = pygame.mixer.music.load("Music/ThemeSong.wav")
pygame.mixer.music.play(-1)

# sound effects
jump_sound = pygame.mixer.Sound("Music/MarioJump.wav")
hit_sound = pygame.mixer.Sound("Music/hit.wav")
game_over = pygame.mixer.Sound("Music/game_over.wav")
phew_sound = pygame.mixer.Sound("Music/phew.wav")

# others
clock = pygame.time.Clock()
score = 0

# class for player
class player(object):
    # initiate variables
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x, self.y, 50, 100)

    # draws out character
    def draw(self, screen):
        if self.walk_count + 1 >= 21:   # the lists of animations will go over three times before resetting
            self.walk_count = 0
        if not self.standing:   # when not standing still, go through the list, displaying each animation
            if self.left:
                screen.blit(walk_left[self.walk_count // 3], (self.x, self.y))  # left animation list
                self.walk_count += 1
            elif self.right:
                screen.blit(walk_right[self.walk_count // 3], (self.x, self.y))     # right animation list
                self.walk_count += 1
        else:   # displays the last direction as the "standing" image
            if self.left:
                screen.blit(walk_left[0], (self.x, self.y))
            else:
                screen.blit(walk_right[0], (self.x, self.y))
        self.hitbox = (self.x, self.y, 50, 100)  # player's hit box follow the player
        #pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)

    # acts when player touches another hitbox
    def hit(self):
        # returns the player to it's orginal spot
        self.is_jump = False
        self.jump_count = 10
        self.x = 50
        self.y = 300
        self.walkCount = 0
        # displays -5
        font1 = pygame.font.SysFont('times', 50)
        text = font1.render('-5', 1, (255, 0, 0))
        screen.blit(text, (450,230))
        pygame.display.update()
        # delay some time before program continues to run
        i = 0
        while i < 300:
            pygame.time.delay(5)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


# class for projectile
class projectile(object):
    # initiate variables
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 10 * facing

    # draws the projectile
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)


# class for enemy entity
class enemy(object):
    # list of animation for enemy(deer)
    walk_left = [pygame.image.load('Images/ER1.png'), pygame.image.load('Images/ER2.png'), pygame.image.load('Images/ER3.png'), pygame.image.load('Images/ER4.png')]
    walk_right = [pygame.image.load('Images/EL1.png'), pygame.image.load('Images/EL2.png'), pygame.image.load('Images/EL3.png'), pygame.image.load('Images/EL4.png')]

    # initiate variables
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkcount = 0
        self.speed = 6
        self.hitbox = (self.x + 25, self.y + 10, 50, 90)
        self.health = 20
        self.visible = True

    # draws the enemy entity
    def draw(self, screen):
        self.move() #calls the self.move funtion
        if self.visible:    # if enemy is visible(alive) continue
            if self.walkcount + 1 >= 12:    # the lists of animations will go over three times before resetting
                self.walkcount = 0
            if self.speed > 0:  # when not standing still, go through the list, displaying each animation
                enemy = pygame.transform.scale(self.walk_right[self.walkcount // 3], (120,110)) # right animation list
                screen.blit(enemy, (self.x, self.y))
                self.walkcount += 1
            else:
                enemy = pygame.transform.scale(self.walk_left[self.walkcount // 3], (120, 110)) # left animation list
                screen.blit(enemy, (self.x, self.y))
                self.walkcount += 1

            self.hitbox = (self.x + 10, self.y + 10, 90, 90) # enemy's hitbox follows the enemy
            # health bar of the enemy
            pygame.draw.rect(screen, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 100, 10))
            pygame.draw.rect(screen, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 100 - (5 * (20 - self.health)), 10))
            #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    # enemy movement
    def move(self):
        if self.speed > 0: # sets a path for the enemy to follow
            if self.x < self.path[1] - self.speed:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkcount = 0
        else: # if enemy is not visible(dead)
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkcount = 0

    # if enemy health drops to 0, make the enemy not visible(dead)
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


# draws game window
# @param None
# @retune None
def redrawGameWindow():
    screen.blit(background, (0,0))
    # displays score
    text = font_score.render('Score: ' + str(score), 1, (0,0,0))
    screen.blit(text, (825,10))
    mario.draw(screen)  # calls the player.draw function
    deer.draw(screen)   # calls the enemy.draw function
    for bullet in bullets : # displays bullet
        bullet.draw(screen) # calls projectile.draw function

    pygame.display.update() # updates game window
    return None

# main loop
font_score = pygame.font.SysFont('times', 30, True, False)  # score font
mario = player(50, 300, 64, 64)     # give mario the player class functions
deer = enemy(100,300,64,64, 900)    # gives deer the enemey class functions
cooldown = 0    # time before each bullet can be launch
bullets = []    # bullets list
run = True
while run:
    clock.tick(25)

    # when "quit" is clicked in the game window, ends the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # if deer is visible and touches the player, 5 points off the score board
    if deer.visible == True:
        if mario.hitbox[1] < deer.hitbox[1] + deer.hitbox[3] and mario.hitbox[1] + mario.hitbox[3] > deer.hitbox[1]:
            if mario.hitbox[0] + mario.hitbox[2] > deer.hitbox[0] and mario.hitbox[0] < deer.hitbox[0] + deer.hitbox[2]:
                game_over.play()
                mario.hit()
                score -= 5

    # when bullet hits enemy, score plus one
    for bullet in bullets:
        if deer.visible:    # if the dear is "alive"
            if bullet.y - bullet.radius < deer.hitbox[1] + deer.hitbox[3] and bullet.y + bullet.radius > deer.hitbox[1]:
                if bullet.x + bullet.radius > deer.hitbox[0] and bullet.x - bullet.radius < deer.hitbox[0] + deer.hitbox[2]:
                    hit_sound.play()
                    deer.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < 1000 and bullet.x > 0:    # allows the bullet to move
            bullet.x += bullet.speed
        else:   # when bullet touches the border, it disappear
            bullets.pop(bullets.index(bullet))

    # bullet fire time cooldown
    if cooldown > 0 :
        cooldown += 1
    if cooldown > 5:
        cooldown = 0

    # delays the program before enemy respawn
    if deer.health == 0:
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()
        deer.health = 20
        deer.visible = True

    # keys
    keys = pygame.key.get_pressed()

    # when space is clicked, fires bullet
    if keys[pygame.K_SPACE] and cooldown == 0:
        phew_sound.play()
        # direction of the bullet
        if mario.left:
            facing = -1
        else:
            facing = 1
        # allows only 7 bullet to be on the game at a time
        if len(bullets) < 7:
            bullets.append(projectile(round(mario.x + mario.width // 2), round(mario.y + mario.height // 2), 10, (255, 0, 0), facing))
        cooldown = 1    # starts the cooldown when bullet is fire

    # when left/a key is pressed move left
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and mario.x > mario.speed:
        mario.x -= mario.speed
        mario.left = True
        mario.right = False
        mario.standing = False

    # when right/d key is pressed move right
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and mario.x < 950 - mario.speed:
        mario.x += mario.speed
        mario.left = False
        mario.right = True
        mario.standing = False

    # if neither of those are pressed, player in "standing" position
    else:
        mario.standing = True
        mario.walk_count = 0

    if not mario.is_jump:   # the player is not in jumping motion
        if keys[pygame.K_w] or keys[pygame.K_UP]:   # press up/w to jump
            jump_sound.play()
            mario.is_jump = True
            mario.left = False
            mario.right = False
            mario.walk_count = 0
    else:   # if in jumping motion
        if mario.jump_count >= -10:
            mario.y -= (mario.jump_count * abs(mario.jump_count)) * 0.5
            mario.jump_count -= 1
        else:
            mario.jump_count = 10
            mario.is_jump = False

    redrawGameWindow()  # redraws game window

pygame.quit()   #ends program when main while loop ends
