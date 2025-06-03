import threading
import time
import cv2
from datetime import datetime
import os
import platform

try:
    # Usar apenas se for Windows
    import winsound
except ImportError:
    winsound = None


class AlertaEmergencia:
    def __init__(self, log_file="logs.txt"):
        self.log_file = log_file
        self.alert_triggered = False

    def trigger_alert(self):
        if self.alert_triggered:
            return  # evita alertas duplicados

        self.alert_triggered = True
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._log_event(timestamp)

        # Executar os alertas em paralelo
        threading.Thread(target=self._play_sound).start()
        threading.Thread(target=self._show_white_screen).start()

        # Esperar um tempo antes de permitir novo alerta
        threading.Timer(10.0, self._reset_alert).start()

    #Essa função é para tocar o som
    def _play_sound(self):
        if winsound:
            # Windows
            winsound.Beep(1000, 500)  # frequência, duração (ms)
        else:
            # Linux/Mac (tenta usar 'afplay' ou 'beep')
            os.system('play -nq -t alsa synth 0.3 sine 1000')  # requer sox instalado

    #Essa função vai abrir uma janela em branco para simular uma lanterna
    def _show_white_screen(self):
        white_image = 255 * np.ones((500, 800, 3), dtype=np.uint8)
        cv2.namedWindow("EMERGENCY LIGHT", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("EMERGENCY LIGHT", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("EMERGENCY LIGHT", white_image)
        cv2.waitKey(3000)
        cv2.destroyWindow("EMERGENCY LIGHT")

    def _log_event(self, timestamp):
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] Alerta acionado por gesto de dois braços levantados\n")

    def _reset_alert(self):
        self.alert_triggered = False


# Necessário para a criação da tela branca
import numpy as np
