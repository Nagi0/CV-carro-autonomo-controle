# CV-carro-autonomo-controle
Hardware e Softwares
Hardware:
Raspberry pi 4 (Micro computador que roda o sistema operacional Raspian, uma distribuição do Linux);
Arduino Nano (usado apenas para modelar o motor, foi removido quando o código principal rodar);
Ponte H;
4 Motores DC 6V;
Encoder;
Fonte 12V, 2.2A;
Carregador potátil para celular (usado para alimentar o Raspberry);
Câmera Raspberry Pi 3;
Chave Liga/Desliga;
Protoboard.
Software:
Mu (IDE para programar em python no Raspberry Pi);
VNC Viwer (software para ver a tela do raspberry, caso o computador e o raspberry estejam conectados na mesma rede, pode-se ver a tela do raspberry sem precisar de usar o cabo HDMI);
Jupyter (IDE para programar em python usando uma arquitetura de Notebook, que é a documentação em questão que está sendo lida. Ela permite escrever anotações, imagens e rodar os códigos em python);
Arduino IDE (Usado para rodar o código que lê a velocidade do motor com os encoders.
Diagrama de Montagem
Foi conectado às portas GPIO do Raspberry às portas ENABLE1, IN1, IN2; ENABLE2, IN3, IN4 da ponte H, e usando o recurso do PWM foi possível controlar a velocidade que os motores irão girar, de acordo com a tensão que os será alimentada, é possível através de código python fazer, então criou-se uma biblioteca chamada MotorModule.py. Essa foi feita com programação orientada a objeto, onde uma classe chamada Motor foi feita junta das diferentes funções que os motores poderiam executar, o código dela segue abaixo:

https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/MotorModule.py

A alimentação é fornecida pela fonte 12V, 2.2A

image.png

Também foi feito uma biblioteca onde é possível ler as teclas pressionadas no teclado do computador, nessa caso será lido as setas do telcado, com isso pode-se enviar um sinal para fazer os 4 motores irem para frente; para trás; reduzir a rotação da esquerda e aumentar o da direita (virar a direita); reduzir a rotação da direita e aumentar a da esquerda (virar a esquerda). O código da biblioteca feita orientada a objeto segue abaixo:

https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/KeyPressModule.py

Modelagem do Motor DC
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
Data Import
Os dados foram coletados usando os módulos MotorModule.py(que foi mencionada anteriormente) e outro código feito no python para ler a porta serial do Arduino chamado read_serial_data.py. Usando um arduino nano conectado na porta USB do raspberry pi e um encoder conectado a esse arduino nano, foi medida a velocidade e os insantes de tempo pelo arduino nano, com uma amostragem de 0.1 segundos. Esses dados foram então enviados ao raspberry pi pela comunicação serial. Finalmente, eles foram registrados em um arquivo CSV, que pode ser aberto no excel.

Código da comunicação Serial: https://github.com/Nagi0/CV-carro-autonomo-controle/tree/main/modelar%20motor

data = pd.read_csv('motor speed data--step 0,2--sample_rate 0,1s.csv', sep=',')
data = data[['tempo', 'velocidade']]
display(data)
data.dtypes
tempo	velocidade
0	0.1	0.0
1	0.2	30.0
2	0.3	30.0
3	0.4	60.0
4	0.5	60.0
...	...	...
95	9.6	180.0
96	9.7	270.0
97	9.8	210.0
98	9.9	180.0
99	10.0	240.0
100 rows × 2 columns

tempo         float64
velocidade    float64
dtype: object
Funções
def time_zero(data):
  time_list = []
  for i in range(len(data)):
    if i == 0:
      time_list.append(0)
    else:
      dif = (data[i] - data[0]).total_seconds()
      time_list.append(dif)
  return time_list
def first_order_tf_control(x, k, tau):
  num = np.array([k])
  den = np.array([tau, 1])
​
  h = control.tf(num, den)
  t, y = control.step_response(h, T=x)
​
  return y
def first_order_tf_control_deadtime(x, k, tau, teta):
  N = 20
  teta = abs(teta)
  num = np.array([k])
  den = np.array([tau, 1]) # [(tau*s + 1)]
  h1 = control.tf(num, den)
​
  print('H: ')
  print(h1)
  print('\n')
​
  [num_pade, den_pade] = control.pade(teta, N)
  h_pade = control.tf(num_pade, den_pade)
  print('Padè Aprox:')
  print(h_pade)
​
  H = control.series(h1, h_pade)
​
  t, y = control.step_response(H, T=x)
​
  return y
def second_order_tf_control(x, k, tau1, tau2, teta):
    teta = abs(teta)
    num = np.array([k])
    den = np.array([tau1*tau2, tau1 + tau2, 1]) # [(tau1*s, 1) * (tau2*s, 1)]
    h1 = control.tf(num, den)
    print(h1)
​
    t, y = control.step_response(H, T=x)
​
    return y
def second_order_tf_control_deadtime(x, k, tau1, tau2, teta):
  N = 4
  teta = abs(teta)
  num = np.array([k])
  den = np.array([tau1*tau2, tau1 + tau2, 1]) # [(tau1*s, 1) * (tau2*s, 1)]
  h1 = control.tf(num, den)
​
  print('H: ')
  print(h1)
  print('\n')
​
  [num_pade, den_pade] = control.pade(teta, N) # teta1 e teta
  h_pade = control.tf(num_pade, den_pade)
  print('Padè Aprox:')
  print(h_pade)
​
  H = control.series(h1, h_pade)
​
  t, y = control.step_response(H, T=x)
​
  return y
def integrator(x, k):
  num = np.array([k])
  den = np.array([1, 0]) # [s]
​
  H = control.tf(num, den)
  t, y = control.step_response(h, T=x)
  
  return y
def integrator_deadtime(x, k, teta):
  N = 4
  num = np.array([k])
  den = np.array([1, 0])
​
  h1 = control.tf(num, den)
  [num_pade, den_pade] = control.pade(teta, N) # teta1 e teta
  h_pade = control.tf(num_pade, den_pade)
  print('Padè Aprox:')
  print(h_pade)
​
  H = control.series(h1, h_pade)
​
  t, y = control.step_response(H, T=x)
  
  return y
def transfer(k, tau):
  num = np.array([k])
  den = np.array([tau, 1, 0]) # [(tau*s, 1) * s]
​
  h = control.tf(num, den)
  print(h)
  t, y = control.step_response(h)
​
  return y
def transfer_deadtime(k, tau):
  N = 4
  num = np.array([k])
  den = np.array([tau, 1, 0]) # [(tau*s, 1) * s]
  h1 = control.tf(num, den)
​
  print('H: ')
  print(h1)
  print('\n')
​
  [num_pade, den_pade] = control.pade(teta, N)
  h_pade = control.tf(num_pade, den_pade)
  print('Padè Aprox:')
  print(h_pade)
​
  H = control.series(h1, h_pade)
​
  t, y = control.step_response(H)
​
  plt.plot(t, y)
  plt.show()
Teste das Funções Criadas
# TESTE.....
​
k = 0.6
t = 240.3
​
num = np.array([k])
print(num)
den = np.array([t, 1])
print(den)
​
h = control.tf(num, den)
print(h)
t, y = control.step_response(h)
print('lenth', len(y))
​
plt.plot(t, y)
plt.show()
[0.6]
[240.3   1. ]

    0.6
-----------
240.3 s + 1

lenth 100

# TESTE.....
​
k = 0.6
tau1 = 240.3
tau2 = 300
teta = 30
​
teta = abs(teta)
num = np.array([k])
den = np.array([tau1*tau2, tau1 + tau2, 1]) # [(tau1*s, 1) * (tau2*s, 1)]
h1 = control.tf(num, den)
print(h1)
​
t, y = control.step_response(h)
​
plt.plot(t, y)
plt.show()

            0.6
---------------------------
7.209e+04 s^2 + 540.3 s + 1


# TESTE.....
​
N = 5
tau = 4
k = 3
teta = 4
​
num = np.array([k])
den = np.array([tau, 1])
h1 = control.tf(num, den)
​
[num_pade, den_pade] = control.pade(teta, N)
h_pade = control.tf(num_pade, den_pade)
​
H = control.series(h1, h_pade)
print(h1)
​
t, y = control.step_response(H)
plt.plot(t, y)
plt.show()

   3
-------
4 s + 1


N = 4
k = 1.056
teta = 2.2719
tau1 = 1.1203
tau2 = 1.1202
​
num = np.array([k])
den = np.array([tau1*tau2, tau1 + tau2, 1]) # [(tau1, 1) * (tau2, 1)]
h1 = control.tf(num, den)
​
print('H: ')
print(h1)
print('\n')
​
[num_pade, den_pade] = control.pade(teta, N) # teta1 e teta
h_pade = control.tf(num_pade, den_pade)
print('Padè Aprox:')
print(h_pade)
​
H = control.series(h1, h_pade)
​
t, y = control.step_response(H)
​
plt.plot(t, y)
plt.show()
H: 

        1.056
----------------------
1.255 s^2 + 2.24 s + 1



Padè Aprox:

s^4 - 8.803 s^3 + 34.87 s^2 - 71.63 s + 63.06
---------------------------------------------
s^4 + 8.803 s^3 + 34.87 s^2 + 71.63 s + 63.06


k = 2
​
num = np.array([k])
den = np.array([1, 0])
​
h = control.tf(num, den)
t, y = control.step_response(h)
​
plt.plot(t, y)
plt.show()

N = 4
k = -2
teta = 1.120
​
num = np.array([k])
den = np.array([1, 0])
​
h1 = control.tf(num, den)
[num_pade, den_pade] = control.pade(teta, N) # teta1 e teta
h_pade = control.tf(num_pade, den_pade)
print('Padè Aprox:')
print(h_pade)
​
H = control.series(h1, h_pade)
​
t, y = control.step_response(H)
​
plt.plot(t, y)
plt.show()
Padè Aprox:

s^4 - 17.86 s^3 + 143.5 s^2 - 597.9 s + 1068
--------------------------------------------
s^4 + 17.86 s^3 + 143.5 s^2 + 597.9 s + 1068


k = 0.6
tau = 240.3
​
num = np.array([k])
den = np.array([tau, 1, 0]) # [(tau*s, 1) * s]
​
h = control.tf(num, den)
print(h)
t, y = control.step_response(h)
​
plt.plot(t, y)
plt.show()

     0.6
-------------
240.3 s^2 + s


k = 0.6
tau = 240.3
teta = 5
N = 4
​
num = np.array([k])
den = np.array([tau, 1, 0]) # [(tau*s, 1) * s]
​
h1 = control.tf(num, den)
​
print('H: ')
print(h1)
print('\n')
​
[num_pade, den_pade] = control.pade(teta, N) # teta1 e teta
h_pade = control.tf(num_pade, den_pade)
print('Padè Aprox:')
print(h_pade)
​
H = control.series(h1, h_pade)
​
t, y = control.step_response(H)
​
plt.plot(t, y)
plt.show()
H: 

     0.6
-------------
240.3 s^2 + s



Padè Aprox:

s^4 - 4 s^3 + 7.2 s^2 - 6.72 s + 2.688
--------------------------------------
s^4 + 4 s^3 + 7.2 s^2 + 6.72 s + 2.688


Modelar Motor
Sabe-se que o valor do step é de 0.2 [seus valores variam de 0.0 a 1.0]
Então será feito um array com o valor de 0.2
step = np.ones(data['tempo'].shape[0]) * 0.2
print(step)
[0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2
 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2
 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2
 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2
 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2
 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2 0.2]
import plotly.graph_objects as go
from plotly.subplots import make_subplots
​
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
​
# Add traces
fig.add_trace(
  go.Scatter(x=data['tempo'], y=step, name="STEP VALUES"),
    secondary_y=False,
)
​
fig.add_trace(
    go.Scatter(x=data['tempo'], y=data['velocidade'], name="SIGNAL VALUES"),
    secondary_y=True,
)
​
# Add figure title
fig.update_layout(
    title_text="STEP x ORIGINAL SIGNAL"
)
​
# Set x-axis title
fig.update_xaxes(title_text="time")
​
# Set y-axes titles
fig.update_yaxes(title_text="<b>STEP</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>ORIGINAL SIGNAL</b>", secondary_y=True)
​
fig.show()
image.png

param = curve_fit(first_order_tf_control, data['tempo'], data['velocidade'])
print('\n')
print('K: ', param[0][0])
print('τ: ', param[0][1])


K:  208.09349472256872
τ:  0.5180713392919336
k = 208.09349060768992
tau = 0.518071097684443
​
num = np.array([k])
print(num)
den = np.array([tau, 1])
print(den)
​
h = control.tf(num, den)
print(h)
t, y = control.step_response(h, T=data['tempo'])
​
import plotly.graph_objects as go
from plotly.subplots import make_subplots
​
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
​
# Add traces
fig.add_trace(
  go.Scatter(x=data['tempo'], y=data['velocidade'], name="ORIGINAL"),
    secondary_y=False,
)
​
fig.add_trace(
    go.Scatter(x=data['tempo'], y=y, name="MODEL"),
    secondary_y=False,
)
​
fig.add_trace(
    go.Scatter(x=data['tempo'], y=step, name="STEP"),
    secondary_y=True,
)
​
​
# Add figure title
fig.update_layout(
    title_text="Step X Original/Model Signal"
)
​
# Set x-axis title
fig.update_xaxes(title_text="time")
​
# Set y-axes titles
fig.update_yaxes(title_text="<b>Step Response</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>Step Value</b>", secondary_y=True)
​
fig.show()
[208.09349061]
[0.5180711 1.       ]

   208.1
------------
0.5181 s + 1

image.png

A função curver fit da biblioteca scilab permite passarmos uma equação e ela ajusta os parâmetro da equação para melhor encaixar aos dados, é utilizado o método dos mínimos quadrados para esse ajuste ser feito. No caso desse trabalho, observou-se pela característica da curva obtida pelos dados que se tratava de um funçã do primeiro grau. Então foi passado como parâmetro para a função curver_fit a função "first_order_tf_control; junto com os dados instantes de tempo e velocidade do motor:
param = curve_fit(first_order_tf_control, data['tempo'], data['velocidade'])

Para saber mais da função segue o link da biblioteca scipy: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
NOTA: A BIBLIOTECA CONTROL DO PYTHON CONSIDERA QUE TODOS OS STEPS SÃO DE MÓDULO 1.0, LOGO O VALOR DE K, FOI ESTIMADO COMO SE A ENTRADA FOSSE UM DEGRAU UNITÁRIO, MAS PODE-SE CORRIGIR ISSO DIVIDINDO O VALOR DE K ENCONTRADO POR 0.2.
1040
------------
0.5181 s + 1
k = 208.09349060768992 / 0.2
tau = 0.518071097684443
​
num = np.array([k])
den = np.array([tau, 1])
​
h = control.tf(num, den)
print('Função Tranferência de 1° ordem do motor DC:')
print(h)
Função Tranferência de 1° ordem do motor DC:

    1040
------------
0.5181 s + 1

Visão Computacional
Em seguida usando o ColorModule.py foi possível filtrar as cores na tela, usando o sistema HSV, o filtro HVS selecionou apenas a cor azul, conforme a imagem abaixo:image.png
Para pegar apenas o objeto desejado, os algoritmos de visão computacional podem selecionar a maior área das cores filtradas na imagem, como o objeto se destaca, ele será na grande parte das vezes o objeto azul de maior área da imagem. Pode-se notar nos logs da imagem os parâmetros encontrados para o filtro HSV que serão usados no código principal para filtrar as cores da imagem da câmera, possibilitando fazer um tracking de apenas objetos azuis.
Segue o link da biblioteca que foi baixada para fazer a filtragem de cores: https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/ColorModule.py
Em seguida os contornos da imagem filtrada é extraído para fazer um tracking do objeto
Para fazer o carrinho seguir o objeto foi feito um algoritmo P+I para que ele siga o objeto no eixo X, o algoritmo visa centralizar o objeto na frente da imagemimage.png
Na imagem há uma linha vertical rosa que representa o centro da imagem, ela é o set-point, o carrinho irá tentar manter o objeto detectado (marcado pelo quadrado verde) em cima dessa linha, centralizando o carrinho da frente do objeto. A linha horizontal roda mostra distância do centro do objeto detectado do centro da imagem. Também é possível estimar a área do objeto na imagem, isso é usado no código principal para ver o quão perto o objeto está da câmera do carrinho. Caso a área seja pequena a distância é grande, a medida que a área do objeto detectado aumenta, siginifica que ele está chegando mais perto.

Foram usadas as bibliotecas Opencv (cv2) e outras bibliotecas baixadas online chamadas ObjectDetectionModule.py e ContourModule.py para fazer os algoritmos de visão cumpuational para detectar os objetos das cores desejadas que rodam no código principal.

Opencv: https://opencv.org/
OjectDetection.py: https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/ObjectDetectionModule.py
ContourModule.py: https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/ContourModule.py
Rodando o Código Principal main.py
Essa sessão irá cobrir como todos as bibliotecas criadas e baixadas anteriormente atuam para que o carrinho faça o tracking do objeto desejado.

main.py: https://github.com/Nagi0/CV-carro-autonomo-controle/blob/main/run/main.py
importanto as bibliotecasimage.png

Usando a biblioteca MotorModule para criar um objeto da classe Motor que irá permitir controlar os motores conectados na ponte H;
Criando um objeto da classe da biblioteca que lê as teclas do teclado;
Leitura da câmera ligada ao Raspberry pi;
Definindo as configurações para gravar a imagem da câmera;
Valores do filtro de cor HSV;
Iniciando a variável erro anterior que será usada no P+I;image.png
A função a seguir controla os movimentos do carrinho de acordo com os objetos detectados na imagem;
Primeiro verifica-se se algum objeto foi detectado;
Caso ele seja, apenas o objeto com a maior área será considerado, isso reduz ruídos causados por cores no ambiente em volta;
lê-se a área do objeto na imagem para saber o quão perto ele está, a medida que a área aumenta a velocidade do motor diminui;
É então calculado a posição do centro do objeto na imagem;
É desenhado uma linha vertical no centro da imagem;
Em seguida é calculado a distância do centro do objeto da linha no centro da imagem (erro);
Aplicaçã do algoritmo P+I incremental, pid[0] é o ganho proporcional (Kp) e o pid[1] é o ganho integral (Ki), nele é comparado o erro atual com o erro lido anteriormente, com isso é possível fazer o carrinho mover-se no eixo X de forma ideal para trackear o objeto;
É usada a biblioteca numpy (np.interp) para ajustar a saída do P+I para uma faixa de valores que o motor lê pela biblioteca MotorModule, esse valor foi normalizado em uma escala de 0 a 1. Será enviado para o motor o quanto deverá reduzir a rotação de um lado e aumentar para outro. Experimentalmente, constatou-se que a faixa máxima da saída do P+I deve ir de 0 a 0.45, mais do que isso o sistema pode ficar instável;
moveF(velocidade que o motor deve se mover para frente, valor que ele precisa virar ([+]direita, [-]esquerda), ciclo PWM)
O erro atual vira o erro anterior (prev_error = error);image.png
Essa parte do código que irá chamar a função acima

Leitura da imagem da câmera
Lendo na image o contorno dos objetos que passaram pelo filtro
Definição das dimensões da imagem da câmera
chamar a função explicada anteriormente
track_object(imagem que detecta contornos, contornos detectados, [Kp, Ki], erro anterior)
Caso o botão de gravar seja acionado pelo teclado a imagem da câmera começa a gravar
Mostra a imagem da câmera na telaimage.png
Caso o ESC do teclado seja precionado, o código é encerrado
Caso o R do teclado seja precionado, a flag para gravar é ligada
Caso o S do teclado seja precionado, a gravação é interrompida e o vídeo é salvo no formato AVI (multiplos vídeos podem ser gravados em uma mesma execução do código)
image.png

Controle manual do carrinho

As setas do teclado podem movimentar o carrinho da mesma forma que o P+I faz, usando o objeto criado a partir da classe Motor da biblioteca MotorModule.image-2.png
Conclusão
Pode-se confirmar a eficássia de usar a visão computacional para o controle de sistemas dinâmicos, usando a câmera foi possível detectar objetos de cores desejadas, definir um set-point, usar algoritmos de controle para controlar os movimentos do carrinho, acessar remotamente o raspberry pi pela rede local, acionar os motores usando o teclado do computador, gravar a imagem da câmera e modelar os motores usando métodos matemáticos. Todas essas tarefas foram feitas com o auxilio da linguagem python, a linguagem C do arduino foi usada para unicamente ler a velocidade dos motores, que foram usadas na etapa de modelagem, e o software VNC permitiu o acesso remoto do raspberry pelo computador.

O Link do repositório GitHub do projeto: https://github.com/Nagi0/CV-carro-autonomo-controle
