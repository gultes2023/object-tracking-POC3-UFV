import random
import xml.etree.ElementTree as ET
from filterpy.kalman import KalmanFilter
import numpy as np
import cv2

def analisar_xml(arquivo_xml):
    tree = ET.parse(arquivo_xml)
    root = tree.getroot()
    dados = []
    for image in root.findall('image'):
        image_info = {
            'id': image.get('id'),
            'file': image.get('name'),
            'annotations': [{
                'label': box.get('label'),
                'occluded': box.get('occluded'),
                'coordinates': {
                    'xtl': box.get('xtl'),
                    'ytl': box.get('ytl'),
                    'xbr': box.get('xbr'),
                    'ybr': box.get('ybr')
                }
            } for box in image.findall('box')]
        }
        dados.append(image_info)
    return dados

def dividir_dados(dados, proporcao_teste):
    ids_imagens = [dado['id'] for dado in dados]
    random.shuffle(ids_imagens)
    num_teste = int(len(ids_imagens) * proporcao_teste)
    ids_teste = ids_imagens[:num_teste]
    ids_treino = ids_imagens[num_teste:]
    dados_treino = [dado for dado in dados if dado['id'] in ids_treino]
    dados_teste = [dado for dado in dados if dado['id'] in ids_teste]
    return dados_treino, dados_teste

def inicializar_filtro(x_centro, y_centro, id_peixe):
    kf = KalmanFilter(dim_x=4, dim_z=2)
    dt = 0.1
    kf.F = np.array([[1, 0, dt, 0],
                     [0, 1, 0, dt],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]]) * 2
    kf.H = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0]]) * 1.01
    kf.R = np.array([[1, 0],
                     [0, 1]]) * 2
    kf.Q = np.array([[1, 0, dt, 0],
                     [0, 1, 0, dt],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]]) * 2
    kf.P = np.eye(4) * 500
    kf.P[2:, 2:] *= 1000
    kf.x = np.array([x_centro, y_centro, 0, 0])
    return kf

def processar_annotations(dados_treino):
    filtros_kalman = {}
    for dado in dados_treino:
        for i, annotation in enumerate(dado['annotations']):
            id_peixe = f"{annotation['label']}_{dado['id']}_{i}"
            x_centro = (float(annotation['coordinates']['xtl']) + float(annotation['coordinates']['xbr'])) / 2
            y_centro = (float(annotation['coordinates']['ytl']) + float(annotation['coordinates']['ybr'])) / 2
            medida_atual = np.array([[x_centro], [y_centro]])
            if id_peixe not in filtros_kalman:
                filtros_kalman[id_peixe] = inicializar_filtro(x_centro, y_centro, id_peixe)
            kf = filtros_kalman[id_peixe]
            kf.predict()
            kf.update(medida_atual)
    return filtros_kalman

def desenhar_caixa(imagem, coordenadas, cor, texto):
    x1, y1, x2, y2 = coordenadas
    cv2.rectangle(imagem, (int(x1), int(y1)), (int(x2), int(y2)), cor, 2)
    cv2.putText(imagem, texto, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cor, 2)

def processar_imagens(dados_treino, filtros_kalman):
    for dado in dados_treino:
        #print(f"{dado}")
        caminho_imagem = "archive/" + dado['file']
        imagem = cv2.imread(caminho_imagem)
    
        if imagem is None:
            print(f"Não foi possível carregar a imagem: {caminho_imagem}")
            continue

        for i, annotation in enumerate(dado['annotations']):
            id_peixe = f"{annotation['label']}_{dado['id']}_{i}"
            if id_peixe in filtros_kalman:
                kf = filtros_kalman[id_peixe]
                xtl_real, ytl_real, xbr_real, ybr_real = [float(annotation['coordinates'][coord]) for coord in ['xtl', 'ytl', 'xbr', 'ybr']]
                desenhar_caixa(imagem, [xtl_real, ytl_real, xbr_real, ybr_real], (0, 255, 0), "Real")

                x_centro_estimado, y_centro_estimado = kf.x[0], kf.x[1]
                largura, altura = xbr_real - xtl_real, ybr_real - ytl_real
                xtl_estimado, ytl_estimado = x_centro_estimado - largura / 2, y_centro_estimado - altura / 2
                xbr_estimado, ybr_estimado = x_centro_estimado + largura / 2, y_centro_estimado + altura / 2
                desenhar_caixa(imagem, [xtl_estimado, ytl_estimado, xbr_estimado, ybr_estimado], (0, 0, 255), "Estimado")
        cv2.imshow('Imagem', imagem)

        # Esperar até que a tecla 'q' seja pressionada para fechar a imagem
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break


def main():
    caminho_xml = 'archive/annotations.xml'
    dados_xml = analisar_xml(caminho_xml)
    dados_treino, _ = dividir_dados(dados_xml, 0.3)
    filtros_kalman = processar_annotations(dados_treino)
    processar_imagens(dados_treino, filtros_kalman)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
