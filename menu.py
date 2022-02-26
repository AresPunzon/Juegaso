import pygame

import juego
import bucle
import conexion
from juego import *


class Menu():
    def __init__(self, juego):
        self.juego = juego
        self.ANCHO_MEDIO, self.ALTO_MEDIO = self.juego.ANCHO / 2, self.juego.ALTO / 2
        self.RUN_DISPLAY = True
        self.CURSOR = pygame.Rect(0, 0, 50, 50)
        self.OFFSET = -100

    def dibujar_cursor(self):
        self.juego.escribir('*', 15, self.CURSOR.x, self.CURSOR.y)

    def blit_pantalla(self):
        self.juego.VENTANA.blit(self.juego.DISPLAY, (0, 0))
        pygame.display.update()
        self.juego.resetear_teclas()


class MenuPrincipal(Menu):
    def __init__(self, juego):
        Menu.__init__(self, juego)
        self.ESTADO = 'Empezar'
        self.EMPEZARX, self.EMPEZARY = self.ANCHO_MEDIO, self.ALTO_MEDIO + 30
        self.PUNTOSX, self.PUNTOSY = self.ANCHO_MEDIO, self.ALTO_MEDIO + 50
        self.CONTROLESX, self.CONTROLESY = self.ANCHO_MEDIO, self.ALTO_MEDIO + 70
        self.CREDITOSX, self.CREDITOSY = self.ANCHO_MEDIO, self.ALTO_MEDIO + 90
        self.SALIRX, self.SALIRY = self.ANCHO_MEDIO, self.ALTO_MEDIO + 110
        self.CURSOR.midtop = (self.EMPEZARX + self.OFFSET, self.EMPEZARY)

    def menu_display(self):
        self.RUN_DISPLAY = True
        while self.RUN_DISPLAY:
            self.juego.comprobar_eventos()
            self.comprobar_input()
            self.juego.DISPLAY.fill(juego.NEGRO)
            self.juego.escribir('Menu Principal', 20, self.juego.ANCHO / 2, self.juego.ALTO / 2 - 20)
            self.juego.escribir('Jugar', 20, self.EMPEZARX, self.EMPEZARY)
            self.juego.escribir('Puntuacion maxima', 20, self.PUNTOSX, self.PUNTOSY)
            self.juego.escribir('Controles', 20, self.CONTROLESX, self.CONTROLESY)
            self.juego.escribir('Creditos', 20, self.CREDITOSX, self.CREDITOSY)
            self.juego.escribir('Salir', 20, self.SALIRX, self.SALIRY)
            self.dibujar_cursor()
            self.blit_pantalla()

    def mover_cursor(self):
        if self.juego.ABAJO:
            if self.ESTADO == 'Empezar':
                self.CURSOR.midtop = (self.PUNTOSX + self.OFFSET, self.PUNTOSY)
                self.ESTADO = 'Puntos'
            elif self.ESTADO == 'Puntos':
                self.CURSOR.midtop = (self.CONTROLESX + self.OFFSET, self.CONTROLESY)
                self.ESTADO = 'Controles'
            elif self.ESTADO == 'Controles':
                self.CURSOR.midtop = (self.CREDITOSX + self.OFFSET, self.CREDITOSY)
                self.ESTADO = 'Creditos'
            elif self.ESTADO == 'Creditos':
                self.CURSOR.midtop = (self.SALIRX + self.OFFSET, self.SALIRY)
                self.ESTADO = 'Salir'
            elif self.ESTADO == 'Salir':
                self.CURSOR.midtop = (self.EMPEZARX + self.OFFSET, self.EMPEZARY)
                self.ESTADO = 'Empezar'
        elif self.juego.ARRIBA:
            if self.ESTADO == 'Empezar':
                self.CURSOR.midtop = (self.SALIRX + self.OFFSET, self.SALIRY)
                self.ESTADO = 'Salir'
            elif self.ESTADO == 'Controles':
                self.CURSOR.midtop = (self.PUNTOSX + self.OFFSET, self.PUNTOSY)
                self.ESTADO = 'Puntos'
            elif self.ESTADO == 'Puntos':
                self.CURSOR.midtop = (self.EMPEZARX + self.OFFSET, self.EMPEZARY)
                self.ESTADO = 'Empezar'
            elif self.ESTADO == 'Creditos':
                self.CURSOR.midtop = (self.CONTROLESX + self.OFFSET, self.CONTROLESY)
                self.ESTADO = 'Controles'
            elif self.ESTADO == 'Salir':
                self.CURSOR.midtop = (self.CREDITOSX + self.OFFSET, self.CREDITOSY)
                self.ESTADO = 'Creditos'

    def comprobar_input(self):
        self.mover_cursor()
        if self.juego.ENTER:
            if self.ESTADO == 'Empezar':
                self.juego.JUGANDO = True
                bucle.bucle_juego()
            elif self.ESTADO == 'Puntos':
                self.juego.MENU_ACTUAL = self.juego.PUNTOS
            elif self.ESTADO == 'Controles':
                self.juego.MENU_ACTUAL = self.juego.CONTROLES
            elif self.ESTADO == 'Creditos':
                self.juego.MENU_ACTUAL = self.juego.CREDITOS
            elif self.ESTADO == 'Salir':
                self.juego.CORRIENDO = False
            self.RUN_DISPLAY = False

class MenuControles(Menu):
    def __init__(self, juego):
        Menu.__init__(self, juego)

    def menu_display(self):
        self.RUN_DISPLAY = True
        while self.RUN_DISPLAY:
            self.juego.comprobar_eventos()
            if self.juego.ENTER or self.juego.BACK:
                self.juego.MENU_ACTUAL = self.juego.MENU_PRINCIPAL
                self.RUN_DISPLAY = False
            self.juego.DISPLAY.fill(juego.NEGRO)
            self.juego.escribir('Controles', 20, self.juego.ANCHO / 2, self.juego.ALTO / 2 - 20)
            self.juego.escribir('WASD - Moverse', 15, self.juego.ANCHO / 2, self.juego.ALTO / 2 + 10)
            self.juego.escribir('Espacio - Disparar', 15, self.juego.ANCHO / 2, self.juego.ALTO / 2 + 30)
            self.blit_pantalla()


class MenuCreditos(Menu):
    def __init__(self, juego):
        Menu.__init__(self, juego)

    def menu_display(self):
        self.RUN_DISPLAY = True
        while self.RUN_DISPLAY:
            self.juego.comprobar_eventos()
            if self.juego.ENTER or self.juego.BACK:
                self.juego.MENU_ACTUAL = self.juego.MENU_PRINCIPAL
                self.RUN_DISPLAY = False
            self.juego.DISPLAY.fill(juego.NEGRO)
            self.juego.escribir('Creditos', 20, self.juego.ANCHO / 2, self.juego.ALTO / 2 - 20)
            self.juego.escribir('Ares Punzon Garcia', 15, self.juego.ANCHO / 2, self.juego.ALTO / 2 + 10)
            self.blit_pantalla()

class MenuPuntos(Menu):
    def __init__(self, juego):
        Menu.__init__(self, juego)

    def menu_display(self):
        self.RUN_DISPLAY = True
        self.pppp = str(conexion.Conexion.mayor())
        print(self.pppp)
        while self.RUN_DISPLAY:
            self.juego.comprobar_eventos()
            if self.juego.ENTER or self.juego.BACK:
                self.juego.MENU_ACTUAL = self.juego.MENU_PRINCIPAL
                self.RUN_DISPLAY = False
            self.juego.DISPLAY.fill(juego.NEGRO)
            self.juego.escribir('Puntuacion mas alta', 20, self.juego.ANCHO / 2, self.juego.ALTO / 2 - 20)
            self.juego.escribir(self.pppp, 15, self.juego.ANCHO / 2, self.juego.ALTO / 2 + 10)
            self.blit_pantalla()

class MenuNombre(Menu):
    def __init__(self, juego):
        Menu.__init__(self, juego)

    def cambiar_pantalla(self):
        self.juego.PERDIDO = True
        self.juego.MENU_ACTUAL = self.juego.PUNTOS

    def menu_display(self):
        self.RUN_DISPLAY = True
        while self.RUN_DISPLAY:
            nombre = ''
            len(nombre)
            self.juego.comprobar_eventos()
            if self.juego.ENTER:
                self.juego.MENU_ACTUAL = self.juego.MENU_PRINCIPAL
                self.RUN_DISPLAY = False
            self.juego.DISPLAY.fill(juego.NEGRO)
            self.juego.escribir('Nombre del jugador: ' + nombre, 15, self.juego.ANCHO / 2, self.juego.ALTO / 2 + 10)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if len(nombre) < 3:
                            nombre = nombre + 'a'
                    if event.key == pygame.K_b:
                        if len(nombre) < 3:
                            nombre.append('b')
                    if event.key == pygame.K_c:
                        if len(nombre) < 3:
                            nombre.append('c')
                    if event.key == pygame.K_d:
                        if len(nombre) < 3:
                            nombre.append('d')
                    if event.key == pygame.K_f:
                        if len(nombre) < 3:
                            nombre.append('f')
                    if event.key == pygame.K_g:
                        if len(nombre) < 3:
                            nombre.append('g')
                    if event.key == pygame.K_h:
                        if len(nombre) < 3:
                            nombre.append('h')
                    if event.key == pygame.K_i:
                        if len(nombre) < 3:
                            nombre.append('i')
                    if event.key == pygame.K_j:
                        if len(nombre) < 3:
                            nombre.append('j')
                    if event.key == pygame.K_k:
                        if len(nombre) < 3:
                            nombre.append('k')
                    if event.key == pygame.K_l:
                        if len(nombre) < 3:
                            nombre.append('l')
                    if event.key == pygame.K_m:
                        if len(nombre) < 3:
                            nombre.append('m')
                    if event.key == pygame.K_n:
                        if len(nombre) < 3:
                            nombre.append('n')
                    if event.key == pygame.K_o:
                        if len(nombre) < 3:
                            nombre.append('o')
                    if event.key == pygame.K_p:
                        if len(nombre) < 3:
                            nombre.append('p')
                    if event.key == pygame.K_q:
                        if len(nombre) < 3:
                            nombre.append('q')
                    if event.key == pygame.K_r:
                        if len(nombre) < 3:
                            nombre.append('r')
                    if event.key == pygame.K_s:
                        if len(nombre) < 3:
                            nombre.append('s')
                    if event.key == pygame.K_t:
                        if len(nombre) < 3:
                            nombre.append('t')
                    if event.key == pygame.K_u:
                        if len(nombre) < 3:
                            nombre.append('u')
                    if event.key == pygame.K_v:
                        if len(nombre) < 3:
                            nombre.append('v')
                    if event.key == pygame.K_w:
                        if len(nombre) < 3:
                            nombre.append('w')
                    if event.key == pygame.K_x:
                        if len(nombre) < 3:
                            nombre.append('x')
                    if event.key == pygame.K_y:
                        if len(nombre) < 3:
                            nombre.append('y')
                    if event.key == pygame.K_z:
                        if len(nombre) < 3:
                            nombre.append('z')
                    if event.key == pygame.K_BACKSPACE:
                        nombre = ''
            self.juego.escribir('Nombre del jugador: '+ nombre, 15, self.juego.ANCHO / 2, self.juego.ALTO / 2 + 10)
            self.blit_pantalla()
