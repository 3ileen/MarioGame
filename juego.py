#----EILEEN KARIN APAZA COAQUIRA---
import pygame
import random
import math
import sys
import time
from pygame.locals import *

FPS = 30  # fotografias por segundo para actualizar la pantalla
ADV = 640  # ancho de la ventana en pixeles
HDV = 480  # altura de la ventana en pixeles

MA = int(ADV / 2)  # medio del ancho
MH = int(HDV / 2)  # medio de la altura

COLORPASTO = (25, 255, 0)  # color del pasto (verde)
BLANCO = (255, 255, 255)  # definiendo el color blanco
ROJO = (255, 0, 0)  # definiendo el color rojo

CS = 90  # la cámara comenzará a seguir al jugador cuando se aleje 90 píxeles del centro de la ventana.
MOVE = 9  # que tan rapido se mueve el jugador
REBOTE_R = 6  # que tan rapido rebota el jugador (grande es mas lento)
REBOTE_H = 30  # que tan alto rebota el jugador
T_INICIO = 25  # que tan grande comienza el jugador
T_GANAR = 300  # que tan grande debe ser jugador para ganar
TIEMPOR_I = 2  # cuanto tiempo es el jugador invulnerable despues de ser golpeado en segundos
TIEMPO_TXT_P = 4  # Ccuanto tiempo permanece el texto "juego terminado " en la pantalla en segundos
VIDA_J = 3  # con cuantas vidas empieza el jugador

NUM_P = 80  # número de objetos de hierba en el área activa
NUM_A = 30  # numero de enemigos en el area activa
MINV_A = 3  # velocidad del enemigo mas lento
MAXV_A = 7  # velocidad del enemigo mas rapido

CAMBIOD = 2  # probabilidad de cambio de direccion por cuadro
IZQUIERDA = "izquierda"
DERECHA = "derecha"


def main() :  # almacena los nombre globales
    global FPSCLOCK, DISPLAYSURF, BASICFONT, JUGADOR_IMG, R_SQUIR_IMG, PASTO_IMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()  # crear un objeto para ayudar a rastrear el tiempo
    pygame.display.set_icon(
        pygame.image.load('gameicon.png'))  # Cambiar la imagen del sistema para la ventana de visualización
    DISPLAYSURF = pygame.display.set_mode((ADV, HDV))  # Inicializar una ventana o pantalla para mostrar
    pygame.display.set_caption('OMEGA MARIO')  # Establecer el título de la ventana actual
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)  # crear un nuevo objeto Font a partir de un archivo


    # Cargando las imagenes
    JUGADOR_IMG = pygame.image.load('mario.png')
    JUGADOR_IMG.set_colorkey(BLANCO)
    R_SQUIR_IMG = pygame.transform.flip(JUGADOR_IMG, True, False)  # voltear verticalmente y horizontalmente
    PASTO_IMG = []
    for i in range(1, 5):
        PASTO_IMG.append(pygame.image.load('grass%s.png' % i))
    # el juego comienza
    while True:
        runGame()

def runGame():
    # configurar variables para el inicio de un nuevo juego
    invulnerableModo = False  # si el jugador es invulnerable
    invulnerableStartTime = 0  # vez que el jugador se volvió invulnerable
    gameOverMode = False  # si el jugador ha perdido
    gameOverStartTime = 0  # tiempo que el jugador perdió
    winMode = False  # si el jugador ha ganado

    # crea las superficies para contener el texto del juego
    gameOverSurf = BASICFONT.render('Game Over', True, BLANCO)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (MA, MH)

    winSurf = BASICFONT.render('¡Has logrado OMEGA !', True, BLANCO)
    winRect = winSurf.get_rect()
    winRect.center = (MA, MH)

    winSurf2 = BASICFONT.render('(Presione "r" para reiniciar.)', True, BLANCO)
    winRect2 = winSurf2.get_rect()
    winRect2.center = (MA, MH + 30)

    # camerax y cameray son la parte superior izquierda de donde está la vista de la cámara.
    camerax = 0
    cameray = 0

    pasto_O = []  # almacena todos los objetos de pasto en el juego
    enemigo = []  # almacena todos los objetos del enemigo
    # almacena el objeto jugador:
    jugadorO = {'surface': pygame.transform.scale(JUGADOR_IMG, (T_INICIO, T_INICIO)),
                'facing': IZQUIERDA,
                'size': T_INICIO,
                'x': MA,
                'y': MH,
                'bounce': 0,
                'salud': VIDA_J}

    m_izquierdo = False
    m_derecho = False
    m_arriba = False
    m_abajo = False

    # comienza con algunas imágenes de pasto al azar en la pantalla
    for i in range(10):
        pasto_O.append(nuevo_p(camerax, cameray))
        pasto_O[i]['x'] = random.randint(0, ADV)
        pasto_O[i]['y'] = random.randint(0, HDV)

    while True:   # manejará los eventos, actualizará el estado del juego y dibujarátodo en la pantalla.
        # Comprobar si debemos desactivar la invulnerabilidad
        if invulnerableModo and time.time() - invulnerableStartTime > TIEMPOR_I:
            invulnerableModo = False

        # mueve todas los enemigos
        for sObj in enemigo:
            # mueve al enemigo y ajusta su rebote
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1  # incrementa en cada iteración del bucle del juego para cada enemigo
            if sObj['bounce'] > sObj['bouncerate']:
                sObj['bounce'] = 0  # restablecer la cantidad de rebote

            # posibilidad aleatoria de que cambien de dirección
            if random.randint(0, 99) < TIEMPOR_I:
                sObj['movex'] = getRandomVelocity()
                sObj['movey'] = getRandomVelocity()
                if sObj['movex'] > 0:  # faces right
                    sObj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (sObj['width'], sObj['height']))
                else:  # faces left
                    sObj['surface'] = pygame.transform.scale(JUGADOR_IMG, (sObj['width'], sObj['height']))

        # revise todos los objetos y vea si es necesario eliminarlos.
        for i in range(len(pasto_O) - 1, -1, -1):  # iterando y eliminando
            if isOutsideActiveArea(camerax, cameray, pasto_O[i]):
                del pasto_O[i]
        for i in range(len(enemigo) - 1, -1, -1):  # iterando y eliminando
            if isOutsideActiveArea(camerax, cameray, enemigo[i]):
                del enemigo[i]

        # agregue más pasto y enemigos si no tenemos suficiente.
        while len(pasto_O) < NUM_P:
            pasto_O.append(nuevo_p(camerax, cameray))
        while len(enemigo) < NUM_A:
            enemigo.append(nuevo_e(camerax, cameray))

        # ajustar camerax y cameray si está más allá de la "holgura de la cámara"
        playerCenterx = jugadorO['x'] + int(jugadorO['size'] / 2)
        playerCentery = jugadorO['y'] + int(jugadorO['size'] / 2)
        if (camerax + MA) - playerCenterx > CS:
            camerax = playerCenterx + CS - MA
        elif playerCenterx - (camerax + MA) > CS:
            camerax = playerCenterx - CS - MA
        if (cameray + MH) - playerCentery > CS:
            cameray = playerCentery + CS - MH
        elif playerCentery - (cameray + MH) > CS:
            cameray = playerCentery - CS - MH

        # dibuja el fondo verde
        DISPLAYSURF.fill(COLORPASTO)

        # dibuja todos lo objetos pasto en la pantalla
        for gObj in pasto_O:
            gRect = pygame.Rect((gObj['x'] - camerax,
                                 gObj['y'] - cameray,
                                 gObj['width'],
                                 gObj['height']))
            DISPLAYSURF.blit(PASTO_IMG[gObj['grassImage']],
                             gRect)  # dibujar la imagen de hierba en la superficie de la pantalla

        # dibuja a los enemigos
        for sObj in enemigo:
            sObj['rect'] = pygame.Rect((sObj['x'] - camerax,
                                        sObj['y'] - cameray - getBounceAmount(sObj['bounce'], sObj['bouncerate'],
                                                                              sObj['bounceheight']),
                                        sObj['width'],
                                        sObj['height']))
            DISPLAYSURF.blit(sObj['surface'], sObj['rect'])

        # draw the player squirrel
        flashIsOn = round(time.time(), 1) * 10 % 2 == 1
        if not gameOverMode and not (invulnerableModo and flashIsOn):
            jugadorO['rect'] = pygame.Rect((jugadorO['x'] - camerax,
                                            # La función getBounceAmount () devolverá el número de píxeles que se debe aumentar el valor superior.
                                            jugadorO['y'] - cameray - getBounceAmount(jugadorO['bounce'], REBOTE_R,
                                                                                      REBOTE_H),
                                            jugadorO['size'],
                                            jugadorO['size']))
            DISPLAYSURF.blit(jugadorO['surface'], jugadorO['rect'])

        # dibuja la ardilla del jugador
        drawHealthMeter(jugadorO['salud'])

        for event in pygame.event.get():  # manejo de elementos
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    m_abajo = False
                    m_arriba = True
                elif event.key in (K_DOWN, K_s):
                    m_arriba = False
                    m_abajo = True
                elif event.key in (K_LEFT, K_a):
                    m_derecho = False
                    m_izquierdo = True
                    if jugadorO['facing'] != IZQUIERDA:  # cambiar la imagen del jugador
                        jugadorO['surface'] = pygame.transform.scale(JUGADOR_IMG, (jugadorO['size'], jugadorO['size']))
                    jugadorO['facing'] = IZQUIERDA
                elif event.key in (K_RIGHT, K_d):
                    m_izquierdo = False
                    m_derecho = True
                    if jugadorO['facing'] != DERECHA:  # cambiar la imagen del jugador
                        jugadorO['surface'] = pygame.transform.scale(R_SQUIR_IMG, (jugadorO['size'], jugadorO['size']))
                    jugadorO['facing'] = DERECHA
                elif winMode and event.key == K_r:
                    return

            elif event.type == KEYUP:  # Si el jugador suelta cualquiera de las teclas de flecha o WASD, entonces el código debe establecer
                # la variable de movimiento para esa dirección en False . Esto evitará que la ardilla se mueva más en esa dirección
                # deja de mover la ardilla del jugador
                if event.key in (K_LEFT, K_a):
                    m_izquierdo = False
                elif event.key in (K_RIGHT, K_d):
                    m_derecho = False
                elif event.key in (K_UP, K_w):
                    m_arriba = False
                elif event.key in (K_DOWN, K_s):
                    m_abajo = False

                elif event.key == K_ESCAPE:  # Si la tecla que se presionó fue la tecla Esc, entonces finalice el programa
                    terminate()

        # Mover el jugador y contabilizar el rebote
        if not gameOverMode:
            # realmente mueve al jugador
            if m_izquierdo:
                jugadorO['x'] -= MOVE  # hace que la ardilla se mueva más rápido
            if m_derecho:
                jugadorO['x'] += MOVE
            if m_arriba:
                jugadorO['y'] -= MOVE
            if m_abajo:
                jugadorO['y'] += MOVE
            # Debido a que la variable playerObj ['rebote'] solo debe estar en el rango de 0 a BOUNCERATE ,
            # si al incrementarla es mayor que BOUNCERATE , debe restablecerse nuevamente a 0
            if (m_izquierdo or m_derecho or m_arriba or m_abajo) or jugadorO['bounce'] != 0:
                jugadorO['bounce'] += 1
            if jugadorO['bounce'] > REBOTE_R:  # la ardilla jugador está al final del rebote.
                jugadorO['bounce'] = 0  # restablecer la cantidad de rebote
            # comer o ser comido
            # comprueba si el jugador ha chocado con algun enemigo
            for i in range(len(enemigo) - 1, -1,
                           -1):  # el código dentro de este bucle for puede terminar eliminando algunos de estos objetos del juego de ardilla enemiga (si la ardilla del jugador termina por comérselos)
                sqObj = enemigo[i]

                if 'rect' in sqObj and jugadorO['rect'].colliderect(sqObj['rect']):
                    # se ha producido una colisión de jugador / ardilla

                    if sqObj['width'] * sqObj['height'] <= jugadorO['size'] ** 2:
                        # jugador es más grande y se come la ardilla
                        jugadorO['size'] += int((sqObj['width'] * sqObj['height']) ** 0.2) + 1
                        del enemigo[i]

                        if jugadorO['facing'] == IZQUIERDA:
                            jugadorO['surface'] = pygame.transform.scale(JUGADOR_IMG,
                                                                         (jugadorO['size'], jugadorO['size']))
                        if jugadorO['facing'] == DERECHA:
                            jugadorO['surface'] = pygame.transform.scale(R_SQUIR_IMG,
                                                                         (jugadorO['size'], jugadorO['size']))

                        if jugadorO['size'] > T_GANAR:
                            winMode = True  # activa el  "modo ganador"

                    elif not invulnerableModo:
                        # jugador es más pequeño y recibe daño
                        invulnerableModo = True
                        invulnerableStartTime = time.time()
                        jugadorO['salud'] -= 1  # disminuye la salud del jugador en 1
                        if jugadorO['salud'] == 0:
                            gameOverMode = True  # activa el "modo de juego terminado"
                            gameOverStartTime = time.time()
        # El juego sobre la pantalla
        else:
            # juego ha terminado, muestra el texto "juego terminado"
            DISPLAYSURF.blit(gameOverSurf, gameOverRect)
            if time.time() - gameOverStartTime > TIEMPO_TXT_P:
                return  # finaliza el juego actual

        # verifica si el jugador ha ganado.
        if winMode:
            DISPLAYSURF.blit(winSurf, winRect)
            DISPLAYSURF.blit(winSurf2, winRect2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Dibujar un medidor gráfico de salud

def drawHealthMeter(currentHealth):
    for i in range(
            currentHealth):  # dibuja barras de salud rojas  #dibuja el rectángulo rojo relleno para la cantidad de salud que tiene el jugado
        pygame.draw.rect(DISPLAYSURF, ROJO, (15, 5 + (10 * VIDA_J) - i * 10, 20, 10))
    for i in range(
            VIDA_J):  # dibuja los contornos blancos #dibuja un rectángulo blanco sin relleno para toda la salud posible que el jugador podría tener
        pygame.draw.rect(DISPLAYSURF, BLANCO, (15, 5 + (10 * VIDA_J) - i * 10, 20, 10), 1)


# El Mismo de terminar () Función
def terminate():
    pygame.quit()
    sys.exit()


def getBounceAmount(currentBounce, bounceRate, bounceHeight):
    # Devuelve el número de píxeles a compensar en función del rebote.
    # BounceRate más grande significa un rebote más lento.
    # BounceHeight más alto significa un rebote más alto.
    # currentBounce siempre será menor que bounceRate
    return int(math.sin((math.pi / float(bounceRate)) * currentBounce) * bounceHeight)


def getRandomVelocity():
    speed = random.randint(MINV_A, MAXV_A)
    if random.randint(0, 1) == 0:
        return speed
    else:
        return -speed


# Encontrar un lugar para agregar nuevos enemigos y pasto
def getRandomOffCameraPos(camerax, cameray, objWidth, objHeight):
    # crea un Rect de la vista de cámara
    cameraRect = pygame.Rect(camerax, cameray, ADV, HDV)
    while True:
        x = random.randint(camerax - ADV, camerax + (2 * ADV))
        y = random.randint(cameray - HDV, cameray + (2 * HDV))
        # crea un objeto Rect con coordenadas aleatorias y usa colliderect ()
        # para asegurarse de que el borde derecho no esté en la vista de la cámara.
        objRect = pygame.Rect(x, y, objWidth, objHeight)
        if not objRect.colliderect(cameraRect):
            return x, y

#creacion de estructuras de datos de enmigos
def nuevo_e(camerax, cameray):
    sq = {}
    generalSize = random.randint(5, 25)
    multiplier = random.randint(1, 3)
    sq['width'] = (generalSize + random.randint(0, 10)) * multiplier
    sq['height'] = (generalSize + random.randint(0, 10)) * multiplier
    sq['x'], sq['y'] = getRandomOffCameraPos(camerax, cameray, sq['width'], sq['height'])
    sq['movex'] = getRandomVelocity()
    sq['movey'] = getRandomVelocity()
    #voltear la imagen de mario
    if sq['movex'] < 0:  # mario esta orientado hacia la izquierda
        sq['surface'] = pygame.transform.scale(JUGADOR_IMG, (sq['width'], sq['height']))
    else:  # mario esta mirando hacia la derecha
        sq['surface'] = pygame.transform.scale(R_SQUIR_IMG, (sq['width'], sq['height']))
    sq['bounce'] = 0
    sq['bouncerate'] = random.randint(10, 18)
    sq['bounceheight'] = random.randint(10, 50)
    return sq

#creando estructuras de pasto
def nuevo_p(camerax, cameray):
    gr = {}
    gr['grassImage'] = random.randint(0, len(PASTO_IMG) - 1)
    gr['width'] = PASTO_IMG[0].get_width()
    gr['height'] = PASTO_IMG[0].get_height()
    gr['x'], gr['y'] = getRandomOffCameraPos(camerax, cameray, gr['width'], gr['height'])
    gr['rect'] = pygame.Rect((gr['x'], gr['y'], gr['width'], gr['height']))
    return gr

#comprobando si esta afuera del area activa
def isOutsideActiveArea(camerax, cameray, obj):
    boundsLeftEdge = camerax - ADV #valor del borde izquierdo
    boundsTopEdge = cameray - HDV #valor del borde superior
    boundsRect = pygame.Rect(boundsLeftEdge, boundsTopEdge, ADV * 3, HDV * 3) #para el cancho y la antura
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not boundsRect.colliderect(objRect)


if __name__ == '__main__':
    main()
