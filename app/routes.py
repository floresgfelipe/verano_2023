import imghdr
import os
from app import app, db
from functools import wraps
from flask import (
    redirect, 
    render_template, 
    url_for, 
    flash, 
    session,
    request,
    redirect,
    url_for,
    abort,
    send_from_directory,
    send_file,
)
from flask_login import current_user, login_user, logout_user
from app.models import Alumno, Admin, Evangelizador
from app.to_xlsx import alumnos_to_excel
from app.genera_boletas import create_pdf
from app.forms import (
    LoginForm,
    RegisterForm, 
    UploadForm, 
    AdminLoginForm,
    RegisterFormEvangelizador,
    EvangelizadorLoginForm,
)
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
from sqlalchemy import func

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

def login_required_alumno(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('account_type') != 'Alumno':
            return redirect(url_for('entrar', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('account_type') != 'Admin':
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def login_required_evangelizador(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('account_type') != 'Evangelizador':
            return redirect(url_for('entrar_ev', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/cambia-calificacion', methods=['POST'])
@login_required_admin
def cambia_calificacion():
    data = request.get_json()
    alumno = Alumno.query.get(int(data['alumno_id']))

    if data['semestre'] == 1:
        alumno.calificacion1 = data['calificacion']
    elif data['semestre'] == 2:
        alumno.calificacion2 = data['calificacion']

    db.session.commit()

    return data

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if current_user.is_authenticated and session['account_type'] == 'Alumno':
        return redirect(url_for('perfil'))

    form = LoginForm()
    if form.validate_on_submit():
        alumnos = Alumno.query.filter(
            func.lower(
                Alumno.apellido_p
            ) == func.lower(str(form.apellido_p.data).strip()),
            func.lower(
                Alumno.apellido_m
            ) == func.lower(str(form.apellido_m.data).strip())
        ).all()   
        if len(alumnos) == 0:
            flash('No hay ningún alumno con esos apellidos')
            return redirect(url_for('entrar'))
        else:
            for alumno in alumnos:
                if (
                    str(alumno.dia_nac) == str(form.dia_nac.data) and
                    str(alumno.mes_nac) == str(form.mes_nac.data) and
                    str(alumno.año_nac) == str(form.año_nac.data)
                ):  
                    login_user(alumno, remember=True)
                    session['account_type'] = 'Alumno'
                    return redirect(url_for('perfil'))

            flash('Fecha de nacimiento incorrecta')
            return redirect(url_for('entrar'))
    
    return render_template('entrar.html', title='Entrar al Curso', form=form)

@app.route('/entrar_ev', methods=['GET', 'POST'])
def entrar_ev():
    if current_user.is_authenticated and session['account_type'] == 'Evangelizador':
        return redirect(url_for('perfil_ev'))

    form = EvangelizadorLoginForm()
    if form.validate_on_submit():
        evangelizadores = Evangelizador.query.filter(
            func.lower(
                Evangelizador.apellido_p
            ) == func.lower(str(form.apellido_p.data).strip()),
            func.lower(
                Evangelizador.apellido_m
            ) == func.lower(str(form.apellido_m.data).strip())
        ).all()   
        if len(evangelizadores) == 0:
            flash('No hay ningún evangelizador con esos apellidos')
            return redirect(url_for('entrar_ev'))
        else:
            for evangelizador in evangelizadores:
                if (
                    str(evangelizador.dia_nac) == str(form.dia_nac.data) and
                    str(evangelizador.mes_nac) == str(form.mes_nac.data) and
                    str(evangelizador.año_nac) == str(form.año_nac.data)
                ):  
                    login_user(evangelizador, remember=True)
                    session['account_type'] = 'Evangelizador'
                    return redirect(url_for('perfil_ev'))

            flash('Fecha de nacimiento incorrecta')
            return redirect(url_for('entrar_ev'))
    
    return render_template('entrar_ev.html', title='Entrar al Curso', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and session['account_type'] == 'Admin':
        return redirect(url_for('admin'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()    
        if admin is None or not admin.check_password(form.contraseña.data):
            flash('Correo o contraseña inválidos')
            return redirect(url_for('login'))
            
        login_user(admin, remember=True)
        session['account_type'] = 'Admin'
        return redirect(url_for('admin'))
    
    return render_template(
        'login.html', 
        title='Admin', 
        form=form, 
    )

@app.route('/verano', methods=['GET', 'POST'])
def verano():
    if current_user.is_authenticated and session['account_type'] == 'Alumno':
        return redirect(url_for('perfil'))

    form = RegisterForm()

    if form.validate_on_submit():

        alumno = Alumno(
            nombres = form.nombres.data.strip(),
            apellido_p = form.apellido_p.data.strip(),
            apellido_m = form.apellido_m.data.strip(),
            dia_nac = form.dia_nac.data,
            mes_nac = form.mes_nac.data,
            año_nac = form.año_nac.data,
            decanato = form.decanato.data.strip(),
            parroquia = form.parroquia.data.strip(),
            telefono = form.telefono.data,
            correo = form.correo.data.strip(),
            grado = form.grado.data,
            servicio = form.servicio.data
        )

        db.session.add(alumno)
        db.session.commit()

        login_user(alumno, remember=True)
        session['account_type'] = 'Alumno'
        flash('¡Felicidades! Te has inscrito en el Curso de Verano 2023 de la \
               Escuela Diocesana de Catequesis')
        return redirect(url_for('perfil'))  
    
    return render_template(
        'verano.html',
        title='Registro al Curso de Verano',
        form=form
    )

@app.route('/evangelizacion', methods=['GET', 'POST'])
def evangelizacion():
    if current_user.is_authenticated and session['account_type'] == 'Evangelizador':
        return redirect(url_for('perfil_ev'))

    form = RegisterFormEvangelizador()

    if form.validate_on_submit():

        evangelizador = Evangelizador(
            nombres = form.nombres.data.strip(),
            apellido_p = form.apellido_p.data.strip(),
            apellido_m = form.apellido_m.data.strip(),
            dia_nac = form.dia_nac.data,
            mes_nac = form.mes_nac.data,
            año_nac = form.año_nac.data,
            decanato = form.decanato.data.strip(),
            parroquia = form.parroquia.data.strip(),
            telefono = form.telefono.data,
            correo = form.correo.data.strip(),
        )

        db.session.add(evangelizador)
        db.session.commit()

        login_user(evangelizador, remember=True)
        
        session['account_type'] = 'Evangelizador'
        flash('¡Felicidades! Te has inscrito en el curso de Evangelización')
        return redirect(url_for('perfil_ev'))  
    
    return render_template(
        'evangelizacion.html',
        title='Registro al Curso de Evangelización',
        form=form
    )

@app.route('/logout')
def logout():
    session.pop('account_type', None)
    logout_user()
    return redirect(url_for('index'))

@app.route('/perfil')
@login_required_alumno
def perfil():
    return render_template(
        'perfil.html', 
        title='Perfil del Alumno', 
        basename=os.path.basename
    )

@app.route('/perfil_ev')
@login_required_evangelizador
def perfil_ev():
    return render_template(
        'perfil_ev.html', 
        title='Perfil del Evangelizador', 
        basename=os.path.basename
    )

@app.route('/subir-foto', methods=['GET', 'POST'])
@login_required_alumno
def subir_foto():
    form = UploadForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            uploaded_file = form.file.data
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                file_ext = str.lower(file_ext)
                if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                        file_ext != validate_image(uploaded_file.stream):
                    abort(400)

                saved_filename = os.path.join(
                        app.config['UPLOAD_PATH_FOTOS'], 
                        current_user.get_id() + file_ext
                    )
                
                pic = Image.open(uploaded_file)
                pic = ImageOps.exif_transpose(pic)
                pic.thumbnail((1200,1200))

                pic.save(saved_filename)
                
                current_user.foto = saved_filename
                db.session.commit()
            
            flash('La foto se ha subido exitosamente')
            return redirect(url_for('perfil'))
    return render_template('subir.html', title='Subir Foto', form=form)

@app.route('/subir-foto-ev', methods=['GET', 'POST'])
@login_required_evangelizador
def subir_foto_ev():
    form = UploadForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            uploaded_file = form.file.data
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                file_ext = str.lower(file_ext)
                if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                        file_ext != validate_image(uploaded_file.stream):
                    abort(400)

                saved_filename = os.path.join(
                        app.config['UPLOAD_PATH_FOTOS_EV'], 
                        current_user.get_id() + file_ext
                    )
                
                pic = Image.open(uploaded_file)
                pic = ImageOps.exif_transpose(pic)
                pic.thumbnail((1200,1200))

                pic.save(saved_filename)
                
                current_user.foto = saved_filename
                db.session.commit()
            
            flash('La foto se ha subido exitosamente')
            return redirect(url_for('perfil_ev'))
    return render_template('subir.html', title='Subir Foto', form=form)

@app.route('/fotos/<filename>')
@login_required_alumno
def fotos(filename):
    return send_from_directory(app.config['UPLOAD_PATH_FOTOS'], filename)

@app.route('/fotos_ev/<filename>')
@login_required_evangelizador
def fotos_ev(filename):
    return send_from_directory(app.config['UPLOAD_PATH_FOTOS_EV'], filename)

@app.route('/subir-boleta', methods=['GET', 'POST'])
@login_required_alumno
def subir_boleta():
    form = UploadForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            uploaded_file = form.file.data
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                file_ext = str.lower(file_ext)
                if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                        file_ext != validate_image(uploaded_file.stream):
                    abort(400)

                saved_filename = os.path.join(
                        app.config['UPLOAD_PATH_BOLETAS'], 
                        current_user.get_id() + file_ext
                    )

                pic = Image.open(uploaded_file)
                pic = ImageOps.exif_transpose(pic)
                pic.thumbnail((1200,1200))

                pic.save(saved_filename)
                
                current_user.boleta_carta = saved_filename
                db.session.commit()

            flash('La boleta se ha subido exitosamente')
            return redirect(url_for('perfil'))
    return render_template('subir.html', title='Subir Foto', form=form)

@app.route('/boletas/<filename>')
@login_required_alumno
def boletas(filename):
    return send_from_directory(app.config['UPLOAD_PATH_BOLETAS'], filename)


    
@app.route('/admin')
@login_required_admin
def admin():
    alumnos = Alumno.query
    return render_template(
        'admin.html',
        alumnos=alumnos,
        basename=os.path.basename,
    )

@app.route('/admin_ev')
@login_required_admin
def admin_ev():
    evangelizadores = Evangelizador.query
    return render_template(
        'admin_ev.html',
        evangelizadores=evangelizadores,
        basename=os.path.basename,
    )

@app.route('/fotos_admin/<filename>')
@login_required_admin
def fotos_admin(filename):
    return send_from_directory(app.config['UPLOAD_PATH_FOTOS'], filename)

@app.route('/fotos_admin_ev/<filename>')
@login_required_admin
def fotos_admin_ev(filename):
    return send_from_directory(app.config['UPLOAD_PATH_FOTOS_EV'], filename)

@app.route('/boletas_admin/<filename>')
@login_required_admin
def boletas_admin(filename):
    return send_from_directory(app.config['UPLOAD_PATH_BOLETAS'], filename)

@app.route('/excel/<filename>')
@login_required_admin
def send_excel(filename):
    alumnos_to_excel(filename)
    return send_from_directory(app.config['EXCEL_PATH'], filename)

@app.route('/descargar-boleta', methods=['POST'])
@login_required_admin
def descargar_boleta():
    data = request.get_json()
    c1 = "ACREDITADO" if data['calificacion1'] == 1 else "NO ACREDITADO" if data['calificacion1'] == 2 else ''
    c2 = "ACREDITADO" if data['calificacion2'] == 1 else "NO ACREDITADO" if data['calificacion2'] == 2 else ''

    return send_file(
        create_pdf(
        nombre=data['nombre'], 
        parroquia=data['parroquia'], 
        decanato=data['decanato'], 
        grado=str(data['grado']),
        calificacion1=c1,
        calificacion2=c2,
        )
    )
