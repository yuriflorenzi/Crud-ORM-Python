# controllers.py
# usando sesion  de sqlalchemy
from models import Cliente, Pedido

class ClienteController:
    def __init__(self, db_session):
        self.session = db_session

    def crear(self, nombre, email):
        cliente = Cliente(nombre=nombre, email=email)
        self.session.add(cliente)
        self.session.commit()
        return cliente
    #se crea una instancia de cliente
    #se agrega la sesion
    #se confirma la transacion con commit

    def obtener_todos(self):
        return self.session.query(Cliente).all()
      # uso de query para todos los registros
    def obtener_por_id(self, cliente_id):
        return self.session.query(Cliente).filter_by(id=cliente_id).first()
    #Se busca un cliente por su id, se modifican los atributos y se confirma con commit.
    def obtener_por_nombre(self, nombre):
        return self.session.query(Cliente).filter_by(nombre=nombre).first()

    def actualizar(self, cliente_id, nombre, email):
        cliente = self.obtener_por_id(cliente_id)
        if cliente:
            cliente.nombre = nombre
            cliente.email = email
            self.session.commit()
        return cliente

    def eliminar(self, cliente_id):
        cliente = self.obtener_por_id(cliente_id)
        if cliente:
            self.session.delete(cliente)
            self.session.commit()
            return True
        return False
  # con delete
class PedidoController:
    def __init__(self, db_session):
        self.session = db_session

    def crear(self, cliente_id, producto, cantidad):
        pedido = Pedido(cliente_id=cliente_id, producto=producto, cantidad=cantidad)
        self.session.add(pedido)
        self.session.commit()
        return pedido

    def obtener_todos(self):
        return self.session.query(Pedido).all()

    def obtener_por_id(self, pedido_id):
        return self.session.query(Pedido).filter_by(id=pedido_id).first()

    def actualizar(self, pedido_id, cliente_id, producto, cantidad):
        pedido = self.obtener_por_id(pedido_id)
        if pedido:
            pedido.cliente_id = cliente_id
            pedido.producto = producto
            pedido.cantidad = cantidad
            self.session.commit()
        return pedido

    def eliminar(self, pedido_id):
        pedido = self.obtener_por_id(pedido_id)
        if pedido:
            self.session.delete(pedido)
            self.session.commit()
            return True
        return False