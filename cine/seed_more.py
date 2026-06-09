import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seeders.providers import ExtraDataProvider
from seeders.seeder import DatabaseSeeder

def seed_more():
    print("Iniciando inserción de datos adicionales usando DI...")
    
    # Inyección de dependencias
    provider = ExtraDataProvider()
    seeder = DatabaseSeeder(provider)
    seeder.seed()
    
    print("Datos insertados con éxito.")

if __name__ == '__main__':
    seed_more()
