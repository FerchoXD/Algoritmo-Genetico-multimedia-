import tkinter as tk
from tkinter import ttk, Frame, Label, Entry, Button, END
import logica
from PIL import Image, ImageTk
from tkinter import messagebox


# Configuración de la ventana
ventana = tk.Tk()
ventana.config(bg='black')
ventana.geometry('560x388')
ventana.resizable(0,0)
ventana.title('Entradas')

# Frames para organizar los widgets
frame1 = Frame(ventana, bg='gray15')
frame1.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)
frame2 = Frame(ventana, bg='gray16')
frame2.grid(column=1, row=0, sticky='nsew', padx=5, pady=5)

# Campos y etiquetas
fields = ["initial_poblation", "max_poblation", "resolution", "a", "b", "probability_individual", "probability_gen", "generations_number"]
entries = {}
for i, field in enumerate(fields):
    Label(frame1, text=f'{field}:', width=10, bg='gray15', fg='green').grid(column=0, row=i, pady=5, padx=5)
    entry = Entry(frame1, width=20, font=('Arial', 12))
    entry.grid(column=1, row=i)
    entries[field] = entry

# Dropdown para 'opt'
opt_options = ["MAX", "MIN"]
var_opt = tk.StringVar()
var_opt.set(opt_options[0])
combo_opt = ttk.Combobox(frame1, textvariable=var_opt, values=opt_options, width=18, font=('Arial', 12))
combo_opt.grid(column=1, row=len(fields), padx=5, pady=5)
Label(frame1, text='option:', width=10, bg='gray15', fg='green').grid(column=0, row=len(fields), pady=5, padx=5)

# Función para obtener datos
def get_data():
    print("Obteniendo datos...")
    try:
        # Recoger los datos de la interfaz y validarlos
        data = {}
        for field in fields:
            value = entries[field].get().strip()
            if not value:
                messagebox.showerror("Error", f"El campo '{field}' está vacío")
                return
            data[field] = value

        # Añadir el valor del dropdown
        data["option"] = var_opt.get()

        # Convertir los valores a los tipos de datos correctos y manejar errores de conversión
        try:
            data_converted = {
                "initial_poblation": int(data["initial_poblation"]),
                "max_poblation": int(data["max_poblation"]),
                "resolution": float(data["resolution"]),
                "a": float(data["a"]),
                "b": float(data["b"]),
                "probability_individual": float(data["probability_individual"]),
                "probability_gen": float(data["probability_gen"]),
                "generations_number": int(data["generations_number"]),
                "option": data["option"]
            }
        except ValueError as e:
            messagebox.showerror("Error de Conversión", f"Error en la conversión de tipos de datos: {e}")
            return

        # Llamada a la función que ejecuta el algoritmo
        print("Llamando a la función main de logica.py")
        print("datos obtenidos")
        print("initial_poblation: ", data_converted["initial_poblation"])
        print("max_poblation: ", data_converted["max_poblation"])
        print("resolution: ", data_converted["resolution"])
        print("a: ", data_converted["a"])
        print("b: ", data_converted["b"])
        print("probability_individual: ", data_converted["probability_individual"])
        print("probability_gen: ", data_converted["probability_gen"])
        print("generations_number: ", data_converted["generations_number"])
        print("option: ", data_converted["option"])
        
        logica.main(**data_converted)
    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar los datos: {e}")



# Botón para obtener datos
button_get_data = Button(frame1, text="Obtener Datos", command=get_data, bg='green', fg='white', bd=5)
button_get_data.grid(columnspan=2, row=len(fields)+1, pady=10)

# Imagen de fondo en el frame2
try:
    pil_image = Image.open('./DNA.jpeg')
    tk_image = ImageTk.PhotoImage(pil_image)
    label_image = tk.Label(frame2, image=tk_image)
    label_image.image = tk_image  # Guarda una referencia a la imagen
    label_image.grid(column=0, row=1, padx=5, pady=5)
except IOError as e:
    print(f"Error al cargar la imagen: {e}")

ventana.mainloop()
