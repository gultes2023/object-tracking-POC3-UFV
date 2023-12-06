import cv2
import numpy as np
import imutils
from collections import deque

# Classe ObjectTracker para rastrear um objeto específico em vídeo.
class ObjectTracker:
    def __init__(self, initial_position):
        # Usa um deque como buffer circular para armazenar posições passadas do objeto.
        self.positions = deque(maxlen=trackingBufferSize)
        self.positions.append(initial_position)  # Inicializa com a posição inicial.
        self.counted = False  # Flag para verificar se o objeto já foi contado.

# Função de callback vazia para usar com as trackbars.
def callback(value):
    pass

# Configura trackbars para ajustar os limites de cor HSV.
def setup_trackbars():
    cv2.namedWindow("Trackbars", 0)
    init_values = {"H_MIN": 30, "S_MIN": 30, "V_MIN": 0, "H_MAX": 105, "S_MAX": 255, "V_MAX": 255}
    # Loop para criar trackbars para Hue, Saturation e Value (MIN e MAX).
    for i in ["MIN", "MAX"]:
        for j in "HSV":
            value = init_values[f"{j}_{i}"]
            cv2.createTrackbar(f"{j}_{i}", "Trackbars", value, 255, callback)

# Obtém os valores atuais das trackbars.
def get_trackbar_values():
    values = {}
    # Loop para obter os valores atuais para Hue, Saturation e Value (MIN e MAX).
    for i in ["MIN", "MAX"]:
        for j in "HSV":
            v = cv2.getTrackbarPos(f"{j}_{i}", "Trackbars")
            values[f"{j}_{i}"] = v
    return values

# Verifica se um novo objeto detectado é realmente novo com base na distância.
def is_new_object(existing_trackers, new_center, min_dist=50):
    for tracker in existing_trackers:
        # Calcula a distância entre o novo centro e centros existentes.
        if np.linalg.norm(np.array(tracker.positions[0]) - np.array(new_center)) < min_dist:
            return False
    return True

# Configura as trackbars para ajuste de cor.
setup_trackbars()

# Inicia a captura de vídeo da webcam.
cap = cv2.VideoCapture(0)

# Define o tamanho do buffer para rastreamento dos objetos.
trackingBufferSize = 64
object_trackers = []  # Lista para armazenar os rastreadores de objetos.
object_count = 0  # Contador de objetos detectados.

# Loop principal para processamento do vídeo.
while True:
    # Lê um frame do vídeo.
    grabbed, frame = cap.read()
    if not grabbed:
        break

    # Obtém valores das trackbars e configura os limites de cor HSV.
    trackbar_values = get_trackbar_values()
    hueLower, saturationLower, valueLower = (trackbar_values["H_MIN"], trackbar_values["S_MIN"], trackbar_values["V_MIN"])
    hueUpper, saturationUpper, valueUpper = (trackbar_values["H_MAX"], trackbar_values["S_MAX"], trackbar_values["V_MAX"])

    # Redimensiona o frame, aplica desfoque para reduzir ruído e converte para HSV.
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Cria uma máscara que isola a cor definida pelos limites de HSV.
    mask = cv2.inRange(hsv, (hueLower, saturationLower, valueLower), (hueUpper, saturationUpper, valueUpper))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Encontra contornos na máscara.
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Processa cada contorno encontrado.
    for c in cnts:
        # Ignora contornos muito pequenos.
        if cv2.contourArea(c) < 100:
            continue

        # Encontra o círculo que envolve o contorno e calcula seu centro.
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))

        # Se o raio for grande o suficiente, desenha um círculo no frame.
        if radius > 10:
            cv2.circle(frame, center, int(radius), (0, 255, 255), 2)

            # Verifica se o centro atual representa um novo objeto.
            if is_new_object(object_trackers, center):
                object_trackers.append(ObjectTracker(center))
                object_count += 1
                print(f"Novo objeto circular verde detectado: {object_count}")
            else:
                # Se não for um novo objeto, atualiza a posição no rastreador existente.
                for tracker in object_trackers:
                    if np.linalg.norm(np.array(tracker.positions[0]) - np.array(center)) < 50:
                        tracker.positions.appendleft(center)
                        break

    # Desenha as linhas de rastreamento para cada objeto.
    for tracker in object_trackers:
        for i in range(1, len(tracker.positions)):
            if tracker.positions[i - 1] is None or tracker.positions[i] is None:
                continue
            cv2.line(frame, tracker.positions[i - 1], tracker.positions[i], (0, 255, 0), 2)

    # Exibe as janelas com a máscara e o frame processado.
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    # Sai do loop se a tecla 'q' for pressionada.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura de vídeo e fecha todas as janelas abertas.
cap.release()
cv2.destroyAllWindows()
