import json
import os
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

RUTA = os.path.join(os.path.dirname(__file__), "data", "demos.json")


def _leer():
    with open(RUTA, encoding="utf-8") as f:
        return json.load(f)


def _guardar(data):
    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_proyecto():
    return _leer()["proyecto"]


def get_secciones():
    return _leer()["secciones"]


def get_seccion(id):
    for s in get_secciones():
        if s["id"] == id:
            return s
    return None


@app.route("/")
def inicio():
    return render_template("inicio.html", proyecto=get_proyecto())


@app.route("/entregables")
def entregables():
    return render_template("entregables.html", secciones=get_secciones())


@app.route("/entregables/<int:id>")
def entregable(id):
    seccion = get_seccion(id)
    if seccion is None:
        return "Entregable no encontrado", 404
    return render_template("entregable.html", seccion=seccion)


@app.route("/entregables/<int:id>/estado", methods=["POST"])
def actualizar_estado(id):
    nuevo_estado = request.form.get("estado")
    estados_validos = ["pendiente", "en_progreso", "completado"]
    if nuevo_estado not in estados_validos:
        return "Estado inválido", 400
    data = _leer()
    for s in data["secciones"]:
        if s["id"] == id:
            s["estado"] = nuevo_estado
    _guardar(data)
    return redirect(url_for("entregable", id=id))


@app.route("/desarrollos-peru")
def desarrollos_peru():
    data = _leer()
    return render_template("desarrollos-peru.html", enlaces=data["desarrollos_peru"])


@app.route("/acerca")
def acerca():
    return render_template("acerca.html", proyecto=get_proyecto())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
