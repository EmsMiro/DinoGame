import pgzrun
import random
from pygame import Rect  # Importar Rect do pygame

# Configurações da tela
WIDTH = 600
HEIGHT = 400

# posição inicial da imagem de fundo
background_x = 0
velocity_camera = 2  # velocidade da câmera

# lista das plataformas
plataforms = []

# variáveis das plataformas
PLATAFORM_HEIGHT = 3
PLATAFORM_MIN_WIDTH = 30
PLATAFORM_MAX_WIDTH = 80
MIN_VERTICAL_DISTANCE = 30  # distância min entre plataformas


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
            y = random.randint(250, HEIGHT - 20)  # posição na vertical
            valid_position = True  # assume que a posição é válida
            for plataform in plataforms:
                if abs(plataform.y - y) < MIN_VERTICAL_DISTANCE:  # p/ verifica a distância
                    valid_position = False  # se estiver muito próxima, marca como inválida
                    break  # sai do loop p/ tentar de novo

        plataform = Rect(x, y, width, PLATAFORM_HEIGHT)
        plataforms.append(plataform)

# função para criar as plataformas no início do game
create_plataforms()

def update():
    global background_x
    background_x -= velocity_camera  # move o fundo p/esquerda da tela

    # reinicia a posição para criar um loop infinito
    if background_x <= -WIDTH:
        background_x = 0
    
    # move todas as plataformas com o fundo
    for plataform in plataforms:
        plataform.x -= velocity_camera

        # verificação para saber se a plataforma saiu da tela
        if plataform.right < 0:  
            width = random.randint(PLATAFORM_MIN_WIDTH, PLATAFORM_MAX_WIDTH)  # largura aleatória
            plataforms[plataforms.index(plataform)] = Rect(WIDTH + random.randint(50, 150), 
                                                            random.randint(100, HEIGHT - 50), 
                                                            width, PLATAFORM_HEIGHT)

def draw():
    screen.fill((255, 255, 255))  # fundo branco

    # a altura da imagem 
    ground_height = images.ground.get_height()

    # desenha o fundo e repete para criar o loop 
    screen.blit("ground", (background_x, HEIGHT - ground_height))
    screen.blit("ground", (background_x + WIDTH, HEIGHT - ground_height)) 

    # desenha todas as plataformas como retângulos
    for plataform in plataforms:
        screen.draw.filled_rect(plataform, (83, 83, 83))  # Cor preta

pgzrun.go()
