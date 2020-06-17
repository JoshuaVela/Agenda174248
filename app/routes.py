from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, PostForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post

@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("agendas"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("agendas"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("No se encontro el usuario o la contraseña esta incorrecta")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash("Iniciaste sesion correctamente, Hola {}".format(form.username.data))
        return redirect("/agendas")
    return render_template("login.html",form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("agendas"))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("El usuario ya existe")
            return redirect(url_for("signup"))
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("El correo ya esta registrado")
            return redirect(url_for("signup"))
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash("Usuario creado exitosamente")
        return redirect("/login")
    return render_template("signup.html",form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/agendas")
@login_required
def agendas():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    # imprimir lo que mando desde newagendas
    contacs = Post.query.filter_by(users_id = current_user.id).all()
    return render_template("agendas.html", contacs = contacs)

@app.route("/newagendas", methods=["GET", "POST"])
@login_required
def newagendas():
    form = PostForm()
    if form.validate_on_submit():
        # Hacemos insesion de datos a la bdd
        p = Post()
        p.first_name = form.first_name.data
        p.last_name = form.last_name.data
        p.phone = form.phone.data
        p.email = form.email.data
        p.note = form.note.data
        p.users_id = current_user.id
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("agendas"))
    return render_template("newagendas.html", form=form)
# Se crea una ruta para elmiar con metodo post
@app.route("/newagendas/delete/<int:id>", methods=["POST"])
@login_required
def delete_agenda(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        if current_user.id == post.users_id:
            db.session.delete(post)
            db.session.commit()
        else:
            flash("No tienes permisos para borrar este contacto")
    else:
        flash("No existe")
    return redirect(url_for("agendas"))

# Se crea una ruta para editar con metodo post
@app.route("/newagendas/edit/<int:id>", methods=["POST"])
@login_required
def edit_agenda(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        if current_user.id == post.users_id:
            pass
            # Editar
            form = PostForm()
            if form.validate_on_submit():
                post.first_name = form.first_name.data
                post.last_name = form.last_name.data
                post.phone = form.phone.data  
                post.email = form.email.data  
                post.note = form.note.data
                db.session.add(post)
                db.session.commit()
                return redirect(url_for("agendas"))
            form.first_name.data = post.first_name
            form.last_name.data = post.last_name
            form.phone.data = post.phone
            form.email.data = post.email
            form.note.data = post.note
            form.submit.data = "Editar"
            return render_template("newagendas.html", form=form, edit=True)
        else:
            flash("No tienes permisos para borrar este contacto")
    else:
        flash("No existe")
    return redirect(url_for("agendas"))
    