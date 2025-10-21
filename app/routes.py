import os, random, socket
from flask import Blueprint, jsonify, render_template
from data.pokeneas import pokeneas

bp = Blueprint('routes', __name__)

def container_id():
    # Hostname sirve como identificador del contenedor en Docker
    return socket.gethostname()

@bp.route('/')
def root():
    return jsonify({
        "ok": True,
        "endpoints": ["/pokenea/json", "/pokenea/view"]
    })

@bp.route('/pokenea/json')
def pokenea_json():
    p = random.choice(pokeneas)
    return jsonify({
        "id": p["id"],
        "nombre": p["nombre"],
        "altura": p["altura"],
        "habilidad": p["habilidad"],
        "container_id": container_id()
    })

@bp.route('/pokenea/view')
def pokenea_view():
    p = random.choice(pokeneas)
    return render_template('view.html', p=p, container_id=container_id())