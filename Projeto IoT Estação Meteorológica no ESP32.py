#Rodrigo Yuji Kawakani
#Importando bibliotecas utilizadas no projeto
import urequests
import dht
import machine
import time

#Função "conecta" para conexão wi-fi
def conecta(ssid, senha):
    import network
    import time
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, senha)
    for t in range(50):
        if station.isconnected():
            break
    time.sleep(0.1)
    return station

#Verificando a conexão
print("Conectando...")
station = conecta("nome wi-fi", "senha wi-fi") #Inserir nome e senha do wi-fi
if not station.isconnected():
    print("Não conectado!\n")
else:
    print("Conectado!\n")

#Variável "d" para acesso ao DHT11, pino 4
d = dht.DHT11(machine.Pin(4))

#Variável "r" para instrução de saída do ESP32 ao Relé, pino 2
r = machine.Pin(2, machine.Pin.OUT)

#Título inicial
print("Estação Meteorológica para Internet das Coisas\nObs: Caso a Temperatura seja maior do que 31 graus OU a Umidade Relativa do Ar for maior do que 70%, o Relé será ligado!\n")

#Medindo a temperatura e a umidade do ar com um laço de repetição
while True:
    d.measure()
    print("Temperatura = {}\nUmidade = {}".format(d.temperature(), d.humidity()))
    temperatura = d.temperature()
    umidade = d.humidity()
    
#Criar a conta no ThingSpeak, criar o canal do projeto e criar os campos temperatura e umidade que serão respectivamente o field1 e field2
#Envio dos dados ao ThingSpeak enquanto o código é executado
    print("Enviando as informações para o ThingSpeak...")
    
    envio = urequests.get('link do ThingSpeak'+'&field1='+str(temperatura)+'&field2='+str(umidade)) #Inserir o link fornecido pelo ThingSpeak localizado dentro do canal criado, na aba API Keys, API Requests, Write a Channel Feed
    envio.close()
    time.sleep(1)

#Condições para que o Relé seja ligado, caso a Temperatura seja maior do que 31 graus OU a Umidade do Ar maior do que 70%
    if d.temperature() > 31 or d.humidity() > 70:
        r.value(1)
        print("O Relé está ligado.\n")
        time.sleep(5)
    else:
        r.value(0)
        print("O Relé está desligado.\n")
        time.sleep(5)