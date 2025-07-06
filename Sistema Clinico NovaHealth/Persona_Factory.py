from models.paciente import Paciente
from models.medico import Medico
from models.laboratorista import Laboratorista
from datetime import date

class PersonaFactory:
    """
    Fábrica que crea instancias de persona según el tipo indicado.
    """

    @staticmethod
    def crear_persona(tipo, nombre, apellido, cedula, telefono, **kwargs):
        """
        Crea una instancia del tipo indicado:
        - "paciente"
        - "medico"
        - "laboratorista"
        """
        if tipo == "paciente":
            return Paciente(
                nombre,
                apellido,
                cedula,
                telefono,
                kwargs.get("fecha_nacimiento", date.today()),
                kwargs.get("sexo", "M"),
                kwargs.get("direccion", "Desconocida")
            )
        elif tipo == "medico":
            return Medico(
                nombre,
                apellido,
                cedula,
                telefono,
                kwargs.get("codigo_medico", "MED001"),
                kwargs.get("especialidad", "General")
            )
        elif tipo == "laboratorista":
            return Laboratorista(
                nombre,
                apellido,
                cedula,
                telefono,
                kwargs.get("codigo_laboratorista", "LAB001"),
                kwargs.get("turno", "Día")
            )
        else:
            raise ValueError(f"Tipo de persona no válido: {tipo}")

from services.PersonaFactory import PersonaFactory
from datetime import date

persona1 = PersonaFactory.crear_persona(
    "paciente",
    "Johan",
    "Gonzalez",
    "1351320518",
    "0989024404",
    fecha_nacimiento=date(2005, 11, 7),
    sexo="M",
    direccion="Manta"
)
print(persona1.mostrar_info())