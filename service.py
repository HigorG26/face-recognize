import cv2
import mahotas
import numpy as np
from tkinter import messagebox

class ProcessadorImagens:
    def __init__(self):
        self.classificador = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    
    def processar_uma_imagem(self, caminho_imagem):
        try:
            imagem = cv2.imdecode(
                np.fromfile(caminho_imagem, dtype=np.uint8), 
                cv2.IMREAD_COLOR
            )
            
            if imagem is None:
                messagebox.showerror("Erro", f"Não foi possível ler a imagem: {caminho_imagem}")
                return None
            
            img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) ##Tons de cinza
            img_suave = cv2.blur(img_gray, (7, 7)) ##Suavização
            T = mahotas.thresholding.otsu(img_suave) ##Binarização
            img_bin = img_suave.copy()
            img_bin[img_bin > T] = 255
            img_bin[img_bin < 255] = 0
            img_bin = cv2.bitwise_not(img_bin) ##Inversão
            bordas = cv2.Canny(img_bin, 70, 150) ##Detecção de bordas
            contornos, _ = cv2.findContours(bordas.copy(),
                                          cv2.RETR_EXTERNAL, 
                                          cv2.CHAIN_APPROX_SIMPLE)
            
            resultado = np.vstack([
                np.hstack([img_gray, img_suave]),
                np.hstack([img_bin, bordas])
            ]) ##Visualização
            
            faces = self.classificador.detectMultiScale(
                img_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            ) ##Detectar faces
            
            img_faces = imagem.copy() 
            for (x, y, w, h) in faces:
                cv2.rectangle(img_faces, (x, y), (x + w, y + h), (0, 255, 255), 2) ##Desenhar retângulos nas faces
            
            return {
                'tem_rosto': len(faces) > 0,
                'faces': faces,
                'resultado': resultado,
                'img_faces': img_faces,
                'num_objetos': len(contornos)
            } ##Retorno
            
        except Exception as e:
            print(f"Erro no processamento: {str(e)}")
            return None