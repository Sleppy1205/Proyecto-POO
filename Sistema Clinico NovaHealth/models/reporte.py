from datetime import date

class Reporte:
    """
    Representa un reporte médico que contiene resultados de exámenes.
    Asociado a un paciente y un médico.
    """

    def __init__(self, paciente, medico):
        self.__paciente = paciente
        self.__medico = medico
        self.__resultados = []  # lista de instancias de Resultado
        self.__fecha_emision = date.today()
        self.__firmado = False

    def agregar_resultado(self, resultado):
        """
        Agrega un resultado clínico al reporte.
        """
        self.__resultados.append(resultado)

    def marcar_como_firmado(self, medico):
        """
        Marca el reporte como firmado si es firmado por el médico correcto.
        """
        if medico == self.__medico:
            self.__firmado = True

    def esta_firmado(self):
        return self.__firmado

    def mostrar_resumen(self):
        """
        Devuelve un resumen con todos los resultados y firma del médico.
        """
        resumen = f"REPORTE MÉDICO\n"
        resumen += f"Paciente: {self.__paciente.nombre} {self.__paciente._apellido}\n"
        resumen += f"Médico: Dr. {self.__medico.nombre} {self.__medico._apellido}\n"
        resumen += f"Fecha: {self.__fecha_emision} - Firmado: {'Sí' if self.__firmado else 'No'}\n\n"
        resumen += "Resultados:\n"

        for res in self.__resultados:
            resumen += f" - {res.mostrar_detalle()}\n"

        return resumen