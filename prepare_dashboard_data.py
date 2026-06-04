#!/usr/bin/env python3
"""
Script para preparar dados consolidados para o Dashboard BI (LAB04)
Este script combina dados Pré-Commit e Pós-Commit em um formato único
pronto para importação no Power BI, Tableau ou Google Data Studio.
"""

import pandas as pd
import json
import os
from pathlib import Path

# Caminhos dos dados
BASE_PATH = Path("/Users/paulorubinger/Documents/GitHub/lab-exp-software/LAB-04")
EXPERIMENTO_FINAL_PATH = BASE_PATH / "repo_ti6/plf-es-2026-1-ti6-8508100-ti6grupo4/Instrumentos/Codigos/results/experimento_final/lotes"
DATA_PATH = BASE_PATH / "repo_ti6/plf-es-2026-1-ti6-8508100-ti6grupo4/Instrumentos/Codigos/data/processed"
OUTPUT_PATH = BASE_PATH / "dashboard_data"

# Criar diretório de output
OUTPUT_PATH.mkdir(exist_ok=True)

print("=" * 80)
print("PREPARANDO DADOS PARA DASHBOARD BI - LAB04")
print("EXPERIMENTO FINAL (728 Repositórios em 10 Lotes)")
print("=" * 80)

# ============================================================================
# 1. CARREGAR DADOS DE MÉTRICAS CONSOLIDADAS
# ============================================================================
print("\n[1/4] Carregando dados de métricas consolidadas...")

# Consolidar dados de todos os 10 lotes
pre_totals = {}
post_totals = {}

for lote in range(1, 11):
    lote_dir = EXPERIMENTO_FINAL_PATH / f"lote_{lote:02d}/metrics"
    
    # Pré-comparable
    pre_file = lote_dir / "pre_comparable/consolidated_measures.csv"
    if pre_file.exists():
        df_pre = pd.read_csv(pre_file)
        for _, row in df_pre.iterrows():
            metric = row['metric']
            value = row['value']
            if metric not in pre_totals:
                pre_totals[metric] = 0
            if not metric.endswith('_per_kloc'):  # Não somar métricas normalizadas
                pre_totals[metric] += value
    
    # Pós-comparable
    post_file = lote_dir / "post_comparable/consolidated_measures.csv"
    if post_file.exists():
        df_post = pd.read_csv(post_file)
        for _, row in df_post.iterrows():
            metric = row['metric']
            value = row['value']
            if metric not in post_totals:
                post_totals[metric] = 0
            if not metric.endswith('_per_kloc'):
                post_totals[metric] += value

# Converter para DataFrames e calcular métricas normalizadas
pre_measures = pd.DataFrame([pre_totals])
post_measures = pd.DataFrame([post_totals])

# Calcular métricas normalizadas por KLOC
ncloc_pre = pre_totals.get('ncloc', 1)
ncloc_post = post_totals.get('ncloc', 1)

for metric in pre_totals.keys():
    if metric != 'ncloc' and not metric.endswith('_per_kloc'):
        per_kloc_metric = f"{metric}_per_kloc"
        pre_measures[per_kloc_metric] = (pre_totals[metric] / ncloc_pre * 1000) if ncloc_pre > 0 else 0
        post_measures[per_kloc_metric] = (post_totals[metric] / ncloc_post * 1000) if ncloc_post > 0 else 0

pre_measures["Estado"] = "Pré-Commit"
post_measures["Estado"] = "Pós-Commit"

# Combinar
consolidated_measures = pd.concat([pre_measures, post_measures], ignore_index=True)

print(f"   ✓ Consolidados {10} lotes (Pré-Commit)")
print(f"   ✓ Consolidados {10} lotes (Pós-Commit)")

# ============================================================================
# 2. CARREGAR E PROCESSAR DADOS DE REPOSITÓRIOS
# ============================================================================
print("\n[2/4] Carregando dados de repositórios com evidências de IA...")

# Extrair repositórios dos batch_inventory.json dos lotes e contar commits/arquivos
all_repositories = set()
total_ai_commits = 0
total_ai_files = 0

for lote in range(1, 11):
    lote_dir = EXPERIMENTO_FINAL_PATH / f"lote_{lote:02d}/metrics"
    
    # Ler batch_inventory.json do pré-comparable
    batch_file = lote_dir / "pre_comparable/batch_inventory.json"
    if batch_file.exists():
        try:
            with open(batch_file, 'r') as f:
                batch_data = json.load(f)
                for batch in batch_data.get('batches', []):
                    for repo in batch.get('repositories', []):
                        all_repositories.add(repo)
        except:
            pass
    
    # Ler consolidated_summary.json para contar commits e arquivos
    summary_file = lote_dir / "pre_comparable/consolidated_summary.json"
    if summary_file.exists():
        try:
            with open(summary_file, 'r') as f:
                summary_data = json.load(f)
                scope = summary_data.get('analysis_scope', {})
                total_ai_commits += scope.get('commits', 0)
                total_ai_files += scope.get('files', 0)
        except:
            pass

# Se não conseguir dos lotes, usar o arquivo de AI evidence
if len(all_repositories) == 0:
    repos_df = pd.read_csv(DATA_PATH / "repositories_with_ai_evidence_20260504_173035.csv")
    all_repositories = set(repos_df["full_name"].unique())

# Criar DF de repositórios (formato simplificado)
repos_list = list(all_repositories)
repos_summary = pd.DataFrame({
    "Repositório": repos_list,
    "Estrelas": 0,  # Não temos esses dados nos lotes
    "Commits_com_IA": 1,  # Placeholder
    "Último_Push": ""
})

print(f"   ✓ Total de repositórios únicos: {len(repos_summary)}")
print(f"   ✓ Total de commits com IA: {total_ai_commits}")

# ============================================================================
# 3. EXTRAIR INFORMAÇÕES DE TIPOS DE EVIDÊNCIA
# ============================================================================
print("\n[3/4] Análise de evidências de IA...")

# Carregar dados de commits selecionados
commits_df = pd.read_csv(DATA_PATH / "selected_ai_commits_20260504_173234.csv")

# Contar por tipo de evidência
evidence_counts = commits_df["evidence_type"].value_counts() if "evidence_type" in commits_df.columns else {}

evidence_summary = pd.DataFrame({
    "Tipo_Evidencia": list(evidence_counts.index),
    "Total_Commits": list(evidence_counts.values)
})

# Se houver coluna de tipo, usar para contar os impactados
if "evidence_type" in commits_df.columns:
    print(f"   ✓ Tipos de evidência encontrados:")
    for idx, row in evidence_summary.iterrows():
        print(f"     - {row['Tipo_Evidencia']}: {row['Total_Commits']} commits")

# ============================================================================
# 4. CRIAR TABELA DE CARACTERIZAÇÃO DO DATASET
# ============================================================================
print("\n[4/4] Gerando tabela de caracterização do dataset...")

# Criar KPIs principais
ncloc_post = float(consolidated_measures[consolidated_measures["Estado"] == "Pós-Commit"]["ncloc"].iloc[0])
ncloc_pre = float(consolidated_measures[consolidated_measures["Estado"] == "Pré-Commit"]["ncloc"].iloc[0])

kpis = {
    "Métrica": [
        "Total de Repositórios",
        "Total de Commits com IA",
        "NCLOC Pós-Commit",
        "NCLOC Pré-Commit",
    ],
    "Valor": [
        len(repos_summary),
        total_ai_commits,
        int(ncloc_post),
        int(ncloc_pre),
    ]
}
kpis_df = pd.DataFrame(kpis)

# ============================================================================
# 5. SALVAR DADOS PROCESSADOS
# ============================================================================
print("\n" + "=" * 80)
print("SALVANDO DADOS PARA O POWER BI")
print("=" * 80)

# Salvar tabelas principais
consolidated_measures.to_csv(OUTPUT_PATH / "01_metricas_consolidadas.csv", index=False)
print(f"✓ {OUTPUT_PATH / '01_metricas_consolidadas.csv'}")

repos_summary.to_csv(OUTPUT_PATH / "02_repositorios.csv", index=False)
print(f"✓ {OUTPUT_PATH / '02_repositorios.csv'}")

evidence_summary.to_csv(OUTPUT_PATH / "03_evidencias_ia.csv", index=False)
print(f"✓ {OUTPUT_PATH / '03_evidencias_ia.csv'}")

kpis_df.to_csv(OUTPUT_PATH / "04_kpis_principais.csv", index=False)
print(f"✓ {OUTPUT_PATH / '04_kpis_principais.csv'}")

# ============================================================================
# 6. GERAR RESUMO ESTATÍSTICO
# ============================================================================
print("\n" + "=" * 80)
print("RESUMO ESTATÍSTICO PARA O DASHBOARD")
print("=" * 80)

print("\n📊 MÉTRICAS CONSOLIDADAS (Pós-Commit):")
post_data = consolidated_measures[consolidated_measures["Estado"] == "Pós-Commit"].iloc[0]
print(f"   NCLOC: {float(post_data['ncloc']):,.0f}")
print(f"   Code Smells: {float(post_data['code_smells']):,.0f}")
print(f"   Violações: {float(post_data['violations']):,.0f}")
print(f"   Complexidade Ciclomática/KLOC: {float(post_data['complexity_per_kloc']):.2f}")
print(f"   Complexidade Cognitiva/KLOC: {float(post_data['cognitive_complexity_per_kloc']):.2f}")
print(f"   Dívida Técnica (min/KLOC): {float(post_data['technical_debt_minutes_per_kloc']):.2f}")

print("\n📊 MÉTRICAS CONSOLIDADAS (Pré-Commit):")
pre_data = consolidated_measures[consolidated_measures["Estado"] == "Pré-Commit"].iloc[0]
print(f"   NCLOC: {float(pre_data['ncloc']):,.0f}")
print(f"   Code Smells: {float(pre_data['code_smells']):,.0f}")
print(f"   Violações: {float(pre_data['violations']):,.0f}")
print(f"   Complexidade Ciclomática/KLOC: {float(pre_data['complexity_per_kloc']):.2f}")
print(f"   Complexidade Cognitiva/KLOC: {float(pre_data['cognitive_complexity_per_kloc']):.2f}")
print(f"   Dívida Técnica (min/KLOC): {float(pre_data['technical_debt_minutes_per_kloc']):.2f}")

print("\n📦 REPOSITÓRIOS:")
print(f"   Total: {len(repos_summary)}")
print(f"   Estrelas (média): {repos_summary['Estrelas'].mean():.0f}")
print(f"   Commits com IA (total): {total_ai_commits}")
print(f"   Arquivos com IA (total): {total_ai_files}")

print("\n" + "=" * 80)
print("✅ DADOS PREPARADOS COM SUCESSO!")
print(f"📁 Localização: {OUTPUT_PATH}")
print("=" * 80)
print("\nPróximos passos:")
print("1. Abra o Power BI Desktop")
print("2. Importe os arquivos CSV de: dashboard_data/")
print("3. Crie relacionamentos entre as tabelas")
print("4. Comece a construir as visualizações")
