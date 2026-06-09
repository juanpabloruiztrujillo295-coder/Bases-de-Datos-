"""
DAOs - Data Access Objects.
Encapsulan el acceso a la base de datos y convierten modelos ORM a VOs.
Se implementan tanto eager loading como lazy loading según el caso de uso.
"""
from typing import List, Optional
from daos.models import (
    Pelicula, Sala, Asiento, Funcion, Cliente, Reserva, Ticket, db
)
from vos.vos import (
    PeliculaVO, SalaVO, AsientoVO, FuncionVO, ClienteVO, ReservaVO, TicketVO
)


# ─── Mappers ORM → VO ────────────────────────────────────────────────────────

def _map_pelicula(p: Pelicula) -> PeliculaVO:
    return PeliculaVO(
        id_pelicula=p.id_pelicula,
        titulo=p.titulo,
        duracion=p.duracion,
        clasificacion=p.clasificacion,
        genero=p.genero,
    )

def _map_sala(s: Sala) -> SalaVO:
    return SalaVO(
        id_sala=s.id_sala,
        numero=s.numero,
        capacidad=s.capacidad,
        tipo_pantalla=s.tipo_pantalla,
    )

def _map_asiento(a: Asiento) -> AsientoVO:
    return AsientoVO(
        id_asiento=a.id_asiento,
        fila=a.fila,
        columna=a.columna,
        estado=a.estado,
        id_sala=a.id_sala_id,
    )

def _map_funcion(f: Funcion, eager=False) -> FuncionVO:
    vo = FuncionVO(
        id_funcion=f.id_funcion,
        fecha=str(f.fecha),
        hora=str(f.hora),
        precio_base=f.precio_base,
        id_pelicula=f.id_pelicula_id,
        id_sala=f.id_sala_id,
    )
    if eager:
        vo.pelicula = _map_pelicula(f.id_pelicula)
        vo.sala = _map_sala(f.id_sala)
    return vo

def _map_cliente(c: Cliente) -> ClienteVO:
    return ClienteVO(
        cedula=c.cedula,
        nombre=c.nombre,
        correo=c.correo,
    )

def _map_reserva(r: Reserva, eager=False) -> ReservaVO:
    vo = ReservaVO(
        id_reserva=r.id_reserva,
        fecha_compra=str(r.fecha_compra),
        total=r.total,
        cedula_cliente=r.cedula_cliente_id,
    )
    if eager:
        vo.cliente = _map_cliente(r.cedula_cliente)
    return vo

def _map_ticket(t: Ticket, eager=False) -> TicketVO:
    vo = TicketVO(
        id_ticket=t.id_ticket,
        subtotal=t.subtotal,
        id_reserva=t.id_reserva_id,
        id_funcion=t.id_funcion_id,
        id_asiento=t.id_asiento_id,
    )
    if eager:
        vo.funcion = _map_funcion(t.id_funcion, eager=True)
        vo.asiento = _map_asiento(t.id_asiento)
    return vo


# ─── PeliculaDAO ─────────────────────────────────────────────────────────────

class PeliculaDAO:
    def get_all(self) -> List[PeliculaVO]:
        return [_map_pelicula(p) for p in Pelicula.select()]

    def get_by_id(self, id_pelicula: int) -> Optional[PeliculaVO]:
        try:
            return _map_pelicula(Pelicula.get_by_id(id_pelicula))
        except Pelicula.DoesNotExist:
            return None

    def create(self, vo: PeliculaVO) -> PeliculaVO:
        p = Pelicula.create(
            titulo=vo.titulo,
            duracion=vo.duracion,
            clasificacion=vo.clasificacion,
            genero=vo.genero,
        )
        vo.id_pelicula = p.id_pelicula
        return vo

    def update(self, vo: PeliculaVO) -> bool:
        rows = (Pelicula.update(
            titulo=vo.titulo,
            duracion=vo.duracion,
            clasificacion=vo.clasificacion,
            genero=vo.genero,
        ).where(Pelicula.id_pelicula == vo.id_pelicula).execute())
        return rows > 0

    def delete(self, id_pelicula: int) -> bool:
        rows = Pelicula.delete().where(Pelicula.id_pelicula == id_pelicula).execute()
        return rows > 0


# ─── SalaDAO ─────────────────────────────────────────────────────────────────

class SalaDAO:
    def get_all(self) -> List[SalaVO]:
        return [_map_sala(s) for s in Sala.select()]

    def get_by_id(self, id_sala: int) -> Optional[SalaVO]:
        try:
            return _map_sala(Sala.get_by_id(id_sala))
        except Sala.DoesNotExist:
            return None

    def create(self, vo: SalaVO) -> SalaVO:
        s = Sala.create(numero=vo.numero, capacidad=vo.capacidad, tipo_pantalla=vo.tipo_pantalla)
        vo.id_sala = s.id_sala
        return vo

    def update(self, vo: SalaVO) -> bool:
        rows = Sala.update(
            numero=vo.numero, capacidad=vo.capacidad, tipo_pantalla=vo.tipo_pantalla
        ).where(Sala.id_sala == vo.id_sala).execute()
        return rows > 0

    def delete(self, id_sala: int) -> bool:
        return Sala.delete().where(Sala.id_sala == id_sala).execute() > 0


# ─── AsientoDAO ──────────────────────────────────────────────────────────────

class AsientoDAO:
    def get_by_sala(self, id_sala: int) -> List[AsientoVO]:
        """Eager loading: carga todos los asientos de una sala."""
        return [_map_asiento(a) for a in Asiento.select().where(Asiento.id_sala == id_sala)]

    def get_disponibles_funcion(self, id_funcion: int) -> List[AsientoVO]:
        """
        Lazy-loaded en contexto: obtiene asientos de la sala de la función
        que no tengan ticket asociado en esa función.
        Caso de uso: mostrar mapa de asientos al comprar.
        """
        funcion = Funcion.get_by_id(id_funcion)
        id_sala = funcion.id_sala_id
        ocupados_ids = (
            Ticket.select(Ticket.id_asiento)
            .where(Ticket.id_funcion == id_funcion)
        )
        asientos = (
            Asiento.select()
            .where(Asiento.id_sala == id_sala)
            .where(Asiento.id_asiento.not_in(ocupados_ids))
        )
        return [_map_asiento(a) for a in asientos]

    def get_by_id(self, id_asiento: int) -> Optional[AsientoVO]:
        try:
            return _map_asiento(Asiento.get_by_id(id_asiento))
        except Asiento.DoesNotExist:
            return None

    def create(self, vo: AsientoVO) -> AsientoVO:
        a = Asiento.create(fila=vo.fila, columna=vo.columna, estado=vo.estado, id_sala=vo.id_sala)
        vo.id_asiento = a.id_asiento
        return vo

    def update_estado(self, id_asiento: int, estado: str) -> bool:
        return Asiento.update(estado=estado).where(Asiento.id_asiento == id_asiento).execute() > 0

    def delete(self, id_asiento: int) -> bool:
        return Asiento.delete().where(Asiento.id_asiento == id_asiento).execute() > 0


# ─── FuncionDAO ──────────────────────────────────────────────────────────────

class FuncionDAO:
    def get_all_eager(self) -> List[FuncionVO]:
        """
        EAGER LOADING: Carga funciones con película y sala en una sola query.
        Caso de uso: listar cartelera con nombre de película y tipo de sala.
        """
        query = (
            Funcion.select(Funcion, Pelicula, Sala)
            .join(Pelicula)
            .switch(Funcion)
            .join(Sala)
        )
        return [_map_funcion(f, eager=True) for f in query]

    def get_by_id_eager(self, id_funcion: int) -> Optional[FuncionVO]:
        try:
            query = (
                Funcion.select(Funcion, Pelicula, Sala)
                .join(Pelicula)
                .switch(Funcion)
                .join(Sala)
                .where(Funcion.id_funcion == id_funcion)
            )
            return _map_funcion(query.get(), eager=True)
        except Funcion.DoesNotExist:
            return None

    def get_by_pelicula(self, id_pelicula: int) -> List[FuncionVO]:
        query = (
            Funcion.select(Funcion, Pelicula, Sala)
            .join(Pelicula)
            .switch(Funcion)
            .join(Sala)
            .where(Funcion.id_pelicula == id_pelicula)
        )
        return [_map_funcion(f, eager=True) for f in query]

    def create(self, vo: FuncionVO) -> FuncionVO:
        f = Funcion.create(
            fecha=vo.fecha, hora=vo.hora, precio_base=vo.precio_base,
            id_pelicula=vo.id_pelicula, id_sala=vo.id_sala
        )
        vo.id_funcion = f.id_funcion
        return vo

    def update(self, vo: FuncionVO) -> bool:
        return Funcion.update(
            fecha=vo.fecha, hora=vo.hora, precio_base=vo.precio_base,
            id_pelicula=vo.id_pelicula, id_sala=vo.id_sala
        ).where(Funcion.id_funcion == vo.id_funcion).execute() > 0

    def delete(self, id_funcion: int) -> bool:
        return Funcion.delete().where(Funcion.id_funcion == id_funcion).execute() > 0


# ─── ClienteDAO ──────────────────────────────────────────────────────────────

class ClienteDAO:
    def get_all(self) -> List[ClienteVO]:
        return [_map_cliente(c) for c in Cliente.select()]

    def get_by_cedula(self, cedula: str) -> Optional[ClienteVO]:
        try:
            return _map_cliente(Cliente.get_by_id(cedula))
        except Cliente.DoesNotExist:
            return None

    def create(self, vo: ClienteVO) -> ClienteVO:
        Cliente.create(cedula=vo.cedula, nombre=vo.nombre, correo=vo.correo)
        return vo

    def update(self, vo: ClienteVO) -> bool:
        return Cliente.update(
            nombre=vo.nombre, correo=vo.correo
        ).where(Cliente.cedula == vo.cedula).execute() > 0

    def delete(self, cedula: str) -> bool:
        return Cliente.delete().where(Cliente.cedula == cedula).execute() > 0


# ─── ReservaDAO ──────────────────────────────────────────────────────────────

class ReservaDAO:
    def get_by_cliente_eager(self, cedula: str) -> List[ReservaVO]:
        """
        EAGER LOADING: carga reservas con cliente.
        Caso de uso: historial de compras del cliente.
        """
        query = (
            Reserva.select(Reserva, Cliente)
            .join(Cliente)
            .where(Reserva.cedula_cliente == cedula)
        )
        return [_map_reserva(r, eager=True) for r in query]

    def get_by_id_eager(self, id_reserva: int) -> Optional[ReservaVO]:
        try:
            query = (
                Reserva.select(Reserva, Cliente)
                .join(Cliente)
                .where(Reserva.id_reserva == id_reserva)
            )
            return _map_reserva(query.get(), eager=True)
        except Reserva.DoesNotExist:
            return None

    def create(self, vo: ReservaVO) -> ReservaVO:
        r = Reserva.create(
            fecha_compra=vo.fecha_compra,
            total=vo.total,
            cedula_cliente=vo.cedula_cliente
        )
        vo.id_reserva = r.id_reserva
        return vo

    def update_total(self, id_reserva: int, nuevo_total: float) -> bool:
        return Reserva.update(total=nuevo_total).where(
            Reserva.id_reserva == id_reserva
        ).execute() > 0

    def delete(self, id_reserva: int) -> bool:
        return Reserva.delete().where(Reserva.id_reserva == id_reserva).execute() > 0

    def get_all_eager(self) -> List[ReservaVO]:
        query = Reserva.select(Reserva, Cliente).join(Cliente)
        return [_map_reserva(r, eager=True) for r in query]


# ─── TicketDAO ────────────────────────────────────────────────────────────────

class TicketDAO:
    def get_by_reserva_eager(self, id_reserva: int) -> List[TicketVO]:
        """
        EAGER LOADING: carga tickets con función y asiento.
        Caso de uso: mostrar detalle de una reserva (qué películas, qué asientos).
        """
        query = (
            Ticket.select(Ticket, Funcion, Pelicula, Asiento, Sala)
            .join(Funcion)
            .join(Pelicula)
            .switch(Funcion)
            .join(Sala)
            .switch(Ticket)
            .join(Asiento)
            .where(Ticket.id_reserva == id_reserva)
        )
        return [_map_ticket(t, eager=True) for t in query]

    def get_by_id(self, id_ticket: int) -> Optional[TicketVO]:
        try:
            return _map_ticket(Ticket.get_by_id(id_ticket))
        except Ticket.DoesNotExist:
            return None

    def create(self, vo: TicketVO) -> TicketVO:
        t = Ticket.create(
            subtotal=vo.subtotal,
            id_reserva=vo.id_reserva,
            id_funcion=vo.id_funcion,
            id_asiento=vo.id_asiento,
        )
        vo.id_ticket = t.id_ticket
        return vo

    def delete(self, id_ticket: int) -> bool:
        return Ticket.delete().where(Ticket.id_ticket == id_ticket).execute() > 0

    def delete_by_reserva(self, id_reserva: int) -> int:
        return Ticket.delete().where(Ticket.id_reserva == id_reserva).execute()
