import pygame
import random
import webbrowser  # Para abrir el navegador con el enlace de Instagram

# Inicializar pygame
pygame.init()
pygame.mixer.init()  # Inicializar el mezclador de audio

# Colores
blanco = (255, 255, 255)
rojo = (213, 50, 80)

# Dimensiones de la pantalla
ancho = 1280
alto = 720
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("JoseFa: Los guevos de Harrison")

# Reloj
reloj = pygame.time.Clock()
fps = 25

# Tamaño del bloque
tamano_bloque = 30

# Fuentes
fuente_titulo = pygame.font.SysFont("ashleyscript", 80)
fuente_texto = pygame.font.SysFont("ashleyscript", 35)
fuente_instagram = pygame.font.SysFont("ashleyscript", 25)

# Cargar imágenes
comida_img = pygame.image.load("fruta.png")
comida_img = pygame.transform.scale(comida_img, (tamano_bloque, tamano_bloque))

segmento_img = pygame.image.load("segmento.png")
segmento_img = pygame.transform.scale(segmento_img, (tamano_bloque, tamano_bloque))

# Cargar música y efectos de sonido
pygame.mixer.music.load("assets/audio/musica_fondo.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Reproducir música en bucle infinito

sonido_comida = pygame.mixer.Sound("assets/audio/comida.wav")
sonido_comida.set_volume(1.0)

sonido_colision = pygame.mixer.Sound("assets/audio/colision.wav")
sonido_colision.set_volume(1.0)


# Funciones
def generar_gradiente_morado():
    """Generar un fondo de color morado degradado."""
    for y in range(alto):
        intensidad = 255 - (y * 255 // alto)
        pygame.draw.line(pantalla, (intensidad, 0, intensidad), (0, y), (ancho, y))


def generar_fondo_arcoiris():
    """Generar un fondo arcoíris dinámico."""
    colores = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
    banda_altura = alto // len(colores)
    for i, color in enumerate(colores):
        pygame.draw.rect(pantalla, color, (0, i * banda_altura, ancho, banda_altura))


def mostrar_mensaje(texto, fuente, color, posicion):
    """Mostrar un mensaje en la pantalla."""
    mensaje = fuente.render(texto, True, color)
    pantalla.blit(mensaje, posicion)


def mostrar_boton(texto, fuente, color, posicion):
    """Mostrar un mensaje que simula un botón."""
    mensaje = fuente.render(texto, True, color)
    rect = mensaje.get_rect()
    rect.topleft = posicion
    pygame.draw.rect(pantalla, color, rect.inflate(10, 10), 2)  # dibujar un borde alrededor del texto
    pantalla.blit(mensaje, posicion)
    return rect


def nuestra_serpiente(lista_serpiente):
    """Dibujar la serpiente."""
    for x in lista_serpiente:
        pantalla.blit(segmento_img, (x[0], x[1]))


def menu_inicio():
    """Menú de inicio."""
    while True:
        generar_gradiente_morado()  # Generar fondo degradado morado
        mostrar_mensaje("JoseFa: Los guevos de Harrison", fuente_titulo, blanco, (ancho / 6, alto / 4))
        mostrar_mensaje("Presiona ESPACIO para comenzar", fuente_texto, blanco, (ancho / 4, alto / 2))
        mostrar_mensaje("Presiona ESC para salir", fuente_texto, blanco, (ancho / 4, alto / 2 + 50))
        mostrar_mensaje("Dentro del juego usa P para pausar el juego", fuente_texto, blanco, (ancho / 4, alto / 2 + 150))
        mostrar_mensaje("Ig del prog: @rossie.luhh", fuente_texto, blanco, (ancho / 4, alto / 2 + 100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Iniciar el juego
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_RETURN:  # ENTER para abrir Instagram
                    webbrowser.open("https://www.instagram.com/rossie.luhh/")


def pausar_juego():
    """Menú de pausa."""
    pausado = True
    while pausado:
        generar_fondo_arcoiris()  # Generar fondo arcoíris
        mostrar_mensaje("Juego pausado", fuente_titulo, blanco, (ancho / 3, alto / 4))
        mostrar_mensaje("Presiona P para continuar", fuente_texto, blanco, (ancho / 3, alto / 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pausado = False


def juego():
    """Función principal del juego."""
    menu_inicio()

    x1, y1 = ancho / 2, alto / 2
    x1_cambio, y1_cambio = 0, 0

    lista_serpiente = []
    largo_serpiente = 1

    comida_x = random.randrange(0, ancho - tamano_bloque, tamano_bloque)
    comida_y = random.randrange(0, alto - tamano_bloque, tamano_bloque)

    direccion_actual = None  # Nueva variable para rastrear la dirección actual
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direccion_actual != "DERECHA":
                    x1_cambio, y1_cambio = -tamano_bloque, 0
                    direccion_actual = "IZQUIERDA"
                elif event.key == pygame.K_RIGHT and direccion_actual != "IZQUIERDA":
                    x1_cambio, y1_cambio = tamano_bloque, 0
                    direccion_actual = "DERECHA"
                elif event.key == pygame.K_UP and direccion_actual != "ABAJO":
                    x1_cambio, y1_cambio = 0, -tamano_bloque
                    direccion_actual = "ARRIBA"
                elif event.key == pygame.K_DOWN and direccion_actual != "ARRIBA":
                    x1_cambio, y1_cambio = 0, tamano_bloque
                    direccion_actual = "ABAJO"
                elif event.key == pygame.K_p:
                    pausar_juego()

        x1 += x1_cambio
        y1 += y1_cambio

        if x1 >= ancho or x1 < 0 or y1 >= alto or y1 < 0:
            sonido_colision.play()
            game_over = True

        pantalla.fill(blanco)
        pantalla.blit(comida_img, (comida_x, comida_y))

        cabeza = [x1, y1]
        lista_serpiente.append(cabeza)
        if len(lista_serpiente) > largo_serpiente:
            del lista_serpiente[0]

        # Comprobar colisión con el cuerpo
        for segmento in lista_serpiente[:-1]:
            if segmento == cabeza:
                sonido_colision.play()
                game_over = True

        # Comprobar colisión con la comida
        if abs(x1 - comida_x) < tamano_bloque and abs(y1 - comida_y) < tamano_bloque:
            sonido_comida.play()
            comida_x = random.randrange(0, ancho - tamano_bloque, tamano_bloque)
            comida_y = random.randrange(0, alto - tamano_bloque, tamano_bloque)
            largo_serpiente += 1

        nuestra_serpiente(lista_serpiente)

        pygame.display.update()
        reloj.tick(fps)

    # Pantalla de fin del juego
    while True:
        pantalla.fill(blanco)
        mostrar_boton("¡Perdiste!", fuente_titulo, rojo, (ancho / 3, alto / 4))

        # Botón de reiniciar y salir
        boton_reiniciar = mostrar_boton("Presiona ESPACIO para reiniciar o ESC para salir", fuente_texto, blanco, (ancho / 2, alto / 2))
        boton_instagram = mostrar_boton("Instagram: @rossie.luhh", fuente_instagram, blanco, (ancho / 2, alto - 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    juego()  # Reiniciar el juego
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(event.pos):
                    juego()
                elif boton_instagram.collidepoint(event.pos):
                    webbrowser.open("https://www.instagram.com/rossie.luhh/")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


# Iniciar el juego
juego()
