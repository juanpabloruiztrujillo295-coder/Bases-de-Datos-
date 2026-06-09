"""
Controladores - Coordinan la interacción entre vistas y servicios.
Reciben eventos de la UI, delegan a servicios y devuelven resultados.
"""
from typing import List, Optional, Tuple
from services.services import (
    PeliculaService, SalaService, FuncionService,
    ClienteService, ReservaService
)
from controllers.app_state import AppState
from vos.vos import PeliculaVO, SalaVO, FuncionVO, ClienteVO, AsientoVO, ReservaVO, TicketVO


class PeliculaController:
    def __init__(self):
        self._service = PeliculaService()

    def listar_peliculas(self) -> List[PeliculaVO]:
        return self._service.listar()

    def crear_pelicula(self, titulo, duracion, clasificacion, genero) -> Tuple[bool, str]:
        ok, msg, _ = self._service.crear(titulo, duracion, clasificacion, genero)
        return ok, msg

    def actualizar_pelicula(self, vo: PeliculaVO) -> Tuple[bool, str]:
        return self._service.actualizar(vo)

    def eliminar_pelicula(self, id_pelicula: int) -> Tuple[bool, str]:
        return self._service.eliminar(id_pelicula)


class SalaController:
    def __init__(self):
        self._service = SalaService()

    def listar_salas(self) -> List[SalaVO]:
        return self._service.listar()

    def crear_sala(self, numero, capacidad, tipo_pantalla) -> Tuple[bool, str]:
        ok, msg, _ = self._service.crear(numero, capacidad, tipo_pantalla)
        return ok, msg


class FuncionController:
    def __init__(self):
        self._service = FuncionService()

    def listar_cartelera(self) -> List[FuncionVO]:
        return self._service.listar_cartelera()

    def crear_funcion(self, fecha, hora, precio, id_pelicula, id_sala) -> Tuple[bool, str]:
        ok, msg, _ = self._service.crear(fecha, hora, precio, id_pelicula, id_sala)
        return ok, msg

    def eliminar_funcion(self, id_funcion: int) -> Tuple[bool, str]:
        return self._service.eliminar(id_funcion)

    def get_asientos_disponibles(self, id_funcion: int) -> List[AsientoVO]:
        return self._service.get_asientos_disponibles(id_funcion)


class ClienteController:
    def __init__(self):
        self._service = ClienteService()

    def listar_clientes(self) -> List[ClienteVO]:
        return self._service.listar()

    def buscar_cliente(self, cedula: str) -> Optional[ClienteVO]:
        return self._service.buscar(cedula)

    def registrar_cliente(self, cedula, nombre, correo) -> Tuple[bool, str, Optional[ClienteVO]]:
        return self._service.crear_o_obtener(cedula, nombre, correo)

    def actualizar_cliente(self, vo: ClienteVO) -> Tuple[bool, str]:
        return self._service.actualizar(vo)

    def eliminar_cliente(self, cedula: str) -> Tuple[bool, str]:
        return self._service.eliminar(cedula)


class CompraController:
    """
    Controlador principal del flujo de compra.
    Usa AppState para mantener la sesión entre pasos.
    """
    def __init__(self):
        self._reserva_service = ReservaService()
        self._cliente_service = ClienteService()
        self._funcion_service = FuncionService()
        self._app_state = AppState()

    def iniciar_compra(self, cedula: str, nombre: str, correo: str, id_funcion: int) -> Tuple[bool, str]:
        ok, msg, cliente = self._cliente_service.crear_o_obtener(cedula, nombre, correo)
        if not ok:
            return False, msg
        funcion = self._funcion_service.buscar(id_funcion)
        if not funcion:
            return False, "Función no encontrada."
        self._app_state.sesion_compra.iniciar(cliente, funcion)
        return True, f"Sesión iniciada para {cliente.nombre}"

    def seleccionar_asiento(self, asiento: AsientoVO) -> Tuple[bool, str]:
        sesion = self._app_state.sesion_compra
        if not sesion.activa:
            return False, "No hay sesión de compra activa."
        sesion.agregar_asiento(asiento)
        return True, f"Asiento {asiento.fila}{asiento.columna} agregado."

    def quitar_asiento(self, asiento: AsientoVO):
        self._app_state.sesion_compra.quitar_asiento(asiento)

    def get_sesion(self):
        return self._app_state.sesion_compra

    def confirmar_compra(self) -> Tuple[bool, str, Optional[ReservaVO]]:
        sesion = self._app_state.sesion_compra
        if not sesion.activa:
            return False, "No hay sesión activa.", None
        if not sesion.asientos_seleccionados:
            return False, "No hay asientos seleccionados.", None

        ids_asientos = [a.id_asiento for a in sesion.asientos_seleccionados]
        ok, msg, reserva = self._reserva_service.crear_reserva(
            sesion.cliente.cedula,
            sesion.funcion.id_funcion,
            ids_asientos
        )
        if ok:
            self._app_state.sesion_compra.limpiar()
        return ok, msg, reserva

    def cancelar_reserva(self, id_reserva: int) -> Tuple[bool, str]:
        return self._reserva_service.cancelar_reserva(id_reserva)

    def deshacer_ultima_accion(self) -> Tuple[bool, str]:
        return self._reserva_service.deshacer_ultima_accion()

    def listar_reservas(self) -> List[ReservaVO]:
        return self._reserva_service.listar_reservas()

    def detalle_reserva(self, id_reserva: int) -> Tuple[Optional[ReservaVO], List[TicketVO]]:
        return self._reserva_service.get_detalle_reserva(id_reserva)

    def listar_reservas_cliente(self, cedula: str) -> List[ReservaVO]:
        return self._reserva_service.listar_por_cliente(cedula)
