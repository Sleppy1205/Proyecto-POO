from datetime import datetime

class Cita:
    """
    Representa una cita médica entre un paciente y un médico.
    """

    def __init__(self, paciente, medico, fecha_hora: datetime, motivo: str):
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__motivo = motivo
        self.__atendida = False

    def marcar_como_atendida(self):
        self.__atendida = True

    def esta_atendida(self):
        return self.__atendida

    def mostrar_detalle(self):
        estado = "Atendida" if self.__atendida else "Pendiente"
        return (
            f"Cita para {self.__paciente.nombre} con el Dr. {self.__medico._apellido}\n"
            f"Fecha y hora: {self.__fecha_hora.strftime('%d/%m/%Y %H:%M')}\n"
            f"Motivo: {self.__motivo} - Estado: {estado}"
        )