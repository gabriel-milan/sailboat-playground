# Sailboat Playground

Idioma: [EN](README.md) (incomplete) / [PT-BR](#) (completo)

Um framework simples para desenvolvimento e teste de algoritmos de navegação autônoma para veleiros com simulações e visualizações 2D.

## Primeiros passos

Há duas maneiras de instalar esse pacote em sua máquina

### Opção #1 - A partir do repositório GitHub (recomendado)

Com esse método, você será capaz de executar os exemplos aqui fornecidos sem fazer nenhuma alteração.

- Clone esse repositório

```
https://github.com/gabriel-milan/sailboat-playground
```

- Navegue até o repositório clonado e execute

```
python3 -m pip install .
```

- E está pronto! Se você quiser executar o exemplo do `upwind` por exemplo, faça

```
python3 examples/upwind/sailing_upwind.py
```

### Opção #2 - A partir do PyPI

Esse pacote também está disponível no PyPI, mas você terá que criar seus próprios arquivos de configuração para o ambiente e barco antes de usá-lo.

- Instalando do PyPI:

```
python3 -m pip install sailboat_playground
```

## Uso básico

Esse framework é dividido em dois módulos principais: `engine` e `visualization`.

### Engine

O módulo `engine` lida com a simulação e gera arquivos com dados de simulação para debugging e visualização posterior. A classe principal do engine é a `Manager`. Nela, você precisa fornecer ambos os arquivos de configuração do barco e ambiente, além de, opcionalmente, fornecer dados sobre a orientação do barco, sua posição inicial e o tamanho do seu mapa (em metros).

Um exemplo de uso (explicado abaixo) é o seguinte:

```py
import pickle
from sailboat_playground.engine import Manager

state_list = []
m = Manager(
    "boats/sample_boat.json",
    "environments/playground.json",
    boat_heading=270
)

for step in range(3000):
    state_list.append(m.state)
    state = m.agent_state
    # do stuff here
    m.step([sail_angle, rudder_angle])

with open("out.sbpickle", "wb+") as f:
    pickle.dump(state_list, f)
    f.close()
```

Nas primeiras linhas, são importados `pickle`, para fazer a serialização dos dados de simulação para um arquivo, e o `Manager`. Em seguida, é criada uma lista de estados `state_list`, que será utilizada para armazenar os estados de simulação.

Depois, é instanciado o `Manager`, passando como argumento dois arquivos de configuração, um para o barco e um para o ambiente (a serem detalhados mais abaixo) e a orientação inicial do barco (a convenção utilizada é a do círculo trigonométrico).

Em seguida, é executado um loop por 3000 iterações. Cada iteração corresponde ao passo de tempo do simulador, configurado atualmente para 0.1 segundos. Ou seja, essa simulação corresponde a 3000 * 0.1s = 300s = 5 minutos.

Dentro desse loop, é armazenado na `state_list` o estado da simulação. Em seguida, é atribuído a `state` o chamado `agent_state`, que são as percepções do ambiente a partir da perspectiva do barco. O `agent_state` tem o seguinte formato:

```py
{
    "heading": xx,
    "wind_speed": xx,
    "wind_direction": xx,
    "position": [xx, xx],
}
```

onde `heading` corresponde à orientação do veleiro (todo o sistema de coordenadas utiliza a convenção do círculo trigonométrico), `wind_speed` à velocidade do vento "sentida" pela embarcação, `wind_direction` à direção do vento "sentida" pelo barco e `position` à posição (coordenada x,y) do barco. O `agent_state` pode ser interpretado como a leitura realizada por sensores em uma embarcação real, apenas ele deve ser utilizado para desenvolvimento do algoritmo de navegação autônoma.

Em seguida, há um comentário `do stuff here`. É nesse trecho que a lógica do algoritmo de navegação deve ser implementada, passando ao `Manager` apenas o ângulo da vela e do leme desejados na linha `m.step([sail_angle, rudder_angle])`.

Por fim, nas últimas três linhas, essa lista de estados é serializada para um arquivo `*.sbpickle`, de forma a permitir a visualização posterior dessa simulação.

### Visualização

O módulo `visualization` trata apenas de demonstrar, visualmente, o que aconteceu durante a simulação, tornando assim mais fácil entender e enxergar problemas que podem haver. A classe principal desse módulo é a `Viewer`.

Uma maneira de visualizar a simulação feita na seção anterior é a seguinte (explicações abaixo):

```py
import pickle
from sailboat_playground.visualization import Viewer

with open("output.sbpickle", "rb") as f:
    state_list = pickle.load(f)
    f.close()

v = Viewer()
v.run(state_list=state_list)
```

Nas duas primeiras linhas importamos o `pickle` para deserializar o arquivo que exportamos na última seção e o `Viewer`. Em seguida, carregamos a `state_list` através do arquivo `output.sbpickle`.

Depois, o `Viewer` é instanciado. Nesse caso, não fornecemos nenhum argumento a ele, porém ele aceita os argumentos `map_size`, para o tamanho do mapa (quadrado, centrado em zero, tamanho em metros, padrão 800 que corresponde a 800m x 800m), e `buoy_list`, para uma lista de bóias, caso queira representá-las na simulação (para fazer uma demonstração de uma prova do IRSC, por exemplo). O formato da `buoy_list` deve ser o seguinte:

```py
example_buoy_list = [
    (0, 0),     # Bóia posicionada no centro do mapa
    (-40, -40), # Bóia posicionada na coordenada (-40, -40)
]
```

Por fim, na última linha, executamos o `Viewer` passando como argumento nossa lista de estados gerada na simulação. O método `run` também aceita um argumento `simulation_speed`, que corresponde ao número de timesteps que o `Viewer` vai tentar executar por segundo. Por exemplo, então, o valor 10 corresponderia a 10 * 0.1s = 1s por segundo de visualização (tempo real). O valor padrão é 100 (10s de simulação por segundo de visualização). Caso um valor muito alto seja configurado, o computador que vai executar as instruções pode ser capaz de não conseguir prover poder de processamento suficiente. Nesse caso, a visualização será executada com a taxa máxima possível.

A visualização tem o seguinte formato:

![visualization.png](https://raw.githubusercontent.com/gabriel-milan/sailboat-playground/master/img/visualization.png)

O veleiro é facilmente identificável na imagem. No canto inferior esquerdo, é possível encontrar uma seta azul com uma velocidade embaixo. Esses são a direção e velocidade do vento real, respectivamente. Logo ao lado, um ícone de velocímetro e outro valor. Essa é a velocidade atual em módulo do veleiro. No canto inferior direito, é possível visualizar a posição atual do veleiro no mapa. Na parte de cima há duas bóias, de modo a exemplificar como elas são demonstradas na visualização. Em cima do veleiro é possível notar dois objetos vermelhos em formato de fólio. O maior deles, no centro do barco, corresponde à vela. O menor deles ao leme. Tanto o barco como vela e leme giram de maneira independente, permitindo uma visualização mais realista.

## Arquivos de configuração

Para deixar os scripts mais limpos, todas as configurações do ambiente (velocidade/direção dos ventos, variação, rajadas, correnteza, etc.) e do barco (massa, comprimento, centro de massa, modelo do fólio, etc.) foram concentradas em arquivos separados no formato JSON. Além disso, para cálculo das forças de interação, são utilizados coeficientes reais de lift e drag, extraídos do software JavaFoil. Esses coeficientes são colocados em arquivos CSV.

### Ambiente

Um exemplo de configuração do ambiente é o seguinte (explicações no próprio exemplo):

```json
{
    "name": "Example environment",       // Nome do ambiente (não tem relevância)
    "wind_min_speed": 3,                 // Velocidade mínima do vento (m/s)
    "wind_max_speed": 7,                 // Velocidade máxima do vento (m/s)
    "wind_max_delta_percent": 5,         // Máxima variação do vento (porcentagem) em um timestep
    "wind_gust_probability": 0.1,        // Probabilidade de rajada (0 a 1 seria de 0 a 100%)
    "wind_gust_min_duration": 3,         // Duração mínima das rajadas (segundos)
    "wind_gust_max_duration": 20,        // Duração máxima das rajadas (segundos)
    "wind_gust_min_speed": 5,            // Velocidade mínima do vento durante rajada (m/s)
    "wind_gust_max_speed": 10,           // Velocidade máxima do vento durante rajada (m/s)
    "wind_gust_max_delta_percent": 10,   // Variação máxima da velocidade do vento durante rajada (%)
    "wind_direction": 270,               // Direção do vento (graus), convenção círculo trigonométrico
    "current_speed": 0,                  // Velocidade da correnteza na água (m/s)
    "current_direction": 45              // Direção da correnteza na água (graus), mesma convenção
}
```

### Barco

Um exemplo de configuração do barco é o seguinte (explicações no próprio exemplo):

```json
{
    "name": "Example boat",              // Nome do barco (não tem relevância)
    "length": 1.1,                       // Comprimento do barco (m)
    "mass": 30,                          // Massa do barco (kg)
    "com_length": 0.5,                   // Comprimento da proa até o centro de massa (m)
    "sail_area": 1.0,                    // Área da vela (m^2)
    "sail_foil": "naca0015",             // Modelo do fólio da vela
    "rudder_area": 0.02,                 // Área do leme (m^2)
    "rudder_foil": "naca0015",           // Modelo do fólio do leme
    "hull_area": 0.03,                   // Área frontal do casco (m^2)
    "hull_friction_coefficient": 0.2,    // Coeficiente de fricção do casco (testar experimentalmente)
    "hull_rotation_resistance": 0.4,     // Coeficiente de resistência à rotação do casco (testar experimentalmente)
    "moment_of_inertia": 100             // Momento de inércia do barco (testar experimentalmente)
}
```

### Modelo de fólio

Como é um fólio com propósito mais genérico (e foi utilizado para construção da vela do veleiro Glória), aqui há um arquivo CSV com os coeficientes necessários para o NACA-0015, utilizado no arquivo de configuração acima. Caso deseje inserir outro modelo de fólio, o padrão é um arquivo CSV com três colunas: `alpha`, `cl` e `cd` e os coeficientes de lift e drag para alpha variando de -180 a 180 graus, com passo de 1 grau.