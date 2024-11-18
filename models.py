from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Departamento(db.Model):
    __tablename__ = 'departamentos'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), nullable=False)
    gastos = db.relationship('Gasto', backref='departamento', lazy=True) 

class Gasto(db.Model):
    __tablename__ = 'gastos'
    id = db.Column(db.Integer, primary_key=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    año = db.Column(db.Integer, nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    pagado = db.Column(db.Boolean, default=False)
    fecha_pago = db.Column(db.Date, nullable=True)
    