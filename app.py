from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "Equipo-9"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    phone = db.Column(db.Integer)
    direction = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    profileId = db.Column(db.Integer, db.ForeignKey('profile.id'))

    def __repr__(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fIngreso = db.Column(db.Date)
    tContrato = db.Column(db.String)
    fTermino = db.Column(db.Date)
    salario = db.Column(db.Integer)
    user = db.relationship("User", backref="profile", uselist=False)


@app.route("/", methods=["GET"])
def index():
    return redirect("/auth/login/")


@app.route("/auth/login/", methods=["GET"])
def getLogin():
    session.clear()
    return render_template("auth/login.html", title="Iniciar sesión")


@app.route("/auth/login/", methods=["POST"])
def postLogin():
    email = escape(request.form["email"].strip())
    password = escape(request.form["password"].strip())
    if email == None or len(email) == 0 or password == None or len(password) == 0:
        flash("ERROR: Rellenar todos los campos")
        return render_template("auth/login.html", title="Iniciar sesión")
    else:
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password) != True:
                flash("El inicio de sesión o la contraseña no son válidos")
                return render_template("auth/login.html", title="Iniciar sesión")
            else:
                flash(f"Bienvenido {user.fullname}")
                session['id'] = user.id
                session['role'] = "Administrador"
                return redirect("/dashboard/")
        else:
            flash("El correo no se encuentra registrado en el sistema")
            return render_template("auth/login.html", title="Iniciar sesión")


@app.route("/auth/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        isValid = True
        fullname = escape(request.form["fullname"].strip())
        phone = escape(request.form["phone"].strip())
        direction = escape(request.form["direction"].strip())
        email = escape(request.form["email"].strip())
        password = escape(request.form["password"].strip())
        confirm = escape(request.form["confirm"].strip())
        if fullname == None or len(fullname) == 0:
            isValid = False
        if phone == None or len(phone) == 0:
            isValid = False
        if direction == None or len(direction) == 0:
            isValid = False
        if email == None or len(email) == 0:
            isValid = False
        if password == None or len(password) == 0:
            isValid = False
        if confirm == None or len(confirm) == 0:
            isValid = False
        if isValid:
            if password == confirm:
                user = User.query.filter_by(email=email).first()
                if user:
                    flash("El correo ya se encuentra registrado en el sistema")
                    return render_template("auth/register.html")
                else:
                    # datos-perfil
                    newProfile = Profile(salario= 1000)
                    db.session.add(newProfile)
                    db.session.commit()
                    # datos-usuario
                    newUser = User(fullname=fullname, phone=phone, direction=direction, email=email, profileId= newProfile.id)
                    newUser.set_password(password)
                    db.session.add(newUser)
                    db.session.commit()
                    flash("Usuario registrado")
                    return render_template('auth/login.html')
            else:
                flash("Las contraseñas no coinciden")
                return render_template("auth/register.html", title="Registro")
        else:
            flash("ERROR: Rellenar todos los campos")
            return render_template("auth/register.html", title="Registro")
    else:
        return render_template("auth/register.html", title="Registro")


@app.route("/dashboard/", methods=["GET"])
def dashboard():
    role = session['role']
    return render_template("dashboard.html", role=role)


@app.route("/dashboard/role/", methods=["GET"])
def role():
    role = session['role']
    if role == "Superadministrador":
        return render_template("dashboard/role.html", role=role)
    else:
        flash("No estás autorizado")
        return render_template("dashboard.html", role=role)


@app.route("/dashboard/users/", methods=["GET"])
def users():
    role = session['role']
    if role == "Superadministrador":
        return render_template("dashboard/users.html", role=role)
    elif role == "Administrador":
        return render_template("dashboard/users.html", role=role)
    else:
        flash("No estas autorizado")
        return render_template("dashboard.html", role=role)


@app.route("/dashboard/profile/", methods=["GET"])
def profile():
    role = session['role']
    return render_template("dashboard/profile.html", role=role)


@app.route("/dashboard/feedback/", methods=["GET"])
def feedback():
    role = session['role']
    if role == "Empleado":
        return render_template("dashboard/feedback.html", role=role)
    else:
        flash("No eres un empleado")
        return render_template("dashboard.html", role=role)


@app.route("/logout/", methods=["GET"])
def logout():
    session.clear()
    return redirect("/auth/login")


# @app.route("/users/", methods=["GET"])
# def users():
#     return "USERS"


# @app.route("/users/<int:id>/", methods=["GET", "POST", "PUT", "DELETE"])
# def usersCRUD(id):
#     if request.method == "GET":
#         return f"USER {id}"
#     elif request.method == "POST":
#         return f"USER {id} CREATED"
#     elif request.method == "PUT":
#         return f"USER {id} UPDATED"
#     elif request.method == "DELETE":
#         return f"USER {id} DELETED"


# @app.route("/admin/")
# def admin():
#     return render_template("admin.html")

# @app.route("/admin/createemployee/")
# def adminCreateEmployee():
#     return render_template("adminCreateEmployee.html", title='CrearEmpleado')
# @app.route("/user/")
# @app.route("/user/profile/")
# def userProfile():
#     return render_template("userProfile.html", title='Perfil')
# @app.route("/user/id/")
# def editUser():
#     return render_template("editUser.html", title='Editar usuario')
# @app.route("/user/feedback/")
# def userFeedback():
#     return render_template("userFeedback.html", title='Retroalimentación')
if __name__ == "__main__":
    app.run(debug=True)
