from daos.models import db, Pelicula, Sala, Asiento, Funcion, Cliente
from seeders.providers import SeedDataProvider

class DatabaseSeeder:
    """
    Seeder principal de la base de datos utilizando Inyección de Dependencias.
    Recibe la fuente de datos a través de `provider`.
    """
    def __init__(self, provider: SeedDataProvider):
        self.provider = provider

    def seed(self):
        """Ejecuta el poblado de base de datos usando el provider inyectado."""
        db.connect(reuse_if_open=True)
        
        self._seed_peliculas()
        self._seed_salas()
        self._seed_funciones()
        self._seed_clientes()

    def _seed_peliculas(self):
        for p_data in self.provider.get_peliculas():
            # Inserción idempotente: verifica que no exista
            if not Pelicula.select().where(Pelicula.titulo == p_data["titulo"]).exists():
                Pelicula.create(**p_data)

    def _seed_salas(self):
        for s_data in self.provider.get_salas():
            if not Sala.select().where(Sala.numero == s_data["numero"]).exists():
                s = Sala.create(
                    numero=s_data["numero"], 
                    capacidad=s_data["capacidad"], 
                    tipo_pantalla=s_data["tipo_pantalla"]
                )
                
                # Crear asientos de la sala
                filas = s_data.get("filas", [])
                cols = s_data.get("cols", 0)
                for fila in filas:
                    for col in range(1, cols + 1):
                        Asiento.create(fila=fila, columna=str(col), id_sala=s)

    def _seed_funciones(self):
        for f_data in self.provider.get_funciones():
            try:
                # Buscar relaciones
                p = Pelicula.get(Pelicula.titulo == f_data["titulo_pelicula"])
                s = Sala.get(Sala.numero == f_data["numero_sala"])
                
                # Prevenir duplicados (idempotencia)
                exists = Funcion.select().where(
                    (Funcion.fecha == f_data["fecha"]) & 
                    (Funcion.hora == f_data["hora"]) & 
                    (Funcion.id_pelicula == p) & 
                    (Funcion.id_sala == s)
                ).exists()

                if not exists:
                    Funcion.create(
                        fecha=f_data["fecha"],
                        hora=f_data["hora"],
                        precio_base=f_data["precio_base"],
                        id_pelicula=p,
                        id_sala=s
                    )
            except Exception as e:
                # Log opcional si no encuentra relaciones
                pass

    def _seed_clientes(self):
        for c_data in self.provider.get_clientes():
            if not Cliente.select().where(Cliente.cedula == c_data["cedula"]).exists():
                Cliente.create(**c_data)
