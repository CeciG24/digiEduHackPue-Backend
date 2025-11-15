from datetime import datetime
from app import db

class Progress(db.Model):
    __tablename__ = 'progress'
    
    id_progreso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_ruta = db.Column(db.Integer, db.ForeignKey('rutaAprendizaje.id_ruta'), nullable=False)
    id_modulo = db.Column(db.Integer, db.ForeignKey('modulo.id_modulo'), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    calificacion = db.Column(db.Numeric(5, 2))
    fecha_ultimo_intento = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Progreso {self.id_progreso}>'
