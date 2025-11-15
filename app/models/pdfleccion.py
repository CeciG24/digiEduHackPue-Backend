from datetime import datetime
from app import db

class PDFLeccion(db.Model):
    __tablename__ = 'pdfleccion'
    
    id_pdf = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_leccion = db.Column(db.Integer, db.ForeignKey('leccion.id_leccion'), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    url_pdf = db.Column(db.String(255), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)

    leccion = db.relationship('Leccion', backref=db.backref('pdfs', lazy=True))

    def __repr__(self):
        return f'<PDFLeccion {self.id_pdf}>'