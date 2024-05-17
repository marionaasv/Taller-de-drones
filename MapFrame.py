import json
import tkinter as tk
import tkintermapview
from tkinter import Canvas
from tkinter import messagebox
from tkinter import ttk
from pymavlink import mavutil
from PIL import Image, ImageTk


class MapFrameClass:

    def __init__(self, dron):
        self.dron = dron

        self.setting_geofence = False
        self.vertex_count = 0
        self.geofencePoints = []

        # Parámetros para poder establecer WP/ realizar GO TO
        self.destination_WP = None
        self.reach_WP = False
        self.activate_goto = False

        # Parámetros para establecer el trazado del dron
        self.trace = False
        self.last_position = None  # actualizar trazado

        # Iconos del dron y markers
        self.drone_marker = None
        self.marker = False  # Para activar el marker (en forma de icono de dron)
        self.icon = Image.open("drone.png")
        self.resized_icon = self.icon.resize((50, 50), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.resized_icon)

        self.marker_photo = Image.open("marker_icon.png")
        self.resized_marker_icon = self.marker_photo.resize((20, 20), Image.LANCZOS)
        self.marker_icon = ImageTk.PhotoImage(self.resized_marker_icon)

    def buildFrame(self, fatherFrame):
        self.MapFrame = tk.Frame(fatherFrame)  # create new frame where the map will be allocated
        self.map_widget = tkintermapview.TkinterMapView(self.MapFrame, width=900, height=600, corner_radius=0)
        self.map_widget.grid(row=1, column=0, columnspan=6, padx=5, pady=5)

        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)

        self.map_widget.set_position(41.276430, 1.988686)  # Coordenadas del Dronelab
        self.map_widget.set_zoom(20)

        self.initial_lat = 41.276430
        self.initial_lon = 1.988686

        self.MapFrame.rowconfigure(0, weight=1)
        self.MapFrame.rowconfigure(1, weight=10)

        self.MapFrame.columnconfigure(0, weight=1)
        self.MapFrame.columnconfigure(1, weight=1)
        self.MapFrame.columnconfigure(2, weight=1)
        self.MapFrame.columnconfigure(3, weight=1)
        self.MapFrame.columnconfigure(4, weight=1)
        self.MapFrame.columnconfigure(5, weight=1)


        # ===== FRAME DE GEO FENCE ======
        self.geofence_frame = tk.LabelFrame(self.MapFrame, text="Geo Fence")
        self.geofence_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=4, sticky=tk.N + tk.S + tk.E + tk.W)

        self.geofence_frame.rowconfigure(0, weight=1)
        self.geofence_frame.rowconfigure(1, weight=1)

        self.geofence_frame.columnconfigure(0, weight=1)
        self.geofence_frame.columnconfigure(1, weight=1)

        self.Button1 = tk.Button(self.geofence_frame, text="Crear Geo Fence", bg="dark green", fg="white",
                                 command=self.activate_geofence_mode)
        self.Button1.grid(row=0, column=0, columnspan=2, padx=5, pady=3, sticky="nesw")

        self.Button2 = tk.Button(self.geofence_frame, text="Establecer Geo Fence ", bg="dark green", fg="white",
                                 command=self.GeoFence)
        self.Button2.grid(row=1, column=0, columnspan=2, padx=5, pady=3, sticky="nesw")

        self.count_WP = 0
        self.dron.geofence_markers = []
        self.markers = []


        # ===== FRAME DE NAVEGACIÓN ======
        self.nav_frame = tk.LabelFrame(self.MapFrame, text="Navegación")
        self.nav_frame.grid(row=0, column=3, columnspan=3, padx=10, pady=4, sticky=tk.N + tk.S + tk.E + tk.W)

        self.nav_frame.rowconfigure(0, weight=1)
        self.nav_frame.rowconfigure(1, weight=1)

        self.nav_frame.columnconfigure(0, weight=1)
        self.nav_frame.columnconfigure(1, weight=1)

        self.Button3 = tk.Button(self.nav_frame, text="Establecer WP", bg="black", fg="white", command=self.enable_wp_setting)
        self.Button3.grid(row=0, column=0, padx=5, pady=3, sticky="nesw")

        self.Button4 = tk.Button(self.nav_frame, text="GO TO WP", bg="black", fg="white", command=self.start_goto)
        self.Button4.grid(row=0, column=1, padx=5, pady=3, sticky="nesw")

        self.Button5 = tk.Button(self.nav_frame, text="Mostrar trazado", bg="black", fg="white", command=self.set_trace)
        self.Button5.grid(row=1, column=0, padx=5, pady=3, sticky="nesw")

        self.Button9 = tk.Button(self.nav_frame, text="Mostrar dron", bg="black", fg="white", command=self.set_drone_marker)
        self.Button9.grid(row=1, column=1, padx=5, pady=3, sticky="nesw")

        return self.MapFrame


    # ====== GEO FENCE ======
    def activate_geofence_mode(self):
        self.setting_geofence = True
        messagebox.showinfo("", "Clic botón derecho para crear los vértices del geo fence.\n Clic 'Establecer Geo Fence' una vez terminado")
        self.map_widget.add_right_click_menu_command(label="Add Marker", command=self.add_marker_event,
                                                     pass_coords=True)

    def add_marker_event(self, coords):
        if self.setting_geofence:
            self.vertex_count+=1
            marker_text = f"Vertex {self.vertex_count}"

            print("Add marker at:", coords)
            marker = self.map_widget.set_marker(coords[0], coords[1], text=marker_text)

            self.geofencePoints.append(
                {'lat':coords[0], 'lon':coords[1]})
            if len(self.geofencePoints) > 1:
                last_two_points = [self.geofencePoints[-2], self.geofencePoints[-1]]
                polygon_geofence = self.map_widget.set_path([
                    (point['lat'], point['lon']) for point in last_two_points])

        elif self.reach_WP:
            marker = self.map_widget.set_marker(coords[0], coords[1], text="", icon=self.marker_icon, icon_anchor="center")
            self.destination_WP = coords
            print(f"Navigate to reach WP: {self.destination_WP}")


    def GeoFence(self):
        try:
            polygon = self.map_widget.set_polygon(
                [(point['lat'], point['lon']) for point in self.geofencePoints],
                fill_color=None,
                #outline_color="blue",
                border_width=12,
                # command=polygon_click,
                name="GeoFence_polygon"
            )
            print ('geofence Points: ', self.geofencePoints)
            self.dron.setGEOFence (json.dumps(self.geofencePoints))
            messagebox.showinfo("Operación correcta", "El geo fence se ha establecido correctamente!")
            self.setting_geofence = False

        except Exception as e:
            messagebox.showerror("Error", f"Error al establecer el geo fence: {str(e)}")


    # ======== ESTABLECER WP Y REALIZAR GO TO ========
    def enable_wp_setting(self):
        self.reach_WP = not self.reach_WP
        if self.reach_WP:
            self.Button3.config(text="Desactivar 'establecer WP'")
            messagebox.showinfo("Establecer WP", "Clic derecho en el mapa para seleccionar el WP de destino.")
            self.map_widget.add_right_click_menu_command(label="Add Marker", command=self.add_marker_event,
                                                             pass_coords=True)

        if not self.reach_WP:
            self.Button3.config(text="Establecer WP")
            self.remove_right_click_menu_command(label="Add Marker")


    def remove_right_click_menu_command(self, label):
        self.map_widget.right_click_menu_commands = [cmd for cmd in self.map_widget.right_click_menu_commands if cmd['label'] != label]


    def start_goto(self):
        self.activate_goto = True
        if self.activate_goto and self.destination_WP:
            print(f"Destionation WP coordinates: {self.destination_WP}")
            self.dron.goto(float(self.destination_WP[0]), float(self.destination_WP[1]), float(8), blocking=False)



 # ======= ESTABLECER ICONO DRON (MARKER) =======
    def set_drone_marker(self):
        self.marker = not self.marker
        if self.marker:
            self.drone_marker = self.map_widget.set_marker(self.initial_lat, self.initial_lon,
                                                           marker_color_outside="blue", marker_color_circle="black",
                                                           text="", text_color="blue",
                                                           icon=self.photo, icon_anchor="center")
            if not self.dron.sendTelemetryInfo:
                self.dron.send_telemetry_info(self.process_telemetry_info, self.update_drone_and_trace)
        else:
            # Eliminar el marker del mapa
            if self.drone_marker:
                self.map_widget.delete(self.drone_marker)
                self.drone_marker = None

            if not self.trace:
                self.dron.stop_sending_telemetry_info()


    def process_telemetry_info(self, telemetry_info):
        print("Received telemetry data:", telemetry_info)


    def update_drone_and_trace(self, lat, lon):
        if self.trace:
            if self.last_position:
                self.map_widget.set_path([self.last_position, (lat, lon)], width=5)
            self.last_position = (lat, lon)

        if self.marker:
            if self.drone_marker:
                self.map_widget.delete(self.drone_marker)
            self.drone_marker = self.map_widget.set_marker(lat, lon,
                                                           marker_color_outside="blue",
                                                           marker_color_circle="black",
                                                           text="", text_color="blue",
                                                           icon=self.photo, icon_anchor="center")

    # ======= MARCAR TRAZADO DEL DRON =======
    def set_trace(self):
        self.trace = not self.trace
        if self.trace:
            if not self.dron.sendTelemetryInfo:
                self.dron.send_telemetry_info(self.process_telemetry_info, self.update_drone_and_trace)

        else:
            self.map_widget.delete_all_path()
            self.last_position = []
            if not self.marker:
                self.dron.stop_sending_telemetry_info()

