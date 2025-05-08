import cv2
import os
from main import FaceRecognizer

def test_image(image_path, recognizer):
    # Carregar a imagem
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        return
    
    # Fazer a previsão
    prediction = recognizer.predict(image)
    
    # Mostrar a imagem com a previsão
    cv2.putText(image, f"Pessoa: {prediction}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Mostrar a imagem
    cv2.imshow("Reconhecimento Facial", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    # Carregar o modelo treinado
    recognizer = FaceRecognizer()
    try:
        recognizer.load_model("modelo_reconhecimento.pkl")
        print("Modelo carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o modelo: {str(e)}")
        return

    # Diretório com as imagens de teste
    test_dir = "imagens"
    
    # Testar cada imagem no diretório
    for img_file in os.listdir(test_dir):
        if img_file.endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(test_dir, img_file)
            print(f"\nTestando imagem: {img_file}")
            test_image(img_path, recognizer)

if __name__ == "__main__":
    main() 