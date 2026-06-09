"""
CineApp - Sistema de Gestión de Cine
Grupo 7
Juan Pablo Ruiz
Santiago Rico
Juan Martin Medrano

Punto de entrada principal de la aplicación.
"""
import sys
import os

# Asegurar que los módulos se encuentren correctamente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from daos.models import init_db
from seeders.providers import DefaultDataProvider
from seeders.seeder import DatabaseSeeder

def main():
    # Inicializar base de datos
    init_db()
    
    # Inyección de Dependencias: inyectamos DefaultDataProvider en DatabaseSeeder
    provider = DefaultDataProvider()
    seeder = DatabaseSeeder(provider)
    seeder.seed()

    # Importar y lanzar la UI
    from PyQt5.QtWidgets import QApplication
    from views.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("CineApp — Grupo 7")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
