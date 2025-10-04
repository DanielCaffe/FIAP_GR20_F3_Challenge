import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Monitoramento Industrial", layout="wide")
st.title("🏭 Monitoramento Industrial – MVP")

DB_PATH = Path("database/factory.db")
CSV_ENV = Path("document/dataset_env.csv")
CSV_IMU = Path("document/dataset_imu.csv")

@st.cache_data
def load_from_sqlite():
    if not DB_PATH.exists():
        return None, None
    con = sqlite3.connect(DB_PATH)

    env = pd.read_sql_query(
        """
        SELECT
            ts AS ts,
            temperature_c AS temperature,
            humidity_pct  AS humidity
        FROM READING_ENV
        ORDER BY ts
        """,
        con,
    )

    imu = pd.read_sql_query(
        """
        SELECT
            ts AS ts,
            acc_x_g AS ax,
            acc_y_g AS ay,
            acc_z_g AS az
        FROM READING_IMU
        ORDER BY ts
        """,
        con,
    )

    con.close()
    return env, imu

@st.cache_data
def load_from_csv():
    env = pd.read_csv(CSV_ENV) if CSV_ENV.exists() else None
    imu = pd.read_csv(CSV_IMU) if CSV_IMU.exists() else None

    if env is not None:
        ren = {}
        cols = {c.lower(): c for c in env.columns}
        if "temperature_c" in cols: ren[cols["temperature_c"]] = "temperature"
        elif "temperature" in cols: ren[cols["temperature"]] = "temperature"
        if "humidity_pct" in cols: ren[cols["humidity_pct"]] = "humidity"
        elif "humidity" in cols: ren[cols["humidity"]] = "humidity"
        if "ts" in cols: ren[cols["ts"]] = "ts"
        elif "timestamp" in cols: ren[cols["timestamp"]] = "ts"
        env = env.rename(columns=ren)

    if imu is not None:
        ren = {}
        cols = {c.lower(): c for c in imu.columns}
        for src, dst in [
            ("acc_x_g", "ax"), ("ax", "ax"),
            ("acc_y_g", "ay"), ("ay", "ay"),
            ("acc_z_g", "az"), ("az", "az"),
            ("ts", "ts"), ("timestamp", "ts")
        ]:
            if src in cols:
                ren[cols[src]] = dst
        imu = imu.rename(columns=ren)

    return env, imu


st.sidebar.header("Fonte de dados")
source = st.sidebar.radio("Carregar dados de:", ["SQLite (database/factory.db)", "CSV (document/)"])
if source.startswith("SQLite"):
    env, imu = load_from_sqlite()
else:
    env, imu = load_from_csv()

if env is None or imu is None:
    st.warning("Não encontrei os dados. Garanta que o banco foi populado (ou os CSVs existam).")
    st.stop()

TEMP_MAX = st.sidebar.number_input("Alerta: Temperatura > (°C)", value=40.0)
H_MIN   = st.sidebar.number_input("Alerta: Umidade < (%)", value=20.0)
H_MAX   = st.sidebar.number_input("Alerta: Umidade > (%)", value=80.0)
ACC_THR = st.sidebar.number_input("Alerta: Norma aceleração > (g)", value=2.5)

st.subheader("🌡️ Ambiente (DHT22)")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Temp média (°C)", f"{env['temperature'].mean():.2f}")
c2.metric("Temp máx (°C)",  f"{env['temperature'].max():.2f}")
c3.metric("Umidade média (%)", f"{env['humidity'].mean():.2f}")
c4.metric("Umidade máx (%)", f"{env['humidity'].max():.2f}")

colA, colB = st.columns(2)
colA.line_chart(env["temperature"], height=230, use_container_width=True)
colA.caption("Temperatura ao longo do tempo")
colB.line_chart(env["humidity"], height=230, use_container_width=True)
colB.caption("Umidade ao longo do tempo")

env_alerts = env[(env["temperature"] > TEMP_MAX) | (env["humidity"] < H_MIN) | (env["humidity"] > H_MAX)]
st.write(f"Alertas críticos (ENV): **{len(env_alerts)}**")
if len(env_alerts) > 0:
    st.error("⚠️ ALERTA: leituras críticas detectadas (ENV).")
else:
    st.success("✅ Sem alertas críticos em ENV.")


st.subheader("📈 Vibração (MPU6050)")
imu = imu.copy()
imu["acc_norm"] = np.sqrt(imu["ax"]**2 + imu["ay"]**2 + imu["az"]**2)

d1, d2, d3 = st.columns(3)
d1.metric("Norma média (g)", f"{imu['acc_norm'].mean():.2f}")
d2.metric("Norma máx (g)",  f"{imu['acc_norm'].max():.2f}")
d3.metric("Alertas críticos (IMU)", f"{(imu['acc_norm'] > ACC_THR).sum()}")

st.line_chart(imu["acc_norm"], height=230, use_container_width=True)
imu_alert = (imu["acc_norm"] > ACC_THR).sum()
if imu_alert > 0:
    st.error("⚠️ ALERTA: vibração/tremor acima do limite (IMU).")
else:
    st.success("✅ Sem alertas críticos em IMU.")


st.caption("Dados carregados de: " + ("SQLite" if source.startswith("SQLite") else "CSV"))
