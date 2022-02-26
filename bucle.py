import pygame, os, random
from pygame import mixer

import conexion


pygame.font.init()

# Recursos
LETRAS = 'rec/Gameplay.ttf'
NEGRO, BLANCO = (0,0,0), (255,255,255)
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode(((ANCHO, ALTO)))
NAVE_JUGADOR = pygame.image.load(os.path.join("img", "nave.png"))
NAVE_ENEM1 = pygame.image.load(os.path.join("img", "ufo.png"))
NAVE_ENEM2 = pygame.image.load(os.path.join("img", "ufo2.png"))
NAVE_ENEM3 = pygame.image.load(os.path.join("img", "spaceship.png"))
NAVE_JEFE = pygame.image.load(os.path.join("img", "ms2.png"))
BALA = pygame.image.load(os.path.join("img", "bala.png"))
BALA_ENEMIGO = pygame.image.load(os.path.join("img", "bomb.png"))
FONDO = pygame.image.load(os.path.join("img", "espacio.jpg"))
ICON = pygame.image.load(os.path.join("img", 'weed.png'))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def dibujar(self, ventana):
        ventana.blit(self.img, (self.x, self.y))

    def mover(self, vel):
        self.y += vel

    def fuera(self, altura):
        return not(self.y <= altura and self.y >= 0)

    def colision(self, obj):
        return choca(self, obj)

class Nave:
    ENFRIAMIENTO = 30

    def __init__(self, x, y, vida=100):
        self.x = x
        self.y = y
        self.vida = vida
        self.img_nave = None
        self.img_bala = None
        self.balas = []
        self.contador_enfriamiento = 0

    def dibujar(self, ventana):
        ventana.blit(self.img_nave, (self.x, self.y))
        for bala in self.balas:
            bala.dibujar(ventana)

    def mover_balas(self, vel, obj):
        self.enfriamiento()
        for bala in self.balas:
            bala.mover(vel)
            if bala.fuera(ALTO):
                self.balas.remove(bala)
            elif bala.colision(obj):
                obj.vida -= 10
                self.balas.remove(bala)

    def enfriamiento(self):
        if self.contador_enfriamiento >= self.ENFRIAMIENTO:
            self.contador_enfriamiento = 0
        elif self.contador_enfriamiento > 0:
            self.contador_enfriamiento += 1

    def disparar(self):
        if self.contador_enfriamiento == 0:
            bala = Laser(self.x, self.y, self.img_bala)
            self.balas.append(bala)
            self.contador_enfriamiento = 1

    def get_ancho(self):
        return self.img_nave.get_width()

    def get_alto(self):
        return self.img_nave.get_height()

class Jugador(Nave):
    def __init__(self, x, y, vida=30):
        super().__init__(x, y, vida)
        self.img_nave = NAVE_JUGADOR
        self.img_bala = BALA
        self.mask = pygame.mask.from_surface(self.img_nave)
        self.vida_max = vida

    def disparar(self):
        if self.contador_enfriamiento == 0:
            bala = Laser(self.x+16, self.y, self.img_bala)
            self.balas.append(bala)
            self.contador_enfriamiento = 1
            # IMPORTANTE -> Sonidos y música .wav porque .mp3 y otros formatos dan problemas
            bala_sonido = pygame.mixer.Sound('sonido/pew.wav')
            bala_sonido.play()

    def dibujar(self, ventana):
        super().dibujar(ventana)
        self.barraVida(ventana)

    def barraVida(self, ventana):
        pygame.draw.rect(ventana, (255,0,0), (self.x, self.y + self.img_nave.get_height() + 10, self.img_nave.get_width(), 10))
        pygame.draw.rect(ventana, (0,255,0), (self.x, self.y + self.img_nave.get_height() + 10, self.img_nave.get_width() * (self.vida/self.vida_max), 10))

class Enemigo(Nave):
    # TODO -> Cambiar patrones para cada enemigo
    ENEMIGOS = {
                "enem1": (NAVE_ENEM1, BALA_ENEMIGO),
                "enem2": (NAVE_ENEM2, BALA_ENEMIGO),
                "enem3": (NAVE_ENEM3, BALA_ENEMIGO)
                }

    def __init__(self, x, y, color, vida=100):
        super().__init__(x, y, vida)
        self.img_nave, self.img_bala = self.ENEMIGOS[color]
        self.mask = pygame.mask.from_surface(self.img_nave)

    # TODO -> hacer que se muevan a los lados
    def mover(self, vel):
        self.y += vel

    def disparar(self):
        if self.contador_enfriamiento == 0:
            bala = Laser(self.x+16, self.y, self.img_bala)
            self.balas.append(bala)
            self.contador_enfriamiento = 1

def choca(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def bucle_juego():
    corriendo = True
    FPS = 60
    nivel = 0
    vidas = 5
    puntos = 0
    texto = pygame.font.SysFont(LETRAS, 50)
    texto_perder = pygame.font.SysFont(LETRAS, 60)

    enemigos = []
    enemigos_por_oleada = 5
    vel_enemigo = 1

    vel_jugador = 5
    vel_bala = 5

    jugador = Jugador(370, 480)

    reloj = pygame.time.Clock()

    perder = False
    contador_perdida = 0

    # Música de fondo
    MUSICA = pygame.mixer.music.load('musica/music.wav')
    pygame.mixer.music.play(loops=-1)

    def redibujar_ventana():
        VENTANA.blit(FONDO, (0,0))

        num_vidas = texto.render(f"Vidas: {vidas}", 1, (255,255,255))
        num_nivel = texto.render(f"Nivel: {nivel}", 1, (255, 255, 255))
        num_puntos = texto.render(f"Puntos: {puntos}", 1, (255, 255, 255))

        VENTANA.blit(num_vidas, (10, 10))
        VENTANA.blit(num_nivel, (ANCHO - num_nivel.get_width() - 10, 10))
        VENTANA.blit(num_puntos, (10, 40))

        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)

        jugador.dibujar(VENTANA)

        if perder:
            perdida = texto_perder.render("Perdiste", 1, (255,255,255))
            VENTANA.blit(perdida, (ANCHO/2 - perdida.get_width()/2, 350))

        pygame.display.update()

    while corriendo:
        reloj.tick(FPS)
        redibujar_ventana()

        if vidas <= 0 or jugador.vida <= 0:
            perder = True
            contador_perdida += 1

        if perder:
            if contador_perdida > FPS * 3:
                pygame.mixer.music.stop()
                conexion.Conexion.guardar(puntos)
                corriendo = False
            else:
                continue

        if len(enemigos) == 0:
            nivel += 1
            enemigos_por_oleada += 5
            for i in range(enemigos_por_oleada):
                enemigo = Enemigo(random.randrange(50, ANCHO-100), random.randrange(-1500, -100), random.choice(["enem1", "enem2", "enem3"]))
                enemigos.append(enemigo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a] and jugador.x - vel_jugador > 0:
            jugador.x -= vel_jugador
        if teclas[pygame.K_d] and jugador.x + vel_jugador + jugador.get_ancho() < ANCHO:
            jugador.x += vel_jugador
        if teclas[pygame.K_w] and jugador.y - vel_jugador > 0:
            jugador.y -= vel_jugador
        if teclas[pygame.K_s] and jugador.y + vel_jugador + jugador.get_alto() + 15 < ALTO:
            jugador.y += vel_jugador
        if teclas[pygame.K_SPACE]:
            jugador.disparar()

        for enemigo in enemigos[:]:
            enemigo.mover(vel_enemigo)
            enemigo.mover_balas(vel_bala, jugador)

            if random.randrange(0, 2*60) == 1:
                enemigo.disparar()

            if choca(enemigo, jugador):
                jugador.vida -= 10
                golpe = mixer.Sound('sonido/a.wav')
                golpe.play()
                puntos += 3
                enemigos.remove(enemigo)
            elif enemigo.y + enemigo.get_alto() > ALTO:
                vidas -= 1
                enemigos.remove(enemigo)

        #jugador.mover_balas(-vel_bala, enemigos)
        # Problema con puntos, por eso moví el método mover_balas aquí
        jugador.enfriamiento()
        for bala in jugador.balas:
            bala.mover(-vel_bala)
            if bala.fuera(ALTO):
                jugador.balas.remove(bala)
            else:
                for obj in enemigos:
                    if bala.colision(obj):
                        golpe = mixer.Sound('sonido/a.wav')
                        golpe.play()
                        puntos += 5
                        enemigos.remove(obj)
                        if bala in jugador.balas:
                            jugador.balas.remove(bala)