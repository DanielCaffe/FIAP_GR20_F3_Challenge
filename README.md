# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto
Plataforma SaaS de Manutenção Preditiva com Cooperação Industrial Inteligente
## Nome do grupo
Graduação - 1TIAOB - 2025/1 - Grupo 20 
## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 1</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 2</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 3</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 4</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 5</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Tutor</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Coordenador</a>


## 📜 Descrição

PROPOSTA TÉCNICA ENTERPRISE CHALLENGE – Sprint 1 - Reply
Em pesquisa realizada em artigos científicos recentes que abordam os principais desafios da manutenção preditiva no setor automotivo, especialmente aqueles que ainda carecem de soluções definitivas, realizamos uma análise dos artigos abaixo com foco em identificar os principais desafios na análise preditiva de manutenção de equipamentos industriais, especialmente com aplicação no setor automotivo, mas também válidos para setores industriais em geral.
________________________________________
Fontes:
Artigo 1:
Predictive maintenance enabled by machine learning: Use cases and challenges in the automotive industry - ScienceDirect
Artigo 2:
https://arxiv.org/abs/2401.07871
Artigo 3:
https://arxiv.org/abs/2301.12467
Artigo 4:
https://www.researchgate.net/publication/357557268_Predictive_Maintenance_in_the_Automotive_Sector_A_Literature_Review
Artigo 5:
https://www.sciencedirect.com/science/article/pii/S1755581722001742

Análise Comparativa dos Artigos Científicos
1. Falta de Dados de Qualidade e em Quantidade
Fontes: Artigos 1, 2, 4, 5
•	Dificuldade em coletar dados rotulados suficientes para treinar modelos eficazes (dados com falhas conhecidas).
•	Dados de sensores frequentemente são ruidosos, incompletos ou não padronizados.
•	Pouca disponibilidade de dados públicos devido à confidencialidade industrial.
•	A maioria dos modelos exige grandes volumes de dados históricos, que muitas empresas não têm.
 “A escassez de dados rotulados é uma barreira crítica para treinar modelos supervisionados eficazes em manutenção preditiva.” (Art. 1)

Soluções Inovadoras:
•	Aprendizado por Transferência (Transfer Learning): Utiliza modelos pré-treinados em máquinas similares, adaptando-os com poucos dados adicionais. Isso reduz a necessidade de grandes volumes de dados específicos. 
•	Inteligência Artificial Generativa (GANs): Gera dados sintéticos de falhas para complementar conjuntos de dados reais, melhorando a robustez dos modelos preditivos. 
•	Aprendizado Federado: Permite o treinamento de modelos em dispositivos locais, preservando a privacidade dos dados e facilitando a colaboração entre diferentes instalações industriais.
________________________________________
 2. Falta de Interpretação e Transparência (Explainability)
Fontes: Artigo 2
•	Modelos complexos como redes neurais profundas (deep learning) são frequentemente caixas-pretas, dificultando a compreensão por parte dos técnicos.
•	Engenheiros e técnicos relutam em adotar soluções cujas decisões não são compreensíveis.
•	Falta de ferramentas de explicação que traduzam previsões em ações claras.
 “A confiança dos operadores em modelos preditivos depende da capacidade de explicar as causas de possíveis falhas.” (Art. 2)

Soluções Inovadoras:
•	Inteligência Artificial Explicável (XAI): Aplica técnicas que tornam as decisões dos modelos mais transparentes, facilitando a confiança e adoção por parte dos operadores. 
•	Visualizações Interativas: Desenvolvimento de dashboards que explicam visualmente as previsões dos modelos, auxiliando na tomada de decisões.
________________________________________
 3. Generalização e Adaptação a Novas Condições (Aprendizado Contínuo)
Fontes: Artigos 3 e 5
•	Modelos treinados com dados antigos podem perdem precisão quando aplicados a novas condições operacionais.
•	Ambientes industriais são dinâmicos: peças trocam, sensores mudam, condições operacionais variam.
•	A maioria dos modelos não se adapta automaticamente (aprendizado contínuo ainda é incipiente).
 “Manter modelos atualizados sem treinamento constante manual é um desafio técnico e operacional significativo.” (Art. 3)

Soluções Inovadoras:
•	Aprendizado Contínuo (Continual Learning): Modelos que se atualizam continuamente com novos dados, adaptando-se a mudanças no ambiente operacional.
•	Gêmeos Digitais (Digital Twins): Criação de réplicas virtuais dos equipamentos que simulam diferentes cenários operacionais, permitindo ajustes proativos nos modelos preditivos. 
________________________________________
 4. Complexidade e Multidimensionalidade dos Dados Industriais
Fontes: Artigo 4
•	Equipamentos industriais geram dados de múltiplos sensores, gerando séries temporais complexas e de difícil análise.
•	Dificuldade em identificar relações entre variáveis e em detectar falhas sutis.
•	Necessidade de ferramentas robustas de análise de séries temporais e extração de padrões.
 “A análise de sinais multivariados e o cruzamento de múltiplas fontes de dados são entraves ainda pouco resolvidos.” (Art. 4)

Soluções Inovadoras:
•	Modelos de Autoencoders: Utilização de redes neurais que aprendem representações compactas dos dados, facilitando a detecção de anomalias em conjuntos de dados multivariados.
•	Análise de Componentes Principais (PCA) Dinâmica: Aplicação de técnicas que reduzem a dimensionalidade dos dados em tempo real, destacando variáveis mais relevantes para a manutenção preditiva.
________________________________________
 5. Processamento em Tempo Real e Custo Computacional
Fontes: Artigo 5
•	Muitas aplicações industriais exigem respostas em tempo real para prevenir falhas iminentes o que pode sobrecarregar os sistemas, especialmente em ambientes com recursos computacionais limitados.
•	Modelos preditivos com alto custo computacional dificultam implementação em tempo real, principalmente em borda (edge computing).
•	Sensores IoT exigem algoritmos leves para análise local.
 “Existe um trade-off entre precisão e custo computacional que ainda não foi equilibrado em muitos sistemas industriais.” (Art. 5)

Soluções Inovadoras:
•	Computação de Borda (Edge Computing): Processamento de dados próximo à fonte (sensores), reduzindo a latência e a carga sobre os servidores centrais.
•	Modelos de Machine Learning Otimizados: Desenvolvimento de algoritmos leves e eficientes, adequados para execução em dispositivos com capacidade computacional limitada.
________________________________________
 Resumo dos Principais Desafios da Manutenção Preditiva Industrial
Desafio	Descrição resumida
 Escassez de dados rotulados	Falta de histórico confiável de falhas reais.
 Modelos pouco interpretáveis	Dificuldade de explicar decisões para técnicos.
 Incapacidade de se adaptar a mudanças operacionais	Modelos fixos não funcionam bem com mudanças no ambiente.
 Complexidade dos dados multivariados e não lineares	Difícil identificar padrões em sinais cruzados e variáveis correlatas.
 Limitações de processamento em tempo real e custo computacional	Difícil aplicar modelos pesados em dispositivos de campo.

Entre os desafios apresentados, desenvolveremos nosso projeto considerando o tópico 1:

1. Falta de Dados de Qualidade e em Quantidade
Fontes: Artigos 1, 2, 4, 5
•	Dificuldade em coletar dados rotulados suficientes para treinar modelos eficazes (dados com falhas conhecidas).
•	Dados de sensores frequentemente são ruidosos, incompletos ou não padronizados.
•	Pouca disponibilidade de dados públicos devido à confidencialidade industrial.
•	A maioria dos modelos exige grandes volumes de dados históricos, que muitas empresas não têm.
 “A escassez de dados rotulados é uma barreira crítica para treinar modelos supervisionados eficazes em manutenção preditiva.” (Art. 1)

A solução inovadora será elaborar um sistema onde as indústrias irão reportar seus dados de forma confidencial os quais serão utilizados para aumentar o volume de dados rotulados por sua vez as indústrias recebem relatórios para que possam gerir a análise preditiva de manutenção de equipamentos industriais. O sistema será a exemplo de empresas como Nielsen, IQVIA, Scanntech.

 Proposta Técnica – Etapa 1
Título do Projeto: Plataforma SaaS de Manutenção Preditiva com Cooperação Industrial Inteligente
________________________________________
 Justificativa do Problema
Indústrias enfrentam falhas inesperadas em equipamentos críticos, resultando em paradas não planejadas, prejuízos produtivos e altos custos. Porém, a falta de dados rotulados de qualidade é o principal obstáculo para adoção de soluções com inteligência artificial.
Artigos citados destacam:
•	Dificuldade de coleta e padronização de dados.
•	Escassez de eventos de falha rotulados.
•	Baixa disponibilidade de datasets abertos.
•	Necessidade de grandes volumes de dados históricos para ML eficaz.
________________________________________
 Solução Proposta
Desenvolver uma plataforma SaaS confidencial e colaborativa, onde indústrias fornecem dados dos sensores em tempo real de forma segura e anônima. Em troca, recebem relatórios de manutenção preditiva e insights.
Essa abordagem:
•	Ajuda a superar a escassez de dados rotulados.
•	Aumenta o poder preditivo dos modelos.
•	Democratiza o acesso a soluções inteligentes para pequenas e médias indústrias.
Inspiração: Modelos de negócios como Nielsen, IQVIA e Scanntech.
________________________________________
 
Tecnologias e Ferramentas
Componente	Tecnologia Sugerida
Linguagem Principal	Python, R
Análise de Dados	Pandas, Scikit-learn, Keras, TensorFlow
IoT e Sensores	ESP32 (Wi-Fi integrado)
Banco de Dados	PostgreSQL (RDS AWS)
Armazenamento Nuvem	AWS S3
Processamento	AWS EC2, ou local (etapa simulada)
Backend/API	FastAPI (Python)
Dashboard	Streamlit, Dash ou Power BI
Alertas	AWS SNS, email (SMTP), Firebase Push
Documentação/Versionamento	GitHub (privado)
________________________________________
 Pipeline de Dados (esboço)
1.	Coleta (simulada e/ou ESP32):
o	Dados gerados em tempo real (temperatura, vibração, rotação).
o	Formato JSON enviado por MQTT/HTTP para API.
2.	Ingestão e Armazenamento:
o	API (FastAPI) processa e envia dados ao banco PostgreSQL e ao S3.
3.	Pré-processamento:
o	Remoção de ruídos, interpolação de dados ausentes.
4.	Modelagem Preditiva:
o	Modelos treinados com dados agregados e rotulados (classificação, LSTM, Random Forest).
5.	Dashboard e Alertas:
o	Interface web exibe status dos equipamentos e previsões.
o	Alertas automáticos enviados aos responsáveis.
6.	Relatórios Automáticos:
o	Geração periódica de PDFs com insights e recomendações.
________________________________________
 Estratégia de Coleta de Dados
•	Simulada (etapa atual): Geração via scripts Python com variabilidade controlada.
•	Planejada (futura): Dispositivos ESP32 enviando dados reais de sensores instalados (temperatura, vibração, ruído).
________________________________________
 Integração com IA
•	Modelos serão treinados com:
o	Dados sintéticos + reais anonimizados.
o	Métodos supervisionados e semi-supervisionados.
•	Técnicas como:
o	Random Forest, LSTM (Keras), Isolation Forest (anomaly detection).
o	Data augmentation para suprir a escassez de rótulos.
•	Futuro uso de aprendizado federado, garantindo privacidade.

ARQUITETURA DA SOLUÇÃO:

 ![Diagrama Arquitetura Saas](https://github.com/user-attachments/assets/c748f3e6-4366-4892-bd0a-3bec09ba42cf)




## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

*Acrescentar as informações necessárias sobre pré-requisitos (IDEs, serviços, bibliotecas etc.) e instalação básica do projeto, descrevendo eventuais versões utilizadas. Colocar um passo a passo de como o leitor pode baixar o seu código e executá-lo a partir de sua máquina ou seu repositório. Considere a explicação organizada em fase.*


## 🗃 Histórico de lançamentos

* 0.5.0 - XX/XX/2024
    * 
* 0.4.0 - XX/XX/2024
    * 
* 0.3.0 - XX/XX/2024
    * 
* 0.2.0 - XX/XX/2024
    * 
* 0.1.0 - XX/XX/2024
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


