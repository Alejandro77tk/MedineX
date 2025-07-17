import customtkinter
import sqlite3
from tkinter import messagebox, PhotoImage
import re


conexion = sqlite3.connect('hospital.db')
cursor = conexion.cursor()



conexion.commit()

conexion.commit()





app = customtkinter.CTk()
app.geometry("1200x700")
app.title("Gestor Médico")
app.configure(fg_color="#fbe8f0")
app.iconbitmap(r"assets/medico.ico")

def mostrar_todos_pacientes():
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    for i, paciente in enumerate(pacientes, start=1):
        dni, apellidos, nombre = paciente
        customtkinter.CTkButton(scrollable_frame, command=lambda d=dni: mostrar_info_paciente(d), text=dni.title(), anchor="w", font=("Cascadia Mono Italic", 14), hover_color="#b8a2aa", fg_color="#ffffff", text_color="#000000").grid(row=i, column=0, sticky="w", padx=0, pady=2)
        customtkinter.CTkLabel(scrollable_frame, text=apellidos.title(), font=("Cascadia Mono Italic", 14), anchor="w").grid(row=i, column=1, sticky="w", padx=5, pady=2)
        customtkinter.CTkLabel(scrollable_frame, text=nombre.title(), font=("Cascadia Mono Italic", 14), anchor="w").grid(row=i, column=2, sticky="w", padx=5, pady=2)



# Si el foco del usuario no está en la entry del DNI del usuario de deselecciona de manera que vuelve a su estado original y no hace nada hasta que se vuelva a presionar, (se quita el foco del widget(entry))
def desenfocar(Event):
    #Este condicional revisa que no se haya hecho clic en un widget.
    if(Event.widget == app):
        app.focus()

def guardar_cerrar_ventana_añadir_paciente():
    conexion.commit()
    exit






def añadir_paciente():
    toplevel = customtkinter.CTkToplevel(app)
    toplevel.geometry("400x250")
    toplevel.title("Nuevo paciente")
    toplevel.resizable(False, False)
    toplevel.configure(fg_color="#fbe8f0")

    # Entradas
    entry_dni = customtkinter.CTkEntry(toplevel, placeholder_text="DNI/NIF del paciente", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_apellidos = customtkinter.CTkEntry(toplevel, placeholder_text="Apellidos del paciente", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_nombre = customtkinter.CTkEntry(toplevel, placeholder_text="Nombre del paciente", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")

    entry_dni.pack(pady=10)
    entry_apellidos.pack(pady=10)
    entry_nombre.pack(pady=10)




    # Función para guardar en la base de datos
    def guardar():
        global refrescar
        dni = entry_dni.get().strip().upper()
        apellidos = entry_apellidos.get().strip().title()
        nombre = entry_nombre.get().strip().title()

        if not dni or not apellidos or not nombre:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        elif not re.match("[0-9]{8}[A-Z]{1}", dni):
            messagebox.showerror("Error", "El DNI introducido no es válido")
            return

        try:
            cursor.execute("INSERT INTO pacientes VALUES (?, ?, ?)", (dni, apellidos, nombre))
            conexion.commit()
            messagebox.showinfo("Éxito", "Paciente añadido correctamente")#. NOTA: para ver la información actualizada del paciente, debes presionar 'refrescar' y volver a hacer click en su dni.")
            toplevel.destroy()
            refrescar()  # Llamar a la función refrescar para actualizar la lista de pacientes
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ese DNI ya está registrado.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


        # Botones
    boton_ok = customtkinter.CTkButton(toplevel, text="OK", command=guardar, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")
    boton_cancelar = customtkinter.CTkButton(toplevel, text="Cancelar", command=toplevel.destroy, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")

    boton_ok.place(x=105,y=150)
    boton_cancelar.place(x=205, y=150)
# ______________________________________________________________________________________________________________________________

def añadir_editar_informacion():
    toplevel2 = customtkinter.CTkToplevel(app)
    toplevel2.geometry("400x325")
    toplevel2.title("Nueva información del paciente")
    toplevel2.resizable(False, False)
    toplevel2.configure(fg_color="#fbe8f0")

    # Entradas
    entry_dni = customtkinter.CTkEntry(toplevel2, placeholder_text="DNI/NIF del paciente", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_grupo_sangineo = customtkinter.CTkEntry(toplevel2, placeholder_text="Grupo sangíneo", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_fecha_nacimiento = customtkinter.CTkEntry(toplevel2, placeholder_text="Fecha de nacimiento", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_direccion = customtkinter.CTkEntry(toplevel2, placeholder_text="Dirección", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_telefono = customtkinter.CTkEntry(toplevel2, placeholder_text="Teléfono", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")

    entry_dni.pack(pady=10)
    entry_grupo_sangineo.pack(pady=10)
    entry_fecha_nacimiento.pack(pady=10)
    entry_direccion.pack(pady=10)
    entry_telefono.pack(pady=10)


    # Función para guardar en la base de datos
    def guardar():
        
        global refrescar
        dni = entry_dni.get().strip().upper()
        grupo_sangineo = entry_grupo_sangineo.get().strip().capitalize()
        fecha_nacimiento = entry_fecha_nacimiento.get().strip().capitalize()
        direccion = entry_direccion.get().strip().capitalize()
        telefono = entry_telefono.get().strip().capitalize()


        if not dni or not grupo_sangineo or not fecha_nacimiento or not direccion or not telefono:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        elif not re.match("[0-9]{8}[A-Z]{1}",dni):
            messagebox.showerror("Error", "El DNI introducido no es válido")
            return

        try:
            cursor.execute("SELECT * FROM informacion_general")
            informacion_general_paciente = cursor.fetchall()
            if dni not in [info[0] for info in informacion_general_paciente]:
                cursor.execute("INSERT INTO informacion_general VALUES (?, ?, ?, ?, ?)", (dni, grupo_sangineo, fecha_nacimiento, direccion, telefono))
            else:
                cursor.execute("UPDATE informacion_general SET grupo_sanguineo = ?, fecha_nacimiento = ?, direccion = ?, telefono = ? WHERE dni = ?", (grupo_sangineo, fecha_nacimiento, direccion, telefono, dni))
            conexion.commit()
            messagebox.showinfo("Éxito", "Informacion actualizada correctamente.")# NOTA: para ver la información actualizada del paciente, debes presionar 'refrescar' y volver a hacer click en su dni.")
            toplevel2.destroy()
            refrescar()  # Llamar a la función refrescar para actualizar la lista de pacientes
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


    # Botones
    boton_ok2 = customtkinter.CTkButton(toplevel2, text="OK", command=guardar, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")
    boton_cancelar2 = customtkinter.CTkButton(toplevel2, text="Cancelar", command=toplevel2.destroy, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")

    boton_ok2.place(x=100,y=250)
    boton_cancelar2.place(x=210,y=250)




# ______________________________________________________________________________________________________________________________
def añadir_alergia():
    toplevel2 = customtkinter.CTkToplevel(app)
    toplevel2.geometry("400x325")
    toplevel2.title("Nueva alergia")
    toplevel2.resizable(False, False)
    toplevel2.configure(fg_color="#fbe8f0")

    # Entradas
    entry_dni = customtkinter.CTkEntry(toplevel2, placeholder_text="DNI/NIF del paciente", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_alergia = customtkinter.CTkEntry(toplevel2, placeholder_text="Alergia", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_gravedad = customtkinter.CTkEntry(toplevel2, placeholder_text="Gravedad", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")

    entry_dni.pack(pady=10)
    entry_alergia.pack(pady=10)
    entry_gravedad.pack(pady=10)


    # Función para guardar en la base de datos
    def guardar():

        global refrescar
        dni = entry_dni.get().strip().upper()
        alergia = entry_alergia.get().strip().capitalize()
        gravedad = entry_gravedad.get().strip().capitalize()


        if not dni or not alergia or not gravedad:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        elif not re.match("[0-9]{8}[A-Z]{1}",dni):
            messagebox.showerror("Error", "El DNI introducido no es válido")
            return

        try:
            cursor.execute("INSERT INTO alergias VALUES (?, ?, ?, ?)", (None, dni, alergia, gravedad))
            conexion.commit()
            messagebox.showinfo("Éxito", "Alergia añadida correctamente.")# NOTA: para ver la información actualizada del paciente, debes presionar 'refrescar' y volver a hacer click en su dni.")
            toplevel2.destroy()
            refrescar()  # Llamar a la función refrescar para actualizar la lista de pacientes
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


    # Botones
    boton_ok2 = customtkinter.CTkButton(toplevel2, text="OK", command=guardar, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")
    boton_cancelar2 = customtkinter.CTkButton(toplevel2, text="Cancelar", command=toplevel2.destroy, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")

    boton_ok2.place(x=100,y=250)
    boton_cancelar2.place(x=210,y=250)



# ______________________________________________________________________________________________________________________________
def añadir_consulta():
    toplevel1 = customtkinter.CTkToplevel(app)
    toplevel1.geometry("400x325")
    toplevel1.title("Nueva consulta")
    toplevel1.resizable(False, False)
    toplevel1.configure(fg_color="#fbe8f0")

    # Entradas
    entry_dni = customtkinter.CTkEntry(toplevel1, placeholder_text="DNI/NIF del paciente", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_fecha = customtkinter.CTkEntry(toplevel1, placeholder_text="Fecha", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_motivo = customtkinter.CTkEntry(toplevel1, placeholder_text="Motivo", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_diagnostico = customtkinter.CTkEntry(toplevel1, placeholder_text="Diagnostico", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_tratamiento = customtkinter.CTkEntry(toplevel1, placeholder_text="Tratamiento", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")

    entry_dni.pack(pady=10)
    entry_fecha.pack(pady=10)
    entry_motivo.pack(pady=10)
    entry_diagnostico.pack(pady=10)
    entry_tratamiento.pack(pady=10)


    # Función para guardar en la base de datos
    def guardar():
        
        global refrescar
        id_ = 0
        dni = entry_dni.get().strip().upper()
        fecha = entry_fecha.get().strip().title()
        motivo = entry_motivo.get().strip().title()
        diagnostico = entry_diagnostico.get().strip().title()
        tratamiento = entry_tratamiento.get().strip().title()


        if not dni or not fecha or not motivo or not diagnostico or not tratamiento:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        elif not re.match("[0-9]{2}[/][0-9]{2}[/][0-9]{4}", fecha):
            messagebox.showerror("Error", "La fecha introducida no es válida")
            return
        elif not re.match("[0-9]{8}[A-Z]{1}",dni):
            messagebox.showerror("Error", "El DNI introducido no es válido")
            return

        try:
            cursor.execute("INSERT INTO historial_consultas VALUES (?, ?, ?, ?, ?, ?)", (None, dni, fecha, motivo, diagnostico, tratamiento))
            conexion.commit()
            messagebox.showinfo("Éxito", "Consulta añadida correctamente.")# NOTA: para ver la información actualizada del paciente, debes presionar 'refrescar' y volver a hacer click en su dni.")
            toplevel1.destroy()
            refrescar()  # Llamar a la función refrescar para actualizar la lista de pacientes
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


    # Botones
    boton_ok1 = customtkinter.CTkButton(toplevel1, text="OK", command=guardar, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")
    boton_cancelar1 = customtkinter.CTkButton(toplevel1, text="Cancelar", command=toplevel1.destroy, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")

    boton_ok1.place(x=100,y=250)
    boton_cancelar1.place(x=210,y=250)



def borrar_paciente():
    toplevel2 = customtkinter.CTkToplevel(app)
    toplevel2.geometry("400x325")
    toplevel2.title("Borrar paciente")
    toplevel2.resizable(False, False)
    toplevel2.configure(fg_color="#fbe8f0")

    # Entradas
    entry_dni = customtkinter.CTkEntry(toplevel2, placeholder_text="DNI/NIF del paciente", width=200, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
    entry_dni.pack(pady=10)


    # Función para guardar en la base de datos
    def guardar():
        
        global refrescar
        dni = entry_dni.get().upper()

        try:
            cursor.execute("DELETE FROM pacientes WHERE dni = ?", (dni,))
            cursor.execute("DELETE FROM historial_consultas WHERE DNI = ?", (dni,))
            cursor.execute("DELETE FROM alergias WHERE DNI = ?", (dni,))
            cursor.execute("DELETE FROM informacion_general WHERE DNI = ?", (dni,))
            # Guardar cambios y cerrar
            conexion.commit()


            messagebox.showinfo("Éxito", "Paciente borrado correctamente.")
            toplevel2.destroy()
            refrescar()  # Llamar a la función refrescar para actualizar la lista de pacientes
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


    # Botones
    boton_ok2 = customtkinter.CTkButton(toplevel2, text="OK", command=guardar, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")
    boton_cancelar2 = customtkinter.CTkButton(toplevel2, text="Cancelar", command=toplevel2.destroy, width=90, anchor="center", fg_color="#a48994", hover_color="#b8a2aa")

    boton_ok2.place(x=100,y=250)
    boton_cancelar2.place(x=210,y=250)
# ______________________________________________________________________________________________________________________________


#--BUSCAR PACIENTES MEDIANTE BUSQUEDA CON LA ENTRADA

entry = customtkinter.CTkEntry(app, placeholder_text="DNI/NIF, nombre o apellidos del paciente...", width=390, height=30, placeholder_text_color="#767676", fg_color="#FFFFFF", font=("Passion One", 15), border_width=1, border_color="#a48994")
entry.place(x=20, y=80)




def buscar_pacientes():
    texto = entry.get().strip()
    # Borrar resultados anteriores del frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Mostrar cabecera de columnas
    cabecera_fuente = ("Passion One", 18)
    customtkinter.CTkLabel(scrollable_frame, text="DNI", width=120, anchor="w", font=cabecera_fuente).grid(row=0, column=0, padx=10, pady=5)
    customtkinter.CTkLabel(scrollable_frame, text="APELLIDOS", width=120, anchor="w", font=cabecera_fuente).grid(row=0, column=1, padx=5, pady=5)
    customtkinter.CTkLabel(scrollable_frame, text="NOMBRE", width=120, anchor="w", font=cabecera_fuente).grid(row=0, column=2, padx=5, pady=5)

    # Consulta SQL usando LIKE
    like_text = f"%{texto}%"
    query = """
        SELECT * FROM pacientes
        WHERE dni LIKE ? OR apellidos LIKE ? OR nombre LIKE ?
    """
    cursor.execute(query, (like_text, like_text, like_text))
    resultados = cursor.fetchall()

    # Mostrar resultados en el frame
    for i, paciente in enumerate(resultados, start=1):  # importante usar enumerate
        dni, apellidos, nombre = paciente

        customtkinter.CTkButton(
            scrollable_frame,
            text=dni.upper(),
            anchor="w",
            hover_color="#b8a2aa",
            fg_color="#ffffff",
            text_color="#000000",
            width=90,
            font=("Cascadia Mono Italic", 14),
            command=lambda d=dni: mostrar_info_paciente(d)
        ).grid(row=i, column=0, sticky="w", padx=0, pady=2)

        customtkinter.CTkLabel(
            scrollable_frame,
            text=apellidos.title(),
            anchor="w",
            font=("Cascadia Mono Italic", 14),
            width=120
        ).grid(row=i, column=1, sticky="w", padx=5, pady=2)

        customtkinter.CTkLabel(
            scrollable_frame,
            text=nombre.title(),
            anchor="w",
            font=("Cascadia Mono Italic", 14),
            width=120
        ).grid(row=i, column=2, sticky="w", padx=5, pady=2)





#_______________________________________________________________
# Mostrar informacion de cada uno de los pacientes en la tabview
#_______________________________________________________________







def mostrar_info_paciente(dni):
    # 1. Borrar información previa de cada scrollable_frame
    for frame in [scrollable_frame_dt]:
        for widget in frame.winfo_children():
            info_widgets = widget.grid_info()
            if "column" in info_widgets and int(info_widgets["column"]) > 0:
                widget.destroy()


    for frame in [scrollable_frame_a]:
        for widget in frame.winfo_children():
            info_widgets = widget.grid_info()
            if "row" in info_widgets and int(info_widgets["row"]) > 0:
                widget.destroy()

    for frame in [scrollable_frame_h]:
        for widget in frame.winfo_children():
            info_widgets = widget.grid_info()
            if "row" in info_widgets and int(info_widgets["row"]) > 0:
                widget.destroy()


    # 2. Información general
    cursor.execute("SELECT * FROM informacion_general WHERE DNI = ?", (dni,))
    info = cursor.fetchone()
    if info:
        # Las etiquetas ya están puestas en la fila 0, solo añadimos valores en la columna 1
        for i, valor in enumerate(info):  # info = (dni, grupo, fecha_nac, direccion, telefono)
            customtkinter.CTkLabel(scrollable_frame_dt, text=valor, font=("Passion One", 20), anchor="w", text_color="#000000").grid(row=i, column=1, padx=10, pady=0, sticky="w")

    # 3. Alergias
    cursor.execute("SELECT dni, alergia, gravedad FROM alergias WHERE DNI = ?", (dni,))
    alergias = cursor.fetchall()
    for i, (dni, alergia, gravedad) in enumerate(alergias, start=1):
        customtkinter.CTkLabel(scrollable_frame_a, text=dni, font=("Passion One", 16)).grid(row=i, column=0, sticky="w")
        customtkinter.CTkLabel(scrollable_frame_a, text=alergia, font=("Passion One", 16)).grid(row=i, column=1, sticky="w")
        customtkinter.CTkLabel(scrollable_frame_a, text=gravedad, font=("Passion One", 16)).grid(row=i, column=2, sticky="w")

    # 4. Historial
    cursor.execute("SELECT * FROM historial_consultas WHERE DNI = ?", (dni,))
    historial = cursor.fetchall()
    for i, (id_, dni, fecha, motivo, diag, trat) in enumerate(historial, start=1):
        customtkinter.CTkLabel(scrollable_frame_h, text=id_, font=("Passion One", 16)).grid(row=i, column=0, sticky="w")
        customtkinter.CTkLabel(scrollable_frame_h, text=dni, font=("Passion One", 16)).grid(row=i, column=1, sticky="w")
        customtkinter.CTkLabel(scrollable_frame_h, text=fecha, font=("Passion One", 16)).grid(row=i, column=2, sticky="w")
        customtkinter.CTkLabel(scrollable_frame_h, text=motivo, font=("Passion One", 16)).grid(row=i, column=3, sticky="w")
        customtkinter.CTkLabel(scrollable_frame_h, text=diag, font=("Passion One", 16)).grid(row=i, column=4, sticky="w")
        customtkinter.CTkLabel(scrollable_frame_h, text=trat, font=("Passion One", 16)).grid(row=i, column=5, sticky="w")



# ______________________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________________

boton_busqueda = customtkinter.CTkButton(app, text="🔎", width=35, height=30,fg_color="#bca2ac",hover_color="#767676", border_width=1, border_color="#a48994", font=("Passion One", 22), command=buscar_pacientes)
boton_busqueda.place(x=410, y=80)



# Frame donde poner el título principal
frame = customtkinter.CTkFrame(master=app, width=1200, height=42, fg_color="#fbd5e5")
frame.place(x=0, y=0)

def refrescar():
    global conexion, cursor
    conexion.commit()  # Asegurarse de que se guarden los cambios
    conexion.close()  # Cerrar la conexión anterior
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    for widget in scrollable_frame.winfo_children():
        info_widgets = widget.grid_info()
        if "row" in info_widgets and int(info_widgets["row"]) > 0:
            widget.destroy()
    for frame in [scrollable_frame_dt]:
        for widget in frame.winfo_children():
            info_widgets = widget.grid_info()
            if "column" in info_widgets and int(info_widgets["column"]) > 0:
                widget.destroy()


    for frame in [scrollable_frame_a]:
        for widget in frame.winfo_children():
            info_widgets = widget.grid_info()
            if "row" in info_widgets and int(info_widgets["row"]) > 0:
                widget.destroy()

    for frame in [scrollable_frame_h]:
        for widget in frame.winfo_children():
            info_widgets = widget.grid_info()
            if "row" in info_widgets and int(info_widgets["row"]) > 0:
                widget.destroy()
    mostrar_todos_pacientes()




# Botón refrescar para actualizar la lista de pacientes
btn_refrescar = customtkinter.CTkButton(frame, text="⭮ Refrescar", width=35, height=30,fg_color="#bca2ac",hover_color="#767676", border_width=1, border_color="#a48994", font=("Passion One", 22), command=refrescar)
btn_refrescar.place(x=10, y=5)


# Título principal
titulo = customtkinter.CTkLabel(frame, text="Gestor Médico", font=("Passion One", 30), anchor="center", fg_color="#fbd5e5")
titulo.place(x=500, y=5) # "GESTOR HOSPITAL"
# titulo.place(x=450, y=5) # GESTOR HOSPITAL MEDICO SOFIA

# Boton para salir del programa
button = customtkinter.CTkButton(app, text="Cerrar sesión", command=exit, fg_color="#ffffff", border_color="#a48994", border_width=1, font=("Passion One", 20), hover_color="#a48994", text_color="#000000")
button.configure()
button.place(x=1040, y=7)


# Titulo "listado de pacientes"
titulo2 = customtkinter.CTkLabel(app, text="LISTADO DE PACIENTES", font=("Passion One", 20), anchor="center", fg_color="#fbe8f0")
titulo2.place(x=140, y=50)




# Lista scrolleable de pacientes
scrollable_frame = customtkinter.CTkScrollableFrame(app, width=400, height=500, fg_color="#ffffff", scrollbar_button_color="#a48994", label_fg_color="#d5c2c9", border_width=1, border_color="#a48994", orientation="vertical")
scrollable_frame.place(x=20, y=120)

# ctk_textbox_scrollbar = customtkinter.CTkScrollbar(app, command=scrollable_frame.xview, orientation="horizontal")
# ctk_textbox_scrollbar.grid(row=1, column=0, sticky="we")

# Mostrar todos los pacientes en la lista


# Cabecera de la lista de pacientes principal
customtkinter.CTkLabel(scrollable_frame, text="DNI", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=0, padx=1, pady=5)
customtkinter.CTkLabel(scrollable_frame, text="APELLIDOS", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=1, padx=5, pady=5)
customtkinter.CTkLabel(scrollable_frame, text="NOMBRE", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=2, padx=5, pady=5)

# Añadir paciente
button = customtkinter.CTkButton(app, text="+ Añadir paciente", command=añadir_paciente, fg_color="#97de65", border_color="#a48994", border_width=1, font=("Passion One", 30), hover_color="#bdf496", text_color="#000000")
button.configure()
button.place(x=20, y=645)





# Frame donde poner el título principal
# frame1 = customtkinter.CTkFrame(app, width=740, height=563, fg_color="#fbd5e5")
# frame1.place(x=450, y=120)


# Informacion detallada sobre el paciente-
tabview = customtkinter.CTkTabview(master=app, height=600, width=700, fg_color="#FFFFFF", segmented_button_fg_color="#a48994", segmented_button_selected_color="#b8a2aa",segmented_button_selected_hover_color="#b8a2aa", segmented_button_unselected_color="#a48994", segmented_button_unselected_hover_color="#b8a2aa", border_width=1 ,border_color="#a48994")
tabview.place(x=470, y=70)

tab_info = tabview.add("Datos generales")  # add tab at the end
tab_alergias = tabview.add("Alergias")  # add tab at the end
tab_historial = tabview.add("Historial de consultas")  # add tab at the end
tabview.set("Datos generales")  # set currently visible tab

# Añadir consulta
button = customtkinter.CTkButton(tab_historial, text="+ Añadir consulta", command=añadir_consulta, fg_color="#f8f884", border_color="#fefeb3", border_width=1, font=("Passion One", 15), hover_color="#ffffd9", text_color="#000000")
button.configure()
button.place(x=250, y=520)

#Editar información del paciente/añadir
button = customtkinter.CTkButton(tab_info, text="+ Añadir/editar infomacion general", command=añadir_editar_informacion, fg_color="#f8f884", border_color="#fefeb3", border_width=1, font=("Passion One", 15), hover_color="#ffffd9", text_color="#000000")
button.configure()
button.place(x=250, y=520)



# Borrar paciente
button1 = customtkinter.CTkButton(app, text="- Borrar paciente", command=borrar_paciente, fg_color="#e84545", border_color="#a48994", border_width=1, font=("Passion One", 30), hover_color="#fc9393", text_color="#000000")
button1.configure()
button1.place(x=240, y=645)

# Titulo "Detalles del paciente"
titulo2 = customtkinter.CTkLabel(app, text="DETALLES DEl PACIENTE", font=("Passion One", 20), anchor="center", fg_color="#fbe8f0")
titulo2.place(x=730, y=50)

# Menú scrolleable de los datos generales
scrollable_frame_dt = customtkinter.CTkScrollableFrame(master=tabview.tab("Datos generales"), width=630, height=485, fg_color="#ffffff", scrollbar_button_color="#a48994", label_fg_color="#d5c2c9", border_width=1, border_color="#a48994", orientation="horizontal")
scrollable_frame_dt.place(x=20, y=10)

# Todas las etiquetas para poner los datos generales de cada paciente
customtkinter.CTkLabel(scrollable_frame_dt, text="DNI: ", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=0, padx=0, pady=0)
customtkinter.CTkLabel(scrollable_frame_dt, text="GRUPO SANGÍNEO: ", width=120, anchor="w", font=("Passion One", 18)).grid(row=1, column=0, padx=0, pady=0)
customtkinter.CTkLabel(scrollable_frame_dt, text="FECHA NACIMIENTO:", width=120, anchor="w", font=("Passion One", 18)).grid(row=2, column=0, padx=0, pady=0)
customtkinter.CTkLabel(scrollable_frame_dt, text="DIRECCION :", width=120, anchor="w", font=("Passion One", 18)).grid(row=3, column=0, padx=0, pady=0)
customtkinter.CTkLabel(scrollable_frame_dt, text="Nº DE TELÉFONO: ", width=120, anchor="w", font=("Passion One", 18)).grid(row=4, column=0, padx=0, pady=0)


# Menú scrolleable de los datos generales
scrollable_frame_a = customtkinter.CTkScrollableFrame(master=tabview.tab("Alergias"), width=630, height=495, fg_color="#ffffff", scrollbar_button_color="#a48994", label_fg_color="#d5c2c9", border_width=1, border_color="#a48994")
scrollable_frame_a.place(x=20, y=10)

customtkinter.CTkLabel(scrollable_frame_a, text="DNI", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=0, padx=0, pady=0, sticky="w")
customtkinter.CTkLabel(scrollable_frame_a, text="ALÉRGIA", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=1, padx=0, pady=0, sticky="w")
customtkinter.CTkLabel(scrollable_frame_a, text="GRAVEDAD", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=2, padx=0, pady=0, sticky="w")


# Menú scrolleable de los datos generales
scrollable_frame_h = customtkinter.CTkScrollableFrame(master=tabview.tab("Historial de consultas"), width=630, height=485, fg_color="#ffffff", scrollbar_button_color="#a48994", label_fg_color="#d5c2c9", border_width=1, border_color="#a48994", orientation="horizontal")
scrollable_frame_h.place(x=20, y=10)

customtkinter.CTkLabel(scrollable_frame_h, text="ID", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=0, padx=0, pady=0)
customtkinter.CTkLabel(scrollable_frame_h, text="DNI", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=1, padx=0, pady=0)
customtkinter.CTkLabel(scrollable_frame_h, text="FECHA", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=2, padx=0, pady=0)
customtkinter.CTkLabel(scrollable_frame_h, text="MOTIVO", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=3, padx=0, pady=0)
customtkinter.CTkLabel(scrollable_frame_h, text="DIAGNOSTICO", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=4, padx=0, pady=0)
customtkinter.CTkLabel(scrollable_frame_h, text="TRATAMIENTO", width=120, anchor="w", font=("Passion One", 18)).grid(row=0, column=5, padx=0, pady=0)


# Botón añdir alergia

button5 = customtkinter.CTkButton(master=tabview.tab("Alergias"), text="+ Añadir alergia", command=añadir_alergia, fg_color="#f8f884", border_color="#fefeb3", border_width=1, font=("Passion One", 15), hover_color="#ffffd9", text_color="#000000")
button5.configure()
button5.place(x=250, y=520)


conexion.commit()


app.bind("<Button-1>", desenfocar)

w = 1200
h = 700
ws = app.winfo_screenwidth()
hs = app.winfo_screenheight()

x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

app.geometry(f"{w}x{h}+{int(x)}+{int(y)}")


app.resizable(False, False)
app.mainloop()