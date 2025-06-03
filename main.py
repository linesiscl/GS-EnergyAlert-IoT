import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from detector import DetectorGestos
from alerta import AlertaEmergencia
import threading
import time


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Detecção de Gestos")
        self.root.geometry("900x600")

        # Detector e alerta
        self.detector = DetectorGestos()
        self.alert_system = AlertaEmergencia()

        # Variáveis de controle
        self.running = False
        self.cap = None

        # Interface
        self.label = tk.Label(root)
        self.label.pack()

        self.status_text = tk.StringVar()
        self.status_text.set("Status: Parado")
        self.status_label = tk.Label(root, textvariable=self.status_text, font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.toggle_button = tk.Button(root, text="Iniciar Detecção", command=self.toggle_detection, font=("Arial", 14))
        self.toggle_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_detection(self):
        if self.running:
            self.running = False
            self.status_text.set("Status: Parado")
            self.toggle_button.config(text="Iniciar Detecção")
        else:
            self.running = True
            self.status_text.set("Status: Detectando...")
            self.toggle_button.config(text="Parar Detecção")
            threading.Thread(target=self.video_loop).start()

    def video_loop(self):
        self.cap = cv2.VideoCapture("videos/cenario_simulado.mp4")

        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            gesture_detected = self.detector.detect_raised_arms(frame)

            if gesture_detected:
                self.alert_system.trigger_alert()
                cv2.putText(frame, "⚠️ Gesto Detectado!", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Aguardando gesto...", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Exibe no Tkinter
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

            time.sleep(0.03)

        if self.cap:
            self.cap.release()

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
