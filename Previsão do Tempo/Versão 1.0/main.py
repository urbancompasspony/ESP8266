# Inicio

# DICAS DISPLAY #

# Resolução do Display: 128x64
# Display Textual: Até 16 colunas; até 6 linhas

# hline/vline (hor.ver.): x, y, comprimento, cor
# line (segmento de reta): x1, y1, x2, y2, c (diagonais)
# rect (retangulo): x, y, comprimento, largura, cor
# text (texto): x, y, cor
# scroll (deslizar conteudo da tela pro lado): X/-x, Y/-y
# disp.contrast (brilho de tela): 0 a 255
# invert(1): troca cor da tela

# WIFI
# ap.ifconfig(('', '255.255.255.0', '192.168.0.1', '208.67.222.222')) 
# Default: ('192.168.4.1', '255.255.255.0', '192.168.4.1', '208.67.222.222')

# Se ESP8266 sem Display, comentar dispz 1 ao 5

# Pressão Atmosferica
# 1.013,25 mBar = hPa
# Cada 8 m = -1 hPa
# Uberaba X
# Rifaina Y

# Import List

import gc
import sys
import uos
import math
import BME280
import ssd1306

import esp
esp.osdebug(None)

import time
from time import sleep

import machine
from machine import Pin, I2C, PWM

#print("Import List") # Debug

# Variáveis

hum = ""
pres = ""
presA = ""
tempc = ""
tempf = 77 # 59F=15C 77F=25C
string = 1
string2 = 1
altloc = ""
altitude = ""
variacao = ""
frequency = 5000

altd1 = -1
altd2 = ""
altd3 = ""
altd4 = ""
altd5 = ""
altd6 = ""
altd7 = ""
altd8 = 0 # seg
altd9 = 0 # min
altd10 = 0 # hor

tempd1 = ""
tempd2 = ""
tempd3 = ""
tempd4 = ""
tempd5 = ""
tempd6 = ""

weather = ""

#print("Variaveis") # Debug

# Funções

def read_sensor():
  global tempc
  global tempf
  global hum
  global pres
  global presA
  global altitude
  global variacao
  global altloc
  global string
  global string2
  
  global altd1
  global altd2
  global altd3
  global altd4
  global altd5
  global altd6
  global altd7
  global altd8
  global altd9
  global altd10
  
  global tempd1
  global tempd2
  global tempd3
  global tempd4
  global tempd5
  global tempd6
  
  global weather

  while True:
    try:   
      tempc = bme.temperature
      tempc = tempc.replace("C","")
      #tempc = str(round(float(tempc), 0)) # Arredondamento
      tempc = math.trunc(float(tempc))
      #print(tempc) # Debug
      
      hum = bme.humidity
      hum = hum.replace("%","")
      #hum = str(round(float(hum), 0)) # Arredondamento
      hum = math.trunc(float(hum))
      #print(hum) # Debug
      
      pres = bme.pressure
      pres = pres.replace("hPa","")
      #print(pres) # Debug
      presA = bme.pressure
      presA = pres.replace("hPa","")
      #pres = str(round(float(pres), 0)) # Arredondamento
      presA = math.trunc(float(presA))
      #print(presA) # Debug
      
      # Temperatura em Fahrenheit - Direto do sensor!
      # Nao arredondar para aumentar precisao, caso use.
      #tempf = (1500/100) * (1.8) + 32 #15grau
      #tempf = str(tempf).replace("F","")
      #print(tempf) # Debug

      # Calculo da Altitude
      pres2 = float(pres)*float(100)
      altitude = float(pres2)/float(101325)
      altitude = math.log(float(altitude))
      altitude = float(altitude)*float(287.053)
      altf = float(tempf)+float(459.67)
      altf = float(altf)*float(5/9)
      altitude = float(altf)*float(altitude)
      altitude = float(altitude)/float(-9.8)
      #altitude = str(round(float(altitude), 0))  # Arredondamento
      altitude = math.trunc(float(altitude)) # Truncar valores apos o ponto

      if string == 1:
        string = 0
        altloc = str(altitude)
      
      variacao = float(altloc)-float(altitude)
      #variacao = str(round(variacao, 0)) # Arredondamento
      variacao = -float(variacao) # Se variou acima, positivo. Se desceu, negativo.
      variacao = math.trunc(float(variacao)) # Truncar valores apos o ponto

      # START Tabela
      altd1 = altd1 + 1
      altd8 = altd1
      altd8 = altd1 * 5

      if altd8 > 59:
        altd1 = 0 # contador de sleeps
        altd8 = 0 # contador convertido para display
        altd9 = altd9 + 1 # minutos

      if altd9 == 0 and altd8 == 0:
        altd2 = altitude
        tempd1 = tempc
        
      if altd9 == 15 and altd8 == 0:
        altd3 = altd2
        altd2 = altitude
        tempd2 = tempd1
        tempd1 = tempc
        
      if altd9 == 30 and altd8 == 0:
        altd4 = altd3
        altd3 = altd2
        altd2 = altitude
        tempd3 = tempd2
        tempd2 = tempd1
        tempd1 = tempc

      if altd9 == 45 and altd8 == 0:
        altd5 = altd4
        altd4 = altd3
        altd3 = altd2
        altd2 = altitude
        tempd4 = tempd3
        tempd3 = tempd2
        tempd2 = tempd1
        tempd1 = tempc
        
      if altd9 == 59 and altd8 == 0:
        altd6 = altd5
        altd5 = altd4
        altd4 = altd3
        altd3 = altd2
        altd2 = altitude
        tempd5 = tempd4
        tempd4 = tempd3
        tempd3 = tempd2
        tempd2 = tempd1
        tempd1 = tempc
        
      if altd9 > 59:
        altd9 = 0    
        altd10 = altd10 + 1 # horas
       
      gc.collect()
      #print("Read Sensor") # Debug
      break
    except:
      gc.collect()
      #print("Read Sensor OSError") # Debug
      break
    else:
      gc.collect()
      #print("Read Sensor Else") # Debug
      break

def prevtemp():
  global tempc
  global tempf
  global hum
  global pres
  global presA
  global altitude
  global variacao
  global altloc
  global string
  global string2
  
  global altd1
  global altd2
  global altd3
  global altd4
  global altd5
  global altd6
  global altd7
  global altd8
  global altd9
  global altd10
  
  global tempd1
  global tempd2
  global tempd3
  global tempd4
  global tempd5
  global tempd6
  
  global weather
  
  # LOGICA: 
  
# 1. AUMENTO DO BARÔMETRO + AUMENTO DA TEMPERATURA = TEMPO BOM, COM VENTOS SECOS E QUENTES;
# 3. AUMENTO DO BARÔMETRO + DIMINUIÇÃO DA TEMPERATURA = TEMPO BOM, COM VENTO FRIO;
# 7. DIMINUIÇÃO DO BARÔMETRO + AUMENTO DA TEMPERATURA = TEMPO INSTÁVEL, COM PROBABILIDADE DE APROXIMAÇÃO DE FRENTE;
# 8. DIMINUIÇÃO DO BARÔMETRO + INALTERAÇÃO DA TEMPERATURA = APROXIMAÇÃO DE FRENTE QUENTE, COM PROBABILIDADE DE CHUVAS;

# A. Pressão Aumenta, Altitude Diminui
# B. Pressão Diminui, Altitude Aumenta

  if int(altd2) > 600: # Detectando região: Uberaba (altitude média 795m)
    if int(altd2) > 795 and int(tempc) > 27: # Ceu Limpo e Calor
      weather = str("Condicao Alpha")
    elif int(altd2) > 800 and int(tempc) < 24: # Ceu Limpo e Frio
      weather = str("Condicao Beta")
    elif int(altd2) < 750 and int(tempc) > 27: # Nublado e Calor
      weather = str("Condicao Gamma")
    elif int(altd2) < 750 and int(tempc) < 27 and int(tempc) > 24: # Tempestade
      weather = str("Condicao Delta")
    else:
      weather = str("Tempo Estavel")
     
  else: # Detectando região: Rifaina (altitude média 565m)
    if int(altd2) > 400:
      weather = str("Prob.Chuva:400")

def display():
  global tempc
  global tempf
  global hum
  global pres
  global presA
  global altitude
  global variacao
  global altloc
  global string
  global string2
  
  global altd1
  global altd2
  global altd3
  global altd4
  global altd5
  global altd6
  global altd7
  global altd8
  global altd9
  global altd10
  
  global tempd1
  global tempd2
  global tempd3
  global tempd4
  global tempd5
  global tempd6

  global weather
  
  while True:
    try:     
      disp.fill(0)
      
      #disp.vline(102, 1, 20, 1)
      disp.hline(1, 53, 126, 1) # de 20 pra 50 preenche até o fim
      #disp.vline(81, 20, 43, 1)
      #disp.text("Weather Station", 1, 2)
      #disp.vline(50, 1, 52, 1)
      disp.vline(69, 1, 52, 1)
      #disp.vline(108, 1, 52, 1)    
        
      # BLOCO 1

      #disp.text("1000", 1, 23)
      disp.text("C", 18, 1)
      disp.text("%", 18, 12)
      disp.text("hPA", 34, 23)
      disp.text("aTR", 34, 34)
      disp.text("Da", 42, 45)
      disp.text(str(altd10) + ":" + str(altd9), 32, 7) #  + ":" + str(altd8) for seconds 27
      
      disp.text(str(tempc), 0, 1)
      disp.text(str(hum), 0, 12)
      disp.text(str(presA), 0, 23) 
      disp.text(str(altitude), 0, 34)
      disp.text(str(variacao), 0, 45)
        
      # BLOCO 2
      
      #disp.text("1000", 1, 23)
      #disp.text("RT", 110, 1)
      disp.text(str(tempd1), 110, 1)
      disp.text(str(tempd2), 110, 12)
      disp.text(str(tempd3), 110, 23)
      disp.text(str(tempd4), 110, 34)
      disp.text(str(tempd5), 110, 45)
      disp.text(str(weather), 0, 56)
      
      disp.text(":", 103, 1)
      disp.text(":", 103, 12)
      disp.text(":", 103, 23)
      disp.text(":", 103, 34)
      disp.text(":", 103, 45)

      disp.text(str(altd2), 72, 1)
      disp.text(str(altd3), 72, 12) 
      disp.text(str(altd4), 72, 23)
      disp.text(str(altd5), 72, 34)
      disp.text(str(altd6), 72, 45)
      
      disp.show()
      gc.collect()
      #print("Display") # Debug
      break
    except:
      gc.collect()
      #print("Display OSError") # Debug
      break
    else:
      gc.collect()
      #print("Display Else") # Debug
      break

# Chamadas Protocolo i2c
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000) # Sensor
i2cc = machine.I2C(scl=machine.Pin(14), sda=machine.Pin(12)) # Display
bme = BME280.BME280(i2c=i2c) # Sensor
disp = ssd1306.SSD1306_I2C(128, 64, i2cc) # Display #DISPz3
disp.fill(0) #DISPz4
disp.show() #DISPz5
#print("Loading i2c") # Debug

# Controle do LED Embutido na Placa!
# Verifique FadeIn LED Embutido no Primeiro While
led = PWM(Pin(2), frequency)
led.duty(1024) # Led off ao ligar!
#print("LED Start") # Debug

# Inicializar o Sistema Principal #

while True:
  #socket_weather()
  disp.show()
  read_sensor()
  prevtemp()
  display()
  sleep(5)

# Fim do Código





