import pygame 
from sys import exit
import random

def gravtiy_bird(grav_down, sound):
    global gravity
    global bird_rect
    global game_active
    
    gravity += grav_down
    bird_rect.y += gravity
            
    if bird_rect.bottom >= 450:
        bird_rect.bottom = 450
        game_active = False
        sound.play()
            
    if bird_rect.top <= 0:
        bird_rect.top = 0

def scroll_img(img, scroll_speed):
        global scroll 
        for i in range(2):
            window.blit(img,(i * 288 + scroll, 450)) 
            
        scroll -= scroll_speed
        if abs(scroll) >= 288:
            scroll = 0


# start window 
bird = pygame.image.load("python/pygame/flappy bird/assets/yellowbird-midflap.png")
pygame.init()
window = pygame.display.set_mode((288,512))
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(bird)

#variables
game_active = False
gravity = 0
scroll = 0
score = 0 
dist = 0
new_score = 0 
clock = pygame.time.Clock() # controls the FPS of the game

#font
font = pygame.font.Font("python/pygame/flappy bird/font/Flappy-Bird.ttf", 50)
font1 = pygame.font.Font("python/pygame/flappy bird/font/Flappy-Bird.ttf", 35) 

#text
score_surf = font1.render(f"YOUR SCORE {score}", False, ("white"))
score_rect = score_surf.get_rect(center = (115, 450))

points_surf = font.render(str(score), True, ('white'))
points_rect = points_surf.get_rect(center = (144, 70))

play_again_surf = font1.render("CLICK TO PLAY!", False, ("white"))
play_again_rect = play_again_surf.get_rect(center = (144, 410))
#sprites
bg = pygame.image.load("python/pygame/flappy bird/assets/background-day.png")

floor = pygame.image.load("python/pygame/flappy bird/assets/base.png")

bird = pygame.image.load("python/pygame/flappy bird/assets/yellowbird-midflap.png")
bird_up = pygame.image.load("python/pygame/flappy bird/assets/yellowbird-upflap.png")

bird_down = pygame.image.load("python/pygame/flappy bird/assets/yellowbird-downflap.png")
bird_rect = bird.get_rect( center =(104,230))

birds = [bird_up, bird, bird_down]
birds_index = 0

flappybirdmsg = pygame.image.load("python/pygame/flappy bird/assets/message.png")
msg_rect = flappybirdmsg.get_rect(center =(144, 100))

pipe = pygame.image.load("python/pygame/flappy bird/assets/pipe-green.png")
pipe_up = pygame.transform.rotozoom(pipe, 0, 0.85)
pipe_down = pygame.transform.rotozoom(pipe, 180, 0.85)
pipe_up_rect = pipe_up.get_rect()
pipe_down_rect = pipe_down.get_rect()

pipes_up_list = []     
pipes_down_list = []   

#sounds
click_sound = pygame.mixer.Sound("python/pygame/flappy bird/sound/sfx_wing.wav")
hit_sound = pygame.mixer.Sound("python/pygame/flappy bird/sound/sfx_hit.wav")
point_sound = pygame.mixer.Sound("python/pygame/flappy bird/sound/sfx_point.wav")
die_sound = pygame.mixer.Sound("python/pygame/flappy bird/sound/sfx_die.wav")

#timers
pipe_event = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_event, random.randint(1500, 1800))

bird_event = pygame.USEREVENT + 2
pygame.time.set_timer(bird_event, 200)


while True:
    pygame.display.update()
    
    
    for event in pygame.event.get(): #verify if player wants to quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            gravity = -6.5
            click_sound.play()
            game_active = True
            birds_index = 0
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active == True:
                birds_index = 2
                
        if event.type == bird_event:
            if game_active == False:
                if birds_index >=2:
                    birds_index = 0
                else:
                    birds_index += 1
                            
        if event.type == pipe_event:
            pos_y = random.randint(130,200)
            dist = random.randint(140, 170)
            pipes_down_list.append(pipe_down.get_rect( bottomleft = (300, pos_y)))
            pipes_up_list.append(pipe_up.get_rect( topleft = (300, pos_y + dist)))
    
    if game_active:
        
        # collisions
        if pipes_down_list:
            for pipes_down in pipes_down_list:
                if bird_rect.colliderect(pipes_down):
                    hit_sound.play()
                    game_active = False
                    new_score = score
                    score = 0
                    
                if round(bird_rect.x, -1) == round(pipes_down.x, -1):
                    score += 1
                    point_sound.play()
        
        if pipes_up_list:
            for pipes_up in pipes_up_list:
                if bird_rect.colliderect(pipes_up):
                    hit_sound.play()
                    game_active = False      
                    new_score = score
                    score = 0

        #sky
        window.blit(bg, (0,0))
        #obstacle
        for pipe_up_rect in pipes_up_list:
            pipe_up_rect.x -= 5
            window.blit(pipe_up, pipe_up_rect)
        
        for pipe_down_rect in pipes_down_list:
            pipe_down_rect.x -= 5
            window.blit(pipe_down, pipe_down_rect)
            
        #points
        points_surf = font.render(str(score), True, ('white'))
        window.blit(points_surf, points_rect)
        
        #floor
        scroll_img(floor, 2)
                    
        # player  
        window.blit(birds[birds_index], bird_rect)
        gravtiy_bird(0.4, die_sound)
        
       
            
    else: # end screen
        window.blit(bg, (0,0))
        window.blit(flappybirdmsg, msg_rect)
        window.blit(play_again_surf, play_again_rect)
        scroll_img(floor, 2)     
        # player   
        bird_rect = bird.get_rect( center =(104,230))
        window.blit(birds[birds_index], bird_rect)
        pipes_down_list.clear()
        pipes_up_list.clear()
        if new_score:
            score_surf = font.render(f"Your score {new_score}", False, ("white"))
            window.blit(score_surf, score_rect)
            
    clock.tick(60) # sets 60 FPS
            
    