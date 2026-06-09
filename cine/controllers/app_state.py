"""
Capa de Aplicación - Maneja el estado compartido entre casos de uso.
Justificación: el controlador maneja múltiples casos de uso que comparten
estado (cliente en sesión, función seleccionada, asientos en carrito).
Esta capa evita que el controlador acumule estado mutable innecesario.
"""
from typing import Optional, List
from vos.vos import ClienteVO, FuncionVO, AsientoVO


class SesionCompra:
    """
    Estado de la sesión de compra activa.
    Patrón: State / Session object.
    Relación de dependencia: depende de VOs (no los posee).
    """
    def __init__(self):
        self.cliente: Optional[ClienteVO] = None
        self.funcion: Optional[FuncionVO] = None
        self.asientos_seleccionados: List[AsientoVO] = []

    def iniciar(self, cliente: ClienteVO, funcion: FuncionVO):
        self.cliente = cliente
        self.funcion = funcion
        self.asientos_seleccionados = []

    def agregar_asiento(self, asiento: AsientoVO):
        if asiento not in self.asientos_seleccionados:
            self.asientos_seleccionados.append(asiento)

    def quitar_asiento(self, asiento: AsientoVO):
        self.asientos_seleccionados = [
            a for a in self.asientos_seleccionados
            if a.id_asiento != asiento.id_asiento
        ]

    def total(self) -> float:
        if not self.funcion:
            return 0.0
        return self.funcion.precio_base * len(self.asientos_seleccionados)

    def limpiar(self):
        self.cliente = None
        self.funcion = None
        self.asientos_seleccionados = []

    @property
    def activa(self) -> bool:
        return self.cliente is not None and self.funcion is not None


class AppState:
    """
    Estado global de la aplicación compartido entre vistas.
    Singleton de estado.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.sesion_compra = SesionCompra()
        self.usuario_admin: bool = False  # toggle admin/cliente

    def reset(self):
        self.sesion_compra.limpiar()
