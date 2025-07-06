from models.persona import Persona
from models.resultado import Resultado  # Hacemos un import anticipado para registrar resultados

class Laboratorista(Persona):
    """
    Clase que representa a un laboratorista.
    Hereda de Persona.
    """

    def __init__(self, nombre, apellido, cedula, telefono, codigo_laboratorista, turno):
        super().__init__(nombre, apellido, cedula, telefono)
        self.__codigo_laboratorista = codigo_laboratorista
        self.__turno = turno

    def mostrar_info(self):
        """
        Devuelve los datos principales del laboratorista.
        """
        return (
            f"Laboratorista: {self.nombre} {self._apellido}\n"
            f"Cédula: {self._cedula}, Teléfono: {self._telefono}\n"
            f"Código: {self.__codigo_laboratorista}, Turno: {self.__turno}"
        )

    def registrar_resultado(self, examen, valor):
        """
        Registra el resultado de un examen (valor obtenido).
        Retorna una instancia de Resultado.
        """
        return Resultado(examen, valor)