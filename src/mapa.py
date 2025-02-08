import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import cv2
import numpy as np
from PIL import Image

# Configurar o caminho do Tesseract OCR (caso necessário)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configurar o caminho do Poppler
poppler_path = r"C:\poppler\Library\bin"

def preprocessar_imagem(img):
    """Pré-processamento para melhorar OCR em texto em negrito."""
    img = img.convert("L")  # Converter para escala de cinza
    img = np.array(img)  # Converter para array NumPy

    # Aplicar threshold para realçar texto escuro (bairros em negrito)
    _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return Image.fromarray(img_bin)

def extrair_bairros(pdf_path):
    """
    Extrai apenas os bairros (textos em negrito) de um mapa em PDF.
    
    Parâmetros:
    - pdf_path (str): Caminho do arquivo PDF.

    Retorna:
    - DataFrame com os bairros extraídos.
    """
    imagens = convert_from_path(pdf_path, poppler_path=poppler_path)
    bairros_extraidos = []

    for img in imagens:
        img = preprocessar_imagem(img)  # Melhorar a imagem antes do OCR

        # Aplicar OCR e extrair texto
        texto_extraido = pytesseract.image_to_string(img, lang="por")
        linhas = texto_extraido.split("\n")  # Dividir por linhas

        for linha in linhas:
            linha = linha.strip()

            # Critérios para identificar bairros (padrão de texto em negrito)
            if linha.isupper() and len(linha) > 3:  # Exemplo: "JARDIM PRIMAVERA"
                bairros_extraidos.append(linha)

    # Criar DataFrame e remover duplicatas
    df_bairros = pd.DataFrame(list(set(bairros_extraidos)), columns=["Bairro"])
    return df_bairros

# 📂 Rodar a extração no PDF
pdf_path = "./datasets/mapa.pdf"
df_bairros = extrair_bairros(pdf_path)

# 📌 Salvar os bairros extraídos em CSV
df_bairros.to_csv("bairros_extraidos.csv", index=False)

print("✅ Bairros extraídos e salvos como CSV!")
