"""
Commands - Patrón Command para encapsular operaciones del sistema.
Permite deshacer/rehacer acciones y mantener historial de operaciones.
Cada comando es una acción del dominio que se puede ejecutar y revertir.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from daos.daos import (
    PeliculaDAO, SalaDAO, AsientoDAO, FuncionDAO,
    ClienteDAO, ReservaDAO, TicketDAO
)
from vos.vos import (
    PeliculaVO, SalaVO, AsientoVO, FuncionVO,
    ClienteVO, ReservaVO, TicketVO
)

# ─── Interfaz base ────────────────────────────────────────────────────────────

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# ─── Commands de Película ─────────────────────────────────────────────────────

class CrearPeliculaCommand(Command):
    def __init__(self, dao: PeliculaDAO, vo: PeliculaVO):
        self._dao = dao
        self._vo = vo

    def execute(self) -> PeliculaVO:
        return self._dao.create(self._vo)

    def undo(self):
        if self._vo.id_pelicula:
            self._dao.delete(self._vo.id_pelicula)


class EliminarPeliculaCommand(Command):
    def __init__(self, dao: PeliculaDAO, id_pelicula: int):
        self._dao = dao
        self._id = id_pelicula
        self._backup: Optional[PeliculaVO] = None

    def execute(self) -> bool:
        self._backup = self._dao.get_by_id(self._id)
        return self._dao.delete(self._id)

    def undo(self):
        if self._backup:
            self._dao.create(self._backup)


class ActualizarPeliculaCommand(Command):
    def __init__(self, dao: PeliculaDAO, nuevo_vo: PeliculaVO):
        self._dao = dao
        self._nuevo = nuevo_vo
        self._anterior: Optional[PeliculaVO] = None

    def execute(self) -> bool:
        self._anterior = self._dao.get_by_id(self._nuevo.id_pelicula)
        return self._dao.update(self._nuevo)

    def undo(self):
        if self._anterior:
            self._dao.update(self._anterior)


# ─── Commands de Función ──────────────────────────────────────────────────────

class CrearFuncionCommand(Command):
    def __init__(self, dao: FuncionDAO, vo: FuncionVO):
        self._dao = dao
        self._vo = vo

    def execute(self) -> FuncionVO:
        return self._dao.create(self._vo)

    def undo(self):
        if self._vo.id_funcion:
            self._dao.delete(self._vo.id_funcion)


class EliminarFuncionCommand(Command):
    def __init__(self, dao: FuncionDAO, id_funcion: int):
        self._dao = dao
        self._id = id_funcion
        self._backup: Optional[FuncionVO] = None

    def execute(self) -> bool:
        self._backup = self._dao.get_by_id_eager(self._id)
        return self._dao.delete(self._id)

    def undo(self):
        if self._backup:
            restore = FuncionVO(
                fecha=self._backup.fecha,
                hora=self._backup.hora,
                precio_base=self._backup.precio_base,
                id_pelicula=self._backup.id_pelicula,
                id_sala=self._backup.id_sala,
            )
            self._dao.create(restore)


# ─── Commands de Reserva (caso de uso principal) ──────────────────────────────

class CrearReservaCommand(Command):
    """
    Crea una reserva completa: reserva + múltiples tickets.
    Composición: La reserva CONTIENE tickets (no existen sin ella).
    """
    def __init__(
        self,
        reserva_dao: ReservaDAO,
        ticket_dao: TicketDAO,
        asiento_dao: AsientoDAO,
        cliente_vo: ClienteVO,
        funcion_vo: FuncionVO,
        asientos_seleccionados: List[AsientoVO],
    ):
        self._reserva_dao = reserva_dao
        self._ticket_dao = ticket_dao
        self._asiento_dao = asiento_dao
        self._cliente = cliente_vo
        self._funcion = funcion_vo
        self._asientos = asientos_seleccionados
        self._reserva_creada: Optional[ReservaVO] = None
        self._tickets_creados: List[TicketVO] = []

    def execute(self) -> ReservaVO:
        subtotal = self._funcion.precio_base
        total = subtotal * len(self._asientos)

        reserva_vo = ReservaVO(
            fecha_compra=str(date.today()),
            total=total,
            cedula_cliente=self._cliente.cedula,
            cliente=self._cliente,
        )
        self._reserva_creada = self._reserva_dao.create(reserva_vo)

        for asiento in self._asientos:
            ticket_vo = TicketVO(
                subtotal=subtotal,
                id_reserva=self._reserva_creada.id_reserva,
                id_funcion=self._funcion.id_funcion,
                id_asiento=asiento.id_asiento,
                funcion=self._funcion,
                asiento=asiento,
            )
            t = self._ticket_dao.create(ticket_vo)
            self._tickets_creados.append(t)
            # Marcar asiento como ocupado
            self._asiento_dao.update_estado(asiento.id_asiento, "ocupado")

        return self._reserva_creada

    def undo(self):
        """Cancela la reserva: elimina tickets y libera asientos."""
        if self._reserva_creada:
            self._ticket_dao.delete_by_reserva(self._reserva_creada.id_reserva)
            for asiento in self._asientos:
                self._asiento_dao.update_estado(asiento.id_asiento, "disponible")
            self._reserva_dao.delete(self._reserva_creada.id_reserva)
            self._reserva_creada = None
            self._tickets_creados = []


class CancelarReservaCommand(Command):
    """Cancela una reserva existente y libera los asientos."""
    def __init__(self, reserva_dao: ReservaDAO, ticket_dao: TicketDAO,
                 asiento_dao: AsientoDAO, id_reserva: int):
        self._reserva_dao = reserva_dao
        self._ticket_dao = ticket_dao
        self._asiento_dao = asiento_dao
        self._id_reserva = id_reserva
        self._reserva_backup: Optional[ReservaVO] = None
        self._tickets_backup: List[TicketVO] = []

    def execute(self) -> bool:
        self._reserva_backup = self._reserva_dao.get_by_id_eager(self._id_reserva)
        self._tickets_backup = self._ticket_dao.get_by_reserva_eager(self._id_reserva)
        for t in self._tickets_backup:
            self._asiento_dao.update_estado(t.id_asiento, "disponible")
        self._ticket_dao.delete_by_reserva(self._id_reserva)
        return self._reserva_dao.delete(self._id_reserva)

    def undo(self):
        if self._reserva_backup:
            nueva = ReservaVO(
                fecha_compra=self._reserva_backup.fecha_compra,
                total=self._reserva_backup.total,
                cedula_cliente=self._reserva_backup.cedula_cliente,
            )
            self._reserva_dao.create(nueva)
            for t in self._tickets_backup:
                nuevo_t = TicketVO(
                    subtotal=t.subtotal,
                    id_reserva=nueva.id_reserva,
                    id_funcion=t.id_funcion,
                    id_asiento=t.id_asiento,
                )
                self._ticket_dao.create(nuevo_t)
                self._asiento_dao.update_estado(t.id_asiento, "ocupado")


# ─── Commands de Cliente ──────────────────────────────────────────────────────

class CrearClienteCommand(Command):
    def __init__(self, dao: ClienteDAO, vo: ClienteVO):
        self._dao = dao
        self._vo = vo

    def execute(self) -> ClienteVO:
        return self._dao.create(self._vo)

    def undo(self):
        self._dao.delete(self._vo.cedula)


class ActualizarClienteCommand(Command):
    def __init__(self, dao: ClienteDAO, nuevo_vo: ClienteVO):
        self._dao = dao
        self._nuevo = nuevo_vo
        self._anterior: Optional[ClienteVO] = None

    def execute(self) -> bool:
        self._anterior = self._dao.get_by_cedula(self._nuevo.cedula)
        return self._dao.update(self._nuevo)

    def undo(self):
        if self._anterior:
            self._dao.update(self._anterior)


# ─── Commands de Sala ─────────────────────────────────────────────────────────

class CrearSalaCommand(Command):
    def __init__(self, dao: SalaDAO, vo: SalaVO):
        self._dao = dao
        self._vo = vo

    def execute(self) -> SalaVO:
        return self._dao.create(self._vo)

    def undo(self):
        if self._vo.id_sala:
            self._dao.delete(self._vo.id_sala)
