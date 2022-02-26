import conexion
from juego import *

conexion.Conexion.create_db('puntuacion.sqlite')
conexion.Conexion.db_connect('puntuacion.sqlite')
j = Juego()

while j.CORRIENDO:
    j.MENU_ACTUAL.menu_display()

# if j.JUGANDO:
#     j.bucle_juego()
# if j.JUGANDO == False or j.PERDIDO:
#     menu.MenuPerder(j)