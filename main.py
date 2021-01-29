__author__ = "Tony Astuhuaman"
'''
Pretty cool flappy bird made by myself and soon launched on github as a repository
'''
#!/usr/bin/python3
import pygame as p
import sys, random

#others python modules for games
#pygame, pyglet,arcade
#Godot(with GDScript)

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,620))
    screen.blit(floor_surface,((floor_x_pos + 400) , 620)) #400 is th width of my floor 

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (400,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (400,random_pipe_pos-200))
    return bottom_pipe , top_pipe

#influences all of the different rectangles and then creates a new list of new rectangles 
def move_pipes(pipes): 
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = p.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >=620:
        return False
    return True

def rotate_bird(bird):
    new_bird = p.transform.rotozoom(bird, -bird_movement *3 ,1) #we can use a lamba function too
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (90,bird_rect.centery))
    return new_bird,new_bird_rect

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255)) #RGB(red,green and blue)
        score_rect = score_surface.get_rect(center = (200,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255)) #RGB(red,green and blue)
        score_rect = score_surface.get_rect(center = (200,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255)) #RGB(red,green and blue)
        high_score_rect = high_score_surface.get_rect(center = (200,600))
        screen.blit(high_score_surface,high_score_rect)



p.init()
screen = p.display.set_mode((400,700))
p.display.set_caption("Flappy Bird")

icon_game = p.image.load("assets/bluebird-midflap.png")
p.display.set_icon(icon_game)

clock = p.time.Clock()
game_font = p.font.Font( '04B_19.TTF',40)

#Game variables 
gravity = 0.25
bird_movement = 0 #starts at 0 
game_active = False
score = 0
high_score = 0

bg_surface = p.image.load('assets/background-night.png').convert()
bg_surface = p.transform.scale(bg_surface,(400,700))

floor_surface = p.image.load('assets/base.png').convert()
floor_surface = p.transform.scale(floor_surface,(400,80))
floor_x_pos = 0

bird_downflap = p.transform.scale((p.image.load('assets/bluebird-downflap.png').convert_alpha()),(63,49))
bird_midflap = p.transform.scale((p.image.load('assets/bluebird-midflap.png').convert_alpha()),(63,49))
bird_upflap = p.transform.scale((p.image.load('assets/bluebird-upflap.png').convert_alpha()),(63,49))
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (90,350)) #this will get a rect around the bird, so that we can check for collission'''

BIRDFLAP = p.USEREVENT +1
p.time.set_timer(BIRDFLAP,200) #200 miliseconds

'''bird = p.image.load('assets/bluebird-midflap.png').convert_alpha()
bird = p.transform.scale(bird,(60,40))
bird_rect = bird.get_rect(center = (90,350)) #this will get a rect around the bird, so that we can check for collission'''

pipe_surface = p.image.load('assets/pipe-green.png')
pipe_surface = p.transform.scale(pipe_surface,(70,450))
pipe_list = []

#using a timer to see when the pipe is going to appear
SPAWNPIPE = p.USEREVENT  #USEREVENT iss goingo to be trigger by timer
p.time.set_timer(SPAWNPIPE,1200) # this is in miliseconds, every 1.2 seconds ...
pipe_height = [310, 250, 270, 300 , 580, 350 ,520] #620 is the maximum point that the pipe can be see.

#game_over image
game_over_surface =p.transform.scale((p.image.load('assets/message.png').convert_alpha()),(300,420))
game_over_rect = game_over_surface.get_rect(center = (200 ,320))

while True:
    #image of player 1
    #background image
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()
        if event.type == p.KEYDOWN:
            if event.key == p.K_SPACE  and game_active:
                bird_movement = 0
                bird_movement -= 7
            if event.key == p.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center =(90,350)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) #instead od append, we use extend
            #print(pipe_list)

        if event.type == BIRDFLAP:
            if bird_index <2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()

#background
    screen.blit(bg_surface,(0,0))

    if game_active:
    #Bird////....
    #here we make the effect of falling down
        bird_movement +=gravity
        rotated_bird = rotate_bird(bird_surface)

        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

    #Pipes////....
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score= update_score(score,high_score)
        score_display('game_over')



#Floor////....
    floor_x_pos -=1
    draw_floor() #call the function to get double pictures
    if floor_x_pos <=-400:
        floor_x_pos = 0 #reset the position of the floor

    screen.blit(floor_surface,(floor_x_pos,620))

    #screen.blit(bird,(200,310))
    p.display.update()
    clock.tick(97) #to get frames look pretty cool/ 95 frames per second
