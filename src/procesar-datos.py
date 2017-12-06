"""
procesar los balances de Mendiolaza publicados
"""

from balance.balance import *
from os.path import dirname, abspath


for anio in range(2017, 2018):
    for mes in range(1, 8):

        b = BalanceIngresos(anio=anio, mes=mes)
        prev_dir = dirname(dirname(abspath(__file__)))
        b.base_path = '{}/data'.format(prev_dir)
        if b.get_PDF():
            b.get_TXT()
            b.get_CSV()

        b = BalanceEgresos(anio=anio, mes=mes)
        prev_dir = dirname(dirname(abspath(__file__)))
        b.base_path = '{}/data'.format(prev_dir)
        if b.get_PDF():
            b.get_TXT()
            b.get_CSV()
