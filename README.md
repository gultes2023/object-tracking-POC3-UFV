## Problema de Rastreamento de Objetos através de vídeo - Case UFV

#### HUB de Inteligência Artificial - Senai PR

## Participantes
-  [Gustavo Estevam Sena (Residente)](https://github.com/Gultes)
-  [Gustavo Rodrigues Wanke (Residente)](https://github.com/GWanke)

- Leonardo Goshi Sanches (Scrum Master)

## Objetivos
- Avaliar  diferentes algoritmos de Object Tracking, com foco em identificar a técnica mais adequada para a análise eficiente de movimentos de animais em ambientes naturais.
- Aplicar os conhecimentos adquiridos durante a fase de estudos do programa em um case envolvendo um problema real.

## Sobre
O trabalho consiste em mapear técnicas de Object Tracking visando identificar a técnica mais adequada para resolução de problema de rastreamento de animais em vídeos de drone disponibilizado pela UFV.

## Branches do Projeto

### Branch Master

Apresenta o rastreamento de objetos utilizando filtragem por cor HSV. Esta abordagem é eficaz para rastrear objetos com cores específicas em vídeos.

## Conteúdo

- **Scripts para rastreamento de objetos com filtro HSV**: Códigos para implementar o rastreamento de objetos usando a filtragem por cor HSV.
- **Funções para ajuste das trackbars HSV em tempo real**: Ferramentas interativas para ajustar as faixas de cores HSV e otimizar o rastreamento.
- **Classe com buffer circular**: Uma classe projetada para armazenar posições anteriores dos objetos rastreados, utilizando um buffer circular para gerenciar os dados.
- **Algoritmo para detecção e diferenciação de objetos baseado na distância**: Um método para identificar e distinguir entre objetos em movimento com base em suas distâncias relativas.
- **Conjunto de dados e imagens para teste e validação**: Recursos visuais fornecidos para testar e validar a eficácia dos algoritmos de rastreamento de objetos.


### Branch Filtro_Kalman

Explora o uso do Filtro de Kalman para rastreamento de objetos, conhecido pela sua eficiência e precisão.

## Conteúdo

- **Scripts de implementação do Filtro de Kalman**: Algoritmo para rastreamento de objetos utilizando o Filtro de Kalman, conhecido por sua precisão e eficiência.
- **Conjunto de dados e imagens para testes e validação do algoritmo**: Dataset de movimento de peixes utilizado para testar e validar o desempenho do Filtro de Kalman em diferentes cenários de rastreamento de objetos.

## Run 🏃‍

```
# Clone este repositório
$ git clone https://github.com/gultes2023/object-tracking-POC3-UFV.git

$Com python 3 instalado na máquina:

# Abra uma IDE - Por exemplo - Visual Studio Code
# Acesse o diretório do projeto via comando - Ex:cd D:\hub23

# Digite no terminal
$ Python Object-Tracking-Circular-Webcam.py ou pressione CTRL + F5 se estiver usando Visual Studio Code

````
A execução irá retornar resposta conforme o exemplo da imagem abaixo para o algoritmo  Object-Tracking-Circular-Webcam.py:

<div align="center">
    <img src="https://i.imgur.com/O5euSwK.png" alt="Classic Object Tracking" width="720">
</div>



````

```
