"""
Services - Capa de lógica de negocio.
Orquesta DAOs y Commands. Implementa reglas de negocio.
Los servicios son independientes de la UI.
"""
from typing import List, Optional, Tuple
from daos.daos import (
    PeliculaDAO, SalaDAO, AsientoDAO, FuncionDAO,
    ClienteDAO, ReservaDAO, TicketDAO
)
from commands.commands import (
    CrearPeliculaCommand, EliminarPeliculaCommand, ActualizarPeliculaCommand,
    CrearFuncionCommand, EliminarFuncionCommand,
    CrearReservaCommand, CancelarReservaCommand,
    CrearClienteCommand, ActualizarClienteCommand,
    CrearSalaCommand
)
from vos.vos import (
    PeliculaVO, SalaVO, AsientoVO, FuncionVO,
    ClienteVO, ReservaVO, TicketVO
)


class PeliculaService:
    def __init__(self):
        self._dao = PeliculaDAO()

    def listar(self) -> List[PeliculaVO]:
        return self._dao.get_all()

    def buscar(self, id_pelicula: int) -> Optional[PeliculaVO]:
        return self._dao.get_by_id(id_pelicula)

    def crear(self, titulo: str, duracion: str, clasificacion: str, genero: str) -> Tuple[bool, str, Optional[PeliculaVO]]:
        if not titulo.strip():
            return False, "El título no puede estar vacío.", None
        vo = PeliculaVO(titulo=titulo.strip(), duracion=duracion, clasificacion=clasificacion, genero=genero)
        cmd = CrearPeliculaCommand(self._dao, vo)
        result = cmd.execute()
        return True, "Película creada exitosamente.", result

    def actualizar(self, vo: PeliculaVO) -> Tuple[bool, str]:
        cmd = ActualizarPeliculaCommand(self._dao, vo)
        ok = cmd.execute()
        return (True, "Película actualizada.") if ok else (False, "No se encontró la película.")

    def eliminar(self, id_pelicula: int) -> Tuple[bool, str]:
        cmd = EliminarPeliculaCommand(self._dao, id_pelicula)
        ok = cmd.execute()
        return (True, "Película eliminada.") if ok else (False, "No se pudo eliminar.")


class SalaService:
    def __init__(self):
        self._dao = SalaDAO()
        self._asiento_dao = AsientoDAO()

    def listar(self) -> List[SalaVO]:
        return self._dao.get_all()

    def buscar(self, id_sala: int) -> Optional[SalaVO]:
        return self._dao.get_by_id(id_sala)

    def crear(self, numero: int, capacidad: int, tipo_pantalla: str) -> Tuple[bool, str, Optional[SalaVO]]:
        vo = SalaVO(numero=numero, capacidad=capacidad, tipo_pantalla=tipo_pantalla)
        cmd = CrearSalaCommand(self._dao, vo)
        result = cmd.execute()
        # Crear asientos automáticamente
        import math
        cols = min(10, capacidad)
        filas_count = math.ceil(capacidad / cols)
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(min(filas_count, 26)):
            for j in range(1, cols + 1):
                if (i * cols + j) <= capacidad:
                    a_vo = AsientoVO(fila=letras[i], columna=str(j), id_sala=result.id_sala)
                    self._asiento_dao.create(a_vo)
        return True, f"Sala {numero} creada con {capacidad} asientos.", result


class FuncionService:
    def __init__(self):
        self._dao = FuncionDAO()
        self._asiento_dao = AsientoDAO()

    def listar_cartelera(self) -> List[FuncionVO]:
        """Eager loading: retorna funciones con película y sala."""
        return self._dao.get_all_eager()

    def buscar(self, id_funcion: int) -> Optional[FuncionVO]:
        return self._dao.get_by_id_eager(id_funcion)

    def crear(self, fecha: str, hora: str, precio_base: float,
              id_pelicula: int, id_sala: int) -> Tuple[bool, str, Optional[FuncionVO]]:
        if precio_base <= 0:
            return False, "El precio debe ser mayor a 0.", None
        vo = FuncionVO(fecha=fecha, hora=hora, precio_base=precio_base,
                       id_pelicula=id_pelicula, id_sala=id_sala)
        cmd = CrearFuncionCommand(self._dao, vo)
        result = cmd.execute()
        return True, "Función creada exitosamente.", result

    def eliminar(self, id_funcion: int) -> Tuple[bool, str]:
        cmd = EliminarFuncionCommand(self._dao, id_funcion)
        ok = cmd.execute()
        return (True, "Función eliminada.") if ok else (False, "No se pudo eliminar.")

    def get_asientos_disponibles(self, id_funcion: int) -> List[AsientoVO]:
        """Lazy loading: asientos se cargan solo cuando se necesitan para compra."""
        return self._asiento_dao.get_disponibles_funcion(id_funcion)


class ClienteService:
    def __init__(self):
        self._dao = ClienteDAO()

    def listar(self) -> List[ClienteVO]:
        return self._dao.get_all()

    def buscar(self, cedula: str) -> Optional[ClienteVO]:
        return self._dao.get_by_cedula(cedula)

    def crear_o_obtener(self, cedula: str, nombre: str, correo: str) -> Tuple[bool, str, ClienteVO]:
        existente = self._dao.get_by_cedula(cedula)
        if existente:
            return True, "Cliente encontrado.", existente
        vo = ClienteVO(cedula=cedula, nombre=nombre, correo=correo)
        cmd = CrearClienteCommand(self._dao, vo)
        result = cmd.execute()
        return True, "Cliente registrado.", result

    def actualizar(self, vo: ClienteVO) -> Tuple[bool, str]:
        cmd = ActualizarClienteCommand(self._dao, vo)
        ok = cmd.execute()
        return (True, "Cliente actualizado.") if ok else (False, "Cliente no encontrado.")

    def eliminar(self, cedula: str) -> Tuple[bool, str]:
        ok = self._dao.delete(cedula)
        return (True, "Cliente eliminado.") if ok else (False, "No se pudo eliminar.")


class ReservaService:
    def __init__(self):
        self._reserva_dao = ReservaDAO()
        self._ticket_dao = TicketDAO()
        self._asiento_dao = AsientoDAO()
        self._cliente_dao = ClienteDAO()
        self._funcion_dao = FuncionDAO()
        self._historial_commands: List = []  # Stack para undo

    def listar_reservas(self) -> List[ReservaVO]:
        return self._reserva_dao.get_all_eager()

    def listar_por_cliente(self, cedula: str) -> List[ReservaVO]:
        return self._reserva_dao.get_by_cliente_eager(cedula)

    def get_detalle_reserva(self, id_reserva: int) -> Tuple[Optional[ReservaVO], List[TicketVO]]:
        """
        Eager loading: carga reserva con cliente y tickets con funciones/asientos.
        Caso de uso: ver resumen de compra.
        """
        reserva = self._reserva_dao.get_by_id_eager(id_reserva)
        tickets = self._ticket_dao.get_by_reserva_eager(id_reserva) if reserva else []
        return reserva, tickets

    def crear_reserva(
        self,
        cedula_cliente: str,
        id_funcion: int,
        ids_asientos: List[int]
    ) -> Tuple[bool, str, Optional[ReservaVO]]:
        # Validaciones
        cliente = self._cliente_dao.get_by_cedula(cedula_cliente)
        if not cliente:
            return False, "Cliente no encontrado.", None

        funcion = self._funcion_dao.get_by_id_eager(id_funcion)
        if not funcion:
            return False, "Función no encontrada.", None

        if not ids_asientos:
            return False, "Debe seleccionar al menos un asiento.", None

        asientos = []
        for id_a in ids_asientos:
            a = self._asiento_dao.get_by_id(id_a)
            if not a:
                return False, f"Asiento {id_a} no existe.", None
            if a.estado == "ocupado":
                return False, f"El asiento {a.fila}{a.columna} ya está ocupado.", None
            asientos.append(a)

        cmd = CrearReservaCommand(
            self._reserva_dao, self._ticket_dao, self._asiento_dao,
            cliente, funcion, asientos
        )
        reserva = cmd.execute()
        self._historial_commands.append(cmd)
        return True, "Reserva creada exitosamente.", reserva

    def cancelar_reserva(self, id_reserva: int) -> Tuple[bool, str]:
        cmd = CancelarReservaCommand(
            self._reserva_dao, self._ticket_dao,
            self._asiento_dao, id_reserva
        )
        ok = cmd.execute()
        if ok:
            self._historial_commands.append(cmd)
            return True, "Reserva cancelada."
        return False, "No se encontró la reserva."

    def deshacer_ultima_accion(self) -> Tuple[bool, str]:
        """Bonificación: deshacer la última operación de reserva."""
        if not self._historial_commands:
            return False, "No hay acciones para deshacer."
        cmd = self._historial_commands.pop()
        cmd.undo()
        return True, "Acción deshecha exitosamente."
