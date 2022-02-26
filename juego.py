import pygame

pygame.font.init()
import menu
from menu import *
from bucle import *

# Recursos
LETRAS = 'rec/Gameplay.ttf'
NEGRO, BLANCO = (0,0,0), (255,255,255)
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode(((ANCHO, ALTO)))
ICON = pygame.image.load(os.path.join("img", 'weed.png'))

class Juego():
    def __init__(self):
        pygame.init()

        # Variables de estado y teclas
        self.CORRIENDO, self.JUGANDO, self.PERDIDO = True, False, False
        self.ARRIBA, self.ABAJO, self.ENTER, self.BACK = False, False, False, False

        # Ajustes de la pantalla
        self.ANCHO, self.ALTO = 800, 600
        self.DISPLAY = pygame.Surface((ANCHO, ALTO))
        self.VENTANA = pygame.display.set_mode(((ANCHO, ALTO)))
        pygame.display.set_caption("Juegaso")
        pygame.display.set_icon(ICON)

        # Menús
        self.MENU_PRINCIPAL = MenuPrincipal(self)
        self.CONTROLES = MenuControles(self)
        self.CREDITOS = MenuCreditos(self)
        self.PUNTOS = MenuPuntos(self)
        self.MENU_ACTUAL = self.MENU_PRINCIPAL

    def comprobar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.CORRIENDO, self.JUGANDO = False, False
                self.MENU_ACTUAL.RUN_DISPLAY = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.ENTER = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK = True
                if event.key == pygame.K_DOWN:
                    self.ABAJO = True
                if event.key == pygame.K_UP:
                    self.ARRIBA = True

    def resetear_teclas(self):
        self.ARRIBA, self.ABAJO, self.ENTER, self.BACK = False, False, False, False

    def escribir(self, texto, tamanho, x, y):
        letra = pygame.font.Font(LETRAS, tamanho)
        color = letra.render(texto, True, BLANCO)
        texto_rect = color.get_rect()
        texto_rect.center = (x, y)
        self.DISPLAY.blit(color, texto_rect)

    def bucle_juego():
        while self.JUGANDO:
            bucle.bucle_juego()