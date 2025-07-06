class OrdenPago:
    """
    Representa una orden de pago generada para un paciente,
    basada en los exámenes que debe pagar.
    """

    def __init__(self, paciente):
        self.__paciente = paciente
        self.__examenes = []  # Lista de exámenes (instancias de Examen)

    def agregar_examen(self, examen):
        """
        Agrega un examen a la orden de pago.
        """
        self.__examenes.append(examen)

    def calcular_total(self):
        """
        Suma los precios de todos los exámenes.
        """
        return sum(examen.precio for examen in self.__examenes)

    def mostrar_detalle(self):
        """
        Devuelve una descripción completa de la orden.
        """
        detalle = f"Orden de Pago - Paciente: {self.__paciente.nombre} {self.__paciente._apellido}\n"
        for examen in self.__examenes:
            detalle += f" - {examen.nombre}: ${examen.precio:.2f}\n"
        detalle += f"Total a pagar: ${self.calcular_total():.2f}"
        return detalle