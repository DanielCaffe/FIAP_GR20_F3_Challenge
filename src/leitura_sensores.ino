#include <DHT.h>
#include <Wire.h>
#include <MPU6050.h>

// Definição dos pinos e constantes
#define DHTPIN 15       // Pino do sensor DHT22
#define DHTTYPE DHT22   // Tipo do sensor DHT
#define INTERVALO 2000  // Intervalo de leitura (2 segundos)

// Inicialização dos objetos dos sensores
DHT dht(DHTPIN, DHTTYPE);
MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  while(!Serial) { delay(100); }  // Aguarda a conexão serial
  
  Serial.println("Iniciando sensores...");
  
  // Inicializa o sensor DHT22
  dht.begin();
  
  // Inicializa o MPU6050
  Wire.begin();
  delay(1000);  // Tempo para estabilizar
  
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("Erro: MPU6050 não encontrado!");
    while (1) { delay(100); }
  }
  
  Serial.println("Sensores inicializados!");
  Serial.println("tempo,temperatura,umidade,acc_x,acc_y,acc_z");
}

void loop() {
  // Lê temperatura e umidade do DHT22
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();
  
  // Lê acelerações do MPU6050
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);
  
  // Converte para g (1g = 9.81 m/s²)
  float acc_x = ax / 16384.0;
  float acc_y = ay / 16384.0;
  float acc_z = az / 16384.0;
  
  // Verifica se as leituras são válidas
  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Erro: Falha na leitura do DHT22!");
    return;
  }
  
  // Imprime os dados no formato CSV
  Serial.printf("%.1f,%.2f,%.2f,%.3f,%.3f,%.3f\n",
    millis()/1000.0, temperatura, umidade, acc_x, acc_y, acc_z);
  
  delay(INTERVALO);
}