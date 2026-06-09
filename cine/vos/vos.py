"""
Value Objects (VOs) - Representaciones de datos del dominio del negocio.
Estos objetos son inmutables y representan el estado de las entidades.
"""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date, time


@dataclass
class PeliculaVO:
    titulo: str
    duracion: str          # time en formato HH:MM:SS
    clasificacion: str
    genero: str
    id_pelicula: Optional[int] = None

    def __str__(self):
        return f"{self.titulo} ({self.clasificacion}) - {self.duracion}"


@dataclass
class SalaVO:
    numero: int
    capacidad: int
    tipo_pantalla: str
    id_sala: Optional[int] = None

    def __str__(self):
        return f"Sala {self.numero} - {self.tipo_pantalla} (cap: {self.capacidad})"


@dataclass
class AsientoVO:
    fila: str
    columna: str
    id_sala: int
    estado: str = "disponible"   # disponible | ocupado
    id_asiento: Optional[int] = None

    def __str__(self):
        return f"{self.fila}{self.columna} ({self.estado})"


@dataclass
class FuncionVO:
    fecha: str             # date en formato YYYY-MM-DD
    hora: str              # time en formato HH:MM:SS
    precio_base: float
    id_pelicula: int
    id_sala: int
    id_funcion: Optional[int] = None
    # Eager loading: objetos relacionados opcionales
    pelicula: Optional[PeliculaVO] = None
    sala: Optional[SalaVO] = None

    def __str__(self):
        titulo = self.pelicula.titulo if self.pelicula else f"Película #{self.id_pelicula}"
        return f"{titulo} - {self.fecha} {self.hora} (${self.precio_base:.2f})"


@dataclass
class ClienteVO:
    cedula: str
    nombre: str
    correo: str

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"


@dataclass
class ReservaVO:
    fecha_compra: str      # date en formato YYYY-MM-DD
    total: float
    cedula_cliente: str
    id_reserva: Optional[int] = None
    # Eager loading: cliente relacionado
    cliente: Optional[ClienteVO] = None
    # Lazy loading: tickets se cargan bajo demanda
    _tickets: Optional[List] = field(default=None, repr=False)

    def __str__(self):
        nombre = self.cliente.nombre if self.cliente else self.cedula_cliente
        return f"Reserva #{self.id_reserva} - {nombre} (${self.total:.2f})"


@dataclass
class TicketVO:
    subtotal: float
    id_reserva: int
    id_funcion: int
    id_asiento: int
    id_ticket: Optional[int] = None
    # Eager loading opcionales
    funcion: Optional[FuncionVO] = None
    asiento: Optional[AsientoVO] = None
    reserva: Optional[ReservaVO] = None

    def __str__(self):
        return f"Ticket #{self.id_ticket} - ${self.subtotal:.2f}"
