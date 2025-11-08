# Pitch 5 Minutos

Tempo sugerido por bloco:

0:00–0:30 – Abertura
0:30–1:30 – Problema
1:30–2:30 – Solução
2:30–3:30 – Como Funciona (Simplificado)
3:30–4:30 – Impacto e Diferenciais
4:30–5:00 – Fechamento / Call to Action

---
## 0:00–0:30 Abertura
"Sou [Seu Nome], finalista entre os 10 melhores. Trouxe uma plataforma de manutenção preditiva acessível para ambientes industriais e educacionais."

## 0:30–1:30 Problema
- Indústria sofre com paradas inesperadas.
- Monitoramento manual é reativo e limitado.
- Pequenas tendências passam despercebidas.
"Perder o momento certo de intervir custa tempo, dinheiro e credibilidade."

## 1:30–2:30 Solução
"Transformamos dados brutos de sensores em alerta inteligente antes da falha." 
Componentes:
- Simulador / ou produção real
- Banco local (SQLite) fácil de trocar
- IA híbrida: isolamentos + classificação
- Dashboard interativo com retraining

## 2:30–3:30 Como Funciona
"Usamos janelas deslizantes de 20 segundos para dar contexto temporal." 
- 500 leituras → 480 análises.
- 40 features por janela (estatística + dinâmica).
- IsolationForest detecta padrões estranhos.
- RandomForest classifica o risco.

## 3:30–4:30 Impacto e Diferenciais
- Antecipação: alerta com base em tendência, não só valor extremo.
- Ajustável: thresholds direto na interface.
- Escalável: trocar SQLite por nuvem é trivial.
- Interpretação: feature importance disponível.
"Aumento de 38x na informação tratada em relação a regras simples."

## 4:30–5:00 Fechamento
"Começamos reduzindo risco imediato. Próximo passo: estimativa de vida útil restante. Quer testar isso no seu laboratório ou operação? Vamos conversar."

---
## Frases de Impacto
- "Vemos o filme, não a foto do sensor."
- "Prevenir antes da anomalia virar falha."
- "Plugável e expansível desde o primeiro dia."

## Se Alguém Interromper
Pergunta sobre algoritmo? → "Híbrido: unsupervised para achar padrões novos e supervised para classificar risco."
Pergunta sobre escalabilidade? → "A arquitetura é modular: substitui storage e adiciona fila de eventos sem refazer lógica."

## Mini Demo (Opcional 1 minuto)
1. Mostrar dashboard carregado.
2. Ajustar threshold e clicar retraining.
3. Exibir mudança na taxa crítica.

## Call to Action Final
"Teste rápido em ambiente real em menos de 1 hora. Topa?"