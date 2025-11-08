# Guia de Apresentação – Feira NEXT

Este diretório é sua cola rápida para apresentar o projeto de Monitoramento Inteligente com IA.

## Estrutura
- pitch_5_minutos.md → Roteiro enxuto
- demonstracao_15_minutos.md → Versão completa com passos
- destaques_diferenciais.md → Bullets de valor + FAQ

## Ordem Recomendada (5–15 min)
1. Abertura curta (quem é você + contexto da competição)
2. Problema real (paradas não previstas, manutenção reativa)
3. Solução (pipeline de dados + IA com janelas deslizantes)
4. Demonstração (gerar dados → treinar → dashboard → ajuste)
5. Impacto e métricas (redução risco, precisão, escalabilidade)
6. Diferenciais e próximos passos
7. Encerrar com convite (integração futura / parceria)

## Fluxo Técnico Resumido
Geração (simulação sensores) → Persistência (SQLite) → Feature Engineering (40 por janela) → Modelos (IsolationForest + RandomForest) → Dashboard interativo (Streamlit) → Retraining rápido.

## Números Chave
- 500 leituras → 480 janelas (20s, slide 1)
- 40 features por janela → 19.200 valores analisados
- Taxa crítica atual: ~31.9% (ajustável)

## Três Frases-Chave
1. "Transformamos leitura crua em contexto temporal rico."
2. "A IA enxerga tendências antes de virar falha."
3. "Escala simples: basta conectar novos sensores."

## Checklist Antes da Feira
- Ambiente Python ok (requirements instalados)
- Rodou treino recente? (ml/treino.py)
- Dashboard abre sem erros? (streamlit run dashboard/app.py)
- Thresholds calibrados (ml/thresholds.json)
- Respostas do FAQ memorizadas (ver destaques_diferenciais.md)

## Perguntas Difíceis (Resposta Curta)
- Por que 20s? Equilíbrio entre granularidade e estabilidade.
- Supervisionado ou não? Híbrido (anomaly + classificação).
- Escalabilidade? Substitui SQLite por Postgres/Cloud + fila.
- Segurança? Dados locais; fácil adicionar criptografia/transmissão.

## Encerramento Memorável
"Hoje mostramos prevenção, amanhã agregamos previsão de tempo restante de vida de componentes. Vamos conversar?"