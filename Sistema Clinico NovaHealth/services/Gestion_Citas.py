from models.cita import Cita
from datetime import datetime

class ServicioCitas:
    """
    Servicio para agendar y consultar citas médicas.
    """

    def __init__(self):
        self.__citas = []

    def agendar_cita(self, paciente, medico, fecha_hora: datetime, motivo: str):
        """
        Crea una nueva cita y la agrega a la lista.
        """
        nueva_cita = Cita(paciente, medico, fecha_hora, motivo)
        self.__citas.append(nueva_cita)
        return nueva_cita

    def listar_citas(self):
        """
        Devuelve una lista con los detalles de todas las citas.
        """
        return [cita.mostrar_detalle() for cita in self.__citas]

    def obtener_citas_pendientes(self):
        """
        Retorna solo las citas que aún no han sido atendidas.
        """
        return [cita for cita in self.__citas if not cita.esta_atendida()]