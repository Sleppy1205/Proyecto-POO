from abc import ABC, abstractmethod

class Persona(ABC):
    """
    Clase abstracta para representar una persona.
    No debe instanciarse directamente.
    """

    def __init__(self, nombre, apellido, cedula, telefono):
        self._nombre = nombre
        self._apellido = apellido
        self._cedula = cedula
        self._telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo):
        if nuevo:
            self._nombre = nuevo

    @abstractmethod
    def mostrar_info(self):
        """
        Método que debe ser implementado por todas las clases hijas.
        """
        pass