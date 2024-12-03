from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Departamento, Gasto
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/generar_gastos', methods=['POST'])
def generar_gastos():
    data = request.get_json()
    mes = data.get('mes')
    año = data.get('año')
    monto = data.get('monto', 110000)

    departamentos = Departamento.query.all()
    for depto in departamentos:
        nuevo_gasto = Gasto(
            departamento_id=depto.id,
            mes=mes,
            año=año,
            monto=monto
        )
        db.session.add(nuevo_gasto)
    
    db.session.commit()
    return jsonify({"mensaje": "Gastos generados correctamente"}), 200


@app.route('/marcar_pagado', methods=['POST'])
def marcar_pagado():
    data = request.get_json()
    departamento_num = data.get('departamento')
    mes = data.get('mes')
    año = data.get('año')
    fecha_pago = data.get('fecha_pago')

    departamento = Departamento.query.filter_by(numero=departamento_num).first()
    if not departamento:
        return jsonify({"error": "Departamento no encontrado"}), 404

    gasto = Gasto.query.filter_by(departamento_id=departamento.id, mes=mes, año=año).first()
    if not gasto:
        return jsonify({"error": "Gasto no encontrado"}), 404

    if gasto.pagado:
        estado_transaccion = "Pago duplicado"
    else:
        gasto.pagado = True
        gasto.fecha_pago = datetime.strptime(fecha_pago, '%Y-%m-%d')
        db.session.commit()
        if str(gasto.fecha_pago.month) <= str(mes):
            estado_transaccion = "Pago exitoso dentro del plazo"
        else:
            estado_transaccion = "Pago exitoso fuera de plazo"

    return jsonify({"departamento": departamento_num, "estado": estado_transaccion}), 200


@app.route('/listar_pendientes', methods=['GET'])
def listar_pendientes():
    mes = request.args.get('mes')
    año = request.args.get('año')

    if not mes or not año:
        return jsonify({"error": "Los parámetros 'mes' y 'año' son obligatorios"}), 400

    pendientes = Gasto.query.filter(
        Gasto.pagado == False,
        (Gasto.año < año) | ((Gasto.año == año) & (Gasto.mes <= mes))
    ).order_by(Gasto.año, Gasto.mes).all()

    print(pendientes)

    if not pendientes:
        return jsonify({"mensaje": "Sin montos pendientes"}), 200

    resultado = []
    for gasto in pendientes:
        resultado.append({
            "departamento": gasto.departamento.numero,
            "periodo": f"{gasto.mes}/{gasto.año}",
            "monto": float(gasto.monto)
        })

    return jsonify(resultado), 200

if __name__ == '__main__':
    app.run(port=5000)
