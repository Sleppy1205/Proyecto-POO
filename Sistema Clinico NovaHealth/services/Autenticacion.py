from models.usuario_sistema import UsuarioSistema

class ServicioAutenticacion:
    """
    Servicio para manejar el inicio de sesión de usuarios del sistema.
    """

    def __init__(self):
        self.__usuarios = []

    def registrar_usuario(self, usuario: UsuarioSistema):
        """
        Registra un nuevo usuario en el sistema.
        """
        self.__usuarios.append(usuario)

    def autenticar(self, nombre_usuario: str, contrasena: str):
        """
        Verifica si las credenciales son correctas.
        Devuelve el usuario autenticado o None.
        """
        for usuario in self.__usuarios:
            if usuario.verificar_credenciales(nombre_usuario, contrasena):
                return usuario
        return None

    def listar_usuarios(self):
        """
        Devuelve una lista de nombres de usuario registrados.
        """
        return [u.get_persona().nombre for u in self.__usuarios]