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
    for i in range(500):
        ts = agora + timedelta(seconds=i)
        temperatura = round(random.uniform(18, 45), 2)  # °C
        umidade = round(random.uniform(10, 90), 2)      # %
        env_rows.append([ts.isoformat(), temperatura, umidade])

    with open(CSV_ENV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temperature_c", "humidity_pct"])
        writer.writerows(env_rows)

    # ---- Dados MPU6050 (acelerações X, Y, Z) ----
    imu_rows = []
    for i in range(500):
        ts = agora + timedelta(seconds=i)
        acc_x = round(random.uniform(-2.0, 2.0), 3)  # g
        acc_y = round(random.uniform(-2.0, 2.0), 3)  # g
        acc_z = round(random.uniform(0.5, 3.0), 3)   # g (sempre perto da gravidade)
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
