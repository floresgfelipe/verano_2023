import os
from app import app, db
from app.models import Alumno, Evangelizador

import pandas as pd


def alumno_to_dict(alumno):
    rt_dict = dict()

    rt_dict['Nombre'] = (str(alumno.nombres) 
                         + ' ' + str(alumno.apellido_p) 
                         + ' ' + str(alumno.apellido_m))
    

    rt_dict['Fecha de Nacimiento'] = (str(alumno.dia_nac) 
                                      + '/' + str(alumno.mes_nac) 
                                      + '/' + str(alumno.año_nac))

    rt_dict['Decanato'] = str(alumno.decanato)

    rt_dict['Parroquia'] = str(alumno.parroquia)

    rt_dict['Teléfono'] = str(alumno.telefono).replace(" ", "")

    rt_dict['Correo'] = str(alumno.correo)

    rt_dict['Grado'] = alumno.get_grado()
    """
    if alumno.foto != 'none':
        rt_dict['Foto'] = ('https://catequesisver.org/fotos_admin/' 
                            + os.path.basename(alumno.foto))
    else:
        rt_dict['Foto'] = 'NO DISPONIBLE'

    if alumno.boleta_carta != 'none':
        rt_dict['Boleta o Carta'] = ('https://catequesisver.org/boletas_admin/' 
                                + os.path.basename(alumno.boleta_carta))
    else:
        rt_dict['Boleta o Carta'] = 'NO DISPONIBLE'
    """

    if alumno.calificacion1 == 1:
        rt_dict['Calificación 1er. sem.'] = "ACREDITADO"
    elif alumno.calificacion1 == 2:
        rt_dict['Calificación 1er. sem.'] = "NO ACREDITADO"
    else:
        rt_dict['Calificación 1er. sem.'] = ""

    if alumno.calificacion2 == 1:
        rt_dict['Calificación 2o. sem.'] = "ACREDITADO"
    elif alumno.calificacion2 == 2:
        rt_dict['Calificación 2o. sem.'] = "NO ACREDITADO"
    else:
        rt_dict['Calificación 2o. sem.'] = ""    
    return rt_dict

def evangelizador_to_dict(evangelizador):
    rt_dict = dict()

    rt_dict['Nombre'] = (str(evangelizador.nombres) 
                         + ' ' + str(evangelizador.apellido_p) 
                         + ' ' + str(evangelizador.apellido_m))
    

    rt_dict['Fecha de Nacimiento'] = (str(evangelizador.dia_nac) 
                                      + '/' + str(evangelizador.mes_nac) 
                                      + '/' + str(evangelizador.año_nac))

    rt_dict['Decanato'] = str(evangelizador.decanato)

    rt_dict['Parroquia'] = str(evangelizador.parroquia)

    rt_dict['Teléfono'] = str(evangelizador.telefono)

    rt_dict['Correo'] = str(evangelizador.correo)

    rt_dict['Grado'] = 'Evangelizador'

    if evangelizador.foto != 'none':
        rt_dict['Foto'] = ('https://catequesisver.org/fotos_admin_ev/' 
                            + os.path.basename(evangelizador.foto))
    else:
        rt_dict['Foto'] = 'NO DISPONIBLE'


    return rt_dict
"""
def split_primero():
    alumnos_1o = Alumno.query.filter_by(grado=1).order_by(Alumno.id).all()
    c = 0

    for alumno in alumnos_1o:
        if c >= 98 and c <= 195:
            alumno.grupo = 'B'
            alumno.generar_matricula()
            db.session.commit()
        elif c > 195:
            alumno.grupo = 'C'
            alumno.generar_matricula()
            db.session.commit()

        c += 1
"""

def alumnos_to_excel(filename):
    alumnos = Alumno.query.all()
    lista_al = [alumno_to_dict(alumno) for alumno in alumnos]
    df = pd.DataFrame(lista_al)
    
    alumnos_1 = Alumno.query.filter_by(grado=1).all()
    lista_1 = [alumno_to_dict(alumno) for alumno in alumnos_1]
    df1 = pd.DataFrame(lista_1)

    alumnos_2o = Alumno.query.filter_by(grado=2).all()
    lista_2o = [alumno_to_dict(alumno) for alumno in alumnos_2o]
    df2 = pd.DataFrame(lista_2o)

    alumnos_3o = Alumno.query.filter_by(grado=3).all()
    lista_3o = [alumno_to_dict(alumno) for alumno in alumnos_3o]
    df3 = pd.DataFrame(lista_3o)

    alumnos_4o = Alumno.query.filter_by(grado=4).all()
    lista_4o = [alumno_to_dict(alumno) for alumno in alumnos_4o]
    df4 = pd.DataFrame(lista_4o)
    
    filename = os.path.join(app.config['EXCEL_PATH'], filename)
    writer = pd.ExcelWriter(filename)

    df.to_excel(writer, sheet_name='General', index=False)
    df1.to_excel(writer, sheet_name='1o', index=False)
    df2.to_excel(writer, sheet_name='2o', index=False)
    df3.to_excel(writer, sheet_name='3o', index=False)
    df4.to_excel(writer, sheet_name='Curso Esp.', index=False)

    writer.close()

def evangelizadores_to_excel():
    evangelizadores = Evangelizador.query.all()
    lista_evangelizadores = [evangelizador_to_dict(evangelizador) for evangelizador in evangelizadores]
    df = pd.DataFrame(lista_evangelizadores)

    filename = os.path.join(app.config['EXCEL_PATH'], 'lista_ev.xlsx')
    writer = pd.ExcelWriter(filename)

    df.to_excel(writer, sheet_name='Evangelizadores', index=False)

    writer.close()



def main():
    alumnos_to_excel()

if __name__ == '__main__':
    main()