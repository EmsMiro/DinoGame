import pgzrun
import random
from pygame import Rect  # Importar somente Rect do pygame

# Configurações da tela
WIDTH = 600
HEIGHT = 400

# posição inicial da imagem de fundo
background_x = 0
velocity_camera = 2  # velocidade da câmera

#img do personagem
player = Actor('dino')
player.x = 100 #posição do player na horizontal
player.y = HEIGHT - 40 #posição na vertical

# sprites do player
player_images = ['dino', 'dino_run1', 'dino_run2']
current_image_index = 0
animation_speed = 0.1  # controla a velocidade da animação
animation_timer = 0

# lista das plataformas
plataforms = []

# variáveis das plataformas
PLATAFORM_HEIGHT = 3
PLATAFORM_MIN_WIDTH = 30
PLATAFORM_MAX_WIDTH = 80
MIN_VERTICAL_DISTANCE = 30  # distância min entre plataformas na vertical
MIN_HORIZONTAL_DISTANCE = 50 # distancia min entre as plataformas na horizontal

# variáveis para pulo
gravity = 0.5
velocity_y = 0
jumping = False
double_jump = False

# Definição dos limites da altura das plataformas
PLATFORM_MIN_Y = HEIGHT - 100  # Um pouco acima do solo
PLATFORM_MAX_Y = HEIGHT // 2   # Metade da tela (mais alto permitido)

# função pra gerar plataformas aleatoriamente
def create_plataforms():
    global plataforms 
    plataforms = []    
    num_plataforms = 2

    for _ in range(num_plataforms):
        width = random.randint(PLATAFORM_MIN_WIDTH, PLATAFORM_MAX_WIDTH)
        x = random.randint(100, WIDTH - width)  # posição horizontal aleatória
       # lógica p/ garantir que as plataformas não se sobreponham
        valid_position = False
        while not valid_position:
            #y = random.randint(200, HEIGHT - 150)  # posição na vertical
            y = random.randint(PLATFORM_MAX_Y, PLATFORM_MIN_Y)            
            valid_position = True  # assume que a posição é válida
            for plataform in plataforms:
                if abs(plataform.y - y) < MIN_VERTICAL_DISTANCE:  # p/ verifica a distância
                    valid_position = False  # se estiver muito próxima, marca como inválida
                    break  # sai do loop p/ tentar de novo
            
                # Verifica a distância horizontal
                if abs(plataform.x - x) < (plataform.width + MIN_HORIZONTAL_DISTANCE):  # p/ verifica a distância horizontal
                    valid_position = False  # se estiver muito próxima, marca como inválida
                    break  # sai do loop p/ tentar de novo


        plataform = Rect(x, y, width, PLATAFORM_HEIGHT)
        plataforms.append(plataform)        

# função para criar as plataformas no início do game
create_plataforms()

def update(dt):
    global background_x, current_image_index, animation_timer, velocity_y, jumping, double_jump
    background_x -= velocity_camera  # move o fundo p/esquerda da tela

    # reinicia a posição para criar um loop infinito
    if background_x <= -WIDTH:
        background_x = 0

    # Atualiza a física do pulo
    if jumping:
        velocity_y += gravity  # aplica gravidade
        player.y += velocity_y  # atualiza a posição vertical do jogador

        # verificação se o jogador atingiu o solo
        on_ground = False
        for plataform in plataforms:
            if player.colliderect(plataform) and velocity_y >= 0:  # verifica colisão com plataformas
                player.y = plataform.top - player.height // 2  # ajusta a posição do jogador
                velocity_y = 0  # reseta a velocidade vertical
                on_ground = True
                double_jump = False  
                break
        # verifica se o player caiu abaixo do chão
        if player.y >= HEIGHT - player.height // 2:  # ajusta para a altura do sprite
            player.y = HEIGHT - player.height // 2  # impeder que o jogador fique abaixo do chão
            jumping = False  # para o pulo se atingir o chão

        if not on_ground and player.y < HEIGHT:  # se não estiver no chão e ainda está no ar
            player.y = min(player.y, HEIGHT)  # impede que o jogador saia da tela
        elif player.y >= HEIGHT:  # se o jogador cair abaixo do chão
            player.y = HEIGHT
            jumping = False  # para o pulo se atingir o chão
    
    # move todas as plataformas com o fundo
    for plataform in plataforms:
        plataform.x -= velocity_camera

        # verificação para saber se a plataforma saiu da tela
        if plataform.right < 0:              
            width = random.randint(PLATAFORM_MIN_WIDTH, PLATAFORM_MAX_WIDTH)
            new_x = WIDTH + random.randint(50, 200)
            new_y = random.randint(PLATFORM_MAX_Y, PLATFORM_MIN_Y)  #área limite
            plataforms[plataforms.index(plataform)] = Rect(new_x, new_y, width, PLATAFORM_HEIGHT)
        # atualiza a animação do personagem
    animation_timer += dt
    if animation_timer > animation_speed:
        current_image_index = (current_image_index + 1) % len(player_images)
        animation_timer = 0

    # atualiza a imagem do jogador
    player.image = player_images[current_image_index]

def on_key_down(key):
    global jumping, velocity_y, double_jump
    if key == keys.SPACE:
        if not jumping:  # se o jogador não está pulando
            jumping = True
            velocity_y = -12  # força do pulo
        elif not double_jump: 
            double_jump = True
            velocity_y = -10  
       
def draw():
    screen.fill((255, 255, 255))  # fundo branco

    # a altura da imagem 
    ground_height = images.ground.get_height()

    # desenha o fundo e repete para criar o loop 
    screen.blit("ground", (background_x, HEIGHT - ground_height))
    screen.blit("ground", (background_x + WIDTH, HEIGHT - ground_height)) 

    # desenha todas as plataformas como retângulos
    for plataform in plataforms:
        screen.draw.filled_rect(plataform, (83, 83, 83))
    
    #desenha o player na tela
    player.draw()    
 
pgzrun.go()
