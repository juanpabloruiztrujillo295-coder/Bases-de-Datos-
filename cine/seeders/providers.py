from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SeedDataProvider(ABC):
    """
    Interfaz/Contrato para los proveedores de datos iniciales.
    Permite implementar Inyección de Dependencias en el Seeder.
    """
    @abstractmethod
    def get_peliculas(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_salas(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_funciones(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_clientes(self) -> List[Dict[str, Any]]:
        pass


class DefaultDataProvider(SeedDataProvider):
    """
    Proveedor de datos por defecto para inicializar la base de datos vacía.
    """
    def get_peliculas(self) -> List[Dict[str, Any]]:
        return [
            {"titulo": "Inception", "duracion": "02:28:00", "clasificacion": "PG-13", "genero": "Ciencia Ficción"},
            {"titulo": "The Dark Knight", "duracion": "02:32:00", "clasificacion": "PG-13", "genero": "Acción"},
            {"titulo": "Interstellar", "duracion": "02:49:00", "clasificacion": "PG-13", "genero": "Ciencia Ficción"},
            {"titulo": "Joker", "duracion": "02:02:00", "clasificacion": "R", "genero": "Drama"},
            {"titulo": "Avengers: Endgame", "duracion": "03:01:00", "clasificacion": "PG-13", "genero": "Acción"},
            {"titulo": "The Matrix", "duracion": "02:16:00", "clasificacion": "R", "genero": "Ciencia Ficción"},
            {"titulo": "The Godfather", "duracion": "02:55:00", "clasificacion": "R", "genero": "Drama"},
            {"titulo": "Pulp Fiction", "duracion": "02:34:00", "clasificacion": "R", "genero": "Crimen"},
            {"titulo": "Spider-Man: No Way Home", "duracion": "02:28:00", "clasificacion": "PG-13", "genero": "Acción"},
            {"titulo": "Coco", "duracion": "01:45:00", "clasificacion": "PG", "genero": "Animación"},
        ]

    def get_salas(self) -> List[Dict[str, Any]]:
        return [
            {"numero": 1, "capacidad": 20, "tipo_pantalla": "IMAX", "filas": ["A", "B", "C", "D"], "cols": 5},
            {"numero": 2, "capacidad": 15, "tipo_pantalla": "3D", "filas": ["A", "B", "C"], "cols": 5},
            {"numero": 3, "capacidad": 12, "tipo_pantalla": "Estándar", "filas": ["A", "B", "C"], "cols": 4},
        ]

    def get_funciones(self) -> List[Dict[str, Any]]:
        return [
            {"fecha": "2025-06-01", "hora": "14:00:00", "precio_base": 18000, "titulo_pelicula": "Inception", "numero_sala": 1},
            {"fecha": "2025-06-01", "hora": "17:30:00", "precio_base": 20000, "titulo_pelicula": "The Dark Knight", "numero_sala": 1},
            {"fecha": "2025-06-02", "hora": "15:00:00", "precio_base": 18000, "titulo_pelicula": "Interstellar", "numero_sala": 2},
            {"fecha": "2025-06-02", "hora": "19:00:00", "precio_base": 22000, "titulo_pelicula": "Joker", "numero_sala": 3},
            {"fecha": "2025-06-03", "hora": "16:00:00", "precio_base": 25000, "titulo_pelicula": "Avengers: Endgame", "numero_sala": 1},
            {"fecha": "2025-06-04", "hora": "18:00:00", "precio_base": 21000, "titulo_pelicula": "The Matrix", "numero_sala": 1},
            {"fecha": "2025-06-04", "hora": "21:00:00", "precio_base": 20000, "titulo_pelicula": "The Godfather", "numero_sala": 2},
            {"fecha": "2025-06-05", "hora": "19:30:00", "precio_base": 20000, "titulo_pelicula": "Pulp Fiction", "numero_sala": 3},
            {"fecha": "2025-06-05", "hora": "15:00:00", "precio_base": 18000, "titulo_pelicula": "Spider-Man: No Way Home", "numero_sala": 1},
            {"fecha": "2025-06-06", "hora": "14:00:00", "precio_base": 15000, "titulo_pelicula": "Coco", "numero_sala": 2},
        ]

    def get_clientes(self) -> List[Dict[str, Any]]:
        return [
            {"cedula": "1001234567", "nombre": "Carlos Ramírez", "correo": "carlos@email.com"},
            {"cedula": "1009876543", "nombre": "María López", "correo": "maria@email.com"},
            {"cedula": "1020304050", "nombre": "Ana Martínez", "correo": "ana.m@email.com"},
            {"cedula": "1098765432", "nombre": "Luis Gómez", "correo": "luis.g@email.com"},
            {"cedula": "1122334455", "nombre": "Sofía Castro", "correo": "sofia.c@email.com"},
        ]

class ExtraDataProvider(SeedDataProvider):
    """
    Proveedor para datos adicionales (para demostrar inyección dinámica o seed_more).
    """
    def get_peliculas(self) -> List[Dict[str, Any]]:
        return [
            {"titulo": "The Matrix", "duracion": "02:16:00", "clasificacion": "R", "genero": "Ciencia Ficción"},
            {"titulo": "The Godfather", "duracion": "02:55:00", "clasificacion": "R", "genero": "Drama"},
            {"titulo": "Pulp Fiction", "duracion": "02:34:00", "clasificacion": "R", "genero": "Crimen"},
            {"titulo": "Spider-Man: No Way Home", "duracion": "02:28:00", "clasificacion": "PG-13", "genero": "Acción"},
            {"titulo": "Coco", "duracion": "01:45:00", "clasificacion": "PG", "genero": "Animación"},
        ]

    def get_salas(self) -> List[Dict[str, Any]]:
        return []

    def get_funciones(self) -> List[Dict[str, Any]]:
        return [
            {"fecha": "2025-06-04", "hora": "18:00:00", "precio_base": 21000, "titulo_pelicula": "The Matrix", "numero_sala": 1},
            {"fecha": "2025-06-04", "hora": "21:00:00", "precio_base": 20000, "titulo_pelicula": "The Godfather", "numero_sala": 2},
            {"fecha": "2025-06-05", "hora": "19:30:00", "precio_base": 20000, "titulo_pelicula": "Pulp Fiction", "numero_sala": 3},
            {"fecha": "2025-06-05", "hora": "15:00:00", "precio_base": 18000, "titulo_pelicula": "Spider-Man: No Way Home", "numero_sala": 1},
            {"fecha": "2025-06-06", "hora": "14:00:00", "precio_base": 15000, "titulo_pelicula": "Coco", "numero_sala": 2},
        ]

    def get_clientes(self) -> List[Dict[str, Any]]:
        return [
            {"cedula": "1020304050", "nombre": "Ana Martínez", "correo": "ana.m@email.com"},
            {"cedula": "1098765432", "nombre": "Luis Gómez", "correo": "luis.g@email.com"},
            {"cedula": "1122334455", "nombre": "Sofía Castro", "correo": "sofia.c@email.com"},
        ]
