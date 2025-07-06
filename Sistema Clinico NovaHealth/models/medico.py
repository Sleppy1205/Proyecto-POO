from models.persona import Persona

class Medico(Persona):
    """
    Clase que representa a un médico.
    Hereda de Persona.
    """

    def __init__(self, nombre, apellido, cedula, telefono, codigo_medico, especialidad):
        super().__init__(nombre, apellido, cedula, telefono)
        self.__codigo_medico = codigo_medico
        self.__especialidad = especialidad

    def mostrar_info(self):
        """
        Devuelve los datos principales del médico.
        """
        return (
            f"Médico: Dr. {self.nombre} {self._apellido}\n"
            f"Cédula: {self._cedula}, Teléfono: {self._telefono}\n"
            f"Especialidad: {self.__especialidad}, Código: {self.__codigo_medico}"
        )

    def firmar_reporte(self, reporte):
        """
        Método para firmar un reporte médico.
        """
        reporte.marcar_como_firmado(self)