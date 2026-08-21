# LAB-04 — Dashboard da Pesquisa sobre IA e Qualidade de Código Python

## Contexto
Este repositório foi criado como repositório de apresentação e publicação do dashboard da pesquisa, não como o repositório principal da investigação. A pesquisa foi conduzida em outro repositório e em outra disciplina, e este espaço serve apenas para disponibilizar a visualização dos resultados.

**Disciplina de origem da pesquisa:** Trabalho Interdisciplinar: Pesquisa em Engenharia de Software  
**Disciplina deste repositório:** Laboratório de Experimentação de Software  
**Curso:** Engenharia de Software — PUC Minas  

---

## Visão Geral

Este projeto apresenta os resultados de uma investigação sobre o impacto de commits com evidência de assistência por IA na qualidade estática de código Python em repositórios públicos do GitHub. A análise compara o estado do código antes e depois da alteração associada a commits com uso de IA, avaliando indicadores como densidade de problemas, complexidade estrutural e carga de manutenção.

A pesquisa foi conduzida em um repositório específico do estudo, e este repositório tem como finalidade centralizar a visualização dos dados em um dashboard interativo, facilitando a exploração e a divulgação dos resultados.

---

## Dashboard

O dashboard interativo com os resultados da pesquisa está disponível em:

- [Dashboard no GitHub Pages](https://paulorubinger.github.io/LAB-04/)

---

## Objetivo da Pesquisa

Investigar se commits assistidos por IA estão associados a variações relevantes na qualidade estática do código, considerando aspectos como:

- densidade de problemas de qualidade;
- complexidade estrutural;
- carga de manutenção e dívida técnica;
- evolução de métricas antes e depois dos commits.

---

## Perguntas de Pesquisa

### Q1 — Variação na densidade de problemas de qualidade estática

Qual é a variação na densidade de problemas de qualidade estática em arquivos impactados por commits assistidos por IA?

### Q2 — Variação na complexidade estrutural

Qual é a variação na complexidade estrutural de arquivos impactados por commits assistidos por IA?

### Q3 — Variação na carga de manutenção

Qual é a variação na carga de manutenção em arquivos impactados por commits assistidos por IA?

---

## Dataset e Metodologia

A pesquisa utilizou uma amostra composta por:

- 728 repositórios populares do GitHub;
- 6.238 commits com evidência de assistência por IA;
- 30.252 arquivos impactados por esses commits;
- comparação entre cenários pré-commit e pós-commit.

A metodologia incluiu:

- coleta de métricas de qualidade estática;
- identificação de commits com indícios de uso de IA;
- análise comparativa do código em momentos distintos do ciclo de desenvolvimento;
- normalização das métricas por KLOC para permitir comparação entre repositórios e arquivos de tamanhos distintos.

As principais métricas avaliadas incluem indicadores de qualidade estática, complexidade e manutenção, com foco em variações por KLOC e no comportamento entre os estados analisados.

---

## Estrutura do Repositório

- `index.html` — dashboard interativo público em HTML/JavaScript;
- `prepare_dashboard_data.py` — script responsável por consolidar e preparar os dados para análise e visualização;
- `data/` — arquivos consolidados em CSV utilizados no dashboard;
- `repo_ti6/` — artefatos do projeto, dados processados, scripts e resultados da investigação.

---

## Como os Dados Foram Organizados

Os dados foram preparados em tabelas consolidadas para suporte ao dashboard, incluindo:

- métricas consolidadas;
- repositórios analisados;
- evidências de IA;
- principais KPIs do estudo.

Essa organização permite visualizar a caracterização do dataset e as respostas às questões de pesquisa de forma integrada.

---

## Observações Finais

Este repositório representa a documentação e a apresentação visual do estudo concluído sobre o impacto da IA na qualidade de código Python. O foco principal é apresentar a análise de forma acessível e exploratória, conectando os dados coletados ao contexto de qualidade estática e manutenção de software.

---

## Material de Apoio

- [GitHub Pages do dashboard](https://paulorubinger.github.io/LAB-04/)
- [SonarQube](https://www.sonarsource.com/products/sonarqube/)
