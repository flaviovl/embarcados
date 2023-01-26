# Sistema de Controle Forno de Soldagem - SCFS

---
<br />
<p align="center"> <img src="images/" width="600"></p>
<br />

---

### 📋 Trabalho 2 - FSE

|Nome|Matrícula|
|---|---|
|Flavio Vieira Leão | 15/0125682|
<br />

### 📌 Visão Geral

  SCFS é um Sistema  que efetua o controle de temperatura do forno utilizando dois atuadores para este controle: um **resistor de potência** de 15 Watts utilizado para aumentar temperatura e; uma **ventoinha** que puxa o ar externo (temperatura ambiente) para reduzir a temperatura do sistema e tem  por objetivo simular o controle de um forno para soldagem de placas de circuito impresso (PCBs).
<br /> <br />

### 📋 **Principais Funcionalidades**

Os comandos do usuário do sistema para definir a temperatura desejada serão controlados de duas maneiras:

1. Manualmente através do seletor de temperatura no dashboard (Thingsboad);
2. Automaticamente seguindo uma curva de temperatura pré-definida em arquivo de configuração ([Arquivo da Curva](./curva_reflow.csv)).

## Componentes do Sistema

O sistema é composto por:

1. Ambiente fechado controlado com o resistor de potência e ventoinha;
2. 01 Sensor DS18B20 (1-Wire) para a medição da temperatura interna (**TI**) do sistema;
3. 01 Sensor BME280 (I2C) para a medição da temperatura externa (**TE**);
4. 01 Conversor lógico bidirecional (3.3V / 5V);
5. 01 Driver de potência para acionamento de duas cargas (L297);
6. 01 ESP32;
7. 01 Raspberry Pi 4;
<br />

### 🔧 **Como Rodar o Projeto**

* Clone esse repositório em uma raspberry PI.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.

```
git clone https://github.com/flaviovl/embarcados/
cd embarcados/scfs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
<br />  
