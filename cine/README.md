# 🎬 CineApp — Sistema de Gestión de Cine
### Grupo 7

---

## Requisitos

```bash
pip install peewee PyQt5
```

## Ejecución

```bash
cd cine
python main.py
```

---

## Arquitectura por Capas

```
┌─────────────────────────────────────────────┐
│               Vista (PyQt5)                 │  views/main_window.py
│  DashboardView │ PeliculasView │ CompraView │
│  FuncionesView │ ClientesView  │ ReservasView│
└─────────────────────┬───────────────────────┘
                      │ eventos UI
┌─────────────────────▼───────────────────────┐
│             Controladores                   │  controllers/controllers.py
│  PeliculaController │ FuncionController     │
│  ClienteController  │ CompraController      │
├─────────────────────────────────────────────┤
│          Capa de Aplicación (State)         │  controllers/app_state.py
│          AppState │ SesionCompra            │
└─────────────────────┬───────────────────────┘
                      │ orquesta
┌─────────────────────▼───────────────────────┐
│                Servicios                    │  services/services.py
│  PeliculaService │ FuncionService           │
│  ClienteService  │ ReservaService           │
└──────────┬──────────────────┬──────────────┘
           │ usa              │ ejecuta
┌──────────▼──────┐  ┌────────▼──────────────┐
│    Commands     │  │        DAOs           │
│  (Abstracción)  │  │  (PeeWee ORM)        │
│  CrearReserva   │  │  PeliculaDAO          │
│  CancelarReserva│  │  FuncionDAO           │
│  CrearPelicula  │  │  ReservaDAO           │
│  + undo()       │  │  TicketDAO            │
└─────────────────┘  └──────────┬────────────┘
                                │ mapea
                     ┌──────────▼────────────┐
                     │    Value Objects (VO) │
                     │  PeliculaVO │ SalaVO  │
                     │  FuncionVO  │ TicketVO│
                     │  ReservaVO  │ ...     │
                     └───────────────────────┘
                                │
                     ┌──────────▼────────────┐
                     │   Base de Datos       │
                     │   SQLite (cine.db)    │
                     │   PeeWee ORM Models   │
                     └───────────────────────┘
```

---

## Tablas de la Base de Datos (7 tablas)

| Tabla     | Descripción                                  |
|-----------|----------------------------------------------|
| pelicula  | Catálogo de películas                        |
| sala      | Salas del cine con tipo de pantalla          |
| asiento   | Asientos por sala (composición con sala)     |
| funcion   | Programación de películas en salas           |
| cliente   | Registro de clientes                         |
| reserva   | Reservas de clientes (contiene tickets)      |
| ticket    | Tiquetes individuales por asiento/función    |

---

## Relaciones OO implementadas

### Composición
- `Sala` → `Asiento`: Los asientos no existen sin la sala. Al crear una sala, los asientos se generan automáticamente.
- `Reserva` → `Ticket`: Los tickets son parte integral de la reserva. Al cancelar la reserva se eliminan en cascada.

### Agregación
- `Funcion` agrega `Pelicula` y `Sala`: La función referencia película y sala, que tienen vida independiente.
- `Ticket` agrega `Funcion` y `Asiento`.

### Dependencia
- `CompraController` depende de `SesionCompra` (AppState) para operar el flujo multi-paso.
- `CrearReservaCommand` depende de los VOs de cliente, función y asientos seleccionados.

---

## Eager vs Lazy Loading

### Eager Loading (JOIN inmediato)
| Caso de uso | Método | Justificación |
|---|---|---|
| Listar cartelera | `FuncionDAO.get_all_eager()` | Siempre necesitamos título de película y sala |
| Ver detalle reserva | `TicketDAO.get_by_reserva_eager()` | Se necesita película, asiento y función juntos |
| Historial cliente | `ReservaDAO.get_by_cliente_eager()` | Nombre del cliente siempre visible |

### Lazy Loading (bajo demanda)
| Caso de uso | Método | Justificación |
|---|---|---|
| Mapa de asientos | `AsientoDAO.get_disponibles_funcion()` | Solo se carga al hacer click en "Buscar asientos" |
| Tickets de reserva | `ReservaVO._tickets` | Se cargan solo al ver el detalle |

---

## Patrón Command + Undo (Bonificación)

El sistema implementa el patrón Command en `commands/commands.py`. Cada operación encapsula:
- `execute()`: realiza la acción
- `undo()`: revierte la acción guardando backup del estado anterior

`ReservaService` mantiene un stack de comandos ejecutados. El botón "↩ Deshacer Última Acción" en la vista de compra permite revertir la última reserva creada o cancelada.

---

## Módulos del Proyecto

```
cine/
├── main.py                    # Punto de entrada
├── requirements.txt
├── vos/
│   └── vos.py                 # Value Objects (dataclasses)
├── daos/
│   ├── models.py              # Modelos PeeWee ORM
│   └── daos.py                # Data Access Objects
├── commands/
│   └── commands.py            # Patrón Command + undo
├── services/
│   └── services.py            # Lógica de negocio
├── controllers/
│   ├── app_state.py           # Estado de aplicación (sesión compra)
│   └── controllers.py         # Coordinación Vista ↔ Servicio
└── views/
    └── main_window.py         # UI PyQt5 completa
```
