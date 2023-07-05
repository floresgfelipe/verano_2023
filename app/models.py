from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from flask import session

APROBADO = 'ACREDITADO'
REPROBADO = 'NO ACREDITADO'

class Alumno(UserMixin, db.Model):
    __tablename__ = 'alumno'

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellido_p = db.Column(db.String(50), nullable=False)
    apellido_m = db.Column(db.String(50), nullable=False)
    dia_nac = db.Column(db.Integer,nullable=False)
    mes_nac = db.Column(db.String(20), nullable=False)
    año_nac = db.Column(db.Integer, nullable=False)
    decanato = db.Column(db.String(50), nullable=False)
    parroquia = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)    
    correo = db.Column(db.String(50), nullable=False)
    foto = db.Column(db.String(200), nullable=False, default='none')
    grado = db.Column(db.Integer, nullable=False)
    boleta_carta = db.Column(db.String(200), nullable=False, default='none')
    servicio = db.Column(db.String(2), nullable=False)
    calificacion1 = db.Column(db.Integer, default=-1)
    calificacion2 = db.Column(db.Integer, default=-1)

    def get_calificacion_primer_semestre(self):        
        if self.calificacion1 == 0:
            return REPROBADO
        elif self.calificacion1 == 1:
            return APROBADO
        else:
            return 'NO DISPONIBLE'

    def get_calificacion_segundo_semestre(self):
        if self.calificacion2 == 0:
            return REPROBADO
        elif self.calificacion2 == 1:
            return APROBADO
        else:
            return 'NO DISPONIBLE'
    
    def get_grado(self):
        if self.grado == 1:
            return 'Primero'
        elif self.grado == 2:
            return 'Segundo'
        elif self.grado == 3:
            return 'Tercero'
        else:
            return 'Curso Especializado'
    
    def __repr__(self) -> str:
        return f'<Alumno {self.id} {self.nombres} \
            {self.apellido_p} {self.apellido_m}>'
    
class Evangelizador(UserMixin, db.Model):
    __tablename__ = 'evangelizador'

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellido_p = db.Column(db.String(50), nullable=False)
    apellido_m = db.Column(db.String(50), nullable=False)
    dia_nac = db.Column(db.Integer,nullable=False)
    mes_nac = db.Column(db.String(20), nullable=False)
    año_nac = db.Column(db.Integer, nullable=False)
    decanato = db.Column(db.String(50), nullable=False)
    parroquia = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)    
    correo = db.Column(db.String(50), nullable=False)
    foto = db.Column(db.String(200), nullable=False, default='none')
    calificacion1 = db.Column(db.Integer, default=-1)
    calificacion2 = db.Column(db.Integer, default=-1)

    def get_calificacion_primer_semestre(self):        
        if self.calificacion1 == 0:
            return REPROBADO
        elif self.calificacion1 == 1:
            return APROBADO
        else:
            return 'NO DISPONIBLE'

    def get_calificacion_segundo_semestre(self):
        if self.calificacion2 == 0:
            return REPROBADO
        elif self.calificacion2 == 1:
            return APROBADO
        else:
            return 'NO DISPONIBLE'
    
    def __repr__(self) -> str:
        return f'<Evangelizador {self.id} {self.nombres} \
            {self.apellido_p} {self.apellido_m}>'

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rol = db.Column(db.String(30))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<Admin {self.email} rol: {self.rol}>'


@login.user_loader
def load_user(id):
    if session.get('account_type') == 'Admin':
        return Admin.query.get(int(id))
    elif session.get('account_type') == 'Alumno':
        return Alumno.query.get(int(id))
    elif session.get('account_type') == 'Evangelizador':
        return Evangelizador.query.get(int(id))
    else:
        return None





