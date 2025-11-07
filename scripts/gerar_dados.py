import csv
import os
import random
from datetime import datetime, timedelta

# Caminhos dos arquivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC_DIR = os.path.join(BASE_DIR, "document")

CSV_ENV = os.path.join(DOC_DIR, "dataset_env.csv")
CSV_IMU = os.path.join(DOC_DIR, "dataset_imu.csv")

def gerar_dados():
    agora = datetime.now()

    # ---- Dados DHT22 (temperatura e umidade) ----
    env_rows = []
    temp_base = 25.0  # temperatura base normal
    humid_base = 55.0  # umidade base normal
    
    for i in range(500):
        ts = agora + timedelta(seconds=i)
        
        # Gera alguns eventos anormais
        if random.random() < 0.1:  # 10% de chance de anomalia
            temperatura = round(temp_base + random.uniform(10, 15), 2)  # anomalia alta
            umidade = round(humid_base + random.uniform(-30, 30), 2)
        else:
            temperatura = round(temp_base + random.uniform(-3, 3), 2)  # variação normal
            umidade = round(humid_base + random.uniform(-10, 10), 2)
            
        env_rows.append([ts.isoformat(), temperatura, umidade])

    with open(CSV_ENV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temperature_c", "humidity_pct"])
        writer.writerows(env_rows)

    # ---- Dados MPU6050 (acelerações X, Y, Z) ----
    imu_rows = []
    for i in range(500):
        ts = agora + timedelta(seconds=i)
        
        # Gera alguns eventos de vibração anormal
        if random.random() < 0.1:  # 10% de chance de anomalia
            acc_x = round(random.uniform(-1.5, 1.5), 3)  # vibração alta
            acc_y = round(random.uniform(-1.5, 1.5), 3)
            acc_z = round(1.0 + random.uniform(-0.5, 0.5), 3)  # variação na gravidade
        else:
            acc_x = round(random.uniform(-0.3, 0.3), 3)  # vibração normal
            acc_y = round(random.uniform(-0.3, 0.3), 3)
            acc_z = round(1.0 + random.uniform(-0.1, 0.1), 3)  # próximo da gravidade
            
        imu_rows.append([ts.isoformat(), acc_x, acc_y, acc_z])

    with open(CSV_IMU, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "acc_x_g", "acc_y_g", "acc_z_g"])
        writer.writerows(imu_rows)

    print(f"[OK] Arquivos gerados:")
    print(f" - {CSV_ENV}")
    print(f" - {CSV_IMU}")


if __name__ == "__main__":
    gerar_dados()
