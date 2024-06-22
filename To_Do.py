from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Configuración de la aplicación Flask y la base de datos SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost:3306/lista_todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo de Tarea
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

# Crear la base de datos y las tablas (si no existen)
db.create_all()

# Rutas de la API REST para la gestión de tareas

@app.route('/tareas', methods=['POST'])
def crear_tarea():
    """Crea una nueva tarea"""
    if not request.json or not 'descripcion' in request.json:
        abort(400)
    
    tarea = Tarea(
        descripcion=request.json['descripcion'],
        fecha_limite=request.json.get('fecha_limite', "")
    )
    
    try:
        db.session.add(tarea)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400)
    
    return jsonify({'tarea': tarea.a_dict()}), 201

@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    """Obtiene todas las tareas"""
    tareas = Tarea.query.all()
    return jsonify({'tareas': [tarea.a_dict() for tarea in tareas]})

@app.route('/tareas/<int:tarea_id>', methods=['GET'])
def obtener_tarea(tarea_id):
    """Obtiene una sola tarea por ID"""
    tarea = Tarea.query.get(tarea_id)
    if tarea is None:
        abort(404)
    return jsonify({'tarea': tarea.a_dict()})

@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    """Elimina una tarea por ID"""
    tarea = Tarea.query.get(tarea_id)
    if tarea is None:
        abort(404)
    
    db.session.delete(tarea)
    db.session.commit()
    
    return jsonify({'mensaje': f'Se ha eliminado exitosamente la tarea con ID {tarea_id}'})

@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def actualizar_tarea(tarea_id):
    """Modifica una tarea"""
    tarea = Tarea.query.get(tarea_id)
    if tarea is None:
        abort(404)
    
    if not request.json:
        abort(400)
    
    if 'descripcion' in request.json and not isinstance(request.json['descripcion'], str):
        abort(400)
    
    if 'fecha_limite' in request.json and not isinstance(request.json['fecha_limite'], str):
        abort(400)
    
    tarea.descripcion = request.json.get('descripcion', tarea.descripcion)
    tarea.fecha_limite = request.json.get('fecha_limite', tarea.fecha_limite)
    
    db.session.commit()
    
    return jsonify({'tarea': tarea.a_dict()})

# Punto de entrada de la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)


