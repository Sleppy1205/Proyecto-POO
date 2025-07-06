class UsuarioSistema:
    """
    Representa un usuario del sistema (paciente, médico, etc.)
    Asociado a una persona.
    """

    def __init__(self, nombre_usuario, contrasena, persona):
        self.__nombre_usuario = nombre_usuario
        self.__contrasena = contrasena
        self.__persona = persona  # Puede ser paciente, médico, laboratorista, etc.

    def verificar_credenciales(self, usuario, contrasena):
        """
        Verifica si las credenciales ingresadas coinciden.
        """
        return self.__nombre_usuario == usuario and self.__contrasena == contrasena

    def mostrar_rol(self):
        """
        Devuelve el tipo de usuario (rol) en minúsculas.
        """
        return self.__persona.__class__.__name__.lower()

    def get_persona(self):
        """
        Devuelve el objeto persona asociado al usuario.
        """
        return self.__persona