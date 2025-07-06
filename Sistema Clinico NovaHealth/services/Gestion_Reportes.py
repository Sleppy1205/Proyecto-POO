from models.reporte import Reporte

class ServicioReportes:
    """
    Servicio que permite generar reportes médicos y consultarlos.
    """

    def __init__(self):
        self.__reportes = []

    def generar_reporte(self, paciente, medico):
        """
        Crea un nuevo reporte vacío y lo asocia al paciente y médico.
        """
        nuevo = Reporte(paciente, medico)
        self.__reportes.append(nuevo)
        return nuevo

    def listar_reportes(self):
        """
        Devuelve un resumen de todos los reportes generados.
        """
        return [reporte.mostrar_resumen() for reporte in self.__reportes]

    def obtener_reportes_firmados(self):
        """
        Retorna solo los reportes que ya fueron firmados.
        """
        return [reporte for reporte in self.__reportes if reporte.esta_firmado()]