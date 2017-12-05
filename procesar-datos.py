"""
Descargar y procesar los archivos PDF con los balances publicados
"""

import requests

# Casi todos los balances tienen una URL previsible pero no siempre :(
balances = []

for anio in range(2016, 2018):
    for mes in range(1, 13):

        adivino_url_egresos = "http://municipiomendiolaza.com.ar/images/pdf/Balances{0}/{1:0>2}e.pdf".format(anio, mes)

        response = requests.get(adivino_url_egresos)
        if response.status_code != 200:
            print('Error al descargar egresos {}-{}'.format(anio, mes))
        else:
            with open('PDFs/PDF-Balance-Egresos-{}-{}.pdf'.format(anio, mes), 'wb') as f:
                f.write(response.content)
            print('OK egresos {}-{}'.format(anio, mes))

        adivino_url_ingresos = "http://municipiomendiolaza.com.ar/images/pdf/Balances{0}/{1:0>2}i.pdf".format(anio, mes)

        response = requests.get(adivino_url_ingresos)
        if response.status_code != 200:
            print('Error al descargar ingresos {}-{}'.format(anio, mes))
        else:
            with open('PDFs/PDF-Balance-Ingresos-{}-{}.pdf'.format(anio, mes), 'wb') as f:
                f.write(response.content)
            print('OK ingresos {}-{}'.format(anio, mes))
