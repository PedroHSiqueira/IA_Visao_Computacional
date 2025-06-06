import cv2
from time import sleep
import math

offset = 6
pos_linha = 550
delay = 60
carros = 0

VIDEO = "./src/videos/video.mp4"
CARS_XML = "./src/models/cars.xml"

def pega_centro(x, y, w, h):
    cx = x + int(w / 2)
    cy = y + int(h / 2)
    return cx, cy

cap = cv2.VideoCapture(VIDEO)
car_cascade = cv2.CascadeClassifier(CARS_XML)
detec = []
carros_passados = []

def ja_contado(centro):
    for c in carros_passados:
        if math.hypot(centro[0] - c[0], centro[1] - c[1]) < 30:
            return True
    return False

while True:
    ret, frame1 = cap.read()
    if not ret:
        break
    tempo = float(1 / delay)
    sleep(tempo)
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    carros_detectados = car_cascade.detectMultiScale(grey, 1.1, 2)

    cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255, 127, 0), 3)
    novos_centros = []
    for (x, y, w, h) in carros_detectados:
        centro = pega_centro(x, y, w, h)
        novos_centros.append(centro)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame1, centro, 4, (0, 0, 255), -1)

    novos_passados = []
    for centro in novos_centros:
        if (pos_linha - offset) < centro[1] < (pos_linha + offset):
            if not ja_contado(centro):
                carros += 1
                novos_passados.append(centro)
                cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
                print("Veiculo Detectado : " + str(carros))
    carros_passados.extend(novos_passados)

    if len(carros_passados) > 1000:
        carros_passados = carros_passados[-500:]

    cv2.putText(frame1, "Contagem: "+str(carros), (800, 675), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),5)
    cv2.imshow("Video Original", frame1)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()