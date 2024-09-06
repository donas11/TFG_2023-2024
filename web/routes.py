from flask_login import logout_user

# Define la ruta para el logout
@app.route('/logout')
def logout():
    logout_user()
    session.pop("usuario", None)  # Eliminar el usuario de la sesión
    return redirect(url_for("login"))