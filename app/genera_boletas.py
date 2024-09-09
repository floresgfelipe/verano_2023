import os
from app import app
from fpdf import FPDF
import pandas as pd
import sys
import pathlib


class PDF(FPDF):
    def add_imagen_boleta(self, path):
        self.set_xy(0.0, 0.0)
        self.image(path, 0, 0, 210, 297, 'png', '')

    def add_texto(self, nombre, parroquia, 
                    decanato, calificacion1, calificacion2):
        self.set_xy(55, 100)
        self.set_font('Courier', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, txt=nombre, align='', link='')

        if len(parroquia) < 31:
            self.set_xy(96, 129) 
            self.set_font('Courier', 'B', 14)
            self.cell(w=90, h=10, border=0, txt=parroquia, align='C', link='')
        else:
            sp = split_parroquia(parroquia)
            
            self.set_xy(96, 128) 
            self.set_font('Courier', 'B', 12)
            self.cell(w=90, h=6, border=0, txt=sp[0], align='C', link='')

            self.set_xy(96, 133) 
            self.set_font('Courier', 'B', 12)
            self.cell(w=90, h=6, border=0, txt=sp[1], align='C', link='')


        self.set_xy(96, 141)
        self.set_font('Courier', 'B', 14)
        self.cell(w=90, h=10, border=0, txt=decanato, align='C', link='')

        if calificacion1 == "ACREDITADO":
            self.set_xy(153, 196)
        else:
            self.set_xy(149, 196)
            
        self.set_font('Courier', 'B', 13)
        self.cell(0, txt=calificacion1, align='', link='')

        if calificacion2 == "ACREDITADO":
            self.set_xy(153, 208)
        else:
            self.set_xy(149, 208)

        self.set_font('Courier', 'B', 13)
        self.cell(0, txt=calificacion2, align='', link='')

def create_pdf(grado, nombre, parroquia, decanato, 
                calificacion1, calificacion2):
    pdf = PDF()
    pdf.add_page()

    if str(grado) == '1':
        pdf.add_imagen_boleta(os.path.join(app.config['IMG_BOLETAS'], '1o.png'))
    elif str(grado) == '2':
        pdf.add_imagen_boleta(os.path.join(app.config['IMG_BOLETAS'], '2o.png'))
    else: 
        pdf.add_imagen_boleta(os.path.join(app.config['IMG_BOLETAS'], '3o.png'))

    pdf.add_texto(nombre, parroquia, decanato, calificacion1, calificacion2) 

    filepath = os.path.join(app.config['PATH_BOLETAS'], str(nombre) + '.pdf')
    pdf.output(filepath, 'F')

    return filepath

def split_parroquia(parroquia):
    sp = parroquia.split()
    i = 0
    splitted_parroquia = ['', '']
    
    for s in sp:
        if i < len(parroquia) / 2:
            splitted_parroquia[0] += s + ' '
            i += len(s)
        else:
            splitted_parroquia[1] += s + ' '
    
    return splitted_parroquia

"""def excel_to_pdf(grado, file):
    df = pd.read_excel(file)

    for(_, nombre, decanato, parroquia, c1, c2) in df.itertuples(name=None):
        s_nombre = nombre.strip()
        s_parroquia = parroquia.strip()
        s_decanato = decanato.strip()
        s_c1 = c1.strip()
        s_c2 = c2.strip()
        
        path = base_dir + "b/" + s_decanato + "/" + s_parroquia + "/" + str(grado) + "/"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        print("Generando boleta de: " + nombre + " en " + path)
        create_pdf(grado, s_nombre, s_parroquia, s_decanato, s_c1, s_c2, path)"""




'''create_pdf(2, 'Felipe Alberto Flores García',
            'Santuario Santo Cristo del Bue',
            'Santa Ana',
            'NO ACREDITADO',
            'ACREDITADO')'''

'''create_pdf(2, 'Leonidez Lendenchy Rodriguez',
            'Ntra. Sra. Del Perpetuo Socorro y San Francisco de Asís',
            'Cristo Rey',
            'ACREDITADO',
            'ACREDITADO')
'''
