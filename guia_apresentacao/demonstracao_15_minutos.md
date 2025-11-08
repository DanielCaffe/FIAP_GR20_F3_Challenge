# Demonstração Completa (15 Minutos)

Roteiro com marcação de tempo e objetivos.

## Visão Geral do Flow
Sensores (simulados) → Coleta CSV → Load SQLite → Feature Engineering (janelas) → Modelos (IsolationForest + RandomForest) → Dashboard (Streamlit) → Ajuste & Retraining → Resultados & Roadmap.

---
## Cronograma

0:00–1:00 Abertura / Contexto
"Projeto finalista. Foco: transformar dados em prevenção inteligente acessível."

1:00–3:00 Problema
- Paradas não planejadas → custo alto.
- Monitoramento tradicional: limites fixos → não detecta tendência.
- Exemplos: temperatura subindo lentamente, vibração oscilando.
"Queremos agir antes de cruzar o limite." 

3:00–6:00 Arquitetura
Mostrar diagrama simples:
- scripts/gerar_dados.py (simulação)
- database/script.sql / load_from_staging.sql
- ml/treino.py (feature engineering + treino)
- dashboard/app.py (visualização + interação)

Pontos:
- Modularidade (trocar storage / sensores facilmente)
- Componentes do modelo salvos separadamente (robustez)

6:00–9:00 IA (Como Funciona)
"Janelas deslizantes de 20s, slide 1." 
- 500 → 480 janelas → 40 features cada
- 19.200 pontos tratados
Features: média, desvio, RMS, pico frequência, frequência média, tendência, kurtosis, skewness.
Modelos:
- IsolationForest: sinaliza comportamento raro
- RandomForest: classifica criticidade
Mostrar importância de features (ex: trend, freq_peak dominando).

9:00–11:00 Demo Prática
Passos:
1. Abrir dashboard.
2. Mostrar métricas atuais.
3. Ajustar threshold (ex: diminuir temp_max para simular sensibilidade).
4. Clicar retraining → explicar diferença (reprocessa janelas com novos rótulos).
5. Mostrar mudança % de janelas críticas.
6. Destacar velocidade (menos de 1 min) e repetibilidade.

11:00–13:00 Diferenciais
Tabela verbal:
- Regras fixas vs IA contextual.
- Monitoramento estático vs adaptável.
- Detecção pós-evento vs prevenção antecipada.
Escalabilidade:
- Substituir SQLite por Postgres / API.
- Adicionar fila (Kafka/Rabbit) para streaming.
- Model serving: joblib → container / endpoint.
Roadmap curto:
- Previsão de tempo restante (RUL)
- Dash de explicabilidade (SHAP)
- Modo aprendizado contínuo.

13:00–14:00 Perguntas & FAQ Rápido
Simulação vs real? → "Estrutura idêntica, troca origem do dado."
Por que dois modelos? → "Combinação robusta para desconhecido + conhecido."
Manutenção? → "Retraining simples, thresholds versionados."
E se aumentar sensores? → "Escalamos features por grupo; pipeline genérico."

14:00–15:00 Fechamento
"Mostramos que contexto temporal + IA acessível previnem falhas. Próxima etapa: pilotar em ambiente real. Vamos avançar juntos?"

---
## Materiais para Mostrar na Tela
- Diagrama (src/diagram.json ou desenhar no slide)
- Exemplo de janela (lista de 20 valores + features calculadas)
- Print importância de features.
- Dashboard antes/depois de retraining.

## Erros Comuns e Como Evitar
- Ficar preso em detalhes matemáticos → manter foco em benefício.
- Falar muito de implementação antes de mostrar valor → inverter ordem.
- Não mencionar escalabilidade → sempre citar modularidade.

## Frases de Alto Impacto
- "Capturamos comportamento emergente antes de virar falha."
- "Transformamos 500 leituras em 19 mil pontos de decisão."
- "Treinar novamente leva segundos, não dias."

## Plano B (Se Demo Travar)
- Abrir print estático de tela final.
- Explicar verbalmente ajuste de threshold.
- Concluir com gráfico já renderizado.

## Mini Check de Respiração
Se estiver acelerado: pausa 2s após cada bloco. Visualizar próxima transição.

## Encerramento Final
"Obrigado pelo tempo. Se quiser ver isso rodando com seus sensores reais, tenho um roteiro de integração pronto."