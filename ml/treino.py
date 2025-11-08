# -*- coding: utf-8 -*-
import os
import math
import numpy as np
import pandas as pd
import joblib
from scipy import stats
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
DOC_DIR = os.path.join(REPO_DIR, "document")
OUT_ENV_IMG = os.path.join(BASE_DIR, "env_confusion.png")
OUT_IMU_IMG = os.path.join(BASE_DIR, "imu_confusion.png")
OUT_FEATURE_IMPORTANCE = os.path.join(BASE_DIR, "feature_importance.png")
MODEL_PATH = os.path.join(BASE_DIR, "modelo_treinado.pkl")
THRESHOLDS_PATH = os.path.join(BASE_DIR, "thresholds.json")

# Carrega thresholds personalizados ou usa padrões
def load_thresholds():
    import json
    if os.path.exists(THRESHOLDS_PATH):
        with open(THRESHOLDS_PATH, 'r') as f:
            return json.load(f)
    return {
        'temp_max': 40.0,
        'humid_min': 30.0,
        'humid_max': 80.0,
        'acc_norm': 3.0
    }

class PredictiveMaintenanceModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.classifier = RandomForestClassifier(n_estimators=200, random_state=42)
        self.feature_importance = None
        
    def extract_features(self, data):
        """
        Extrai características baseadas em artigos científicos sobre manutenção preditiva
        Ref: "Predictive maintenance enabled by machine learning: Use cases and challenges"
        """
        features = {}
        
        # Características estatísticas (baseadas no artigo 1)
        features['mean'] = np.mean(data)
        features['std'] = np.std(data)
        features['rms'] = np.sqrt(np.mean(np.square(data)))
        
        # Características do domínio da frequência (artigo 2)
        freq_features = np.abs(np.fft.fft(data))
        features['freq_peak'] = np.max(freq_features)
        features['freq_mean'] = np.mean(freq_features)
        
        # Indicadores de tendência (artigo 3)
        features['trend'] = stats.linregress(range(len(data)), data)[0]
        features['kurtosis'] = stats.kurtosis(data)
        features['skewness'] = stats.skew(data)
        
        return features

    def prepare_data(self, env_data, imu_data, thresholds=None):
        """
        Prepara dados combinando sensores diferentes
        Ref: "Data fusion techniques for machine learning in predictive maintenance"
        """
        if thresholds is None:
            thresholds = load_thresholds()
        
        # Janela deslizante para análise temporal
        window_size = 20  # Baseado em estudos empíricos
        features_list = []
        labels = []
        
        for i in range(len(env_data) - window_size):
            window_env = env_data.iloc[i:i+window_size]
            window_imu = imu_data.iloc[i:i+window_size]
            
            # Extrai features de temperatura
            temp_features = self.extract_features(window_env['temperature_c'])
            humid_features = self.extract_features(window_env['humidity_pct'])
            
            # Extrai features de vibração
            acc_x_features = self.extract_features(window_imu['acc_x_g'])
            acc_y_features = self.extract_features(window_imu['acc_y_g'])
            acc_z_features = self.extract_features(window_imu['acc_z_g'])
            
            # Combina todas as features
            combined_features = {
                **{f'temp_{k}': v for k, v in temp_features.items()},
                **{f'humid_{k}': v for k, v in humid_features.items()},
                **{f'acc_x_{k}': v for k, v in acc_x_features.items()},
                **{f'acc_y_{k}': v for k, v in acc_y_features.items()},
                **{f'acc_z_{k}': v for k, v in acc_z_features.items()}
            }
            
            features_list.append(combined_features)
            
            # Define condições críticas usando thresholds dinâmicos
            temp_max = window_env['temperature_c'].max()
            humid_min = window_env['humidity_pct'].min()
            humid_max = window_env['humidity_pct'].max()
            acc_norm = np.sqrt(
                window_imu['acc_x_g']**2 + 
                window_imu['acc_y_g']**2 + 
                window_imu['acc_z_g']**2
            ).max()
            
            # Usa thresholds configuráveis
            is_critical = (
                (temp_max > thresholds['temp_max']) or
                (humid_min < thresholds['humid_min']) or
                (humid_max > thresholds['humid_max']) or
                (acc_norm > thresholds['acc_norm'])
            )
            
            # Debug para os primeiros registros
            if i < 5:
                print(f"\nRegistro {i}:")
                print(f"Temp Max: {temp_max:.2f}°C")
                print(f"Humid Min: {humid_min:.2f}%")
                print(f"Humid Max: {humid_max:.2f}%")
                print(f"Acc Norm: {acc_norm:.2f}g")
                print(f"Crítico: {is_critical}")
            labels.append(1 if is_critical else 0)
            
        return pd.DataFrame(features_list), np.array(labels)

    def train(self, X, y):
        """
        Treina modelo com validação cruzada e otimização de hiperparâmetros
        Ref: "Machine Learning for Predictive Maintenance: A Multiple Classifier Approach"
        """
        print("\nIniciando treinamento do modelo...")
        
        # Normaliza dados
        X_scaled = self.scaler.fit_transform(X)
        print("Dados normalizados")
        
        # Detecta anomalias
        print("Treinando detector de anomalias...")
        self.anomaly_detector.fit(X_scaled)
        
        # Otimiza hiperparâmetros
        print("Otimizando hiperparâmetros...")
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        grid_search = GridSearchCV(
            self.classifier, param_grid, cv=5, 
            scoring='f1', n_jobs=-1, verbose=1
        )
        grid_search.fit(X_scaled, y)
        
        print(f"\nMelhores parâmetros encontrados: {grid_search.best_params_}")
        
        self.classifier = grid_search.best_estimator_
        self.feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.classifier.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return self.evaluate(X_scaled, y)
    
    def evaluate(self, X, y):
        """
        Avalia modelo com métricas múltiplas
        """
        print("\nAvaliando modelo...")
        y_pred = self.classifier.predict(X)
        precision, recall, f1, _ = precision_recall_fscore_support(y, y_pred, average='binary')
        
        # Gera matriz de confusão
        cm = confusion_matrix(y, y_pred)
        plt.figure(figsize=(8, 6))
        plt.imshow(cm, interpolation='nearest', cmap='Blues')
        plt.title("Matriz de Confusão")
        plt.colorbar()
        plt.xlabel("Predito")
        plt.ylabel("Real")
        plt.xticks([0,1], ["NORMAL","CRÍTICO"])
        plt.yticks([0,1], ["NORMAL","CRÍTICO"])
        
        # Adiciona valores na matriz
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, str(cm[i, j]),
                        horizontalalignment="center",
                        verticalalignment="center")
        
        plt.tight_layout()
        plt.savefig(OUT_ENV_IMG)
        plt.close()
        
        # Plot feature importance
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(self.feature_importance)), self.feature_importance['importance'])
        plt.xticks(range(len(self.feature_importance)), 
                  self.feature_importance['feature'], rotation=45, ha='right')
        plt.title("Importância das Features")
        plt.tight_layout()
        plt.savefig(OUT_FEATURE_IMPORTANCE)
        plt.close()
        
        return {
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def predict(self, X):
        """
        Faz predições combinando classificador e detector de anomalias
        """
        X_scaled = self.scaler.transform(X)
        anomalies = self.anomaly_detector.predict(X_scaled)
        classifications = self.classifier.predict(X_scaled)
        
        # Combina resultados (-1 do IsolationForest indica anomalia)
        return np.logical_or(anomalies == -1, classifications == 1)

if __name__ == "__main__":
    print("Carregando dados...")
    # Carrega thresholds
    thresholds = load_thresholds()
    print(f"\nUsando thresholds:")
    print(f"  Temperatura máxima: {thresholds['temp_max']}°C")
    print(f"  Umidade mínima: {thresholds['humid_min']}%")
    print(f"  Umidade máxima: {thresholds['humid_max']}%")
    print(f"  Aceleração máxima: {thresholds['acc_norm']}g")
    
    # Carrega dados
    env_data = pd.read_csv(os.path.join(DOC_DIR, "dataset_env.csv"))
    imu_data = pd.read_csv(os.path.join(DOC_DIR, "dataset_imu.csv"))
    
    print("\nInformações dos dados carregados:")
    print("Dados ENV:")
    print(env_data.info())
    print("\nPrimeiras linhas ENV:")
    print(env_data.head())
    print("\nDados IMU:")
    print(imu_data.info())
    print("\nPrimeiras linhas IMU:")
    print(imu_data.head())
    
    # Verifica nomes das colunas
    print("\nColunas ENV:", env_data.columns.tolist())
    print("Colunas IMU:", imu_data.columns.tolist())
    
    # Ajusta nomes das colunas se necessário
    column_mapping_env = {
        'timestamp': 'timestamp',
        'temperature': 'temperature_c',
        'humidity': 'humidity_pct'
    }
    
    column_mapping_imu = {
        'timestamp': 'timestamp',
        'acc_x': 'acc_x_g',
        'acc_y': 'acc_y_g',
        'acc_z': 'acc_z_g'
    }
    
    env_data = env_data.rename(columns={k: v for k, v in column_mapping_env.items() if k in env_data.columns})
    imu_data = imu_data.rename(columns={k: v for k, v in column_mapping_imu.items() if k in imu_data.columns})
    
    print("\nPreparando modelo...")
    # Inicializa e treina modelo
    model = PredictiveMaintenanceModel()
    X, y = model.prepare_data(env_data, imu_data, thresholds)
    
    print("\nInformações dos dados processados:")
    print("Shape de X:", X.shape)
    print("Shape de y:", y.shape)
    print("\nDistribuição das classes:")
    print(pd.Series(y).value_counts())
    
    # Divide dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    print("\nTamanho dos conjuntos de treino/teste:")
    print(f"X_train: {X_train.shape}")
    print(f"X_test: {X_test.shape}")
    print(f"y_train: {y_train.shape}")
    print(f"y_test: {y_test.shape}")
    
    # Treina e avalia
    metrics = model.train(X_train, y_train)
    
    # Imprime resultados
    print("\nResultados do Modelo:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")
        
    print("\nFeatures mais importantes:")
    print(model.feature_importance.head())
    
    # Salva apenas os componentes do modelo (não o objeto inteiro)
    print(f"\nSalvando modelo treinado em: {MODEL_PATH}")
    model_components = {
        'scaler': model.scaler,
        'anomaly_detector': model.anomaly_detector,
        'classifier': model.classifier,
        'feature_importance': model.feature_importance
    }
    joblib.dump(model_components, MODEL_PATH)
    print("[OK] Modelo salvo com sucesso!")
    
    print(f"\n[OK] Imagens salvas em:")
    print(f" - {OUT_ENV_IMG}")
    print(f" - {OUT_FEATURE_IMPORTANCE}")
