from datetime import datetime

class Factura:
    """
    Representa una factura generada a partir de una orden de pago.
    """

    def __init__(self, orden_pago):
        self.__orden_pago = orden_pago
        self.__fecha_emision = datetime.now()
        self.__pagada = False

    def pagar(self):
        """
        Marca la factura como pagada.
        """
        self.__pagada = True

    def esta_pagada(self):
        return self.__pagada

    def mostrar_factura(self):
        """
        Muestra los detalles de la factura y su estado.
        """
        estado = "Pagada" if self.__pagada else "Pendiente"
        detalle = f"FACTURA - Fecha: {self.__fecha_emision.strftime('%d/%m/%Y %H:%M')} - Estado: {estado}\n"
        detalle += self.__orden_pago.mostrar_detalle()
        return detalle