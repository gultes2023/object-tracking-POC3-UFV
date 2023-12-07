import cv2
import numpy as np
import imutils
from collections import deque

# Classe para rastrear objetos em movimento em vídeos.
class ObjectTracker:
    def __init__(self, initial_position):
        # Deque para armazenar as posições do objeto, limitada pelo tamanho do buffer de rastreamento.
        self.positions = deque(maxlen=trackingBufferSize)
        self.positions.append(initial_position)  # Adiciona a posição inicial ao deque.
        self.counted = False  # Indica se o objeto foi contado ou não.

# Função de callback para os controles deslizantes (trackbars), mas não faz nada.
def callback(value):
    pass

# Configuração dos controles deslizantes (trackbars) para ajuste dos valores HSV.
def setup_trackbars():
    cv2.namedWindow("Trackbars", 0)
    init_values = {"H_MIN": 0, "S_MIN": 0, "V_MIN": 145, "H_MAX": 220, "S_MAX": 50, "V_MAX": 255}
    # Cria controles deslizantes para cada componente HSV (Mínimo e Máximo).
    for i in ["MIN", "MAX"]:
        for j in "HSV":
            cv2.createTrackbar(f"{j}_{i}", "Trackbars", init_values[f"{j}_{i}"], 255, callback)

# Obtém os valores dos controles deslizantes.
def get_trackbar_values():
    values = {}
    # Recupera os valores de cada controle deslizante para as componentes HSV.
    for i in ["MIN", "MAX"]:
        for j in "HSV":
            values[f"{j}_{i}"] = cv2.getTrackbarPos(f"{j}_{i}", "Trackbars")
    return values

# Verifica se o objeto detectado é novo, baseado na distância mínima.
def is_new_object(existing_trackers, new_center, min_dist=50):
    for tracker in existing_trackers:
        # Se a distância entre o novo centro e algum centro existente for menor que a mínima, não é um novo objeto.
        if np.linalg.norm(np.array(tracker.positions[0]) - np.array(new_center)) < min_dist:
            return False
    return True

# Configura os controles deslizantes.
setup_trackbars()
# Inicializa a captura de vídeo.
cap = cv2.VideoCapture('Muriquis.mp4')

# Define o tamanho do buffer de rastreamento e inicializa a lista de rastreadores e o contador de objetos.
trackingBufferSize = 64
object_trackers = []
object_count = 0

# Loop principal para processamento de cada frame do vídeo.
while True:
    grabbed, frame = cap.read()
    if not grabbed:
        break

    # Obtém os valores atuais dos controles deslizantes para o filtro HSV.
    trackbar_values = get_trackbar_values()
    hueLower, saturationLower, valueLower = trackbar_values["H_MIN"], trackbar_values["S_MIN"], trackbar_values["V_MIN"]
    hueUpper, saturationUpper, valueUpper = trackbar_values["H_MAX"], trackbar_values["S_MAX"], trackbar_values["V_MAX"]

    # Redimensiona, desfoca e converte o frame para o espaço de cor HSV.
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Cria uma máscara com os valores HSV especificados.
    mask = cv2.inRange(hsv, (hueLower, saturationLower, valueLower), (hueUpper, saturationUpper, valueUpper))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Encontra contornos na máscara.
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Processa cada contorno encontrado.
    for c in cnts:
        if cv2.contourArea(c) < 100:
            continue

        # Calcula o círculo mínimo envolvente e o centro do contorno.
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))

        # Desenha um círculo ao redor do objeto detectado se o raio for suficientemente grande.
        if radius > 10:
            cv2.circle(frame, center, int(radius), (0, 255, 255), 2)

            # Verifica se é um novo objeto e, em caso afirmativo, adiciona um rastreador.
            if is_new_object(object_trackers, center):
                object_trackers.append(ObjectTracker(center))
                object_count += 1
                print(f"Novo objeto branco detectado: {object_count}")
            else:
                # Atualiza a posição do objeto nos rastreadores existentes.
                for tracker in object_trackers:
                    if np.linalg.norm(np.array(tracker.positions[0]) - np.array(center)) < 50:
                        tracker.positions.appendleft(center)
                        break

    # Desenha linhas de rastreamento para cada objeto.
    for tracker in object_trackers:
        for i in range(1, len(tracker.positions)):
            if tracker.positions[i - 1] is None or tracker.positions[i] is None:
                continue
            cv2.line(frame, tracker.positions[i - 1], tracker.positions[i], (255, 255, 255), 2)

    # Exibe a máscara e o frame processado.
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    # Encerra o loop se a tecla 'q' for pressionada.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o recurso de captura de vídeo e fecha todas as janelas.
cap.release()
cv2.destroyAllWindows()
