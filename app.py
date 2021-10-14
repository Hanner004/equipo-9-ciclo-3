from flask import Flask, render_template, request
from werkzeug.utils import redirect

app = Flask(__name__)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/user")
    else:
        return render_template("login.html", title="Iniciar sesión")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect("/login")
    else:
        return render_template("register.html", title="Registro")


@app.route("/users", methods=["GET"])
def users():
    return "USERS"


@app.route("/users/<int:id>", methods=["GET", "POST", "PUT", "DELETE"])
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
