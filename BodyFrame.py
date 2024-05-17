from TresPoses import initialize, prepareBody, detectPose
import tkinter as tk
import tkintermapview
from tkinter import Canvas
from tkinter import messagebox
from tkinter import ttk
import cv2
import threading
from PIL import Image, ImageTk



class BodyFrameClass:

    def __init__(self, dron):
        self.dron = dron

        self.pose_commands = {1: "North",  # Pose 1
                              2: "NorthEast",  # Pose 2
                              3: "South"}  # Pose 3

        self.body_control_active = False

    def buildFrame(self, fatherFrame):
        self.BodyFrame = tk.Frame(fatherFrame)

        self.BodyFrame.rowconfigure(0, weight=1)
        self.BodyFrame.rowconfigure(1, weight=30)

        self.BodyFrame.columnconfigure(0, weight=1)
        self.BodyFrame.columnconfigure(1, weight=1)

        # ===== BODY CONTROL FRAME =====
        self.mov_frame = tk.LabelFrame(self.BodyFrame, text="Movimiento")
        self.mov_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

        self.mov_frame.rowconfigure(0, weight=1)
        self.mov_frame.rowconfigure(1, weight=1)

        self.mov_frame.columnconfigure(0, weight=1)
        self.mov_frame.columnconfigure(1, weight=5)

        self.Button6 = tk.Button(self.mov_frame, text="Control por poses", bg="dark orange", fg="black", command=self.start_body_control)
        self.Button6.grid(row=0, column=0, columnspan=2, padx=5, pady=3, sticky="nesw")

        self.Button7 = tk.Button(self.mov_frame, text="Detener control por poses", bg="dark orange", fg="black", command=self.stop_body_control)
        self.Button7.grid(row=1, column=0, columnspan=2, padx=5, pady=3, sticky="nesw")

        # Cargar imágenes
        image1 = Image.open("C:\\Users\\Mariona\\Desktop\\TelecoRenta\\poses_1.png").resize((310, 310), Image.LANCZOS)    # Ruta a la imágen
        image2 = Image.open("C:\\Users\\Mariona\\Desktop\\TelecoRenta\\poses_2.png").resize((305, 150), Image.LANCZOS)
        tk_image1 = ImageTk.PhotoImage(image1)
        tk_image2 = ImageTk.PhotoImage(image2)

        # Crear etiquetas para imágenes
        label1 = tk.Label(self.BodyFrame, image=tk_image1)
        label1.image = tk_image1
        label2 = tk.Label(self.BodyFrame, image=tk_image2)
        label2.image = tk_image2

        label1.grid(row=1, column=0, padx=5, pady=2, sticky="new")
        label2.grid(row=1, column=1, padx=5, pady=2, sticky="nsew")

        self.BodyFrame.pack(expand=True, fill="both")

        return self.BodyFrame


    # ======= POSES (BODY CONTROL) =======
    def start_body_control(self):
        self.body_control_active = True
        messagebox.showinfo("Control con poses", "Mueve los brazos para seguir una trayectoria determinada")
        threading.Thread(target=self.capture_and_process_frames, daemon=True).start()

    def capture_and_process_frames(self):
        cap = cv2.VideoCapture(0)
        initialize()

        while self.body_control_active:
            result, computer_frame = cap.read()
            if result:
                computer_frame = cv2.resize(computer_frame, (720, 480))
                body_landmarks, frame_with_landmarks = prepareBody(computer_frame)
                frame_with_landmarks = cv2.flip(frame_with_landmarks, 1)

                if len(body_landmarks) > 0:
                    mi_pose = detectPose(body_landmarks)
                    if mi_pose is not None:
                        self.dron.changeNavSpeed(float(self.dron.navSpeed))
                        print(f"navigation speed: {self.dron.navSpeed} ")

                        self.dron.startGo()

                        command = self.pose_commands.get(mi_pose, "Stop")
                        self.dron.go(command)
                        print("***** Detected pose:", mi_pose)
                        print(f"Going to: {command}")

                    cv2.putText(frame_with_landmarks, f"Pose {mi_pose}", (100, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)


                cv2.imshow("computer", frame_with_landmarks)
                cv2.waitKey(1)



    def stop_body_control(self):
        self.body_control_active = False
