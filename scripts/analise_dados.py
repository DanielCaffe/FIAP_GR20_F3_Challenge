#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de análise de dados dos sensores industriais
Challenge FIAP - Fase 3
Análise de temperatura, umidade e aceleração
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime

# Verifica e instala dependências se necessário
try:
    import seaborn as sns
    sns.set_style("whitegrid")
except ImportError:
    print("Instalando dependências necessárias...")
    import subprocess
    subprocess.check_call(["pip", "install", "seaborn"])
    import seaborn as sns
    sns.set_style("whitegrid")

# Configuração para melhor visualização dos gráficos
plt.rcParams.update({
    'font.family': 'sans-serif',
    'figure.figsize': [12, 8],
    'axes.grid': True,
    'grid.linestyle': '--',
    'grid.alpha': 0.7,
    'lines.linewidth': 2
})

# Lê o arquivo CSV e calcula estatísticas
dados = pd.read_csv('../document/dados_coletados.csv')
stats = dados.describe()

# Cria o diretório assets se não existir
os.makedirs('../assets', exist_ok=True)

# Salva as estatísticas em um arquivo
with open('../document/estatisticas.txt', 'w', encoding='utf-8') as f:
    f.write(f"Analise Estatistica dos Dados - {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    f.write("="*50 + "\n\n")
    f.write("TEMPERATURA (C):\n")
    f.write(f"Media: {stats['temperatura']['mean']:.2f}\n")
    f.write(f"Minima: {stats['temperatura']['min']:.2f}\n")
    f.write(f"Maxima: {stats['temperatura']['max']:.2f}\n")
    f.write(f"Desvio Padrao: {stats['temperatura']['std']:.2f}\n\n")
    
    f.write("UMIDADE (%):\n")
    f.write(f"Media: {stats['umidade']['mean']:.2f}\n")
    f.write(f"Minima: {stats['umidade']['min']:.2f}\n")
    f.write(f"Maxima: {stats['umidade']['max']:.2f}\n")
    f.write(f"Desvio Padrao: {stats['umidade']['std']:.2f}\n\n")
    
    f.write("ACELERACAO (g):\n")
    for eixo in ['acc_x', 'acc_y', 'acc_z']:
        f.write(f"\nEixo {eixo.split('_')[1].upper()}:\n")
        f.write(f"Media: {stats[eixo]['mean']:.3f}\n")
        f.write(f"Minima: {stats[eixo]['min']:.3f}\n")
        f.write(f"Maxima: {stats[eixo]['max']:.3f}\n")
        f.write(f"Desvio Padrao: {stats[eixo]['std']:.3f}\n")

# Gráfico 1: Temperatura e Umidade
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle('Monitoramento Ambiental ao Longo do Tempo', fontsize=14, y=1.05)

# Subplot para Temperatura
temp_line = ax1.plot(dados['tempo'], dados['temperatura'], 'r-', label='Temperatura', linewidth=2)[0]
ax1.fill_between(dados['tempo'], dados['temperatura'], alpha=0.2, color='red')
ax1.set_ylabel('Temperatura (°C)', fontsize=10)
ax1.set_xlabel('Tempo (s)', fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(loc='upper left')

# Adiciona anotações para temperatura
temp_max_idx = dados['temperatura'].idxmax()
ax1.annotate(f'Máx: {dados["temperatura"].max():.1f}°C',
             xy=(dados['tempo'][temp_max_idx], dados['temperatura'][temp_max_idx]),
             xytext=(10, 10), textcoords='offset points',
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
             arrowprops=dict(arrowstyle='->'))

# Subplot para Umidade
humid_line = ax2.plot(dados['tempo'], dados['umidade'], 'b-', label='Umidade', linewidth=2)[0]
ax2.fill_between(dados['tempo'], dados['umidade'], alpha=0.2, color='blue')
ax2.set_ylabel('Umidade (%)', fontsize=10)
ax2.set_xlabel('Tempo (s)', fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(loc='upper right')

# Adiciona anotações para umidade
humid_min_idx = dados['umidade'].idxmin()
ax2.annotate(f'Mín: {dados["umidade"].min():.1f}%',
             xy=(dados['tempo'][humid_min_idx], dados['umidade'][humid_min_idx]),
             xytext=(10, -10), textcoords='offset points',
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
             arrowprops=dict(arrowstyle='->'))

plt.tight_layout()
plt.savefig('../assets/temperatura_umidade.png')
plt.close()

# Gráfico 2: Aceleração nos três eixos
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(dados['tempo'], dados['acc_x'], 'r-', label='Eixo X', linewidth=2, alpha=0.7)
ax.plot(dados['tempo'], dados['acc_y'], 'g-', label='Eixo Y', linewidth=2, alpha=0.7)
ax.plot(dados['tempo'], dados['acc_z'], 'b-', label='Eixo Z', linewidth=2, alpha=0.7)

# Adiciona área sombreada para mostrar a variação
ax.fill_between(dados['tempo'], dados['acc_z'] - dados['acc_z'].std(),
                dados['acc_z'] + dados['acc_z'].std(), color='blue', alpha=0.1)

ax.set_title('Aceleração nos Três Eixos ao Longo do Tempo', y=1.05, fontsize=14)
ax.set_xlabel('Tempo (s)', fontsize=10)
ax.set_ylabel('Aceleração (g)', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='center right', bbox_to_anchor=(1.15, 0.5))

# Adiciona anotações para valores significativos
max_z_idx = dados['acc_z'].abs().idxmax()
ax.annotate(f'Pico Z: {dados["acc_z"][max_z_idx]:.2f}g',
            xy=(dados['tempo'][max_z_idx], dados['acc_z'][max_z_idx]),
            xytext=(10, 10), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->'))

plt.tight_layout()
plt.savefig('../assets/aceleracao.png', bbox_inches='tight', dpi=300)
plt.close()

print("\nAnálise concluída! Arquivos gerados:")
print("1. Gráficos salvos em 'assets/':")
print("   - temperatura_umidade.png")
print("   - aceleracao.png")
print("2. Relatório estatístico em 'document/estatisticas.txt'")
