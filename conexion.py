import sqlite3
from PyQt5 import QtSql, QtWidgets

class Conexion:
    def create_db(filename):
        try:
            con = sqlite3.connect(database=filename)
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS puntuacion (id INTEGER NOT NULL, '
                        'puntos INTEGER NOT NULL, PRIMARY KEY (id AUTOINCREMENT))')
            con.commit()
        except Exception as error:
            print('Base de datos no creada ', error)

    def db_connect(filedb):
        try:
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(filedb)
            if not db.open():
                QtWidgets.QMessageBox.critical(None,
                                               "No se puede abrir la base de alta.\n Haz clic para continuar",
                                               QtWidgets.QMessageBox.Cancel)
                return False
            else:
                print("Conexión establecida")
                return True
        except Exception as error:
            print('Problemas en la conexión', error)

    def guardar(puntos):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into puntuacion (puntos) VALUES (:puntos)')
            query.bindValue(':puntos', puntos)

            if query.exec_():
                print('Puntuación guardada')
            else:
                print('Puntuación NO guardada')

        except Exception as error:
            print('Problemas al guardar la puntuación ', error)

    def mayor():
        try:
            pppp = []
            query = QtSql.QSqlQuery()
            query.prepare('SELECT MAX(puntos) FROM puntuacion')

            if query.exec_():
                while query.next():
                    pppp.append(query.value(0))
                p = pppp[0]
                return p
                print('Dalle jas')
            else:
                print('PPPP')

        except Exception as error:
            print('Problemas para devolver la puntuacione más alta ', error)
