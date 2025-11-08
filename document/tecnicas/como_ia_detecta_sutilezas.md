# 🧠 Como a IA Detecta Sutilezas - Explicação Detalhada

## 📊 Etapa 1: Extração de Features (Características)

Para cada janela de 20 segundos, a IA extrai **8 características** de cada sensor:

### **Exemplo com Temperatura:**

```
Dados brutos (20 segundos):
[25.5, 26.1, 26.8, 27.2, 27.9, 28.3, 29.1, 29.8, 30.2, 30.9, 
 31.5, 32.1, 32.8, 33.4, 34.1, 34.8, 35.5, 36.2, 36.9, 37.5]

↓ A IA extrai 8 características:

1. mean (média): 31.3°C
2. std (desvio padrão): 3.8°C ← ALTA VARIAÇÃO!
3. rms (root mean square): 31.5°C
4. freq_peak (pico frequência): 12.5 ← PADRÃO OSCILANTE!
5. freq_mean (média frequência): 8.3
6. trend (tendência): +0.62 ← SUBINDO RÁPIDO!
7. kurtosis (curtose): 1.2 ← DISTRIBUIÇÃO NORMAL
8. skewness (assimetria): 0.15 ← LEVEMENTE ASSIMÉTRICO
```

### **Regra Manual vs IA:**

**Regra Manual:**
```python
if temperatura > 42:
    alerta()  # Só olha o valor final (37.5°C) → SEM ALERTA
```

**IA:**
```python
# Analisa TODAS as 8 características:
- Temperatura está subindo rápido (trend: +0.62)
- Variação muito alta (std: 3.8)
- Padrão de oscilação anormal (freq_peak: 12.5)
# Conclusão: CRÍTICO! Tendência de superaquecimento!
```

---

## 🔢 Etapa 2: Combinação de Sensores

A IA não analisa sensores isoladamente, mas **combinações**:

### **5 sensores × 8 features = 40 características totais:**

```
Temperatura:  8 features → temp_mean, temp_std, temp_rms, ...
Umidade:      8 features → humid_mean, humid_std, humid_rms, ...
Aceleração X: 8 features → acc_x_mean, acc_x_std, acc_x_rms, ...
Aceleração Y: 8 features → acc_y_mean, acc_y_std, acc_y_rms, ...
Aceleração Z: 8 features → acc_z_mean, acc_z_std, acc_z_rms, ...
────────────────────────────────────────────────────────────
TOTAL:       40 features
```

### **Exemplo de Correlação que Regras Não Veem:**

```
Situação:
- Temperatura: 35°C (abaixo de 42°C - OK para regra manual)
- Vibração X: 0.8g (abaixo de 2.8g - OK para regra manual)
- Vibração Y: 0.9g (abaixo de 2.8g - OK para regra manual)

Mas a IA vê:
- temp_trend: +0.5 (subindo)
- acc_x_freq_peak: 15.2 (vibrando em frequência específica)
- acc_y_freq_peak: 15.3 (mesma frequência!)
- Correlação: humid_std ↑ quando temp_trend ↑

IA: "Padrão de desbalanceamento de rolamento iniciando!"
→ ALERTA mesmo com valores individuais OK!
```

---

## 🎯 Etapa 3: Dois Modelos Trabalhando Juntos

### **Modelo 1: IsolationForest (Detector de Anomalias)**

```python
IsolationForest(contamination=0.1)
```

**O que faz:**
- Aprende o que é "normal" nos 40 features
- Detecta qualquer coisa "fora do padrão"
- Não precisa saber o que é crítico, só "diferente"

**Exemplo:**
```
Padrão Normal:
- temp_std geralmente entre 1.5 e 2.5
- acc_x_freq_peak geralmente entre 5 e 10

Análise 153:
- temp_std: 4.8 ← MUITO ALTO!
- acc_x_freq_peak: 18.5 ← MUITO ALTO!

IsolationForest: "Isso é ANORMAL!" → -1 (anomalia)
```

### **Modelo 2: RandomForest (Classificador)**

```python
RandomForestClassifier(n_estimators=100-300)
```

**O que faz:**
- Aprende com exemplos rotulados (NORMAL vs CRÍTICO)
- Usa 100-300 árvores de decisão votando
- Cada árvore analisa subconjuntos diferentes de features

**Exemplo de Árvore de Decisão:**
```
                    humid_std > 12?
                    /            \
                  SIM            NÃO
                   |              |
          temp_trend > 0.4?   acc_x_freq > 14?
           /        \          /           \
         SIM       NÃO       SIM          NÃO
          |         |         |            |
       CRÍTICO   NORMAL   CRÍTICO      NORMAL
```

Cada árvore vota, e a maioria decide!

---

## 🔄 Etapa 4: Combinação Final

```python
def predict(X):
    anomalies = IsolationForest.predict(X)      # -1 ou 1
    classifications = RandomForest.predict(X)    # 0 ou 1
    
    # Combina: Se QUALQUER um detectar problema
    return (anomalies == -1) OR (classifications == 1)
```

**Por que combinar?**

| Situação | IsolationForest | RandomForest | Resultado Final |
|----------|-----------------|--------------|-----------------|
| Padrão novo nunca visto | ✅ Detecta | ❌ Não conhece | ✅ **ALERTA** |
| Padrão conhecido crítico | ❌ Parece normal | ✅ Detecta | ✅ **ALERTA** |
| Variação sazonal normal | ✅ Detecta | ❌ Sabe que é OK | ❌ Sem alerta |
| Tudo normal | ❌ Normal | ❌ Normal | ❌ Sem alerta |

---

## 📈 Por Que 153 Alertas (31.9%)?

Vamos analisar o que a IA está vendo:

### **Análise de uma Janela Crítica (exemplo):**

```python
Janela 42 (segundos 42-62):

Dados brutos parecem OK:
- Temp: 36.5°C (< 42°C threshold)
- Humid: 68% (entre 25-85%)
- Acc: 1.8g (< 2.8g threshold)

Mas as FEATURES mostram:

1. temp_std = 4.2 (variação alta!)
2. temp_trend = +0.58 (subindo rápido!)
3. humid_std = 15.3 (oscilando muito!)
4. acc_x_freq_peak = 16.8 (vibração em freq. específica!)
5. acc_y_freq_peak = 16.9 (mesma freq. em Y!)
6. acc_z_rms = 1.95 (energia alta no eixo Z!)

Correlações detectadas:
- Quando temp_trend ↑ → acc_freq_peak ↑ (correlação 0.85!)
- Quando humid_std ↑ → temp_std ↑ (correlação 0.72!)

IA: "Padrão de desbalanceamento mecânico com aquecimento!"
→ CRÍTICO!
```

---

## 🎓 Resumo: IA vs Regras Manuais

### **Regras Manuais:**
```python
if temp > 42 or humid < 25 or humid > 85 or acc > 2.8:
    alerta()
```
- Olha apenas valores instantâneos
- Ignora tendências
- Ignora correlações
- Ignora padrões de frequência

### **IA:**
```python
# Para CADA janela de 20 segundos:
features = extrair_40_caracteristicas()
anomalia = IsolationForest(features)  # Detecta padrões estranhos
criticidade = RandomForest(features)   # Classifica gravidade
resultado = anomalia OR criticidade
```
- Analisa 40 características complexas
- Detecta tendências temporais
- Identifica correlações entre sensores
- Reconhece padrões de frequência
- Compara com histórico de falhas

---

## 🔍 Visualizando as 480 Análises

```
Linha do tempo (500 registros de 1 segundo cada):

0    10   20   30   40   50   60   70   80   90   100
|----|----|----|----|----|----|----|----|----|----|
[===================]  ← Janela 0 (0-19): NORMAL
 [===================] ← Janela 1 (1-20): NORMAL
  [===================]← Janela 2 (2-21): CRÍTICO! (temp_trend alto)
   [===================]Janela 3 (3-22): CRÍTICO!
    ...
                        [===================]
                         ← Janela 479 (479-498): NORMAL

Total: 480 janelas analisadas
Críticas: 153 janelas (31.9%)
```

---

## 💡 Por Que Isso é Poderoso?

### **Caso Real:**

**Regra Manual:**
- Alerta quando temperatura > 42°C
- Motor quebra de repente aos 41°C

**IA:**
- Vê temperatura subindo 0.5°C/min há 5 minutos
- Vê vibração aumentando em frequência específica
- Vê umidade caindo (lubrificação evaporando?)
- **Alerta 10 minutos ANTES da falha**
- Tempo para desligar e prevenir dano

---

## 🎯 Configurando a Sensibilidade

Os thresholds controlam o TREINAMENTO, não a detecção:

```python
# Thresholds baixos (conservadores):
temp_max = 38°C
→ IA aprende: "Acima de 38°C é problema grave"
→ Mais alertas (sensível)

# Thresholds altos (tolerantes):
temp_max = 45°C
→ IA aprende: "Só acima de 45°C é grave"
→ Menos alertas (específico)
```

Os 153 alertas (31.9%) com thresholds atuais (42°C, 25-85%, 2.8g) significam:
- IA detectou 153 períodos de 20s com padrões preocupantes
- Mesmo que valores individuais estejam "OK"
- Baseado em combinações, tendências e correlações
