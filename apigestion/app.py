# 0. ejecutamos pip install flask flask-sqlalchemy flask-migrate flask-cors
# 1. Crear modelos
# 2. importamos las librerias de flask
# 8. comando para iniciar mi app flask: flask db init
# 9. comando para migrar mis modelos:   flask db migrate
# 10. comando para crear nuestros modelos como tablas : flask db upgrade
# 11. comando para iniciar la app flask: flask run

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from models import db, Region, Comuna, Categoria, Producto, TipoPago, Venta, DetalleVenta, Usuario
    
# 3. instanciamos la app
app = Flask(__name__)
cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
#app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MusicProDB.db'

db.init_app(app)

Migrate(app, db)

# 5. Creamos la ruta por defecto para saber si mi app esta funcionado
# 6. ejecutamos el comando en la consola: python app.py o python3 app.py y revisamos nuestro navegador
@cross_origin()
@app.route('apigestion/')
def index():
    """Bienvenida a la API de MusicPro"""
    return 'MusicPro Api V 0.1'

########     CRUD para cada tabla   ########

#### Region ####

@cross_origin()
@app.route('/regiones', methods=['GET'])
def get_regiones():
    """Ruta para consultar todas las regiones"""
    regiones = Region.query.all()
    regiones = list(map(lambda region: region.serialize(), regiones))
    return jsonify(regiones), 200
    
@cross_origin()
@app.route('/agregar-region', methods=['POST'])
def agregar_region():
    """Ruta para agregar una region"""
    data = request.get_json()
    region = Region()
    region.nombre = data['nombre']
    region.save()
    return jsonify(region.serialize()), 201

@cross_origin()
@app.route('/regiones/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_region(id):
    """Ruta para consultar, actualizar y eliminar una region"""
    region = Region.query.get(id)
    if not region:
        return jsonify({"msg": "Region no encontrada"}), 404
    if request.method == 'GET':
        return jsonify(region.serialize()), 200
    if request.method == 'PUT':
        data = request.get_json()
        region.nombre = data['nombre']
        region.update()
        return jsonify(region.serialize()), 200
    if request.method == 'DELETE':
        region.delete()
        return jsonify({"msg": "Region eliminada"}), 200
    
#### Comuna ####

@cross_origin()
@app.route('/comunas', methods=['GET'])
def get_comunas():
    """Ruta para consultar todas las comunas"""
    comunas = Comuna.query.all()
    comunas = list(map(lambda comuna: comuna.serialize(), comunas))
    return jsonify(comunas), 200

@cross_origin()
@app.route('/agregar-comuna', methods=['POST'])
def agregar_comuna():
    """Ruta para agregar una comuna"""
    data = request.get_json()
    comuna = Comuna()
    comuna.nombre = data['nombre']
    comuna.id_region = data['id_region']
    comuna.save()
    return jsonify(comuna.serialize()), 201

@cross_origin()
@app.route('/comunas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_comuna(id):
    """Ruta para consultar, actualizar y eliminar una comuna"""
    comuna = Comuna.query.get(id)
    if not comuna:
        return jsonify({"msg": "Comuna no encontrada"}), 404
    if request.method == 'GET':
        return jsonify(comuna.serialize()), 200
    if request.method == 'PUT':
        data = request.get_json()
        comuna.nombre = data['nombre']
        comuna.id_region = data['id_region']
        comuna.update()
        return jsonify(comuna.serialize()), 200
    if request.method == 'DELETE':
        comuna.delete()
        return jsonify({"msg": "Comuna eliminada"}), 200

#### Categoria ####

@cross_origin()
@app.route('/categorias', methods=['GET'])
def get_categorias():
    """Ruta para consultar todas las categorias"""
    categorias = Categoria.query.all()
    categorias = list(map(lambda categoria: categoria.serialize(), categorias))
    return jsonify(categorias), 200

@cross_origin()
@app.route('/agregar-categoria', methods=['POST'])
def agregar_categoria():
    """Ruta para agregar una categoria"""
    data = request.get_json()
    categoria = Categoria()
    categoria.nombre = data['nombre']
    categoria.save()
    return jsonify(categoria.serialize()), 201

@cross_origin()
@app.route('/categorias/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_categoria(id):
    """Ruta para consultar, actualizar y eliminar una categoria"""
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({"msg": "Categoria no encontrada"}), 404
    if request.method == 'GET':
        return jsonify(categoria.serialize()), 200
    if request.method == 'PUT':
        data = request.get_json()
        categoria.nombre = data['nombre']
        categoria.update()
        return jsonify(categoria.serialize()), 200
    if request.method == 'DELETE':
        categoria.delete()
        return jsonify({"msg": "Categoria eliminada"}), 200
    
#### Producto ####

@cross_origin()
@app.route('/productos', methods=['GET'])
def get_productos():
    """Ruta para consultar todos los productos"""
    productos = Producto.query.all()
    productos = list(map(lambda producto: producto.serialize(), productos))
    #opcional con imagen
    #productos = list(map(lambda producto: producto.serialize_with_image(), productos))
    return jsonify(productos), 200

@cross_origin()
@app.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    """Ruta para agregar un producto desde formulario"""
    data = request.values
    img = request.files['imagen']
    producto = Producto()
    producto.marca = data['marca']
    producto.cod_producto = producto.marca+'-'+data['cod_producto']
    producto.serie_producto = data['serie_producto']
    producto.nombre = producto.marca+'-'+producto.serie_producto
    producto.descripcion = data['descripcion']
    producto.precio = data['precio']
    producto.stock = data['stock']
    producto.precio_dolar = data['precio_dolar']
    producto.id_categoria = data['id_categoria']
    producto.imagen = img.read()
    producto.save()
    return jsonify(producto.serialize()), 201

@cross_origin()
@app.route('/productos/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_producto(id):
    """Ruta para consultar, actualizar y eliminar un producto"""
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({"msg": "Producto no encontrado"}), 404
    if request.method == 'GET':
        return jsonify(producto.serialize()), 200
    if request.method == 'PUT':
        data = request.get_json()
        producto.marca = data['marca']
        producto.cod_producto = producto.marca+'-'+data['cod_producto']
        producto.serie_producto = data['serie_producto']
        producto.nombre = producto.marca+'-'+producto.serie
        producto.descripcion = data['descripcion']
        producto.precio = data['precio']
        producto.stock = data['stock']
        producto.precio_dolar = data['precio_dolar']
        producto.id_categoria = data['id_categoria']
        producto.update()
        return jsonify(producto.serialize()), 200
    if request.method == 'DELETE':
        producto.delete()
        return jsonify({"msg": "Producto eliminado"}), 200
    
#### TipoPago ####

@cross_origin()
@app.route('/tipos-pago', methods=['GET'])
def get_tipos_pago():
    """Ruta para consultar todos los tipos de pago"""
    tipos_pago = TipoPago.query.all()
    tipos_pago = list(map(lambda tipo_pago: tipo_pago.serialize(), tipos_pago))
    return jsonify(tipos_pago), 200

@cross_origin()
@app.route('/agregar-tipo-pago', methods=['POST'])
def agregar_tipo_pago():
    """Ruta para agregar un tipo de pago"""
    data = request.get_json()
    tipo_pago = TipoPago()
    tipo_pago.nombre = data['nombre']
    tipo_pago.save()
    return jsonify(tipo_pago.serialize()), 201

@cross_origin()
@app.route('/tipos-pago/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_tipo_pago(id):
    """Ruta para consultar, actualizar y eliminar un tipo de pago"""
    tipo_pago = TipoPago.query.get(id)
    if not tipo_pago:
        return jsonify({"msg": "Tipo de pago no encontrado"}), 404
    if request.method == 'GET':
        return jsonify(tipo_pago.serialize()), 200
    if request.method == 'PUT':
        data = request.get_json()
        tipo_pago.nombre = data['nombre']
        tipo_pago.update()
        return jsonify(tipo_pago.serialize()), 200
    if request.method == 'DELETE':
        tipo_pago.delete()
        return jsonify({"msg": "Tipo de pago eliminado"}), 200
    
#### Venta ####

@cross_origin()
@app.route('/ventas', methods=['GET'])
def get_ventas():
    """Ruta para consultar todas las ventas"""
    ventas = Venta.query.all()
    ventas = list(map(lambda venta: venta.serialize(), ventas))
    return jsonify(ventas), 200

@cross_origin()
@app.route('/agregar-venta', methods=['POST'])
def agregar_venta():
    """Ruta para agregar una venta"""
    data = request.get_json()
    venta = Venta()
    venta.total = data['total']
    venta.id_tipo_pago = data['id_tipo_pago']
    venta.id_usuario = data['id_usuario']
    venta.save()
    return jsonify(venta.serialize()), 201

@cross_origin()
@app.route('/ventas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_venta(id):
    """Ruta para consultar, actualizar y eliminar una venta"""
    venta = Venta.query.get(id)
    if not venta:
        return jsonify({"msg": "Venta no encontrada"}), 404
    if request.method == 'GET':
        return jsonify(venta.serialize()), 200
    if request.method == 'PUT':
        data = request.get_json()
        venta.total = data['total']
        venta.fecha = data['fecha']
        venta.id_tipo_pago = data['id_tipo_pago']
        venta.id_usuario = data['id_usuario']
        venta.update()
        return jsonify(venta.serialize()), 200
    if request.method == 'DELETE':
        venta.delete()
        return jsonify({"msg": "Venta eliminada"}), 200
    
#### DetalleVenta ####

@cross_origin()
@app.route('/detalles-venta', methods=['GET'])
def get_detalles_venta():
    """Ruta para consultar todos los detalles de venta"""
    detalles_venta = DetalleVenta.query.all()
    detalles_venta = list(map(lambda detalle_venta: detalle_venta.serialize(), detalles_venta))
    return jsonify(detalles_venta), 200

@cross_origin()
@app.route('/agregar-detalle-venta', methods=['POST'])
def agregar_detalle_venta():
    """Ruta para agregar un detalle de venta"""
    data = request.get_json()
    detalle_venta = DetalleVenta()
    detalle_venta.cantidad = data['cantidad']
    detalle_venta.valor = data['valor']
    detalle_venta.id_venta = data['id_venta']
    detalle_venta.cod_producto = data['cod_producto']
    detalle_venta.descuento = data['descuento']
    detalle_venta.save()
    return jsonify(detalle_venta.serialize()), 201

@cross_origin()
@app.route('/detalles-venta/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_detalle_venta(id):
    """Ruta para consultar, actualizar y eliminar un detalle de venta"""
    detalle_venta = DetalleVenta.query.get(id)
    if not detalle_venta:
        return jsonify({"msg": "Detalle de venta no encontrado"}), 404
    if request.method == 'GET':
        return jsonify(detalle_venta.serialize()), 200
    if request.method == 'PUT':
        data = request.get_json()
        detalle_venta.cantidad = data['cantidad']
        detalle_venta.valor = data['valor']
        detalle_venta.id_venta = data['id_venta']
        detalle_venta.cod_producto = data['cod_producto']
        detalle_venta.descuento = data['descuento']
        detalle_venta.update()
        return jsonify(detalle_venta.serialize()), 200
    if request.method == 'DELETE':
        detalle_venta.delete()
        return jsonify({"msg": "Detalle de venta eliminado"}), 200
    
#### Usuario ####

@cross_origin()
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    """Ruta para consultar todos los usuarios"""
    usuarios = Usuario.query.all()
    usuarios = list(map(lambda usuario: usuario.serialize(), usuarios))
    return jsonify(usuarios), 200

@cross_origin()
@app.route('/agregar-usuario', methods=['POST'])
def agregar_usuario():
    """Ruta para agregar un usuario"""
    data = request.get_json()
    usuario = Usuario()
    usuario.nombres = data['nombres']
    usuario.apellidos = data['apellidos']
    usuario.domicilio = data['domicilio']
    usuario.id_comuna = data['id_comuna']
    usuario.fono = data['fono']
    usuario.nombre_usuario = data['nombre_usuario']
    usuario.password = data['password'] #TODO: encriptar password
    usuario.tipo = data['tipo']
    usuario.save()
    return jsonify(usuario.serialize()), 201

@cross_origin()
@app.route('/usuarios/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_usuario(id):
    """Ruta para consultar, actualizar y eliminar un usuario"""
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    if request.method == 'GET':
        return jsonify(usuario.serialize()), 200
    if request.method == 'PUT':
        data = request.get_json()
        usuario.nombres = data['nombres']
        usuario.apellidos = data['apellidos']
        usuario.domicilio = data['domicilio']
        usuario.id_comuna = data['id_comuna']
        usuario.fono = data['fono']
        usuario.nombre_usuario = data['nombre_usuario']
        usuario.password = data['password']
        usuario.tipo = data['tipo']
        usuario.update()
        return jsonify(usuario.serialize()), 200
    if request.method == 'DELETE':
        usuario.delete()
        return jsonify({"msg": "Usuario eliminado"}), 200
    
############# Metodos Utilitarios #############
    
#### Login ####

#TODO: crear token
@cross_origin()
@app.route('/login', methods=['POST'])
def login():
    """Ruta para iniciar sesion"""
    data = request.get_json()
    usuario = Usuario.query.filter_by(nombre_usuario=data['nombre_usuario']).first()
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    if usuario.password != data['password']:
        return jsonify({"msg": "Contraseña incorrecta"}), 404
    return jsonify(usuario.serialize()), 200

# 4. Configurar los puertos nuestra app 
if __name__ == '__main__':
    app.run(port=5000, debug=True)


