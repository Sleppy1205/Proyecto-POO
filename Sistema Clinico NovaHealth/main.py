# main.py

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
from services.Json_Manager import guardar_json, cargar_json
from models.paciente import Paciente
from models.medico import Medico
from models.laboratorista import Laboratorista
from models.usuario_sistema import UsuarioSistema

# Rutas de archivos JSON
RUTA_USUARIOS = "data/usuarios.json"
RUTA_PACIENTES = "data/pacientes.json"
RUTA_MEDICOS = "data/medicos.json"
RUTA_LABORATORISTAS = "data/laboratoristas.json"
RUTA_CITAS = "data/citas.json"
RUTA_RESULTADOS = "data/resultados.json"
RUTA_REPORTES = "data/reportes.json"
RUTA_FACTURAS = "data/facturas.json"
RUTA_EXAMENES = "data/examenes.json"

# Ventana para registrar un nuevo usuario del sistema
def ventana_registrar_usuario():
    ventana = tk.Toplevel()
    ventana.title("Registrar Usuario del Sistema")
    ventana.geometry("500x650")
    ventana.configure(bg="#f0f8ff")

    tk.Label(ventana, text="Selecciona tu rol:", bg="#f0f8ff", font=("Arial", 13)).pack(pady=10)

    rol_var = tk.StringVar(value="Paciente")
    tk.OptionMenu(ventana, rol_var, "Paciente", "Médico", "Laboratorista").pack()

    form_frame = tk.Frame(ventana, bg="#f0f8ff")
    form_frame.pack(pady=15)

    campos = {}
    entradas = []
    campo_codigo_autorizacion = None  # Se usará solo si es necesario

    comunes = [
        ("Nombre", "nombre"),
        ("Apellido", "apellido"),
        ("Cédula", "cedula"),
        ("Teléfono", "telefono")
    ]

    por_rol = {
        "Paciente": [
            ("Dirección", "direccion"),
            ("Sexo (M/F)", "sexo"),
            ("Fecha nacimiento (YYYY-MM-DD)", "nacimiento")
        ],
        "Médico": [
            ("Código Médico", "codigo"),
            ("Especialidad", "especialidad")
        ],
        "Laboratorista": [
            ("Código Laboratorista", "codigo"),
            ("Turno", "turno")
        ]
    }

    cuenta = [
        ("Usuario", "usuario"),
        ("Contraseña", "contrasena")
    ]

    def registrar():
        try:
            rol = rol_var.get()
            datos = {k: v.get() for k, v in campos.items()}
            cedula = datos.get("cedula", "")

            # Verificación de código de autorización
            if rol in ["Médico", "Laboratorista"]:
                if campo_codigo_autorizacion:
                    codigo_ingresado = campo_codigo_autorizacion.get()
                    ultimos_digitos = cedula[-3:] if len(cedula) >= 3 else ""
                    if codigo_ingresado != ultimos_digitos:
                        raise ValueError("Código de autorización incorrecto. Deben ser los últimos 3 dígitos de tu cédula.")

            if rol == "Paciente":
                nacimiento = datetime.strptime(datos["nacimiento"], "%Y-%m-%d").date()
                persona = Paciente(datos["nombre"], datos["apellido"], datos["cedula"], datos["telefono"],
                                   nacimiento, datos["sexo"], datos["direccion"])
                ruta = RUTA_PACIENTES
            elif rol == "Médico":
                persona = Medico(datos["nombre"], datos["apellido"], datos["cedula"], datos["telefono"],
                                 datos["codigo"], datos["especialidad"])
                ruta = RUTA_MEDICOS
            elif rol == "Laboratorista":
                persona = Laboratorista(datos["nombre"], datos["apellido"], datos["cedula"], datos["telefono"],
                                        datos["codigo"], datos["turno"])
                ruta = RUTA_LABORATORISTAS

            # Guardar persona
            guardar_json(ruta, cargar_json(ruta) + [persona.__dict__])

            # Guardar usuario
            usuarios = cargar_json(RUTA_USUARIOS)
            usuarios.append({
                "usuario": datos["usuario"],
                "contrasena": datos["contrasena"],
                "rol": rol,
                "persona": persona.__dict__
            })
            guardar_json(RUTA_USUARIOS, usuarios)

            messagebox.showinfo("Éxito", f"{rol} registrado correctamente.")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Revisa los campos.\n{str(e)}")

    def mostrar_campos(*args):
        nonlocal campo_codigo_autorizacion
        for widget in entradas:
            widget.destroy()
        entradas.clear()
        campos.clear()
        campo_codigo_autorizacion = None

        # Limpiar botón anterior
        for child in form_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.destroy()

        def agregar_campos(lista):
            for texto, key in lista:
                lbl = tk.Label(form_frame, text=texto, bg="#f0f8ff", font=("Arial", 11))
                entry = tk.Entry(form_frame, font=("Arial", 11))
                lbl.pack()
                entry.pack()
                entradas.extend([lbl, entry])
                campos[key] = entry

        agregar_campos(comunes)
        agregar_campos(por_rol[rol_var.get()])
        agregar_campos(cuenta)

        # Agregar campo de código secreto SOLO si es médico o laboratorista
        if rol_var.get() in ["Médico", "Laboratorista"]:
            lbl_auth = tk.Label(form_frame, text="Código de autorización (últimos 3 dígitos de tu cédula):", bg="#f0f8ff", font=("Arial", 11))
            campo_codigo_autorizacion = tk.Entry(form_frame, font=("Arial", 11))
            lbl_auth.pack()
            campo_codigo_autorizacion.pack()
            entradas.extend([lbl_auth, campo_codigo_autorizacion])

        btn_registrar = tk.Button(form_frame, text="Registrar", bg="#4caf50", fg="white",
                                  font=("Arial", 12), command=registrar)
        btn_registrar.pack(pady=15)

    rol_var.trace_add("write", mostrar_campos)
    mostrar_campos()
    
# Funcion de inicio de sesion real
def verificar_login():
    usuario_ingresado = entry_usuario.get()
    contrasena_ingresada = entry_contrasena.get()

    try:
        usuarios = cargar_json(RUTA_USUARIOS)
        for u in usuarios:
            if u["usuario"] == usuario_ingresado and u["contrasena"] == contrasena_ingresada:
                rol = u["rol"]
                datos = u["persona"]

                if rol == "Paciente":
                    persona = Paciente(**datos)
                elif rol == "Médico":
                    persona = Medico(**datos)
                elif rol == "Laboratorista":
                    persona = Laboratorista(**datos)

                messagebox.showinfo("Bienvenido", f"Hola {persona._nombre}, ingresaste como {rol}.")
                ventana_login.destroy()
                mostrar_menu_principal(rol, persona)
                return

        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo verificar.\n{e}")

# Menú principal por rol
def mostrar_menu_principal(rol, persona):
    ventana = tk.Tk()
    ventana.title("NovaHealth - Panel Principal")
    ventana.geometry("800x500")
    ventana.configure(bg="#e3f2fd")

    tk.Label(ventana, text=f"Bienvenido {persona._nombre}", font=("Arial Black", 18),
             bg="#1565c0", fg="white", pady=15).pack(fill="x")

    frame = tk.Frame(ventana, bg="#e3f2fd")
    frame.pack(pady=30)

    opciones = []

    if rol == "Paciente":
        opciones = [
            ("Agendar Cita", lambda: ventana_agendar_cita(persona)),
            ("Ver Factura", lambda: ventana_ver_factura(persona))
        ]
    elif rol == "Médico":
        opciones = [
            ("Ver Reporte", lambda: ventana_ver_reporte(persona))
        ]
    elif rol == "Laboratorista":
        opciones = [
            ("Registrar Resultado", lambda: ventana_registrar_resultado(persona))
        ]

    opciones.append(("Cerrar Sesión", ventana.destroy))

    for texto, accion in opciones:
        btn = tk.Button(frame, text=texto, width=30, height=2, font=("Arial", 12),
                        bg="#42a5f5", fg="white", command=accion)
        btn.pack(pady=10)

    ventana.mainloop()

# Interfaz de login
ventana_login = tk.Tk()
ventana_login.title("NovaHealth - Iniciar sesión")
ventana_login.geometry("800x500")
ventana_login.configure(bg="#dceefc")
ventana_login.columnconfigure(0, weight=1)
ventana_login.rowconfigure(0, weight=1)

frame_login = tk.Frame(ventana_login, bg="#dceefc")
frame_login.grid(row=0, column=0, sticky="nsew")

tk.Label(frame_login, text="Sistema Clínico NovaHealth", font=("Helvetica", 20, "bold"),
         bg="#dceefc", fg="#1a237e").pack(pady=30)

tk.Label(frame_login, text="Usuario:", font=("Arial", 14), bg="#dceefc").pack()
entry_usuario = tk.Entry(frame_login, font=("Arial", 14), width=30)
entry_usuario.pack(pady=5)

tk.Label(frame_login, text="Contraseña:", font=("Arial", 14), bg="#dceefc").pack()
entry_contrasena = tk.Entry(frame_login, show="*", font=("Arial", 14), width=30)
entry_contrasena.pack(pady=5)

btn_frame = tk.Frame(frame_login, bg="#dceefc")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Ingresar", bg="#1565c0", fg="white", font=("Arial", 12),
          width=12, command=verificar_login).pack(side="left", padx=10)

tk.Button(btn_frame, text="Registrarse", bg="#2e7d32", fg="white", font=("Arial", 12),
          width=12, command=ventana_registrar_usuario).pack(side="left", padx=10)

ventana_login.mainloop()

# Ventana - Agendar Cita (Paciente)
def ventana_agendar_cita(paciente):
    nueva = tk.Toplevel()
    nueva.title("Agendar Cita")
    nueva.geometry("500x350")
    nueva.configure(bg="#f0f4ff")

    tk.Label(nueva, text="Nombre del Médico:", bg="#f0f4ff").pack()
    entry_medico = tk.Entry(nueva)
    entry_medico.pack()

    tk.Label(nueva, text="Motivo de la cita:", bg="#f0f4ff").pack()
    entry_motivo = tk.Entry(nueva)
    entry_motivo.pack()

    tk.Label(nueva, text="Fecha y hora (YYYY-MM-DD HH:MM):", bg="#f0f4ff").pack()
    entry_fecha = tk.Entry(nueva)
    entry_fecha.pack()

    def agendar():
        try:
            fecha = datetime.strptime(entry_fecha.get(), "%Y-%m-%d %H:%M")
            cita = {
                "paciente": paciente._nombre + " " + paciente._apellido,
                "medico": entry_medico.get(),
                "motivo": entry_motivo.get(),
                "fecha": entry_fecha.get()
            }
            citas = cargar_json(RUTA_CITAS)
            citas.append(cita)
            guardar_json(RUTA_CITAS, citas)
            messagebox.showinfo("Éxito", "Cita agendada correctamente.")
            nueva.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(nueva, text="Agendar Cita", bg="#2196f3", fg="white", command=agendar).pack(pady=10)

# Ventana - Registrar Resultado (Laboratorista)
def ventana_registrar_resultado(laboratorista):
    nueva = tk.Toplevel()
    nueva.title("Registrar Resultado")
    nueva.geometry("400x520")
    nueva.configure(bg="#fefae0")

    campos = {}

    etiquetas = [
        ("Nombre del paciente", "paciente"),
        ("Nombre del examen", "nombre"),
        ("Unidad (ej: mg/dL)", "unidad"),
        ("Valor obtenido", "valor"),
        ("Valor mínimo", "minimo"),
        ("Valor máximo", "maximo"),
        ("Precio", "precio")
    ]

    for texto, clave in etiquetas:
        tk.Label(nueva, text=texto, bg="#fefae0").pack()
        entrada = tk.Entry(nueva)
        entrada.pack()
        campos[clave] = entrada

    def registrar():
        try:
            from models.examen import Examen
            from models.resultado import Resultado
            from services.Json_Manager import guardar_json, cargar_json

            paciente = campos["paciente"].get()
            nombre = campos["nombre"].get()
            unidad = campos["unidad"].get()
            valor = float(campos["valor"].get())
            minimo = float(campos["minimo"].get())
            maximo = float(campos["maximo"].get())
            precio = float(campos["precio"].get())

            examen = Examen(nombre, unidad, minimo, maximo, precio)
            resultado = Resultado(examen, valor)

            # Guardar en archivo resultados.json
            ruta = "data/resultados.json"
            resultados = cargar_json(ruta)
            resultados.append({
                "paciente": paciente,
                "examen": nombre,
                "unidad": unidad,
                "valor": valor,
                "minimo": minimo,
                "maximo": maximo,
                "precio": precio
            })
            guardar_json(ruta, resultados)

            mensaje = resultado.mostrar_detalle()
            messagebox.showinfo("Resultado Registrado", mensaje)
            nueva.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos.\n{str(e)}")

    tk.Button(nueva, text="Registrar", bg="#90be6d", fg="white", command=registrar).pack(pady=15)

# Ventana - Ver Reporte (Médico)
def ventana_ver_reporte(usuario_actual):
    nueva = tk.Toplevel()
    nueva.title("Ver Reporte Médico")
    nueva.geometry("600x520")
    nueva.configure(bg="#e0f7fa")

    persona = usuario_actual.get_persona()
    if persona.__class__.__name__ != "Medico":
        messagebox.showerror("Acceso Denegado", "Solo los médicos pueden ver y firmar reportes.")
        nueva.destroy()
        return

    tk.Label(nueva, text="Ingrese nombre del paciente:", bg="#e0f7fa", font=("Arial", 12)).pack(pady=10)
    entry_nombre = tk.Entry(nueva, font=("Arial", 12))
    entry_nombre.pack()

    def generar():
        try:
            from models.reporte import Reporte
            from models.resultado import Resultado
            from models.examen import Examen
            from models.paciente import Paciente
            from services.Json_Manager import cargar_json
            from datetime import date

            nombre_paciente = entry_nombre.get().strip()
            resultados = cargar_json("data/resultados.json")

            # Filtrar resultados por paciente
            datos_paciente = [r for r in resultados if r["paciente"].lower() == nombre_paciente.lower()]
            if not datos_paciente:
                raise ValueError("Este paciente no tiene resultados registrados.")

            # Crear el paciente temporal
            paciente = Paciente(nombre_paciente, "", "", "", date(2000,1,1), "N/A", "N/A")
            medico = persona  # Médico que inició sesión
            reporte = Reporte(paciente, medico)

            for r in datos_paciente:
                examen = Examen(r["examen"], r["unidad"], r["minimo"], r["maximo"], r["precio"])
                resultado = Resultado(examen, r["valor"])
                reporte.agregar_resultado(resultado)

            reporte.marcar_como_firmado(medico)
            resumen = reporte.mostrar_resumen()

            texto = tk.Text(nueva, width=65, height=18, wrap="word", bg="white", font=("Arial", 11))
            texto.pack(pady=10)
            texto.insert("1.0", resumen)
            texto.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte.\n{str(e)}")

    tk.Button(nueva, text="Generar Reporte", bg="#0077b6", fg="white", font=("Arial", 12), command=generar).pack(pady=10)

# Ventana - Ver Factura (Paciente)
def ventana_ver_factura(paciente):
    nueva = tk.Toplevel()
    nueva.title("Factura del Paciente")
    nueva.geometry("600x500")
    nueva.configure(bg="#fefae0")

    tk.Label(nueva, text="Nombre del paciente:", bg="#fefae0", font=("Arial", 12)).pack(pady=10)
    entry_nombre = tk.Entry(nueva, font=("Arial", 12))
    entry_nombre.pack()

    texto = tk.Text(nueva, width=70, height=18, wrap="word", bg="white", font=("Arial", 11))
    texto.pack(pady=10, padx=10)
    texto.config(state="disabled")

    factura_actual = {"factura": None}  # Para guardar temporalmente

    def generar_factura():
        try:
            from models.orden_pago import OrdenPago
            from models.factura import Factura
            from models.paciente import Paciente
            from models.examen import Examen
            from services.Json_Manager import cargar_json
            from datetime import date

            nombre_paciente = entry_nombre.get()
            resultados = cargar_json("data/resultados.json")
            datos = [r for r in resultados if r["paciente"].lower() == nombre_paciente.lower()]
            if not datos:
                raise ValueError("Este paciente no tiene exámenes registrados.")

            paciente = Paciente(nombre_paciente, "", "", "", date(2000,1,1), "N/A", "N/A")
            orden = OrdenPago(paciente)

            for r in datos:
                examen = Examen(r["examen"], r["unidad"], r["minimo"], r["maximo"], r["precio"])
                orden.agregar_examen(examen)

            factura = Factura(orden)
            factura_actual["factura"] = factura

            texto.config(state="normal")
            texto.delete("1.0", tk.END)
            texto.insert("1.0", factura.mostrar_factura())
            texto.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la factura.\n{str(e)}")

    def marcar_pagada():
        if factura_actual["factura"]:
            factura_actual["factura"].pagar()
            texto.config(state="normal")
            texto.delete("1.0", tk.END)
            texto.insert("1.0", factura_actual["factura"].mostrar_factura())
            texto.config(state="disabled")
            messagebox.showinfo("Pagado", "Factura marcada como pagada.")
        else:
            messagebox.showwarning("Primero genera la factura", "Debes generar una factura antes de marcarla como pagada.")

    btn_gen = tk.Button(nueva, text="Generar Factura", bg="#f4a261", command=generar_factura)
    btn_gen.pack(pady=5)

    btn_pagar = tk.Button(nueva, text="Marcar como Pagada", bg="#2a9d8f", fg="white", command=marcar_pagada)
    btn_pagar.pack(pady=5)