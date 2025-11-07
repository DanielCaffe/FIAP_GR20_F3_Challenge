import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import joblib
import sys
from pathlib import Path

# Adiciona o diretório ml ao path para importar a classe do modelo
sys.path.append(str(Path(__file__).parent.parent / "ml"))

st.set_page_config(page_title="Monitoramento Industrial", layout="wide")
st.title("🏭 Monitoramento Industrial – MVP")

DB_PATH = Path("../database/factory.db")
CSV_ENV = Path("../document/dataset_env.csv")
CSV_IMU = Path("../document/dataset_imu.csv")
MODEL_PATH = Path("../ml/modelo_treinado.pkl")

@st.cache_resource
def load_ai_model():
    """Carrega os componentes do modelo de IA treinado"""
    if not MODEL_PATH.exists():
        return None
    try:
        # Carrega apenas os componentes (não precisa da classe)
        model_components = joblib.load(MODEL_PATH)
        return model_components
    except Exception as e:
        st.warning(f"Erro ao carregar modelo de IA: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None


def extract_features_simple(data):
    """Extrai características simples dos dados"""
    features = {}
    features['mean'] = np.mean(data)
    features['std'] = np.std(data)
    features['rms'] = np.sqrt(np.mean(np.square(data)))
    
    freq_features = np.abs(np.fft.fft(data))
    features['freq_peak'] = np.max(freq_features)
    features['freq_mean'] = np.mean(freq_features)
    
    from scipy import stats
    features['trend'] = stats.linregress(range(len(data)), data)[0]
    features['kurtosis'] = stats.kurtosis(data)
    features['skewness'] = stats.skew(data)
    
    return features


def prepare_data_for_prediction(env, imu):
    """Prepara dados para predição"""
    window_size = 20
    features_list = []
    
    for i in range(len(env) - window_size):
        window_env = env.iloc[i:i+window_size]
        window_imu = imu.iloc[i:i+window_size]
        
        temp_features = extract_features_simple(window_env['temperature'].values)
        humid_features = extract_features_simple(window_env['humidity'].values)
        acc_x_features = extract_features_simple(window_imu['ax'].values)
        acc_y_features = extract_features_simple(window_imu['ay'].values)
        acc_z_features = extract_features_simple(window_imu['az'].values)
        
        combined_features = {
            **{f'temp_{k}': v for k, v in temp_features.items()},
            **{f'humid_{k}': v for k, v in humid_features.items()},
            **{f'acc_x_{k}': v for k, v in acc_x_features.items()},
            **{f'acc_y_{k}': v for k, v in acc_y_features.items()},
            **{f'acc_z_{k}': v for k, v in acc_z_features.items()}
        }
        
        features_list.append(combined_features)
        
    return pd.DataFrame(features_list)

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
colA.line_chart(env["temperature"], height=230, width="stretch")
colA.caption("Temperatura ao longo do tempo")
colB.line_chart(env["humidity"], height=230, width="stretch")
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


# ========== SEÇÃO DE IA ==========
st.divider()
st.header("🤖 Análise com Inteligência Artificial")

model_components = load_ai_model()

if model_components is not None:
    try:
        # Prepara dados para a IA
        with st.spinner("🧠 IA analisando dados..."):
            X_features = prepare_data_for_prediction(env, imu)
            
            # Faz predições usando os componentes salvos
            scaler = model_components['scaler']
            anomaly_detector = model_components['anomaly_detector']
            classifier = model_components['classifier']
            
            X_scaled = scaler.transform(X_features)
            anomalies = anomaly_detector.predict(X_scaled)
            classifications = classifier.predict(X_scaled)
            
            # Combina resultados
            predictions = np.logical_or(anomalies == -1, classifications == 1)
            
            # Estatísticas da IA
            total_analises = len(predictions)
            alertas_ia = int(predictions.sum())
            taxa_critico = (alertas_ia / total_analises) * 100
            
            # Exibe métricas
            col_ia1, col_ia2, col_ia3 = st.columns(3)
            col_ia1.metric("📊 Análises realizadas", total_analises)
            col_ia2.metric("⚠️ Alertas críticos (IA)", alertas_ia)
            col_ia3.metric("📈 Taxa de criticidade", f"{taxa_critico:.1f}%")
            
            # Explicação
            if alertas_ia > 0:
                st.error(f"🚨 A IA detectou {alertas_ia} períodos críticos nos dados analisados!")
                st.info("""
                **O que a IA detectou:**
                - Padrões anormais de temperatura e vibração
                - Combinações de sensores indicando problemas
                - Tendências que precedem falhas
                
                **Recomendação:** Agendar manutenção preventiva
                """)
            else:
                st.success("✅ A IA não detectou padrões críticos. Sistema operando normalmente!")
            
            # Gráfico de predições ao longo do tempo
            st.subheader("Predições da IA ao longo do tempo")
            pred_df = pd.DataFrame({
                'Análise': range(len(predictions)),
                'Estado': ['CRÍTICO' if p else 'NORMAL' for p in predictions],
                'Valor': [1 if p else 0 for p in predictions]
            })
            
            st.line_chart(pred_df.set_index('Análise')['Valor'], height=200, width="stretch")
            st.caption("1 = CRÍTICO | 0 = NORMAL")
            
            # Comparação: Regras vs IA
            st.subheader("📊 Comparação: Regras Manuais vs IA")
            alertas_regras = len(env_alerts) + imu_alert
            
            comp_col1, comp_col2 = st.columns(2)
            comp_col1.metric("🔧 Alertas (Regras Manuais)", alertas_regras)
            comp_col2.metric("🤖 Alertas (IA)", alertas_ia)
            
            if alertas_ia > alertas_regras:
                st.warning("⚡ A IA detectou mais problemas que as regras manuais! Ela identifica padrões sutis.")
            elif alertas_ia < alertas_regras:
                st.info("🎯 A IA é mais conservadora, reduzindo falsos alarmes.")
            else:
                st.success("✅ Ambos os métodos estão alinhados.")
                
    except Exception as e:
        st.error(f"Erro ao executar análise de IA: {e}")
        import traceback
        st.code(traceback.format_exc())
        st.info("Verifique se o modelo foi treinado corretamente executando: `python ml/treino.py`")
else:
    st.warning("""
    ⚠️ **Modelo de IA não encontrado!**
    
    Para habilitar a análise com IA:
    1. Execute: `python ml/treino.py`
    2. Recarregue o dashboard
    """)
