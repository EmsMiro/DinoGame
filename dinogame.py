import pgzrun
import random
from pygame import Rect

# config da tela
WIDTH = 600
HEIGHT = 400
background_x = 0
velocity_camera = 2

# config do personagem
player = Actor('dino')
player.x = 100
player.y = HEIGHT - 40

player_images = ['dino', 'dino_run1', 'dino_run2']
current_image_index = 0
animation_speed = 0.1
animation_timer = 0

# variáveis da música
music_on = True
music_button = Rect(230, 220, 140, 50)

#botão exit
exit_button = Rect(230, 280, 140, 50)

#botão tentar novamente
try_again_button = Rect(230, 220, 140, 50)

# iniciar música junto com o game
music.play('happysong')
music.set_volume(0.1)

def toggle_music():
    global music_on
    if music_on:
        music.stop()
    else:
        music.play('happysong')
    music_on = not music_on

# variáveis das plataformas
plataforms = []
PLATAFORM_HEIGHT = 3
PLATAFORM_MIN_WIDTH = 30
PLATAFORM_MAX_WIDTH = 80
PLATFORM_MIN_Y = HEIGHT - 100
PLATFORM_MAX_Y = HEIGHT // 2

# variáveis para a mecânica do pulo
gravity = 0.5
velocity_y = 0
jumping = False
double_jump = False
score = 0  

eggs = []  # array p/ armazenar os ovos
available_eggs = []  # Array p/ ovos que ainda estão disponíveis
collected_eggs = []  # Array p/ rastrear os ovos coletados

# variáveis dos inimigos
cacti = []
CACTUS_IMAGES = ['cactus1', 'cactus2']
CACTUS_MIN_DISTANCE = 450
CACTUS_MAX_DISTANCE = 500
CACTUS_SPEED = 2

# Variáveis do pássaro
bird_images = ['bird1', 'bird2']
bird_animation_index = 0
bird_animation_speed = 0.2
bird_animation_timer = 0
birds = [] 

# variáveis de estado do jogo
game_over = False
game_started = False
start_button = Rect(230, 150, 140, 50) 
show_game_over = False 

def create_plataforms():
    global plataforms, eggs, available_eggs
    plataforms = []
    eggs = []
    available_eggs = []  
    num_plataforms = 2

    for _ in range(num_plataforms):
        width = random.randint(PLATAFORM_MIN_WIDTH, PLATAFORM_MAX_WIDTH)
        x = random.randint(100, WIDTH - width)

        valid_position = False
        while not valid_position:
            y = random.randint(PLATFORM_MAX_Y, PLATFORM_MIN_Y)
            valid_position = True
            for plataform, _ in plataforms:
                if abs(plataform.y - y) < 30:
                    valid_position = False
                    break
                if abs(plataform.x - x) < (plataform.width + 50):
                    valid_position = False
                    break

        plataform = Rect(x, y, width, PLATAFORM_HEIGHT)

        # adicionar um ovo aleatoriamente
        egg = None
        if random.random() < 0.5:
            egg_x = x + width // 2
            egg_y = y - 20
            egg = Actor('dino_egg', (egg_x, egg_y))
            eggs.append(egg)  
            available_eggs.append(egg)  

        plataforms.append((plataform, egg))

def create_enemy():
    if len(cacti) == 0 or cacti[-1].x < WIDTH - random.randint(CACTUS_MIN_DISTANCE, CACTUS_MAX_DISTANCE):
        cactus = Actor(random.choice(CACTUS_IMAGES))
        cactus.x = WIDTH + 20
        cactus.y = HEIGHT - 35
        cacti.append(cactus)

def create_bird():
    bird = Actor(random.choice(bird_images))
    bird.x = WIDTH + 20
    bird.y = random.randint(100, 200) 
    birds.append(bird)

create_plataforms()

# função de atualização do jogo
def update(dt):
    global background_x, current_image_index, animation_timer, velocity_y, jumping, double_jump, score, collected_eggs
    global bird_animation_timer, bird_animation_index, game_over

    if not game_started:  # verifca se o jogo não começou, não atualiza
        return 

    if game_over:        
        return 

    background_x -= velocity_camera

    if background_x <= -WIDTH:
        background_x = 0

    if jumping:
        velocity_y += gravity
        player.y += velocity_y

        on_ground = False
        for plataform, _ in plataforms:
            if player.colliderect(plataform) and velocity_y >= 0:
                player.y = plataform.top - player.height // 2
                velocity_y = 0
                on_ground = True
                double_jump = False
                break
            
        if player.y >= HEIGHT - player.height // 2:
            player.y = HEIGHT - player.height // 2
            jumping = False

    # atualiza as plataformas e ovos
    for i in range(len(plataforms)):
        plataform, egg = plataforms[i]
        plataform.x -= velocity_camera

        if egg:
            egg.x -= velocity_camera
            
        if plataform.right < 0:
            width = random.randint(PLATAFORM_MIN_WIDTH, PLATAFORM_MAX_WIDTH)
            new_x = WIDTH + random.randint(50, 200)
            new_y = random.randint(PLATFORM_MAX_Y, PLATFORM_MIN_Y)
            new_plataform = Rect(new_x, new_y, width, PLATAFORM_HEIGHT)

            new_egg = None
            if random.random() < 0.5:
                egg_x = new_x + width // 2
                egg_y = new_y - 15
                new_egg = Actor('dino_egg', (egg_x, egg_y))
                available_eggs.append(new_egg) 

            plataforms[i] = (new_plataform, new_egg)

    # verificação de colisão com os ovos
    for i in range(len(available_eggs) - 1, -1, -1):
        egg = available_eggs[i]
        if player.colliderect(egg):
            score += 1
            collected_eggs.append(egg)
            available_eggs.pop(i)
            print(f'Ovo coletado! Score: {score}')

    # atualiza a animação do player
    animation_timer += dt
    if animation_timer > animation_speed:
        current_image_index = (current_image_index + 1) % len(player_images)
        animation_timer = 0

    player.image = player_images[current_image_index]

    # atualiza os obstáculos
    create_enemy()
    for cactus in cacti:
        cactus.x -= CACTUS_SPEED
    
    # verifica colisão com os cactos
    for cactus in cacti:
        if player.colliderect(cactus):
            game_over = True

    cacti[:] = [cactus for cactus in cacti if cactus.right > 0]

    # atualiza os pássaros
    if random.random() < 0.005:  
        create_bird()
        
    for bird in birds:
        bird.x -= 3  
        if player.colliderect(bird):
            game_over = True  # colisão com pássaros

    # remover pássaros fora da tela
    birds[:] = [bird for bird in birds if bird.right > 0]

    # atualiza a animação do pássaro
    bird_animation_timer += dt
    if bird_animation_timer > bird_animation_speed:
        bird_animation_index = (bird_animation_index + 1) % len(bird_images)
        bird_animation_timer = 0

    for bird in birds:
        bird.image = bird_images[bird_animation_index]

# função de escuta do teclado
def on_key_down(key):
    global jumping, velocity_y, double_jump
    if key == keys.SPACE:
        if not jumping:
            jumping = True
            velocity_y = -13
        elif not double_jump:
            double_jump = True
            velocity_y = -10


# função para escutar cliques do mouse
def on_mouse_down(pos):
    global game_started, game_over
    if game_over:
        if try_again_button.collidepoint(pos):
            reset_game()        
        return
    if not game_started and start_button.collidepoint(pos):
        game_started = True
    elif music_button.collidepoint(pos):
        toggle_music()
    elif exit_button.collidepoint(pos):
        exit()

# função p/ reiniciar variáveis do jogo pós clique no try again button
def reset_game():
    global player, current_image_index, animation_timer, velocity_y, jumping, double_jump, score
    global cacti, eggs, available_eggs, birds, game_over, game_started, background_x
    
    player.x = 100
    player.y = HEIGHT - 40
    current_image_index = 0
    animation_timer = 0
    velocity_y = 0
    jumping = False
    double_jump = False
    score = 0
    cacti.clear()
    eggs.clear()
    available_eggs.clear()
    birds.clear()
    game_over = False
    game_started = True
    background_x = 0

    create_plataforms()  
    print("Game reset!")  # p/ verificar se a função foi chamada
  

# função que desenha os elementos na tela
def draw():
    if not game_started:  # esse primeiro if verifica se o jogo não começou, e desenha a tela inicial
        screen.blit("telainicial", (0, 0))         
        screen.draw.text("DINO GAME", center=(WIDTH // 2, start_button.y - 30), fontname="gameplay", color='#535353', fontsize=50)        
        screen.draw.rect(start_button, (0, 0, 0)) 
        screen.draw.text("Start", center=(start_button.x + start_button.width // 2, start_button.y + start_button.height // 2), color='#535353', fontname="gameplay", fontsize=30)
        
        screen.draw.rect(music_button, (0,0,0))
        screen.draw.text("Music On" if music_on else "Music Off", center=(music_button.x + music_button.width // 2, music_button.y + music_button.height // 2), color='#535353', fontname="gameplay", fontsize=20)
        
        screen.draw.rect(exit_button, (255, 0, 0))
        screen.draw.text("Exit", center=(exit_button.x + exit_button.width // 2, exit_button.y + exit_button.height // 2), color='#535353', fontname="gameplay", fontsize=30)
        return
        # tela de GAME OVER
    if game_over:
        screen.fill((255, 255, 255))  # Fundo branco
        screen.draw.text('Game Over!', center=(WIDTH // 2, HEIGHT // 2 - 50), color='#535353', fontname='gameplay', fontsize=60)
        screen.draw.text(f'Score: {score}', center=(WIDTH // 2, HEIGHT // 2 + 20), color='#535353', fontname='gameplay', fontsize=30)
     
        try_again_button.y = HEIGHT // 2 + 70  # Ajuste a posição do botão
        screen.draw.rect(try_again_button, (0, 0, 0))
        screen.draw.text("Try Again", center=(try_again_button.x + try_again_button.width // 2, try_again_button.y + try_again_button.height // 2), color='#535353', fontname="gameplay", fontsize=20)
        return

    # desenha a tela do game em si
    screen.fill((255, 255, 255))
    ground_height = images.ground.get_height()
    screen.blit("ground", (background_x, HEIGHT - ground_height))
    screen.blit("ground", (background_x + WIDTH, HEIGHT - ground_height))

    for plataform, _ in plataforms:
        screen.draw.filled_rect(plataform, (83, 83, 83))

    for egg in available_eggs:
        egg.draw()

    for cactus in cacti:
        cactus.draw()

    for bird in birds:
        bird.draw() 
    
    player.draw()
    screen.draw.text(f'Score: {score}', (10, 10), color='black')    
    
pgzrun.go()
