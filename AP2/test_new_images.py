import cv2
import os
from main import FaceRecognizer

def test_new_images():
    # Carregar o modelo treinado
    recognizer = FaceRecognizer()
    try:
        recognizer.load_model("modelo_reconhecimento.pkl")
        print("Modelo carregado com sucesso!")
        print(f"Pessoas que o modelo reconhece: {', '.join(recognizer.get_known_persons())}")
    except Exception as e:
        print(f"Erro ao carregar o modelo: {str(e)}")
        return

    # Diretório com as imagens de teste
    test_dir = "imagens_teste"
    
    # Verificar se o diretório existe
    if not os.path.exists(test_dir):
        print(f"\nDiretório {test_dir} não encontrado!")
        print("Por favor, crie uma pasta 'imagens_teste' e adicione as imagens que deseja testar lá.")
        return
    
    # Testar cada imagem no diretório
    for img_file in os.listdir(test_dir):
        if img_file.endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(test_dir, img_file)
            print(f"\nTestando imagem: {img_file}")
            
            # Carregar a imagem
            image = cv2.imread(img_path)
            if image is None:
                print(f"Erro ao carregar a imagem: {img_path}")
                continue
            
            # Fazer a previsão
            prediction = recognizer.predict(image)
            
            # Mostrar a imagem com a previsão
            cv2.putText(image, f"Pessoa: {prediction}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Mostrar a imagem
            cv2.imshow("Reconhecimento Facial", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    test_new_images() 