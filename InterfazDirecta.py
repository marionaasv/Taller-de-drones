import tkinter as tk
from Dron import Dron
from tkinter import Canvas
from tkinter import ttk
from tkinter import messagebox


def connect ():
    global dron, speedSldr
    connection_string ='tcp:127.0.0.1:5763'
    baud = 115200
    dron.connect(connection_string, baud)
    print("Connected!")
    #speedSldr.set(1)


def arm_button_callback(button):
    button.config(bg="light green")

def arm (button):
    global dron
    button.config(bg="red")

    dron.arm(callback=arm_button_callback(button))


def takeoff ():
    global dron
    alt = float(8)
    print(f"Selected TO altitude: {alt} m")
    dron.takeOff (alt, blocking=False,  callback=informar, params='VOLANDO')

def informar (mensaje):
    global dron
    print ('informar')
    messagebox.showinfo("showinfo", "Mensaje del dron:--->  "+mensaje)

def RTL():
    global dron
    dron.RTL(blocking = False, callback = informar, params= 'EN TIERRA')

# ====== NAVIGATION FUNCTIONS ======

def change_speed (speed):
    global dron
    global speedSldr
    dron.changeNavSpeed(float(speed))
    print(f"speed: {speed}")

def go(direction):
    global dron
    if not dron.going:
        dron.startGo()
    print('vamos a: ', direction)
    dron.go(direction)

def stopGo():
    global dron
    dron.stopGo()

def new_function():
    pass


# ================= DASHBOARD INICIAL =================

def crear_ventana():
    global dron
    global  altShowLbl, headingShowLbl,  speedSldr, gradesSldr, speedShowLbl
    global takeOffBtn

    dron = Dron()

    ventana = tk.Tk()
    ventana.title("Ventana con botones y entradas")
    ventana.rowconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=1)
    ventana.rowconfigure(2, weight=1)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)
    ventana.columnconfigure(2, weight=1)
    ventana.columnconfigure(3, weight=1)

    # Configuración del Frame de Control
    controlFrame = tk.LabelFrame(ventana, text="Control")
    controlFrame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    controlFrame.rowconfigure(0, weight=1)
    controlFrame.rowconfigure(1, weight=1)
    controlFrame.rowconfigure(2, weight=1)
    controlFrame.rowconfigure(3, weight=1)
    controlFrame.rowconfigure(4, weight=1)
    controlFrame.rowconfigure(5, weight=1)
    controlFrame.rowconfigure(6, weight=1)
    controlFrame.rowconfigure(7, weight=1)
    controlFrame.rowconfigure(8, weight=1)
    controlFrame.rowconfigure(9, weight=1)
    controlFrame.rowconfigure(10, weight=1)

    controlFrame.columnconfigure(0, weight=1)
    controlFrame.columnconfigure(1, weight=1)
    controlFrame.columnconfigure(2, weight=1)
    controlFrame.columnconfigure(3, weight=1)

    connectBtn = tk.Button(controlFrame, text="Conectar", bg="dark orange", command = connect)
    connectBtn.grid(row=0, column=0, columnspan=4, padx=3, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    armBtn = tk.Button(controlFrame, text="Armar", bg="dark orange", command=lambda: arm(armBtn))
    armBtn.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    takeOffBtn = tk.Button(controlFrame, text="Despegar", bg="dark orange", command=takeoff)
    takeOffBtn.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    RTLBtn = tk.Button(controlFrame, text="RTL", bg="dark orange", command=RTL)
    RTLBtn.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)


# ================= FRAME/BOTONES NAVEGACIÓN =================

    speedSldr = tk.Scale(controlFrame, label="Velocidad (m/s):", resolution=1, from_=0, to=20, tickinterval=5,
                         orient=tk.HORIZONTAL, command=change_speed)
    speedSldr.set(1)
    speedSldr.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    navFrame = tk.LabelFrame (controlFrame, text = "Navegación")
    navFrame.grid(row=7, column=0, columnspan=4, padx=50, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # Configuración del Frame de Navegación
    navFrame.rowconfigure(0, weight=1)
    navFrame.rowconfigure(1, weight=1)
    navFrame.rowconfigure(2, weight=1)

    navFrame.columnconfigure(0, weight=1)
    navFrame.columnconfigure(1, weight=1)
    navFrame.columnconfigure(2, weight=1)


    NWBtn = tk.Button(navFrame, text="NW", bg="dark orange",
                        command= lambda: go("NorthWest"))
    NWBtn.grid(row=0, column=0, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    NoBtn = tk.Button(navFrame, text="No", bg="dark orange",
                        command= lambda: go("North"))
    NoBtn.grid(row=0, column=1, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    NEBtn = tk.Button(navFrame, text="NE", bg="dark orange",
                        command= lambda: go("NorthEast"))
    NEBtn.grid(row=0, column=2, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    WeBtn = tk.Button(navFrame, text="We", bg="dark orange",
                        command=lambda: go("West"))
    WeBtn.grid(row=1, column=0, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    StopBtn = tk.Button(navFrame, text="St", bg="dark orange",
                        command=lambda: go("Stop"))
    StopBtn.grid(row=1, column=1, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    EaBtn = tk.Button(navFrame, text="Ea", bg="dark orange",
                        command=lambda: go("East"))
    EaBtn.grid(row=1, column=2, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    SWBtn = tk.Button(navFrame, text="SW", bg="dark orange",
                        command=lambda: go("SouthWest"))
    SWBtn.grid(row=2, column=0, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    SoBtn = tk.Button(navFrame, text="So", bg="dark orange",
                        command=lambda: go("South"))
    SoBtn.grid(row=2, column=1, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    SEBtn = tk.Button(navFrame, text="SE", bg="dark orange",
                        command=lambda: go("SouthEast"))
    SEBtn.grid(row=2, column=2, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)


    # ================ FRAME ADICIONAL (AÑADIR FUNCIONALIDADES EXTRA/RETOS) ================

    userFrame = tk.LabelFrame(ventana, text="Funcionalidades extra")
    userFrame.grid(row=0, column=3, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    # Configuración del Frame de usuario: el usuario puede añadir/quitar filas y columnas como prefiera
    userFrame.rowconfigure(0, weight=1)
    userFrame.rowconfigure(1, weight=1)
    userFrame.rowconfigure(2, weight=1)
    userFrame.rowconfigure(3, weight=1)
    userFrame.rowconfigure(4, weight=1)
    userFrame.rowconfigure(5, weight=1)
    userFrame.rowconfigure(6, weight=1)
    userFrame.rowconfigure(7, weight=1)
    userFrame.rowconfigure(8, weight=1)
    userFrame.rowconfigure(9, weight=1)
    userFrame.rowconfigure(10, weight=1)

    userFrame.columnconfigure(0, weight=1)
    userFrame.columnconfigure(1, weight=1)
    userFrame.columnconfigure(2, weight=1)
    userFrame.columnconfigure(3, weight=1)

    # Estos botones se pueden configurar como se prefiera y añadir cualquier funcionalidad deseada
    newButton1 = tk.Button(userFrame, text="Button 1", bg="light grey", command=new_function)
    newButton1.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky=tk.N + tk.E + tk.W)

    newButton2 = tk.Button(userFrame, text="Button 2", bg="light grey", command=new_function)
    newButton2.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky=tk.N + tk.E + tk.W)

    newButton3 = tk.Button(userFrame, text="Button 3", bg="light grey", command=new_function)
    newButton3.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky=tk.N + tk.E + tk.W)


    return ventana

if __name__ == "__main__":
    ventana = crear_ventana()
    ventana.mainloop()