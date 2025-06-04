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

    def alerta(self):
        if self.alert_triggered:
            return  # evita alertas duplicados

        self.alert_triggered = True
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._log_event(timestamp)

        # Executar os alertas em paralelo
        threading.Thread(target=self._som).start()
        threading.Thread(target=self._abrir_janela).start()

        # Esperar um tempo antes de permitir novo alerta
        threading.Timer(10.0, self._reset_alert).start()

    #Essa função é para tocar o som
    def _som(self):
        if winsound:
            # Windows
            winsound.Beep(1000, 500)  # frequência, duração (ms)
        else:
            # Linux/Mac (tenta usar 'afplay' ou 'beep')
            os.system('play -nq -t alsa synth 0.3 sine 1000')  # requer sox instalado

    #Essa função vai abrir uma janela em branco para simular uma lanterna
    def _abrir_janela(self):
        tela_branca = 255 * np.ones((500, 800, 3), dtype=np.uint8)
        cv2.imshow("EMERGENCY LIGHT", tela_branca)
        cv2.waitKey(3000)
        cv2.destroyWindow("EMERGENCY LIGHT")

    def _log_event(self, timestamp):
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] Alerta acionado por gesto de dois bracos levantados\n")

    def _reset_alert(self):
        self.alert_triggered = False


# Necessário para a criação da tela branca
import numpy as np
