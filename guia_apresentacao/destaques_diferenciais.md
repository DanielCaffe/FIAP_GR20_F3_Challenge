# Destaques e Diferenciais

## Valor para Negócio
- Redução de risco operacional com alertas antecipados.
- Tempo de setup curto: roda localmente com dados simulados ou reais.
- Custo baixo: stack open-source, escalável depois.

## Diferenciais Técnicos
- Janelas deslizantes (20s, slide 1) → contexto temporal real.
- Pipeline híbrido: IsolationForest + RandomForest.
- Treinamento e thresholds ajustáveis via dashboard.
- Serialização por componentes (scaler, detector, classifier) → robusta.
- 40 features por janela (estatística + frequência + tendência).

## Métricas & Números
- 500 leituras → 480 janelas → 19.200 valores analisados.
- Taxa crítica atual: ~31.9% (ajustável).
- Treinamento em ~30s local (depende da máquina).

## Arquitetura (Resumo)
- Fonte de dados: CSV/SQLite (plugável para Postgres/Cloud).
- Processamento: pandas/numpy/scikit-learn.
- App: Streamlit com retraining e visualização.

## Comparativo (Regras Simples x IA)
- Regras: valores isolados; não veem tendência/correlação.
- IA: contexto de 20s; detecta aquecimento progressivo e vibração periódica.
- +38x mais informação processada por janela.

## Segurança & Escalabilidade
- Dados locais por padrão; fácil migrar p/ nuvem segura.
- Suporte a fila/eventos para streaming (ex.: Kafka/RabbitMQ).
- Modelo servido via joblib → container/endpoint REST.

## FAQ Curto
- Por que 20 segundos? Equilíbrio entre ruído e contexto; validado na literatura.
- Onde estão os limiares? `ml/thresholds.json`; persistidos entre sessões.
- Como retrain? Botão no dashboard chama `ml/treino.py` e recarrega.
- Explicabilidade? Importância de features disponível; roadmap: SHAP.
- E sensores novos? Adicionar colunas e mapear no extrator de features.

## Próximos Passos
- Estimar RUL (Remaining Useful Life).
- Conectar a um broker e banco gerenciado.
- Painel de explicabilidade por janela.

## Fechamento Curto
"Contexto temporal + IA acessível = prevenção real, agora."