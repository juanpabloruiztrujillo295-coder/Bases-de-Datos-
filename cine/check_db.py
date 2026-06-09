from daos.models import db, Pelicula, Sala, Funcion, Cliente, Ticket
import os

def check_db():
    print(f"Checking database at {os.path.abspath('cine.db')}")
    try:
        db.connect()
        print(f"Peliculas: {Pelicula.select().count()}")
        print(f"Salas: {Sala.select().count()}")
        print(f"Funciones: {Funcion.select().count()}")
        print(f"Clientes: {Cliente.select().count()}")
    except Exception as e:
        print(f"Error checking DB: {e}")

if __name__ == '__main__':
    check_db()
