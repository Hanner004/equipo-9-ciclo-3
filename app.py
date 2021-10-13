from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/admin/")
def admin():
    return render_template("admin.html")


@app.route("/user/")
@app.route("/user/profile/")
def userProfile():
    return render_template("userProfile.html", title='Perfil')

@app.route("/user/id/")
def editUser():
    return render_template("editUser.html", title='Editar usuario')


@app.route("/user/feedback/")
def userRetroalimentacion():
    return render_template("userRetro.html", title='Retroalimentación')


if __name__ == "__main__":
    app.run(debug=True)
