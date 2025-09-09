import os
import math
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
DOC_DIR = os.path.join(REPO_DIR, "document")
OUT_ENV_IMG = os.path.join(BASE_DIR, "env_confusion.png")
OUT_IMU_IMG = os.path.join(BASE_DIR, "imu_confusion.png")

# ======================
# 1) Dataset ENV (DHT22)
# ======================
env = pd.read_csv(os.path.join(DOC_DIR, "dataset_env.csv"))
# Regras de rótulo (NORMAL/CRITICO)
def rotulo_env(row):
    t = row["temperature_c"]
    h = row["humidity_pct"]
    if t > 40 or h < 20 or h > 80:
        return 1  # CRITICO
    return 0      # NORMAL

env["label"] = env.apply(rotulo_env, axis=1).astype(int)
X_env = env[["temperature_c", "humidity_pct"]].values
y_env = env["label"].values
Xtr, Xte, ytr, yte = train_test_split(X_env, y_env, test_size=0.30, random_state=42, stratify=y_env)

clf_env = RandomForestClassifier(n_estimators=200, random_state=42)
clf_env.fit(Xtr, ytr)
pred_env = clf_env.predict(Xte)

acc_env = accuracy_score(yte, pred_env)
cm_env = confusion_matrix(yte, pred_env)

print(f"[ENV] accuracy = {acc_env:.4f}")
print("[ENV] confusion matrix:")
print(cm_env)
print("[ENV] classification report:")
print(classification_report(yte, pred_env, target_names=["NORMAL","CRITICO"]))

plt.figure()
plt.imshow(cm_env, interpolation="nearest")
plt.title("ENV - Matriz de Confusão")
plt.xlabel("Predito"); plt.ylabel("Real")
plt.xticks([0,1], ["NORMAL","CRITICO"])
plt.yticks([0,1], ["NORMAL","CRITICO"])
for (i, j), v in np.ndenumerate(cm_env):
    plt.text(j, i, str(v), ha='center', va='center')
plt.tight_layout()
plt.savefig(OUT_ENV_IMG, dpi=140)
plt.close()

# ======================
# 2) Dataset IMU (MPU6050)
# ======================
imu = pd.read_csv(os.path.join(DOC_DIR, "dataset_imu.csv"))

# Norma do vetor de aceleração
def norm(row):
    return math.sqrt(row["acc_x_g"]**2 + row["acc_y_g"]**2 + row["acc_z_g"]**2)

imu["g_norm"] = imu.apply(norm, axis=1)

# Regra de rótulo: vibração alta => CRITICO
imu["label"] = (imu["g_norm"] > 2.5).astype(int)

X_imu = imu[["acc_x_g", "acc_y_g", "acc_z_g"]].values
y_imu = imu["label"].values
Xtr, Xte, ytr, yte = train_test_split(X_imu, y_imu, test_size=0.30, random_state=42, stratify=y_imu)

clf_imu = RandomForestClassifier(n_estimators=200, random_state=42)
clf_imu.fit(Xtr, ytr)
pred_imu = clf_imu.predict(Xte)

acc_imu = accuracy_score(yte, pred_imu)
cm_imu = confusion_matrix(yte, pred_imu)

print(f"[IMU] accuracy = {acc_imu:.4f}")
print("[IMU] confusion matrix:")
print(cm_imu)
print("[IMU] classification report:")
print(classification_report(yte, pred_imu, target_names=["NORMAL","CRITICO"]))

plt.figure()
plt.imshow(cm_imu, interpolation="nearest")
plt.title("IMU - Matriz de Confusão")
plt.xlabel("Predito"); plt.ylabel("Real")
plt.xticks([0,1], ["NORMAL","CRITICO"])
plt.yticks([0,1], ["NORMAL","CRITICO"])
for (i, j), v in np.ndenumerate(cm_imu):
    plt.text(j, i, str(v), ha='center', va='center')
plt.tight_layout()
plt.savefig(OUT_IMU_IMG, dpi=140)
plt.close()

print(f"[OK] Imagens salvas em:\n - {OUT_ENV_IMG}\n - {OUT_IMU_IMG}")
