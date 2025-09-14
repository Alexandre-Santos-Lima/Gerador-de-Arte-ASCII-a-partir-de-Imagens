# -*- coding: utf-8 -*-

# ---
# Projeto: Gerador de Arte ASCII a partir de Imagens (CLI)
# Descrição: Este script converte qualquer imagem (JPG, PNG, etc.) em uma representação
#            de arte ASCII e a exibe no terminal. A ferramenta permite ajustar a largura
#            da arte final e inverter o esquema de cores.
# Bibliotecas necessárias: Pillow. Instale com o comando: pip install Pillow
# Como executar: python main.py <caminho_para_sua_imagem> [--largura <numero>] [--invertido]
# Exemplo 1 (básico): python main.py minha_foto.jpg
# Exemplo 2 (mais largo): python main.py logo.png --largura 120
# Exemplo 3 (cores invertidas): python main.py paisagem.jpg --largura 100 --invertido
# ---

import argparse
from PIL import Image

# Paleta de caracteres ASCII, do mais denso/escuro para o mais esparso/claro
ASCII_CHARS_PADRAO = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def redimensionar_imagem(imagem, nova_largura=100):
    """Redimensiona a imagem mantendo a proporção."""
    (largura_original, altura_original) = imagem.size
    proporcao = altura_original / float(largura_original)
    
    # Ajuste para caracteres de terminal, que são geralmente mais altos que largos
    nova_altura = int((nova_largura * proporcao) * 0.55)
    
    imagem_redimensionada = imagem.resize((nova_largura, nova_altura))
    return imagem_redimensionada

def converter_para_escala_de_cinza(imagem):
    """Converte a imagem para escala de cinza."""
    return imagem.convert("L")

def mapear_pixels_para_ascii(imagem, invertido=False):
    """Mapeia cada pixel para um caractere ASCII com base em sua intensidade."""
    # Inverte a paleta se a flag --invertido for usada
    caracteres_ascii = ASCII_CHARS_PADRAO[::-1] if invertido else ASCII_CHARS_PADRAO
    
    pixels = imagem.getdata()
    caracteres = []
    for pixel_valor in pixels:
        # Mapeia o valor do pixel (0-255) para um índice na nossa paleta de caracteres
        indice = int((pixel_valor / 255) * (len(caracteres_ascii) - 1))
        caracteres.append(caracteres_ascii[indice])
        
    return "".join(caracteres)

def gerar_arte_ascii(caminho_imagem, largura, invertido):
    """Função principal que orquestra a conversão da imagem."""
    try:
        imagem = Image.open(caminho_imagem)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_imagem}' não foi encontrado.")
        return
    except Exception as e:
        print(f"Erro ao abrir a imagem: {e}")
        return

    # 1. Redimensionar
    imagem_redimensionada = redimensionar_imagem(imagem, largura)
    
    # 2. Converter para escala de cinza
    imagem_cinza = converter_para_escala_de_cinza(imagem_redimensionada)
    
    # 3. Mapear pixels para caracteres ASCII
    string_ascii = mapear_pixels_para_ascii(imagem_cinza, invertido)
    
    # 4. Formatar e imprimir a string final
    largura_imagem = imagem_redimensionada.width
    arte_ascii_final = ""
    for i in range(0, len(string_ascii), largura_imagem):
        arte_ascii_final += string_ascii[i:i + largura_imagem] + "\n"
        
    print(arte_ascii_final)

if __name__ == "__main__":
    # Configuração do parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description="Converte uma imagem em arte ASCII e a exibe no terminal."
    )
    
    parser.add_argument(
        "caminho_imagem", 
        type=str,
        help="O caminho para o arquivo de imagem a ser convertido."
    )
    parser.add_argument(
        "-l", "--largura", 
        type=int, 
        default=80, 
        help="A largura desejada para a arte ASCII final (em caracteres). Padrão: 80."
    )
    parser.add_argument(
        "-i", "--invertido", 
        action="store_true",
        help="Inverte a paleta de caracteres (pixels claros se tornam caracteres escuros)."
    )
    
    args = parser.parse_args()
    
    # Executa a função principal com os argumentos fornecidos
    gerar_arte_ascii(args.caminho_imagem, args.largura, args.invertido)
