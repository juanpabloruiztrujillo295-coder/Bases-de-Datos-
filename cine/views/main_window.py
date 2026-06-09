"""
Vista principal - CineApp PyQt5
Sistema de Gestión de Cine - Grupo 7
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit,
    QHeaderView, QFrame, QGridLayout, QScrollArea, QMessageBox,
    QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QSizePolicy,
    QAbstractItemView, QCheckBox, QTextEdit, QSplitter
)
from PyQt5.QtCore import Qt, QDate, QTime, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QIcon, QPainter, QBrush, QPen

from controllers.controllers import (
    PeliculaController, SalaController, FuncionController,
    ClienteController, CompraController
)
from vos.vos import PeliculaVO, SalaVO, FuncionVO, ClienteVO, AsientoVO


# ─── ESTILOS GLOBALES ──────────────────────────────────────────────────────────

STYLE = """
QMainWindow, QWidget {
    background-color: #0a0a0f;
    color: #e8e0d0;
    font-family: 'Segoe UI', Arial;
}
QWidget#sidebar {
    background-color: #0d0d14;
    border-right: 1px solid #1a1a2e;
}
QPushButton#nav_btn {
    background-color: transparent;
    color: #8a8a9a;
    border: none;
    padding: 14px 20px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
    border-radius: 0px;
}
QPushButton#nav_btn:hover {
    background-color: #1a1a2e;
    color: #e8c96a;
}
QPushButton#nav_btn:checked {
    background-color: #1a1a2e;
    color: #e8c96a;
    border-left: 3px solid #e8c96a;
}
QLabel#title_label {
    font-size: 22px;
    font-weight: bold;
    color: #e8c96a;
    padding: 8px 0px;
}
QLabel#subtitle_label {
    font-size: 13px;
    color: #8a8a9a;
    padding: 2px 0px;
}
QLabel#section_title {
    font-size: 16px;
    font-weight: bold;
    color: #e8c96a;
    padding: 4px 0px;
}
QLabel#logo_label {
    font-size: 26px;
    font-weight: bold;
    color: #e8c96a;
    padding: 20px 16px;
    letter-spacing: 2px;
}
QTableWidget {
    background-color: #0f0f1a;
    color: #e8e0d0;
    border: 1px solid #1e1e30;
    border-radius: 8px;
    gridline-color: #1a1a2e;
    selection-background-color: #2a2a42;
    font-size: 13px;
}
QTableWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid #15151f;
}
QTableWidget::item:selected {
    background-color: #2a2a42;
    color: #e8c96a;
}
QHeaderView::section {
    background-color: #13131f;
    color: #e8c96a;
    font-weight: bold;
    font-size: 12px;
    padding: 10px 12px;
    border: none;
    border-bottom: 1px solid #1e1e30;
}
QPushButton#primary_btn {
    background-color: #e8c96a;
    color: #0a0a0f;
    border: none;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: bold;
    border-radius: 6px;
}
QPushButton#primary_btn:hover {
    background-color: #f0d880;
}
QPushButton#primary_btn:pressed {
    background-color: #d4b550;
}
QPushButton#danger_btn {
    background-color: #c0392b;
    color: #ffffff;
    border: none;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: bold;
    border-radius: 6px;
}
QPushButton#danger_btn:hover {
    background-color: #e74c3c;
}
QPushButton#secondary_btn {
    background-color: transparent;
    color: #e8c96a;
    border: 1px solid #e8c96a;
    padding: 9px 20px;
    font-size: 13px;
    border-radius: 6px;
}
QPushButton#secondary_btn:hover {
    background-color: #1a1a2e;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit {
    background-color: #13131f;
    color: #e8e0d0;
    border: 1px solid #2a2a42;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #e8c96a;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #13131f;
    color: #e8e0d0;
    selection-background-color: #2a2a42;
    border: 1px solid #2a2a42;
}
QGroupBox {
    color: #e8c96a;
    border: 1px solid #1e1e30;
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 8px;
    font-size: 13px;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
QScrollBar:vertical {
    background: #0f0f1a;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #2a2a42;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #e8c96a;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QDialog {
    background-color: #0f0f1a;
}
QMessageBox {
    background-color: #0f0f1a;
    color: #e8e0d0;
}
QFrame#card {
    background-color: #0f0f1a;
    border: 1px solid #1e1e30;
    border-radius: 10px;
}
QLabel#stat_number {
    font-size: 28px;
    font-weight: bold;
    color: #e8c96a;
}
QLabel#stat_label {
    font-size: 11px;
    color: #6a6a7a;
    text-transform: uppercase;
}
"""


# ─── COMPONENTES REUTILIZABLES ─────────────────────────────────────────────────

class SeatButton(QPushButton):
    """Botón de asiento para el mapa interactivo."""
    toggled_seat = pyqtSignal(object, bool)  # AsientoVO, seleccionado

    def __init__(self, asiento: AsientoVO):
        super().__init__(f"{asiento.fila}{asiento.columna}")
        self.asiento = asiento
        self._selected = False
        self.setFixedSize(48, 42)
        self.setCheckable(True)
        self._update_style()
        self.clicked.connect(self._on_click)

    def _on_click(self):
        self._selected = not self._selected
        self._update_style()
        self.toggled_seat.emit(self.asiento, self._selected)

    def _update_style(self):
        if self._selected:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #e8c96a;
                    color: #0a0a0f;
                    border-radius: 6px;
                    font-size: 10px;
                    font-weight: bold;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e30;
                    color: #8a8a9a;
                    border: 1px solid #2a2a42;
                    border-radius: 6px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #2a2a42;
                    color: #e8e0d0;
                }
            """)


class StatCard(QFrame):
    def __init__(self, number: str, label: str, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        n = QLabel(number)
        n.setObjectName("stat_number")
        l = QLabel(label.upper())
        l.setObjectName("stat_label")
        layout.addWidget(n)
        layout.addWidget(l)
        self.setMinimumWidth(140)


def make_btn(text, btn_type="primary", parent=None) -> QPushButton:
    btn = QPushButton(text, parent)
    btn.setObjectName(f"{btn_type}_btn")
    return btn


def make_label(text, label_type="default", parent=None) -> QLabel:
    lbl = QLabel(text, parent)
    if label_type != "default":
        lbl.setObjectName(f"{label_type}_label")
    return lbl


# ─── VISTAS ────────────────────────────────────────────────────────────────────

class DashboardView(QWidget):
    def __init__(self, pel_ctrl, func_ctrl, cliente_ctrl, reserva_ctrl):
        super().__init__()
        self._pel = pel_ctrl
        self._func = func_ctrl
        self._cli = cliente_ctrl
        self._res = reserva_ctrl
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        title = make_label("Panel de Control", "title")
        subtitle = make_label("Resumen del sistema", "subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.stat_peliculas = StatCard("0", "Películas")
        self.stat_funciones = StatCard("0", "Funciones")
        self.stat_clientes = StatCard("0", "Clientes")
        self.stat_reservas = StatCard("0", "Reservas")

        for w in [self.stat_peliculas, self.stat_funciones, self.stat_clientes, self.stat_reservas]:
            stats_layout.addWidget(w)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # Cartelera rápida
        grp = QGroupBox("Próximas Funciones")
        grp_layout = QVBoxLayout(grp)
        self.tabla_cartelera = QTableWidget()
        self.tabla_cartelera.setColumnCount(5)
        self.tabla_cartelera.setHorizontalHeaderLabels(["Película", "Fecha", "Hora", "Sala", "Precio"])
        self.tabla_cartelera.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_cartelera.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_cartelera.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_cartelera.verticalHeader().setVisible(False)
        grp_layout.addWidget(self.tabla_cartelera)
        layout.addWidget(grp)
        layout.addStretch()
        self.refresh()

    def refresh(self):
        pels = self._pel.listar_peliculas()
        funcs = self._func.listar_cartelera()
        clis = self._cli.listar_clientes()
        ress = self._res.listar_reservas()

        self.stat_peliculas.findChild(QLabel, "", Qt.FindChildrenRecursively)
        # Update stat cards
        for card, val in zip(
            [self.stat_peliculas, self.stat_funciones, self.stat_clientes, self.stat_reservas],
            [len(pels), len(funcs), len(clis), len(ress)]
        ):
            card.findChildren(QLabel)[0].setText(str(val))

        self.tabla_cartelera.setRowCount(0)
        for f in funcs[:10]:
            row = self.tabla_cartelera.rowCount()
            self.tabla_cartelera.insertRow(row)
            titulo = f.pelicula.titulo if f.pelicula else "?"
            sala = f"Sala {f.sala.numero}" if f.sala else "?"
            for col, val in enumerate([titulo, f.fecha, f.hora[:5], sala, f"${f.precio_base:,.0f}"]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla_cartelera.setItem(row, col, item)


class PeliculasView(QWidget):
    def __init__(self, controller: PeliculaController):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = make_label("Películas", "title")
        btn_new = make_btn("+ Nueva Película")
        btn_new.clicked.connect(self._nueva_pelicula)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(btn_new)
        layout.addLayout(header)

        # Búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Buscar por título...")
        self.search_input.textChanged.connect(self._filtrar)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Título", "Género", "Clasificación", "Duración", "Acciones"])
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setRowHeight(0, 44)
        layout.addWidget(self.tabla)
        self.refresh()

    def refresh(self):
        self._peliculas = self._ctrl.listar_peliculas()
        self._mostrar(self._peliculas)

    def _mostrar(self, lista):
        self.tabla.setRowCount(0)
        for p in lista:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setRowHeight(row, 44)
            for col, val in enumerate([p.titulo, p.genero, p.clasificacion, p.duracion]):
                item = QTableWidgetItem(str(val))
                item.setData(Qt.UserRole, p)
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(row, col, item)

            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(4, 4, 4, 4)
            btn_edit = make_btn("Editar", "secondary")
            btn_edit.setFixedHeight(30)
            btn_del = make_btn("Eliminar", "danger")
            btn_del.setFixedHeight(30)
            btn_edit.clicked.connect(lambda _, pelicula=p: self._editar(pelicula))
            btn_del.clicked.connect(lambda _, pelicula=p: self._eliminar(pelicula))
            w = QWidget()
            hl = QHBoxLayout(w)
            hl.setContentsMargins(4, 2, 4, 2)
            hl.addWidget(btn_edit)
            hl.addWidget(btn_del)
            self.tabla.setCellWidget(row, 4, w)

    def _filtrar(self, text):
        filtradas = [p for p in self._peliculas if text.lower() in p.titulo.lower()]
        self._mostrar(filtradas)

    def _nueva_pelicula(self):
        dlg = PeliculaDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.get_data()
            ok, msg = self._ctrl.crear_pelicula(d["titulo"], d["duracion"], d["clasificacion"], d["genero"])
            QMessageBox.information(self, "Resultado", msg) if ok else QMessageBox.warning(self, "Error", msg)
            self.refresh()

    def _editar(self, p: PeliculaVO):
        dlg = PeliculaDialog(self, p)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.get_data()
            p.titulo = d["titulo"]
            p.duracion = d["duracion"]
            p.clasificacion = d["clasificacion"]
            p.genero = d["genero"]
            ok, msg = self._ctrl.actualizar_pelicula(p)
            QMessageBox.information(self, "Resultado", msg) if ok else QMessageBox.warning(self, "Error", msg)
            self.refresh()

    def _eliminar(self, p: PeliculaVO):
        reply = QMessageBox.question(self, "Confirmar", f"¿Eliminar '{p.titulo}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            ok, msg = self._ctrl.eliminar_pelicula(p.id_pelicula)
            QMessageBox.information(self, "Resultado", msg)
            self.refresh()


class PeliculaDialog(QDialog):
    def __init__(self, parent, pelicula: PeliculaVO = None):
        super().__init__(parent)
        self.setWindowTitle("Película" if not pelicula else "Editar Película")
        self.setMinimumWidth(400)
        self.setStyleSheet(STYLE)
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        self.titulo = QLineEdit()
        self.genero = QComboBox()
        self.genero.addItems(["Acción", "Ciencia Ficción", "Drama", "Terror", "Comedia", "Animación", "Romance", "Thriller"])
        self.clasificacion = QComboBox()
        self.clasificacion.addItems(["G", "PG", "PG-13", "R", "NC-17"])
        self.duracion = QTimeEdit()
        self.duracion.setDisplayFormat("HH:mm:ss")

        if pelicula:
            self.titulo.setText(pelicula.titulo)
            idx = self.genero.findText(pelicula.genero)
            if idx >= 0: self.genero.setCurrentIndex(idx)
            idx = self.clasificacion.findText(pelicula.clasificacion)
            if idx >= 0: self.clasificacion.setCurrentIndex(idx)
            parts = pelicula.duracion.split(":")
            self.duracion.setTime(QTime(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0))

        layout.addRow("Título:", self.titulo)
        layout.addRow("Género:", self.genero)
        layout.addRow("Clasificación:", self.clasificacion)
        layout.addRow("Duración:", self.duracion)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def get_data(self):
        t = self.duracion.time()
        return {
            "titulo": self.titulo.text(),
            "genero": self.genero.currentText(),
            "clasificacion": self.clasificacion.currentText(),
            "duracion": f"{t.hour():02d}:{t.minute():02d}:{t.second():02d}",
        }


class FuncionesView(QWidget):
    def __init__(self, func_ctrl: FuncionController, pel_ctrl: PeliculaController, sala_ctrl: SalaController):
        super().__init__()
        self._ctrl = func_ctrl
        self._pel_ctrl = pel_ctrl
        self._sala_ctrl = sala_ctrl
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = make_label("Cartelera / Funciones", "title")
        btn_new = make_btn("+ Nueva Función")
        btn_new.clicked.connect(self._nueva_funcion)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(btn_new)
        layout.addLayout(header)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["Película", "Fecha", "Hora", "Sala", "Pantalla", "Precio"])
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.verticalHeader().setVisible(False)
        layout.addWidget(self.tabla)
        self.refresh()

    def refresh(self):
        self._funciones = self._ctrl.listar_cartelera()
        self.tabla.setRowCount(0)
        for f in self._funciones:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setRowHeight(row, 44)
            titulo = f.pelicula.titulo if f.pelicula else "?"
            tipo = f.sala.tipo_pantalla if f.sala else "?"
            sala_n = f"Sala {f.sala.numero}" if f.sala else "?"
            for col, val in enumerate([titulo, f.fecha, f.hora[:5], sala_n, tipo, f"${f.precio_base:,.0f}"]):
                item = QTableWidgetItem(str(val))
                item.setData(Qt.UserRole, f)
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(row, col, item)

    def _nueva_funcion(self):
        peliculas = self._pel_ctrl.listar_peliculas()
        salas = self._sala_ctrl.listar_salas()
        if not peliculas or not salas:
            QMessageBox.warning(self, "Advertencia", "Debe tener películas y salas registradas.")
            return
        dlg = FuncionDialog(self, peliculas, salas)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.get_data()
            ok, msg = self._ctrl.crear_funcion(d["fecha"], d["hora"], d["precio"], d["id_pelicula"], d["id_sala"])
            QMessageBox.information(self, "Resultado", msg) if ok else QMessageBox.warning(self, "Error", msg)
            self.refresh()


class FuncionDialog(QDialog):
    def __init__(self, parent, peliculas, salas):
        super().__init__(parent)
        self.setWindowTitle("Nueva Función")
        self.setMinimumWidth(420)
        self.setStyleSheet(STYLE)
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        self.pelicula_combo = QComboBox()
        for p in peliculas:
            self.pelicula_combo.addItem(p.titulo, p.id_pelicula)

        self.sala_combo = QComboBox()
        for s in salas:
            self.sala_combo.addItem(f"Sala {s.numero} - {s.tipo_pantalla}", s.id_sala)

        self.fecha = QDateEdit(QDate.currentDate())
        self.fecha.setCalendarPopup(True)
        self.fecha.setDisplayFormat("yyyy-MM-dd")

        self.hora = QTimeEdit(QTime(14, 0))
        self.hora.setDisplayFormat("HH:mm:ss")

        self.precio = QDoubleSpinBox()
        self.precio.setMinimum(1000)
        self.precio.setMaximum(100000)
        self.precio.setValue(18000)
        self.precio.setSingleStep(1000)
        self.precio.setPrefix("$ ")

        layout.addRow("Película:", self.pelicula_combo)
        layout.addRow("Sala:", self.sala_combo)
        layout.addRow("Fecha:", self.fecha)
        layout.addRow("Hora:", self.hora)
        layout.addRow("Precio:", self.precio)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def get_data(self):
        t = self.hora.time()
        return {
            "id_pelicula": self.pelicula_combo.currentData(),
            "id_sala": self.sala_combo.currentData(),
            "fecha": self.fecha.date().toString("yyyy-MM-dd"),
            "hora": f"{t.hour():02d}:{t.minute():02d}:{t.second():02d}",
            "precio": self.precio.value(),
        }


class ClientesView(QWidget):
    def __init__(self, controller: ClienteController):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = make_label("Clientes", "title")
        btn_new = make_btn("+ Nuevo Cliente")
        btn_new.clicked.connect(self._nuevo_cliente)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(btn_new)
        layout.addLayout(header)

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍  Buscar por nombre o cédula...")
        self.search.textChanged.connect(self._filtrar)
        layout.addWidget(self.search)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Cédula", "Nombre", "Correo", "Acciones"])
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.verticalHeader().setVisible(False)
        layout.addWidget(self.tabla)
        self.refresh()

    def refresh(self):
        self._clientes = self._ctrl.listar_clientes()
        self._mostrar(self._clientes)

    def _mostrar(self, lista):
        self.tabla.setRowCount(0)
        for c in lista:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setRowHeight(row, 44)
            for col, val in enumerate([c.cedula, c.nombre, c.correo]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(row, col, item)
            w = QWidget()
            hl = QHBoxLayout(w)
            hl.setContentsMargins(4, 2, 4, 2)
            btn_edit = make_btn("Editar", "secondary")
            btn_edit.setFixedHeight(30)
            btn_del = make_btn("Eliminar", "danger")
            btn_del.setFixedHeight(30)
            btn_edit.clicked.connect(lambda _, cl=c: self._editar(cl))
            btn_del.clicked.connect(lambda _, cl=c: self._eliminar(cl))
            hl.addWidget(btn_edit)
            hl.addWidget(btn_del)
            self.tabla.setCellWidget(row, 3, w)

    def _filtrar(self, text):
        t = text.lower()
        filtrados = [c for c in self._clientes if t in c.nombre.lower() or t in c.cedula]
        self._mostrar(filtrados)

    def _nuevo_cliente(self):
        dlg = ClienteDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.get_data()
            ok, msg, _ = self._ctrl.registrar_cliente(d["cedula"], d["nombre"], d["correo"])
            QMessageBox.information(self, "Resultado", msg) if ok else QMessageBox.warning(self, "Error", msg)
            self.refresh()

    def _editar(self, c: ClienteVO):
        dlg = ClienteDialog(self, c)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.get_data()
            c.nombre = d["nombre"]
            c.correo = d["correo"]
            ok, msg = self._ctrl.actualizar_cliente(c)
            QMessageBox.information(self, "Resultado", msg)
            self.refresh()

    def _eliminar(self, c: ClienteVO):
        reply = QMessageBox.question(self, "Confirmar", f"¿Eliminar cliente '{c.nombre}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            ok, msg = self._ctrl.eliminar_cliente(c.cedula)
            QMessageBox.information(self, "Resultado", msg)
            self.refresh()


class ClienteDialog(QDialog):
    def __init__(self, parent, cliente: ClienteVO = None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Cliente" if not cliente else "Editar Cliente")
        self.setMinimumWidth(380)
        self.setStyleSheet(STYLE)
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        self.cedula = QLineEdit()
        self.nombre = QLineEdit()
        self.correo = QLineEdit()

        if cliente:
            self.cedula.setText(cliente.cedula)
            self.cedula.setEnabled(False)
            self.nombre.setText(cliente.nombre)
            self.correo.setText(cliente.correo)

        layout.addRow("Cédula:", self.cedula)
        layout.addRow("Nombre:", self.nombre)
        layout.addRow("Correo:", self.correo)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def get_data(self):
        return {
            "cedula": self.cedula.text().strip(),
            "nombre": self.nombre.text().strip(),
            "correo": self.correo.text().strip(),
        }


class CompraView(QWidget):
    """Flujo completo de compra de tiquetes."""
    def __init__(self, compra_ctrl: CompraController, func_ctrl: FuncionController):
        super().__init__()
        self._ctrl = compra_ctrl
        self._func_ctrl = func_ctrl
        self._seat_buttons = []
        self._build()

    def _build(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(32, 28, 32, 28)
        main_layout.setSpacing(24)

        # Panel izquierdo: pasos
        left = QVBoxLayout()
        left.setSpacing(16)

        title = make_label("Compra de Tiquetes", "title")
        left.addWidget(title)

        # Paso 1: Cliente
        grp_cliente = QGroupBox("1. Datos del Cliente")
        form_cliente = QFormLayout(grp_cliente)
        form_cliente.setSpacing(8)
        self.inp_cedula = QLineEdit()
        self.inp_cedula.setPlaceholderText("Número de cédula")
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setPlaceholderText("Nombre completo")
        self.inp_correo = QLineEdit()
        self.inp_correo.setPlaceholderText("correo@ejemplo.com")
        form_cliente.addRow("Cédula:", self.inp_cedula)
        form_cliente.addRow("Nombre:", self.inp_nombre)
        form_cliente.addRow("Correo:", self.inp_correo)
        left.addWidget(grp_cliente)

        # Paso 2: Función
        grp_funcion = QGroupBox("2. Seleccionar Función")
        form_func = QVBoxLayout(grp_funcion)
        self.func_combo = QComboBox()
        self.func_combo.currentIndexChanged.connect(self._on_funcion_changed)
        btn_iniciar = make_btn("Buscar Asientos Disponibles")
        btn_iniciar.clicked.connect(self._iniciar_sesion)
        form_func.addWidget(QLabel("Función:"))
        form_func.addWidget(self.func_combo)
        form_func.addWidget(btn_iniciar)
        left.addWidget(grp_funcion)

        # Paso 3: Resumen
        grp_resumen = QGroupBox("3. Resumen de Compra")
        resumen_layout = QVBoxLayout(grp_resumen)
        self.lbl_cliente_sel = QLabel("—")
        self.lbl_funcion_sel = QLabel("—")
        self.lbl_asientos_sel = QLabel("Asientos: ninguno")
        self.lbl_total = QLabel("Total: $0")
        self.lbl_total.setStyleSheet("font-size: 18px; font-weight: bold; color: #e8c96a;")
        resumen_layout.addWidget(QLabel("Cliente:"))
        resumen_layout.addWidget(self.lbl_cliente_sel)
        resumen_layout.addWidget(QLabel("Función:"))
        resumen_layout.addWidget(self.lbl_funcion_sel)
        resumen_layout.addWidget(self.lbl_asientos_sel)
        resumen_layout.addWidget(self.lbl_total)
        left.addWidget(grp_resumen)

        btn_confirmar = make_btn("✓  Confirmar Compra")
        btn_confirmar.clicked.connect(self._confirmar)
        btn_deshacer = make_btn("↩  Deshacer Última Acción", "secondary")
        btn_deshacer.clicked.connect(self._deshacer)
        left.addWidget(btn_confirmar)
        left.addWidget(btn_deshacer)
        left.addStretch()

        # Panel derecho: mapa de asientos
        right = QVBoxLayout()
        right.setSpacing(12)
        lbl_mapa = QLabel("Mapa de Asientos")
        lbl_mapa.setObjectName("section_title")
        right.addWidget(lbl_mapa)

        # Leyenda
        leyenda = QHBoxLayout()
        for color, text in [("#1e1e30", "Disponible"), ("#e8c96a", "Seleccionado")]:
            box = QLabel("  ")
            box.setFixedSize(20, 20)
            box.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #8a8a9a; font-size: 11px;")
            leyenda.addWidget(box)
            leyenda.addWidget(lbl)
            leyenda.addSpacing(12)
        leyenda.addStretch()
        right.addLayout(leyenda)

        # Pantalla (decorativa)
        screen = QFrame()
        screen.setFixedHeight(8)
        screen.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1a1a2e, stop:0.5 #e8c96a, stop:1 #1a1a2e); border-radius: 4px;")
        right.addWidget(screen)
        lbl_screen = QLabel("PANTALLA")
        lbl_screen.setAlignment(Qt.AlignCenter)
        lbl_screen.setStyleSheet("color: #4a4a5a; font-size: 10px; letter-spacing: 4px;")
        right.addWidget(lbl_screen)

        # Área de asientos (scrollable)
        self.scroll_asientos = QScrollArea()
        self.scroll_asientos.setWidgetResizable(True)
        self.asientos_widget = QWidget()
        self.asientos_layout = QGridLayout(self.asientos_widget)
        self.asientos_layout.setSpacing(6)
        self.scroll_asientos.setWidget(self.asientos_widget)
        self.scroll_asientos.setMinimumWidth(340)
        right.addWidget(self.scroll_asientos)

        main_layout.addLayout(left, 2)
        main_layout.addLayout(right, 3)
        self._cargar_funciones()

    def _cargar_funciones(self):
        self.func_combo.clear()
        funciones = self._func_ctrl.listar_cartelera()
        self._funciones = funciones
        for f in funciones:
            titulo = f.pelicula.titulo if f.pelicula else "?"
            self.func_combo.addItem(f"{titulo} - {f.fecha} {f.hora[:5]}", f.id_funcion)

    def _on_funcion_changed(self, idx):
        # Limpiar mapa anterior
        for btn in self._seat_buttons:
            btn.deleteLater()
        self._seat_buttons = []

    def _iniciar_sesion(self):
        cedula = self.inp_cedula.text().strip()
        nombre = self.inp_nombre.text().strip()
        correo = self.inp_correo.text().strip()

        if not cedula or not nombre:
            QMessageBox.warning(self, "Datos incompletos", "Ingrese cédula y nombre del cliente.")
            return

        id_funcion = self.func_combo.currentData()
        if id_funcion is None:
            QMessageBox.warning(self, "Sin función", "Seleccione una función.")
            return

        ok, msg = self._ctrl.iniciar_compra(cedula, nombre, correo, id_funcion)
        if not ok:
            QMessageBox.warning(self, "Error", msg)
            return

        sesion = self._ctrl.get_sesion()
        self.lbl_cliente_sel.setText(f"{sesion.cliente.nombre} ({sesion.cliente.cedula})")
        self.lbl_funcion_sel.setText(str(sesion.funcion))

        # Cargar mapa de asientos
        self._cargar_mapa_asientos(id_funcion)

    def _cargar_mapa_asientos(self, id_funcion: int):
        # Limpiar
        for btn in self._seat_buttons:
            btn.deleteLater()
        self._seat_buttons = []

        asientos = self._func_ctrl.get_asientos_disponibles(id_funcion)

        # Organizar por fila
        filas = {}
        for a in asientos:
            if a.fila not in filas:
                filas[a.fila] = []
            filas[a.fila].append(a)

        for r_idx, fila in enumerate(sorted(filas.keys())):
            lbl_fila = QLabel(fila)
            lbl_fila.setStyleSheet("color: #6a6a7a; font-size: 11px; font-weight: bold;")
            lbl_fila.setFixedWidth(20)
            lbl_fila.setAlignment(Qt.AlignCenter)
            self.asientos_layout.addWidget(lbl_fila, r_idx, 0)
            for c_idx, asiento in enumerate(sorted(filas[fila], key=lambda a: a.columna)):
                btn = SeatButton(asiento)
                btn.toggled_seat.connect(self._on_asiento_toggled)
                self.asientos_layout.addWidget(btn, r_idx, c_idx + 1)
                self._seat_buttons.append(btn)

    def _on_asiento_toggled(self, asiento: AsientoVO, seleccionado: bool):
        if seleccionado:
            self._ctrl.seleccionar_asiento(asiento)
        else:
            self._ctrl.quitar_asiento(asiento)
        self._actualizar_resumen()

    def _actualizar_resumen(self):
        sesion = self._ctrl.get_sesion()
        if sesion.activa:
            asientos = sesion.asientos_seleccionados
            texto = ", ".join(f"{a.fila}{a.columna}" for a in asientos) if asientos else "ninguno"
            self.lbl_asientos_sel.setText(f"Asientos: {texto}")
            self.lbl_total.setText(f"Total: ${sesion.total():,.0f}")

    def _confirmar(self):
        ok, msg, reserva = self._ctrl.confirmar_compra()
        if ok:
            QMessageBox.information(self, "¡Compra Exitosa!",
                                    f"{msg}\nReserva #{reserva.id_reserva}\nTotal: ${reserva.total:,.0f}")
            self._reset_form()
        else:
            QMessageBox.warning(self, "Error", msg)

    def _deshacer(self):
        ok, msg = self._ctrl.deshacer_ultima_accion()
        QMessageBox.information(self, "Deshacer", msg)
        self._cargar_funciones()

    def _reset_form(self):
        self.inp_cedula.clear()
        self.inp_nombre.clear()
        self.inp_correo.clear()
        self.lbl_cliente_sel.setText("—")
        self.lbl_funcion_sel.setText("—")
        self.lbl_asientos_sel.setText("Asientos: ninguno")
        self.lbl_total.setText("Total: $0")
        for btn in self._seat_buttons:
            btn.deleteLater()
        self._seat_buttons = []
        self._cargar_funciones()

    def showEvent(self, event):
        self._cargar_funciones()
        super().showEvent(event)


class ReservasView(QWidget):
    def __init__(self, compra_ctrl: CompraController):
        super().__init__()
        self._ctrl = compra_ctrl
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = make_label("Reservas", "title")
        btn_refresh = make_btn("↻  Actualizar", "secondary")
        btn_refresh.clicked.connect(self.refresh)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(btn_refresh)
        layout.addLayout(header)

        # Búsqueda por cédula
        search_layout = QHBoxLayout()
        self.search_cedula = QLineEdit()
        self.search_cedula.setPlaceholderText("🔍  Buscar por cédula de cliente...")
        btn_buscar = make_btn("Buscar")
        btn_buscar.clicked.connect(self._buscar_por_cliente)
        btn_todas = make_btn("Ver Todas", "secondary")
        btn_todas.clicked.connect(self.refresh)
        search_layout.addWidget(self.search_cedula)
        search_layout.addWidget(btn_buscar)
        search_layout.addWidget(btn_todas)
        layout.addLayout(search_layout)

        splitter = QSplitter(Qt.Vertical)

        # Tabla de reservas
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["#", "Cliente", "Fecha Compra", "Total", "Acciones"])
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.cellClicked.connect(self._ver_detalle)
        splitter.addWidget(self.tabla)

        # Detalle de tickets
        detalle_widget = QWidget()
        detalle_layout = QVBoxLayout(detalle_widget)
        detalle_layout.setContentsMargins(0, 8, 0, 0)
        lbl_det = QLabel("Detalle de Tickets")
        lbl_det.setObjectName("section_title")
        detalle_layout.addWidget(lbl_det)
        self.tabla_tickets = QTableWidget()
        self.tabla_tickets.setColumnCount(4)
        self.tabla_tickets.setHorizontalHeaderLabels(["Ticket", "Película", "Asiento", "Subtotal"])
        self.tabla_tickets.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_tickets.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_tickets.verticalHeader().setVisible(False)
        detalle_layout.addWidget(self.tabla_tickets)
        splitter.addWidget(detalle_widget)

        layout.addWidget(splitter)
        self.refresh()

    def refresh(self):
        reservas = self._ctrl.listar_reservas()
        self._mostrar_reservas(reservas)

    def _buscar_por_cliente(self):
        cedula = self.search_cedula.text().strip()
        if not cedula:
            self.refresh()
            return
        reservas = self._ctrl.listar_reservas_cliente(cedula)
        self._mostrar_reservas(reservas)

    def _mostrar_reservas(self, reservas):
        self.tabla.setRowCount(0)
        for r in reservas:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setRowHeight(row, 44)
            nombre = r.cliente.nombre if r.cliente else r.cedula_cliente
            for col, val in enumerate([str(r.id_reserva), nombre, r.fecha_compra, f"${r.total:,.0f}"]):
                item = QTableWidgetItem(str(val))
                item.setData(Qt.UserRole, r.id_reserva)
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(row, col, item)

            w = QWidget()
            hl = QHBoxLayout(w)
            hl.setContentsMargins(4, 2, 4, 2)
            btn_cancel = make_btn("Cancelar", "danger")
            btn_cancel.setFixedHeight(30)
            btn_cancel.clicked.connect(lambda _, res=r: self._cancelar(res))
            hl.addWidget(btn_cancel)
            self.tabla.setCellWidget(row, 4, w)

    def _ver_detalle(self, row, col):
        item = self.tabla.item(row, 0)
        if not item:
            return
        id_reserva = int(item.text())
        reserva, tickets = self._ctrl.detalle_reserva(id_reserva)
        self.tabla_tickets.setRowCount(0)
        for t in tickets:
            r = self.tabla_tickets.rowCount()
            self.tabla_tickets.insertRow(r)
            titulo = t.funcion.pelicula.titulo if (t.funcion and t.funcion.pelicula) else "?"
            asiento = f"{t.asiento.fila}{t.asiento.columna}" if t.asiento else "?"
            for c, v in enumerate([str(t.id_ticket), titulo, asiento, f"${t.subtotal:,.0f}"]):
                itm = QTableWidgetItem(str(v))
                itm.setTextAlignment(Qt.AlignCenter)
                self.tabla_tickets.setItem(r, c, itm)

    def _cancelar(self, reserva):
        reply = QMessageBox.question(self, "Confirmar",
                                     f"¿Cancelar reserva #{reserva.id_reserva}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            ok, msg = self._ctrl.cancelar_reserva(reserva.id_reserva)
            QMessageBox.information(self, "Resultado", msg)
            self.refresh()

    def showEvent(self, event):
        self.refresh()
        super().showEvent(event)


class SalasView(QWidget):
    def __init__(self, controller: SalaController):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = make_label("Salas de Cine", "title")
        btn_new = make_btn("+ Nueva Sala")
        btn_new.clicked.connect(self._nueva_sala)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(btn_new)
        layout.addLayout(header)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Número", "Capacidad", "Tipo Pantalla", "#"])
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.verticalHeader().setVisible(False)
        layout.addWidget(self.tabla)
        layout.addStretch()
        self.refresh()

    def refresh(self):
        salas = self._ctrl.listar_salas()
        self.tabla.setRowCount(0)
        for s in salas:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setRowHeight(row, 44)
            for col, val in enumerate([str(s.numero), str(s.capacidad), s.tipo_pantalla, str(s.id_sala)]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(row, col, item)

    def _nueva_sala(self):
        dlg = SalaDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.get_data()
            ok, msg = self._ctrl.crear_sala(d["numero"], d["capacidad"], d["tipo_pantalla"])
            QMessageBox.information(self, "Resultado", msg) if ok else QMessageBox.warning(self, "Error", msg)
            self.refresh()


class SalaDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Nueva Sala")
        self.setMinimumWidth(360)
        self.setStyleSheet(STYLE)
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        self.numero = QSpinBox()
        self.numero.setMinimum(1)
        self.numero.setMaximum(99)

        self.capacidad = QSpinBox()
        self.capacidad.setMinimum(10)
        self.capacidad.setMaximum(300)
        self.capacidad.setValue(50)

        self.tipo = QComboBox()
        self.tipo.addItems(["Estándar", "3D", "IMAX", "4DX", "VIP"])

        layout.addRow("Número de sala:", self.numero)
        layout.addRow("Capacidad:", self.capacidad)
        layout.addRow("Tipo de pantalla:", self.tipo)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def get_data(self):
        return {
            "numero": self.numero.value(),
            "capacidad": self.capacidad.value(),
            "tipo_pantalla": self.tipo.currentText(),
        }


# ─── VENTANA PRINCIPAL ────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineApp — Grupo 7")
        self.setMinimumSize(1200, 740)
        self.setStyleSheet(STYLE)

        # Controladores
        self.pel_ctrl = PeliculaController()
        self.sala_ctrl = SalaController()
        self.func_ctrl = FuncionController()
        self.cli_ctrl = ClienteController()
        self.compra_ctrl = CompraController()

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ──
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        logo = QLabel("🎬  CINEAPP")
        logo.setObjectName("logo_label")
        sidebar_layout.addWidget(logo)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #1a1a2e;")
        sidebar_layout.addWidget(sep)

        self.nav_buttons = []
        nav_items = [
            ("🏠  Dashboard", 0),
            ("🎬  Películas", 1),
            ("🎭  Cartelera", 2),
            ("🏛  Salas", 3),
            ("👥  Clientes", 4),
            ("🎟  Comprar Tiquetes", 5),
            ("📋  Reservas", 6),
        ]

        for label, idx in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("nav_btn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, i=idx: self._navigate(i))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Versión
        version_lbl = QLabel("Grupo 7 — v2.0")
        version_lbl.setStyleSheet("color: #3a3a4a; font-size: 10px; padding: 12px;")
        sidebar_layout.addWidget(version_lbl)

        # ── Contenido ──
        self.stack = QStackedWidget()

        self.dash_view = DashboardView(self.pel_ctrl, self.func_ctrl, self.cli_ctrl, self.compra_ctrl)
        self.pel_view = PeliculasView(self.pel_ctrl)
        self.func_view = FuncionesView(self.func_ctrl, self.pel_ctrl, self.sala_ctrl)
        self.sala_view = SalasView(self.sala_ctrl)
        self.cli_view = ClientesView(self.cli_ctrl)
        self.compra_view = CompraView(self.compra_ctrl, self.func_ctrl)
        self.reserva_view = ReservasView(self.compra_ctrl)

        for v in [self.dash_view, self.pel_view, self.func_view, self.sala_view,
                  self.cli_view, self.compra_view, self.reserva_view]:
            self.stack.addWidget(v)

        root.addWidget(sidebar)
        root.addWidget(self.stack)

        self._navigate(0)

    def _navigate(self, idx: int):
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == idx)
        # Refrescar dashboard al volver
        if idx == 0:
            self.dash_view.refresh()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

def main():
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    from daos.models import init_db, seed_db
    init_db()
    seed_db()

    app = QApplication(sys.argv)
    app.setApplicationName("CineApp")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
