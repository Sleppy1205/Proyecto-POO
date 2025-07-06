from models.examen import Examen

class Resultado:
    """
    Representa el resultado de un examen realizado.
    """

    def __init__(self, examen: Examen, valor_obtenido: float):
        self.__examen = examen
        self.__valor_obtenido = valor_obtenido

    def es_normal(self):
        """
        Devuelve True si el valor está dentro del rango permitido.
        """
        return self.__examen.es_valor_normal(self.__valor_obtenido)

    def mostrar_detalle(self):
        """
        Devuelve los detalles del resultado, incluyendo si es normal.
        """
        estado = "Normal" if self.es_normal() else "Fuera de rango"
        return (
            f"{self.__examen.nombre}: {self.__valor_obtenido} {estado}"
        )