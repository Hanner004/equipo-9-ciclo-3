from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    phone = db.Column(db.Integer)
    direction = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return "Usuario registrado " + str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@app.route("/", methods=["GET"])
def index():
    return redirect("/login/")


@app.route("/login/", methods=["GET"])
def getLogin():
    return render_template("login.html", title="Iniciar sesión")


@app.route("/login/", methods=["POST"])
def postLogin():
    email = escape(request.form["email"].strip())
    password = escape(request.form["password"].strip())
    if email == None or len(email) == 0 or password == None or len(password) == 0:
        flash("ERROR: Rellenar todos los campos")
        return render_template("login.html", title="Iniciar sesión")
    else:
        user = Users.query.filter_by(email=email).first()
        if check_password_hash(user.password, password) != True:
            flash("El inicio de sesión o la contraseña no son válidos")
            return render_template("login.html", title="Iniciar sesión")
        else:
            flash(f"Bienvenido {user.fullname}")
            return redirect("/dashboard/")


@app.route("/register/", methods=["GET", "POST"])
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
                user = Users(fullname=fullname, phone=phone, direction=direction, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash("Usuario registrado")
                return render_template('login.html')
            else:
                flash("Las contraseñas no coinciden")
                return render_template("register.html", title="Registro")
        else:
            flash("ERROR: Rellenar todos los campos")
            return render_template("register.html", title="Registro")
    else:
        return render_template("register.html", title="Registro")


@app.route("/dashboard/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/users/", methods=["GET"])
def users():
    return "USERS"


@app.route("/users/<int:id>/", methods=["GET", "POST", "PUT", "DELETE"])
def usersCRUD(id):
    if request.method == "GET":
        return f"USER {id}"
    elif request.method == "POST":
        return f"USER {id} CREATED"
    elif request.method == "PUT":
        return f"USER {id} UPDATED"
    elif request.method == "DELETE":
        return f"USER {id} DELETED"


@app.route("/admin/")
def admin():
    return render_template("admin.html")


@app.route("/admin/createemployee/")
def adminCreateEmployee():
    return render_template("adminCreateEmployee.html", title='CrearEmpleado')


@app.route("/user/")
@app.route("/user/profile/")
def userProfile():
    return render_template("userProfile.html", title='Perfil')


@app.route("/user/id/")
def editUser():
    return render_template("editUser.html", title='Editar usuario')


@app.route("/user/feedback/")
def userFeedback():
    return render_template("userFeedback.html", title='Retroalimentación')


if __name__ == "__main__":
    app.run(debug=True)
