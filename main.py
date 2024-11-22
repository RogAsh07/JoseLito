import pygame
import random

# Inicializar pygame
pygame.init()

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)
verde = (0, 255, 0)
azul_claro = (50, 153, 213)

# Dimensiones de la pantalla
ancho = 1280
alto = 720
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("JoseFa: Los Guevos de Harrison")

# Configuración de FPS
fps = 60

# Reloj
reloj = pygame.time.Clock()

# Tamaño del bloque original y escalado
tamano_bloque_original = 20
tamano_bloque = int(tamano_bloque_original * 1.5)  # Escalado 1.5x

# Fuentes
fuente_guevos = pygame.font.SysFont("ashleyscript", 35)
fuente_mensaje = pygame.font.SysFont("ashleyscript", 50)

# Cargar imágenes con manejo de errores
try:
    fondo_img = pygame.image.load("fondo.png")
    fondo_img = pygame.transform.scale(fondo_img, (ancho, alto))  # Ajustar al tamaño de la pantalla

    segmento_img = pygame.image.load("segmento.png")
    segmento_img = pygame.transform.scale(segmento_img, (tamano_bloque, tamano_bloque))  # Escalar al nuevo tamaño

    comida_img = pygame.image.load("fruta.png")
    comida_img = pygame.transform.scale(comida_img, (tamano_bloque, tamano_bloque))  # Escalar al nuevo tamaño
except pygame.error as e:
    print(f"Error al cargar las imágenes: {e}")
    quit()

# Funciones
def mostrar_guevos(guevos, nivel):
    texto = fuente_guevos.render(f"Guevos: {guevos} | Nivel: {nivel}", True, blanco)
    pantalla.blit(texto, [10, 10])

def nuestra_serpiente(lista_serpiente):
    for x in lista_serpiente:
        pantalla.blit(segmento_img, (x[0], x[1]))  # Dibujar cada segmento como una imagen

def mensaje_final(msg, color):
    mensaje = fuente_mensaje.render(msg, True, color)
    pantalla.blit(mensaje, [ancho / 6, alto / 3])

def juego():
    # Variables iniciales
    game_over = False
    game_close = False

    x1 = ancho / 2
    y1 = alto / 2

    x1_cambio = 0
    y1_cambio = 0

    lista_serpiente = []
    largo_serpiente = 1

    # Comida inicial
    comida_x = random.randrange(0, ancho - tamano_bloque, tamano_bloque)
    comida_y = random.randrange(0, alto - tamano_bloque, tamano_bloque)

    velocidad = 10  # Velocidad inicial
    nivel = 1

    while not game_over:

        while game_close:
            pantalla.fill(negro)
            mensaje_final("¡PULILLA JAJA!. Presiona ESC para salir y J para jugar", rojo)
            mostrar_guevos(largo_serpiente - 1, nivel)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_j:
                        juego()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_cambio == 0:
                    x1_cambio = -tamano_bloque
                    y1_cambio = 0
                elif event.key == pygame.K_RIGHT and x1_cambio == 0:
                    x1_cambio = tamano_bloque
                    y1_cambio = 0
                elif event.key == pygame.K_UP and y1_cambio == 0:
                    y1_cambio = -tamano_bloque
                    x1_cambio = 0
                elif event.key == pygame.K_DOWN and y1_cambio == 0:
                    y1_cambio = tamano_bloque
                    x1_cambio = 0

        if x1 >= ancho or x1 < 0 or y1 >= alto or y1 < 0:
            game_close = True
        x1 += x1_cambio
        y1 += y1_cambio

        # Dibujar fondo
        pantalla.blit(fondo_img, (0, 0))

        # Dibujar comida
        pantalla.blit(comida_img, (comida_x, comida_y))

        # Dibujar la serpiente
        cabeza = [x1, y1]
        lista_serpiente.append(cabeza)
        if len(lista_serpiente) > largo_serpiente:
            del lista_serpiente[0]

        for x in lista_serpiente[:-1]:
            if x == cabeza:
                game_close = True

        nuestra_serpiente(lista_serpiente)
        mostrar_guevos(largo_serpiente - 1, nivel)

        pygame.display.update()

        # Comprobar si la serpiente come la comida
        if abs(x1 - comida_x) < tamano_bloque and abs(y1 - comida_y) < tamano_bloque:
            comida_x = random.randrange(0, ancho - tamano_bloque, tamano_bloque)
            comida_y = random.randrange(0, alto - tamano_bloque, tamano_bloque)
            largo_serpiente += 1

            # Aumentar nivel y velocidad de forma controlada
            if largo_serpiente % 5 == 0:
                # Aumentar velocidad de manera más suave
                if velocidad < 30:  # Limitar la velocidad máxima
                    velocidad += 1
                nivel += 1

          # Mantener el juego corriendo a 60 FPS

    pygame.quit()
    quit()

juego()
