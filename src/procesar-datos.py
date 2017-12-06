"""
procesar los balances de Mendiolaza publicados
"""
import os
from balance.balance import Balances

b = Balances()
prev_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b.base_path = '{}/data'.format(prev_dir)

# traer todos los meses
b.load()

# ver que cargó
print(b)
