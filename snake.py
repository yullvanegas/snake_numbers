

import pygame, sys, time, random

difficulty = 10

#tamaño de la ventana
frame_size_x = 720
frame_size_y = 480

#checks para errores encontrados
check_errors = pygame.init()

if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors  when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')
    
#inicializar la ventana de juego 

pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x,frame_size_y))

#colores en rgb
black= pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

#fps
fps_controller = pygame.time.Clock()

# variables de juego 
snake_pos = [100,50]
snake_body = [[100,50], [100-10,50], [100-(2*10), 50]]

food_number = random.randrange(2, 21, 2)
food_pos = [random.randrange(1, (frame_size_x//10))*10, random.randrange(1, (frame_size_y//10))*10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

#game over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()    
#score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score:' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    #pygame.display.flip()

#main logic
while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()
        #WHENEVER A KEY IS PRESSED DOWN
        elif event.type == pygame.KEYDOWN:
            # W-> UP; S -> DOWN; A -> LEFT; D -> RIGHT
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            #ESC-> CREATE EVENT TO QUIT THE GAME
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    #making sure the snake cannot move in the oppositive direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
        
    #MOVING THE SNAKE
    if direction == 'UP':
        snake_pos[1] -=10
    if direction == 'DOWN':
        snake_pos[1] +=10
    if direction == 'LEFT':
        snake_pos[0] -=10
    if direction == 'RIGHT':
        snake_pos[0] +=10
    
    #SNKE BODY GROWING MECHANISM
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score+=1
        #se asegura que ambos numeros hagan parte de la comida
        snake_body.insert(1, [int(digit) for digit in str(food_number)])
        food_spawn = False
    else:
        snake_body.pop()
    
    #spawing food on the screen
    if not food_spawn:
        food_number = random.randrange(2, 101, 2)
        food_pos = [random.randrange(1, (frame_size_x//10))*10, random.randrange(1,(frame_size_y//10))*10]
    food_spawn = True
    
    #gfx
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, white, pygame.Rect(pos[0], pos[1], 10, 10))
    
    #snake food
    font= pygame.font.SysFont('times new roman', 10)
    food_text = font.render(str(food_number), True, white)
    game_window.blit(food_text, (food_pos[0], food_pos[1]))
    #pygame.draw.rect(game_window,white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    
    #game over condition
    #getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
    #touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
            
    show_score(1, white, 'consolas', 20)
    #refresh game screen
    pygame.display.update()
    #refresh rate
    fps_controller.tick(difficulty)
    
    
    