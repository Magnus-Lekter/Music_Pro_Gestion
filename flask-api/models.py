"""Modelos para la base de datos de MusicPro"""

import base64
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#Tablas que usaremos en el proyecto music Pro:

class Usuario(db.Model):
    __tablename__ = 'usuario'
    rut = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(250), nullable= False)
    apellidos = db.Column(db.String(250), nullable= False)
    domicilio = db.Column(db.String(250), nullable= True)
    id_comuna = db.Column(db.Integer, db.ForeignKey('comuna.id_comuna'), nullable= True)
    fono = db.Column(db.Integer, nullable= True)
    email = db.Column(db.String(250), nullable= False)
    password = db.Column(db.String(250), nullable= False)
    estado = db.Column(db.Integer, nullable= False)  #0: inactivo, 1: activo
    tipo = db.Column(db.Integer, nullable= False) #1: cliente, 2: Vendedor, 3: Bodeguero, 4: Contador, 5: Administrador

    def __str__(self):
        return f"Rut Usuario: {self.rut}, Nombres: {self.nombres}, Apellidos: {self.apellidos}, Domicilio: {self.domicilio}, id comuna: {self.id_comuna}, fono: {self.fono}, email: {self.email}, estado: {self.estado}, id Privilegios: {self.tipo}"
    def serialize(self):
        return{
            "Rut Usuario": self.rut,
            "Nombres":self.nombres,
            "Apellidos":self.apellidos,
            "Domicilio":self.domicilio,
            "id comuna": self.id_comuna,
            "fono": self.fono,
            "email": self.email,
            "estado": self.estado,
            "id Privilegios": self.tipo 
        }
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Region(db.Model):
    __tablename__ = 'region'
    id_region = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable= False)

    def __str__(self):
        return f"id_region: {self.id_region}, nombre Region: {self.nombre}"
    
    def serialize(self):
        return{
            "id_region": self.id_region,
            "nombre": self.nombre,
            }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Comuna(db.Model):
    __tablename__ = 'comuna'
    id_comuna = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable= False)
    id_region = db.Column(db.Integer, db.ForeignKey('region.id_region'), nullable= False)

    def __str__(self):
        return f"id_comuna: {self.id_comuna}, nombre Comuna: {self.nombre}, id Region: {self.id_region}"
    
    def serialize(self):
        return{
            "id_comuna": self.id_comuna,
            "nombre": self.nombre,
            "id Region": self.id_region
            }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Categoria(db.Model): #Cuerdas, Percusion, Amplificadores, Varios.
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable= False)

    def __str__(self):
        return f"id_categoria: {self.id_categoria}, nombre Categoria: {self.nombre}"
    
    def serialize(self):
        return{
            "id_categoria": self.id_categoria,
            "nombre": self.nombre,
            }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Producto(db.Model):
    __tablename__ = 'producto'
    cod_producto = db.Column(db.Integer, primary_key=True)
    serie_producto = db.Column(db.String(250), nullable= False)
    marca = db.Column(db.String(250), nullable= False)
    nombre = db.Column(db.String(250), nullable= False)
    imagen = db.Column(db.String(250), nullable= False)
    descripcion = db.Column(db.String(250), nullable= False)
    precio = db.Column(db.Integer, nullable= False)
    precio_dolar = db.Column(db.Integer, nullable= False)
    stock = db.Column(db.Integer, nullable= False, default=0)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable= False)

    def __str__(self):
        return f"cod_producto: {self.cod_producto}, serie_producto: {self.serie_producto}, marca: {self.marca}, nombre: {self.nombre}, imagen: Base64img, descripcion: {self.descripcion}, precio: {self.precio}, precio_dolar: {self.precio_dolar}, stock: {self.stock}, id_categoria: {self.id_categoria}"
    
    def serialize(self):
        return{
            "cod_producto": self.cod_producto,
            "serie_producto": self.serie_producto,
            "marca": self.marca,
            "nombre": self.nombre,
            "imagen": self.imagen,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "precio_dolar": self.precio_dolar,
            "stock": self.stock,
            "id_categoria": self.id_categoria
            }
    def serialize_with_img(self):
        return{
            "cod_producto": self.cod_producto,
            "serie_producto": self.serie_producto,
            "marca": self.marca,
            "nombre": self.nombre,
            "imagen": 'data:image/jpeg;base64,'+base64.b64encode(self.imagen).decode('utf-8'),
            "descripcion": self.descripcion,
            "precio": self.precio,
            "precio_dolar": self.precio_dolar,
            "stock": self.stock,
            "id_categoria": self.id_categoria,
            }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class TipoPago(db.Model):
    __tablename__ = 'tipo_pago'
    id_tipo_pago = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable= False)

    def __str__(self):
        return f"id_tipo_pago: {self.id_tipo_pago}, nombre: {self.nombre}"
    
    def serialize(self):
        return{
            "id_tipo_pago": self.id_tipo_pago,
            "nombre": self.nombre,
            }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Venta(db.Model):
    __tablename__ = 'venta'
    id_venta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable= False, default=datetime.now())
    total = db.Column(db.Integer, nullable= False)
    id_tipo_pago = db.Column(db.Integer, db.ForeignKey('tipo_pago.id_tipo_pago'), nullable= False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable= False)

    def __str__(self):
        return f"id_venta: {self.id_venta}, fecha: {self.fecha}, total: {self.total}, id_tipo_pago: {self.id_tipo_pago}, id_usuario: {self.id_usuario}"
    
    def serialize(self):
        return{
            "id_venta": self.id_venta,
            "fecha": self.fecha,
            "total": self.total,
            "id_tipo_pago": self.id_tipo_pago,
            "id_usuario": self.id_usuario
            }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    id_detalle_venta = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable= False)
    valor = db.Column(db.Integer, nullable= False)
    descuento = db.Column(db.Integer, nullable= False)
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id_venta'), nullable= False)
    cod_producto = db.Column(db.Integer, db.ForeignKey('producto.cod_producto'), nullable= False)

    def __str__(self):
        return f"id_detalle_venta: {self.id_detalle_venta}, cantidad: {self.cantidad}, valor: {self.valor}, descuento: {self.descuento}, id_venta: {self.id_venta}, cod_producto: {self.cod_producto}"
    
    def serialize(self):
        return{
            "id_detalle_venta": self.id_detalle_venta,
            "cantidad": self.cantidad,
            "valor": self.valor,
            "descuento": self.descuento,
            "id_venta": self.id_venta,
            "cod_producto": self.cod_producto
            }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()