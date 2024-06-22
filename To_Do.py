from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuración de la aplicación Flask y la base de datos SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost:3306/lista_todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo de datos Tarea
class Tarea(db.Model):
    __tablename__ = 'To_Do'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha_limite = db.Column(db.String(50))

    def a_dict(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'fecha_limite': self.fecha_limite
        }

# Creación de la base de datos y las tablas (si no existen)
db.create_all()
