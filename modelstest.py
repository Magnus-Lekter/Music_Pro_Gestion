
from flask_pymongo import pymongo
from datetime import date


class Proyecto():
    """Proyecto model"""
    nombre = ""

    def serialize(self):
        return {
            "nombre": self.nombre
        }