from .{{cookiecutter.package_name}} import db


class PDNBase():

    """
    data es un diccionario con los atributos de la entidad
    """
    def __init__(self, data):
        for key in data:
            setattr(self, key, data[key])

    def set(self, data):
        self.__init__(data)


class PDN(PDNBase, db.Model):
    """PDN es un Armario - Punto de Desarrollo de Negocio"""
    __tablename__ = 'pdns'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(45), unique=True)
    descripcion = db.Column(db.String(255))
    ip_master = db.Column(db.String(45))

    def __repr__(self):
        return 'PDN {}, {}'.format(self.codigo, self.ip_master)
