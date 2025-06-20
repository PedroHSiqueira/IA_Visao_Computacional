import cv2
import numpy as np
from time import sleep

largura_min=80
altura_min=80
offset=6
pos_linha=550
delay= 60

detec = []
carros= 0

VIDEO_UM = "./src/videos/video.mp4"
VIDEO_DOIS = "./src/videos/video2.mp4"

def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture(VIDEO_UM)
subtracao = cv2.createBackgroundSubtractorMOG2()

while True:
    ret , frame1 = cap.read()
    tempo = float(1/delay)
    sleep(tempo) 
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    img_sub = subtracao.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
    dilatada = cv2.morphologyEx (dilatada, cv2. MORPH_CLOSE , kernel)
    contorno,h=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255,127,0), 3) 
    for(i,c) in enumerate(contorno):
        (x,y,w,h) = cv2.boundingRect(c)
        validar_contorno = (w >= largura_min) and (h >= altura_min)
        if not validar_contorno:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        centro = pega_centro(x, y, w, h)
        detec.append(centro)
        cv2.circle(frame1, centro, 4, (0, 0,255), -1)

        for (x,y) in detec:
            if y<(pos_linha+offset) and y>(pos_linha-offset):
                carros+=1
                cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0,127,255), 3)
                detec.remove((x,y))
                print("Veiculo Detectado : "+str(carros))

    cv2.putText(frame1, "Contagem: "+str(carros), (800, 675), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),5)
    cv2.imshow("Video Original" , frame1)

    if cv2.waitKey(1) == 27:
        break
    
cap2 = cv2.VideoCapture(VIDEO_UM)
fps = cap2.get(cv2.CAP_PROP_FPS)
total_frames = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
frame_to_capture = max(0, total_frames - int(fps))  

cap2.set(cv2.CAP_PROP_POS_FRAMES, frame_to_capture)
ret, last_frame = cap2.read()
if ret:
    cv2.putText(last_frame, "Contagem: "+str(carros), (800, 675), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),5)
    cv2.imwrite("./src/imagens/screenshot_final.png", last_frame)
    print("Screenshot salva como screenshot_final.png")
cap2.release()

print("Total de Veiculos: " + str(carros))
cv2.destroyAllWindows()
cap.release()
