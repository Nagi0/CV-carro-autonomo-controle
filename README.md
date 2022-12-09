# CV-carro-autonomo-controle
O objetivo desse trabalho é fazer um carrinho que possa seguir um objeto usando uma câmera. Com o auxilio de algoritmos python de visão computacional foi possível detectar um objeto de uma cor escolhida arbitrariamente, também conseguiu-se quantificar o quão longe o objeto está do centro da câmera (no eixo X) e o quão distante ele está da câmera em geral. Com esses valores quantificados, utilizou-se um algoritmo de controle P+I incremental, analisando o erro passado com o erro atual para então obter uma saída que atue nos motores do carrinho visando centraliza-lo e aproima-lo do objeto. 

Nesse trabalho também foi incluido uma forma de gravar a imagem da câmera do carrinho para o formato de vídeo AVI, assim, pode-se assistir a visão do carrinho depois que o código for encerrado; também foi implementado um controle manual pelo teclado do computador; além de uma forma de acessar a tela do sistema operacional do Raspberry pi em tempo real, remotamente, através da rede Wi-Fi, assim é possível ver tudo por outro dispositivo, sem precisar conectar o carrinho em nenhuma entrada de vídeo, permitindo-o mover livremente pelo ambiente.
# Hardware e Softwares
## Hardware:
- Raspberry pi 4 (Micro computador que roda o sistema operacional Raspian, uma distribuição do Linux);
- Arduino Nano (usado apenas para modelar o motor, foi removido quando o código principal rodar);
- Ponte H;
- 4 Motores DC 6V;
- Encoder;
- Fonte 12V, 2.2A;
- Carregador potátil para celular (usado para alimentar o Raspberry);
- Câmera Raspberry Pi 3;
- Chave Liga/Desliga;
- Protoboard.
## Software:
- Mu (IDE para programar em python no Raspberry Pi);
- VNC Viwer (software para ver a tela do raspberry, caso o computador e o raspberry estejam conectados na mesma rede, pode-se ver a tela do raspberry sem precisar de usar o cabo HDMI);
- Jupyter (IDE para programar em python usando uma arquitetura de Notebook, que é a documentação em questão que está sendo lida. Ela permite escrever anotações, imagens e rodar os códigos em python);
- Arduino IDE (Usado para rodar o código que lê a velocidade do motor com os encoders.

# Diagrama de Montagem
Foi conectado às portas GPIO do Raspberry às portas ENABLE1, IN1, IN2; ENABLE2, IN3, IN4 da ponte H, e usando o recurso do PWM foi possível controlar a velocidade que os motores irão girar, de acordo com a tensão que os será alimentada, é possível através de código python fazer, então criou-se uma biblioteca chamada MotorModule.py. Essa foi feita com programação orientada a objeto, onde uma classe chamada Motor foi feita junta das diferentes funções que os motores poderiam executar, o código dela segue abaixo:

https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/MotorModule.py


A alimentação é fornecida pela fonte 12V, 2.2A

![image](https://user-images.githubusercontent.com/75706345/206335295-c7126775-2c3a-4968-80b6-05cc440ae03f.png)

- Também foi feito uma biblioteca onde é possível ler as teclas pressionadas no teclado do computador, nessa caso será lido as setas do telcado, com isso pode-se enviar um sinal para fazer os 4 motores irem para frente; para trás; reduzir a rotação da esquerda e aumentar o da direita (virar a direita); reduzir a rotação da direita e aumentar a da esquerda (virar a esquerda). O código da biblioteca feita orientada a objeto segue abaixo:

- https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/KeyPressModule.py

# Modelagem do Motor DC
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl
import numpy as np
import datetime
from scipy.optimize import curve_fit
from scipy.signal import TransferFunction, lti
import control
import plotly.express as px

### Data Import
- Os dados foram coletados usando os módulos MotorModule.py(que foi mencionada anteriormente) e outro código feito no python para ler a porta serial do Arduino chamado read_serial_data.py. Usando um arduino nano conectado na porta USB do raspberry pi e um encoder conectado a esse arduino nano, foi medida a velocidade e os insantes de tempo pelo arduino nano, com uma amostragem de 0.1 segundos. Esses dados foram então enviados ao raspberry pi pela comunicação serial. Finalmente, eles foram registrados em um arquivo CSV, que pode ser aberto no excel.

- Código da comunicação Serial: https://github.com/Nagi0/CV-carro-autonomo-controle/tree/main/modelar%20motor

![image](https://user-images.githubusercontent.com/75706345/206335490-4ec995dc-d739-4d94-b008-b12410b777de.png)
![image](https://user-images.githubusercontent.com/75706345/206335550-2ef347e9-f170-49b1-af3d-6a5971a9d66b.png)

![image](https://user-images.githubusercontent.com/75706345/206335603-34aeadc8-473f-467f-9b3d-92ee2fe1536e.png)

![image](https://user-images.githubusercontent.com/75706345/206335640-19840bcb-ac49-4d63-a570-69b0396e660c.png)

![image](https://user-images.githubusercontent.com/75706345/206335673-b5e6a99f-da76-4ca9-a789-e903e4f252d5.png)

![image](https://user-images.githubusercontent.com/75706345/206335729-f9eb877a-34e4-4c1b-ba01-0bc942a4ff60.png)

![image](https://user-images.githubusercontent.com/75706345/206335873-be7b99bb-ede9-4de6-a757-ab32b306ba0a.png)

![image](https://user-images.githubusercontent.com/75706345/206335899-8abd341d-4484-4f7a-af07-e82c3581159d.png)

![image](https://user-images.githubusercontent.com/75706345/206335943-46439214-dd0f-4859-9d5e-40460b2104b4.png)

![image](https://user-images.githubusercontent.com/75706345/206336010-f385ea1b-13a4-4491-afa7-080bf95e6716.png)
![image](https://user-images.githubusercontent.com/75706345/206336039-e658a511-faf8-4c23-a298-68d421e4d21a.png)

![image](https://user-images.githubusercontent.com/75706345/206336107-c6be8107-521e-449a-9768-aa364dea090c.png)
![image](https://user-images.githubusercontent.com/75706345/206336156-61a8d70e-61ec-41f8-9b82-1223335a70af.png)
![image](https://user-images.githubusercontent.com/75706345/206336192-b209e5d6-d692-4684-b166-3d6ba6c01ef9.png)
![image](https://user-images.githubusercontent.com/75706345/206336306-45de856f-4fb0-418c-ad1a-dcc36fb52c3d.png)
![image](https://user-images.githubusercontent.com/75706345/206336319-7d7d80b0-941b-48f3-a24a-4d56180f4d8d.png)

![image](https://user-images.githubusercontent.com/75706345/206336346-09c700d4-409a-4bd9-aad8-62d4942fa85a.png)
![image](https://user-images.githubusercontent.com/75706345/206336376-ee7bd61b-3111-4518-b2e4-9c3b9f32a3a7.png)

![image](https://user-images.githubusercontent.com/75706345/206336410-482ad18f-ede1-4763-b269-e9d3f86894cf.png)
![image](https://user-images.githubusercontent.com/75706345/206336442-9061edd7-c4ef-4328-9233-0b823f855dd0.png)

A função curver fit da biblioteca scilab permite passarmos uma equação e ela ajusta os parâmetro da equação para melhor encaixar aos dados, é utilizado o método dos mínimos quadrados para esse ajuste ser feito. No caso desse trabalho, observou-se pela característica da curva obtida pelos dados que se tratava de um funçã do primeiro grau. Então foi passado como parâmetro para a função curver_fit a função "first_order_tf_control; junto com os dados instantes de tempo e velocidade do motor:
param = curve_fit(first_order_tf_control, data['tempo'], data['velocidade'])
- Para saber mais da função segue o link da biblioteca scipy: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html

![image](https://user-images.githubusercontent.com/75706345/206336523-9ddb54e0-ca1d-403f-8267-2583da78bfa7.png)
![image](https://user-images.githubusercontent.com/75706345/206336560-e17ccb9e-c50f-4d3e-9756-9b9ae4ec5f10.png)

# Visão Computacional
- Em seguida usando o ColorModule.py foi possível filtrar as cores na tela, usando o sistema HSV, o filtro HVS selecionou apenas a cor azul, conforme a imagem abaixo
![image](https://user-images.githubusercontent.com/75706345/206336636-124bc9f5-95f9-49e0-a3b9-a82c5599bb81.png)
- Para pegar apenas o objeto desejado, os algoritmos de visão computacional podem selecionar a maior área das cores filtradas na imagem, como o objeto se destaca, ele será na grande parte das vezes o objeto azul de maior área da imagem. Pode-se notar nos logs da imagem os parâmetros encontrados para o filtro HSV que serão usados no código principal para filtrar as cores da imagem da câmera, possibilitando fazer um tracking de apenas objetos azuis.
- Segue o link da biblioteca que foi baixada para fazer a filtragem de cores: https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/ColorModule.py
- Em seguida os contornos da imagem filtrada é extraído para fazer um tracking do objeto
- Para fazer o carrinho seguir o objeto foi feito um algoritmo P+I para que ele siga o objeto no eixo X, o algoritmo visa centralizar o objeto na frente da imagem

![image](https://user-images.githubusercontent.com/75706345/206336750-eb56bc22-7d85-45e7-b719-2c082c96ef48.png)

Na imagem há uma linha vertical rosa que representa o centro da imagem, ela é o set-point, o carrinho irá tentar manter o objeto detectado (marcado pelo quadrado verde) em cima dessa linha, centralizando o carrinho da frente do objeto. A linha horizontal roda mostra distância do centro do objeto detectado do centro da imagem. Também é possível estimar a área do objeto na imagem, isso é usado no código principal para ver o quão perto o objeto está da câmera do carrinho. Caso a área seja pequena a distância é grande, a medida que a área do objeto detectado aumenta, siginifica que ele está chegando mais perto.

Foram usadas as bibliotecas Opencv (cv2) e outras bibliotecas baixadas online chamadas ObjectDetectionModule.py e ContourModule.py para fazer os algoritmos de visão cumpuational para detectar os objetos das cores desejadas que rodam no código principal.

- Opencv: https://opencv.org/
- OjectDetection.py: https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/ObjectDetectionModule.py
- ContourModule.py: https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/ContourModule.py

# Rodando o Código Principal main.py
Essa sessão irá cobrir como todos as bibliotecas criadas e baixadas anteriormente atuam para que o carrinho faça o tracking do objeto desejado. Havará uma imagem do código e logo abaixo a explicação do que cada linha está fazendo.
- main.py: https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/main.py
![image](https://user-images.githubusercontent.com/75706345/206337008-c1a6d1ae-8c4a-4911-8515-d642b5c30b3c.png)
- Usando a biblioteca MotorModule para criar um objeto da classe Motor que irá permitir controlar os motores conectados na ponte H;
- Criando um objeto da classe da biblioteca que lê as teclas do teclado;
- Leitura da câmera ligada ao Raspberry pi;
- Definindo as configurações para gravar a imagem da câmera;
- Valores do filtro de cor HSV;
- Iniciando a variável erro anterior que será usada no P+I;

![image](https://user-images.githubusercontent.com/75706345/206337094-8fb44795-bbb0-4698-915e-dc678476de3f.png)
- A função a seguir controla os movimentos do carrinho de acordo com os objetos detectados na imagem;
- Primeiro verifica-se se algum objeto foi detectado;
- Caso ele seja, apenas o objeto com a maior área será considerado, isso reduz ruídos causados por cores no ambiente em volta;
- lê-se a área do objeto na imagem para saber o quão perto ele está, a medida que a área aumenta a velocidade do motor diminui;
- É então calculado a posição do centro do objeto na imagem;
- É desenhado uma linha vertical no centro da imagem;
- Em seguida é calculado a distância do centro do objeto da linha no centro da imagem (erro);
- Aplicaçã do algoritmo P+I incremental, pid[0] é o ganho proporcional (Kp) e o pid[1] é o ganho integral (Ki), nele é comparado o erro atual com o erro lido anteriormente, com isso é possível fazer o carrinho mover-se no eixo X de forma ideal para trackear o objeto;
- É usada a biblioteca numpy (np.interp) para ajustar a saída do P+I para uma faixa de valores que o motor lê pela biblioteca MotorModule, esse valor foi normalizado em uma escala de 0 a 1. Será enviado para o motor o quanto deverá reduzir a rotação de um lado e aumentar para outro. Experimentalmente, constatou-se que a faixa máxima da saída do P+I deve ir de 0 a 0.45, mais do que isso o sistema pode ficar instável;
- moveF(velocidade que o motor deve se mover para frente, valor que ele precisa virar ([+]direita, [-]esquerda), ciclo PWM)
- O erro atual vira o erro anterior (prev_error = error);

![image](https://user-images.githubusercontent.com/75706345/206337150-7a88eb58-5e11-4719-9d2d-aa6dbb3aa787.png)
Essa parte do código que irá chamar a função acima
- Leitura da imagem da câmera
- Lendo na image o contorno dos objetos que passaram pelo filtro
- Definição das dimensões da imagem da câmera
- chamar a função explicada anteriormente
    - track_object(imagem que detecta contornos, contornos detectados, [Kp, Ki], erro anterior)
- Caso o botão de gravar seja acionado pelo teclado a imagem da câmera começa a gravar
- Mostra a imagem da câmera na tela

![image](https://user-images.githubusercontent.com/75706345/206337192-9ed272a8-43d4-4b64-a82c-af8f2000c946.png)
- Caso o ESC do teclado seja precionado, o código é encerrado
- Caso o R do teclado seja precionado, a flag para gravar é ligada
- Caso o S do teclado seja precionado, a gravação é interrompida e o vídeo é salvo no formato AVI (multiplos vídeos podem ser gravados em uma mesma execução do código)

![image](https://user-images.githubusercontent.com/75706345/206337241-f7be9755-7f99-4e8b-905e-e8a59995b29d.png)
Controle manual do carrinho
- As setas do teclado podem movimentar o carrinho da mesma forma que o P+I faz, usando o objeto criado a partir da classe Motor da biblioteca MotorModule.

# Conclusão
Pode-se confirmar a eficássia de usar a visão computacional para o controle de sistemas dinâmicos, usando a câmera foi possível detectar objetos de cores desejadas, definir um set-point, usar algoritmos de controle para controlar os movimentos do carrinho, acessar remotamente o raspberry pi pela rede local, acionar os motores usando o teclado do computador, gravar a imagem da câmera e modelar os motores usando métodos matemáticos. Todas essas tarefas foram feitas com o auxilio da linguagem python, a linguagem C do arduino foi usada para unicamente ler a velocidade dos motores, que foram usadas na etapa de modelagem, e o software VNC permitiu o acesso remoto do raspberry pelo computador.

O Link do repositório GitHub do projeto: https://github.com/Nagi0/CV-carro-autonomo-controle

