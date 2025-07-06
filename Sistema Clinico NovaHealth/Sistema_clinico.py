import datetime
import tkinter as tk
from tkinter import messagebox

# Clases del sistema interno 
class Paciente:
    def __init__(self, nombre, apellido, cedula, telefono, nacimiento, sexo, direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.telefono = telefono
        self.nacimiento = nacimiento
        self.sexo = sexo
        self.direccion = direccion

    def mostrar(self):
        return (
            f"Paciente: {self.nombre} {self.apellido}\n"
            f"Cédula: {self.cedula} | Teléfono: {self.telefono}\n"
            f"Nacimiento: {self.nacimiento} | Sexo: {self.sexo}\n"
            f"Dirección: {self.direccion}"
        )

class GestorPacientes:
    def __init__(self):
        self.pacientes = []

    def registrar(self, paciente: Paciente):
        self.pacientes.append(paciente)

    def buscar_por_cedula(self, cedula):
        for p in self.pacientes:
            if p.cedula == cedula:
                return p
        return None

# Aqui se añade facade
class SistemaClinicoFacade:
    def __init__(self):
        self.gestor = GestorPacientes()

    def registrar_paciente(self, datos: dict):
        try:
            fecha = datetime.datetime.strptime(datos["nacimiento"], "%Y-%m-%d").date()
            paciente = Paciente(
                datos["nombre"], datos["apellido"], datos["cedula"],
                datos["telefono"], fecha, datos["sexo"], datos["direccion"]
            )
            self.gestor.registrar(paciente)
            return True, paciente
        except Exception as e:
            return False, str(e)

    def obtener_info_paciente(self, cedula):
        paciente = self.gestor.buscar_por_cedula(cedula)
        return paciente

# Interfaz gráfica con el FACADE
class VentanaClinica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Clínico")
        self.geometry("500x600")
        self.facade = SistemaClinicoFacade()

        # Campos de entrada
        self.entries = {}
        campos = ["nombre", "apellido", "cedula", "telefono", "nacimiento (YYYY-MM-DD)", "sexo", "direccion"]
        for campo in campos:
            tk.Label(self, text=campo.capitalize()).pack()
            entry = tk.Entry(self, width=50)
            entry.pack(pady=2)
            self.entries[campo] = entry

        # Botones
        tk.Button(self, text="Registrar Paciente", command=self.registrar).pack(pady=10)

        tk.Label(self, text="Buscar paciente por cédula:").pack()
        self.buscar_cedula = tk.Entry(self, width=30)
        self.buscar_cedula.pack()
        tk.Button(self, text="Buscar", command=self.buscar).pack(pady=5)

    def registrar(self):
        datos = {
            "nombre": self.entries["nombre"].get(),
            "apellido": self.entries["apellido"].get(),
            "cedula": self.entries["cedula"].get(),
            "telefono": self.entries["telefono"].get(),
            "nacimiento": self.entries["nacimiento (YYYY-MM-DD)"].get(),
            "sexo": self.entries["sexo"].get(),
            "direccion": self.entries["direccion"].get()
        }

        exito, resultado = self.facade.registrar_paciente(datos)
        if exito:
            messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
        else:
            messagebox.showerror("Error", f"No se pudo registrar: {resultado}")

    def buscar(self):
        cedula = self.buscar_cedula.get()
        paciente = self.facade.obtener_info_paciente(cedula)

        if paciente:
            self.mostrar_ventana_info(paciente)
        else:
            messagebox.showwarning("No encontrado", "Paciente no encontrado con esa cédula.")

    def mostrar_ventana_info(self, paciente):
        # Crear ventana emergente para mostrar la info
        ventana = tk.Toplevel(self)
        ventana.title("Información del Paciente")
        ventana.geometry("400x200")
        tk.Label(ventana, text=paciente.mostrar(), justify="left").pack(padx=10, pady=10)

# Ejecutar
if __name__ == "__main__":
    app = VentanaClinica()
    app.mainloop()