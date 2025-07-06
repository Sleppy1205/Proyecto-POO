from models.persona import Persona
from datetime import date

class Paciente(Persona):
    """
    Clase que representa a un paciente del sistema.
    Hereda de Persona.
    """

    def __init__(self, nombre, apellido, cedula, telefono, fecha_nacimiento, sexo, direccion):
        super().__init__(nombre, apellido, cedula, telefono)
        self.__fecha_nacimiento = fecha_nacimiento  # tipo: datetime.date
        self.__sexo = sexo
        self.__direccion = direccion

    def obtener_edad(self):
        """
        Calcula la edad del paciente a partir de la fecha de nacimiento.
        """
        hoy = date.today()
        edad = hoy.year - self.__fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.__fecha_nacimiento.month, self.__fecha_nacimiento.day):
            edad -= 1
        return edad

    def mostrar_info(self):
        """
        Devuelve los datos principales del paciente en texto.
        """
        return (
            f"Paciente: {self.nombre} {self._apellido}\n"
            f"Cédula: {self._cedula}, Teléfono: {self._telefono}\n"
            f"Edad: {self.obtener_edad()}, Sexo: {self.__sexo}, Dirección: {self.__direccion}"
        )