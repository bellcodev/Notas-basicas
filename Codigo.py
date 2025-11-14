from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os

archivoPath = None

pt = ""
def evento(e):
  global pt
  if pt == "Control_L" and e.keysym == "s":
    if archivoPath == None:
      guardarComo()
    elif archivoPath != None:
      guardar()
  pt = e.keysym

def abrir():
  try:
    global archivoPath
    archivoPath = filedialog.askopenfilename(title="Selecciona un archivo", filetypes=[("Todos los archivos", "*.*")])
    if os.path.exists(archivoPath):
      archivo = open(archivoPath, 'r')
      texto.delete(1.0, END)
      texto.insert(1.0, archivo.read())
      app.title(f"Notas - {os.path.basename(archivoPath)}")
      archivo.close()
    else:
      messagebox.showerror(title="error", message=f"El archivo en la ubicacion: {archivoPath} no existe")
  except ValueError as e:
    messagebox.showerror(title="error", message=f"Error al abrir el archivo: {e}")
    archivoPath = None

def guardar():
  if archivoPath != None:
    archivo = open(archivoPath, 'w')
    archivo.write(texto.get(1.0, END))
    app.after(10, guardar)
    archivo.close()
  else:
    guardarComo()

def guardarComo():
  archivoPath = filedialog.asksaveasfilename(title="Selecciona un archivo", filetypes=[("Todos los archivos", "*.*")])
  archivo = open(f"{archivoPath}.txt", 'w')
  archivo.write(texto.get(1.0, END))
  archivo.close()

def verInfo():
  try:
    messagebox.showinfo('Información del Archivo', f"Nombre: {os.path.basename(archivoPath)} \nUbicacion: {archivoPath} \nExtencion: {os.path.splitext(archivoPath)[1]} \nTamaño: {os.path.getsize(archivoPath)}kb \nFecha de modificación: {os.path.getmtime(archivoPath)} \nFecha de creación: {os.path.getctime(archivoPath)}")
  except ValueError as e:
    print(e)
  except Exception as e:
    messagebox.showerror(title="Error", message="No puedes ver la informacion de un archivo sin tenerlo abierto.")

app = Tk()
app.title("Notas")

app.bind("<Key>", evento)

texto = Text(app)
texto.config(font=(12))
texto.pack(side=LEFT, fill=BOTH, expand=True)
scr = Scrollbar(app)
scr.pack(side=RIGHT, fill=Y)
texto.config(yscrollcommand=scr.set)
scr.config(command=texto.yview)

menu = Menu(app)
app.config(menu=menu)

menufile = Menu(menu, tearoff=0)
menu.add_cascade(label='Archivo', menu=menufile)
menufile.add_command(label='Abrir', command=abrir)
menufile.add_command(label='Guardar', command=guardar)
menufile.add_command(label='Guardar Como', command=guardarComo)

menuview = Menu(menu, tearoff=0)
menu.add_cascade(label='Ver', menu=menuview)
menutema = Menu(menuview, tearoff=0)
menuview.add_cascade(label='Tema', menu=menutema)
menutema.add_cascade(label="Oscuro", command=lambda: texto.config(bg="#333333", fg="#ffffff"))
menutema.add_cascade(label="Claro", command=lambda: texto.config(bg="#ffffff", fg="#000000"))
menuview.add_cascade(label="Ver Info", command=verInfo)

app.mainloop()
