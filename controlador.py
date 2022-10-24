from flask import Flask, render_template, request, redirect,session, flash
import models

app = Flask(__name__)
app.secret_key = b'\xaa\xe4V}y~\x84G\xb5\x95\xa0\xe0\x96\xca\xa7\xe7'
"""
Definición de rutas
"""

# Formulario para iniciar sesión

@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

# Manejar login


@app.route("/hacer_login", methods=["POST"])
def hacer_login():
    correo = request.form["correo"]
    palabra_secreta = request.form["palabra_secreta"]
    # Aquí comparamos. Lo hago así de fácil por simplicidad
    # En la vida real debería ser con una base de datos y una contraseña hasheada
    if correo == "hola@admin.com" and palabra_secreta == "1234":
        # Si coincide, iniciamos sesión y además redireccionamos
        session["usuario"] = correo
        # Aquí puedes colocar más datos. Por ejemplo
        # session["nivel"] = "administrador"
        return redirect("/juegos")
    else:
        # Si NO coincide, lo regresamos
        flash("Correo o contraseña incorrectos")
        return redirect("/login")


# Cerrar sesión
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")


# Un "middleware" que se ejecuta antes de responder a cualquier ruta. Aquí verificamos si el usuario ha iniciado sesión
@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'usuario' in session and ruta != "/login" and ruta != "/hacer_login" and ruta != "/logout" and not ruta.startswith("/static"):
        flash("Inicia sesión para continuar")
        return redirect("/login")
    # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar
    
@app.route('/agradecimiento') #Decoramos con método routes la próxima función arguementando la url "/agradecimiento"
def agradecer(): #Definimos una función llamada agradecer
    return 'Gracias https://pythones.net/ y a https://parzibyte.me/blog' #Retorno de la función

@app.route("/agregar_juego")
def formulario_agregar_juego():
    return render_template("agregar_juego.html")


@app.route("/guardar_juego", methods=["POST"])
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    models.insertar_juego(nombre, descripcion, precio)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/juegos")



@app.route("/juegos")
def juegos():
    juegos = models.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)


@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    models.eliminar_juego(request.form["id"])
    return redirect("/juegos")


@app.route("/formulario_editar_juego/<int:id>")
def editar_juego(id):
    # Obtener el juego por ID
    juego = models.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)


@app.route("/actualizar_juego", methods=["POST"])
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    models.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")


# Iniciar el app

if __name__ == "__main__":#Condicional de que si la aplicación ejecutada se coincide al nombre de la aplicación
    app.run(host='0.0.0.0', port=8000, debug=True)#Método que inicia la app con la dirección, puertos y modo de argumentos
