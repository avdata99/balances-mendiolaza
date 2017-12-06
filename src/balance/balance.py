"""
Descargar y procesar los archivos PDF con los balances publicados en
http://municipiomendiolaza.com.ar/index.php/transparencia#balances
"""

import requests
import os
import PyPDF2
import csv
import slugify


class Balances:
    ''' balances agrupados '''

    balances_ingresos = []
    balances_egresos = []
    base_path = ''

    def load(self, desde_anio=2017, hasta_anio=2017):


        for anio in range(desde_anio, hasta_anio + 1):
            BalanceIngresos(anio=anio, mes=1).clean_full_CSV()
            BalanceEgresos(anio=anio, mes=1).clean_full_CSV()
            for mes in range(1, 13):
                b = BalanceIngresos(anio=anio, mes=mes)
                b.base_path = self.base_path
                if b.get_PDF():
                    b.get_TXT()
                    b.get_CSV()
                    b.get_full_CSV()

                    self.balances_ingresos.append(b)

                b = BalanceEgresos(anio=anio, mes=mes)
                b.base_path = self.base_path
                if b.get_PDF():
                    b.get_TXT()
                    b.get_CSV()
                    b.get_full_CSV()

                    self.balances_egresos.append(b)


class Balance:
    anio = 0
    mes = 0
    base_path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, anio, mes):
        self.anio = anio
        self.mes = mes

    def get_PDF(self, force=False):
        ''' descargar el PDF si no existe '''
        print('************* \n Obtener PDF {} {}'.format(self.anio, self.mes))
        local_path = self.save_PDF_path.format(self.base_path, self.anio, self.mes)
        if not force and os.path.exists(local_path):
            print('Ya existe {}-{}'.format(self.anio, self.mes))
            return True
        else:
            url = self.url.format(self.anio, self.mes)

            response = requests.get(url)
            if response.status_code != 200:
                print('Error al descargar {}-{}. URL:{} STATUS:{}'.format(self.anio, self.mes, url, response.status_code))
                return False
            else:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                print('OK {}-{}'.format(self.anio, self.mes))
        return True

    def get_TXT(self):
        ''' pasar el PDF a TXT '''
        print('************* \n Pasar PDF a TXT {} {}'.format(self.anio, self.mes))
        local_path = self.save_PDF_path.format(self.base_path, self.anio, self.mes)
        pdfFileObj = open(local_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        txt_file = self.save_TXT_path.format(self.base_path, self.anio, self.mes)
        f = open(txt_file, 'w')
        for page in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(page)
            text = pageObj.extractText()
            f.write(text)

        print('PDF a TXT {}-{}'.format(self.anio, self.mes))
        f.close()

    def get_CSV(self):
        ''' pasar el TXT a CSV '''
        print('************* \n Pasar TXT a CSV {} {}'.format(self.anio, self.mes))
        local_path = self.save_TXT_path.format(self.base_path, self.anio, self.mes)

        f = open(local_path, 'r')
        full_txt = f.read()
        f.close()
        lines = full_txt.split('\n')

        csv_file = self.save_CSV_path.format(self.base_path, self.anio, self.mes)
        with open(csv_file, 'w', newline='') as csvfile:
            fieldnames = self.fieldnames
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for line in lines:
                # las líneas que me interesan tienen el códigop de la cuenta al inicio
                cols = line.split('|')
                if len(cols[0].split('.')) == 7:
                    # print('Linea OK {}'.format(cols[0]))
                    row = {}
                    c = 0
                    for field in fieldnames:
                        row[field] = cols[c].strip()
                        c += 1

                    writer.writerow(row)

        print('TXT a CSV {}-{}'.format(self.anio, self.mes))
        f.close()

    def clean_full_CSV(self):
        csv_file = self.save_CSV_path.format(self.base_path, self.anio, 'FULL')
        if os.path.exists(csv_file):
            os.remove(csv_file)

    def get_full_CSV(self):
        ''' pasar el TXT a un CSV acumulado '''
        print('************* \n Pasar TXT a CSV {} {}'.format(self.anio, self.mes))
        local_path = self.save_TXT_path.format(self.base_path, self.anio, self.mes)

        f = open(local_path, 'r')
        full_txt = f.read()
        f.close()
        lines = full_txt.split('\n')

        csv_file = self.save_CSV_path.format(self.base_path, self.anio, 'FULL')
        with open(csv_file, 'a', newline='') as csvfile:
            fieldnames = self.fieldnames + ['anio', 'mes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for line in lines:
                # las líneas que me interesan tienen el códigop de la cuenta al inicio
                cols = line.split('|')
                if len(cols[0].split('.')) == 7:
                    # print('Linea OK {}'.format(cols[0]))
                    row = {'anio': self.anio, 'mes': self.mes}
                    c = 0
                    for field in self.fieldnames:
                        row[field] = cols[c].strip()
                        c += 1

                    writer.writerow(row)

        print('TXT a CSV {}-{}'.format(self.anio, self.mes))
        f.close()


class BalanceIngresos(Balance):

    save_PDF_path = '{}/PDFs/Ingresos-{}-{}.pdf'
    save_TXT_path = '{}/TXTs/Ingresos-{}-{}.txt'
    save_CSV_path = '{}/CSVs/Ingresos-{}-{}.csv'
    url = "http://municipiomendiolaza.com.ar/images/pdf/Balances{0}/{1:0>2}i.pdf"
    # explicacion de las columnas del PDF
    fieldnames = ['codigo', 'descripcion', 'Autorizado presupuesto', 'recaudación mes', 'acumulado','en menos', 'en más']

    def __str__(self):
        return 'Balance Ingresos {} {}'.format(self.anio, self.mes)

class BalanceEgresos(Balance):

    save_PDF_path = '{}/PDFs/Egresos-{}-{}.pdf'
    save_TXT_path = '{}/TXTs/Egresos-{}-{}.txt'
    save_CSV_path = '{}/CSVs/Egresos-{}-{}.csv'
    url = "http://municipiomendiolaza.com.ar/images/pdf/Balances{0}/{1:0>2}e.pdf"
    # explicacion de las columnas del PDF
    fieldnames = ['codigo', 'descripcion', 'Autorizado presupuesto', 'imputado mes', 'imputado acumulado','saldo a imputar', 'pagado mes', 'pagado acumulado', 'saldo a pagar']

    def __str__(self):
        return 'Balance Egresos {} {}'.format(self.anio, self.mes)




# fin
