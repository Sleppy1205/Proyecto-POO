class Examen:
    """
    Clase que representa un examen clínico.
    Incluye unidad de medida, rango normal y precio.
    """
    def __init__(self, nombre, unidad, valor_minimo, valor_maximo, precio):
        self.__nombre = nombre
        self.__unidad = unidad
        self.__valor_minimo = valor_minimo
        self.__valor_maximo = valor_maximo
        self.__precio = precio

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio(self):
        return self.__precio

    def es_valor_normal(self, valor):
        """
        Devuelve True si el valor está dentro del rango normal.
        """
        return self.__valor_minimo <= valor <= self.__valor_maximo

    def mostrar_info(self):
        """
        Devuelve los datos del examen en texto.
        """
        return (
            f"Examen: {self.__nombre} ({self.__unidad})\n"
            f"Rango normal: {self.__valor_minimo} - {self.__valor_maximo} {self.__unidad}\n"
            f"Precio: ${self.__precio:.2f}"
        )