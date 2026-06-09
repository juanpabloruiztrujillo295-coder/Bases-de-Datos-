"""
Modelos ORM usando PeeWee.
Estos modelos mapean directamente a las tablas de la base de datos.
"""
from peewee import (
    Model, SqliteDatabase, AutoField, CharField, IntegerField,
    FloatField, DateField, TimeField, ForeignKeyField, TextField
)

db = SqliteDatabase("cine.db", pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class Pelicula(BaseModel):
    id_pelicula = AutoField()
    titulo = CharField(max_length=100)
    duracion = CharField(max_length=8)       # HH:MM:SS
    clasificacion = CharField(max_length=10)
    genero = CharField(max_length=30)

    class Meta:
        table_name = "pelicula"


class Sala(BaseModel):
    id_sala = AutoField()
    numero = IntegerField()
    capacidad = IntegerField()
    tipo_pantalla = CharField(max_length=20)

    class Meta:
        table_name = "sala"


class Asiento(BaseModel):
    id_asiento = AutoField()
    fila = CharField(max_length=10)
    columna = CharField(max_length=10)
    estado = CharField(max_length=15, default="disponible")
    id_sala = ForeignKeyField(Sala, backref="asientos", column_name="id_sala")

    class Meta:
        table_name = "asiento"


class Funcion(BaseModel):
    id_funcion = AutoField()
    fecha = DateField()
    hora = TimeField()
    precio_base = FloatField()
    id_pelicula = ForeignKeyField(Pelicula, backref="funciones", column_name="id_pelicula")
    id_sala = ForeignKeyField(Sala, backref="funciones", column_name="id_sala")

    class Meta:
        table_name = "funcion"


class Cliente(BaseModel):
    cedula = CharField(primary_key=True, max_length=20)
    nombre = CharField(max_length=50)
    correo = CharField(max_length=100)

    class Meta:
        table_name = "cliente"


class Reserva(BaseModel):
    id_reserva = AutoField()
    fecha_compra = DateField()
    total = FloatField()
    cedula_cliente = ForeignKeyField(Cliente, backref="reservas", column_name="cedula_cliente")

    class Meta:
        table_name = "reserva"


class Ticket(BaseModel):
    id_ticket = AutoField()
    subtotal = FloatField()
    id_reserva = ForeignKeyField(Reserva, backref="tickets", column_name="id_reserva")
    id_funcion = ForeignKeyField(Funcion, backref="tickets", column_name="id_funcion")
    id_asiento = ForeignKeyField(Asiento, backref="tickets", column_name="id_asiento")

    class Meta:
        table_name = "ticket"


TABLES = [Pelicula, Sala, Asiento, Funcion, Cliente, Reserva, Ticket]


def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables(TABLES, safe=True)



