# 🚀 Guia Rápido - Iniciar Projeto

## Comandos na Ordem

### 1️⃣ Gerar Dados Simulados
```powershell
cd B:\Games\challenge\FIAP_GR20_F3_Challenge
python scripts\gerar_dados.py
```

### 2️⃣ Popular Banco de Dados
```powershell
# Criar schema
& "B:\ENRICO\sql\sqlite-tools-win-x64-3500400\sqlite3.exe" database/factory.db ".read database/script.sql"

# Importar CSVs para staging
& "B:\ENRICO\sql\sqlite-tools-win-x64-3500400\sqlite3.exe" database/factory.db ".mode csv" ".import --skip 1 document/dataset_env.csv STG_ENV" ".import --skip 1 document/dataset_imu.csv STG_IMU"

# Carregar dados nas tabelas finais
& "B:\ENRICO\sql\sqlite-tools-win-x64-3500400\sqlite3.exe" database/factory.db ".read database/load_from_staging.sql"
```

### 3️⃣ Treinar Modelo de IA
```powershell
python ml\treino.py
```

### 4️⃣ Iniciar Dashboard
```powershell
cd dashboard
streamlit run app.py
```

**URL do Dashboard:** http://localhost:8501

---

## ⚠️ Resetar Banco (Se Necessário)

Se precisar recomeçar do zero:

```powershell
cd B:\Games\challenge\FIAP_GR20_F3_Challenge
Remove-Item database\factory.db -Force
```

Depois rode os passos 1, 2, 3, 4 novamente.

---

## 🎯 Ajustar Thresholds

Na barra lateral do Streamlit:
- **Temperatura crítica**: Padrão 42°C
- **Umidade mínima**: Padrão 25%
- **Umidade máxima**: Padrão 85%
- **Aceleração crítica**: Padrão 2.8g

Depois de ajustar, clique em **🔄 Retreinar IA** para aplicar.

---

## 📊 Estrutura do Projeto

```
FIAP_GR20_F3_Challenge/
├── scripts/          # Geração de dados simulados
├── database/         # Schema SQL e banco SQLite
├── ml/              # Treinamento da IA
├── dashboard/       # Interface Streamlit
├── document/        # CSVs e documentação
└── guia_apresentacao/ # Materiais para feira NEXT
```

---

## 🔧 Troubleshooting

### Dashboard não carrega dados
- Verificar se `database/factory.db` existe
- Rodar passo 2 (popular banco)

### IA não funciona
- Verificar se `ml/modelo_treinado.pkl` existe
- Rodar passo 3 (treinar modelo)

### Gráficos não aparecem
- Recarregar página (F5)
- Verificar se Streamlit está rodando

---

## 💡 Para Apresentação

Use os materiais em `guia_apresentacao/`:
- `pitch_5_minutos.md` → Roteiro rápido
- `demonstracao_15_minutos.md` → Demo completa
- `destaques_diferenciais.md` → FAQ e métricas

**Boa sorte na feira NEXT! 🎓🏆**
