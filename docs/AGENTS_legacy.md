# Jules Swarm & Research Agents

## O que é o Jules?
**Jules** é um *AI Coding Agent* do Google que opera em uma Máquina Virtual (VM) na nuvem. Ele funciona como um "desenvolvedor par" remoto e autônomo, capaz de receber tarefas, executar código e criar Pull Requests.

### O que ele NÃO é:
- Não é um agente rodando localmente na sua máquina (como o `agent_os` do VIVI).
- Não consome recursos da sua máquina local.
- Não é um componente do produto VIVI OS; é uma **ferramenta de produtividade** para o time de desenvolvimento.

---

## O que é este diretório (`scripts/research/`)?
Este diretório contém a infraestrutura do **"Jules Swarm"** (Enxame de Jules). O objetivo é **paralelizar tarefas repetitivas ou de longa duração**.

> **Conceito de Swarm:** Em vez de pedir para o agente fazer 10 tarefas sequencialmente, usamos scripts para "disparar" 10 instâncias do Jules ao mesmo tempo, cada uma cuidando de uma micro-tarefa.

### Funcionalidades Principais:
1.  **Research Pipeline**: Scripts como `launch_paper_analysis.py` usam o Swarm para ler papers (PDFs), analisar o código do VIVI e propor integrações.
2.  **Merge Train**: O script `jules-swarm/merge_train.sh` automatiza a revisão e merge dos Pull Requests gerados pelos agentes.

---

## ⚠️ Nota sobre Atomic Design (Legado)
Você encontrará pastas e scripts referenciando **Atomic Design** (`atoms`, `molecules`, `organisms`) e Storybook dentro de `jules-swarm/`.

> **CONTEXTO IMPORTANTE:**
> Esses scripts foram importados de um **projeto anterior** focado em design system/storybook.
> *   **Status**: As tarefas de UI/Atomic Design presentes aqui são **herança** desse projeto antigo.
> *   **Relevância**: Não considere essas tarefas como parte do roadmap oficial do VIVI OS, a menos que explicitamente reativadas.
> *   **Reuso**: O que estamos aproveitando é a **infraestrutura do Swarm** (o mecanismo de delegação), não necessariamente o conteúdo das tarefas de UI antigas.

---

## Como Usar

### 1. Iniciar Análise de Papers
Para delegar a leitura de novos papers adicionados ao backlog:
```bash
python scripts/research/launch_paper_analysis.py
```

### 2. Processar Entregas (Merge Train)
Para verificar se os agentes terminaram e integrar o código (PRs):
```bash
bash scripts/research/jules-swarm/merge_train.sh
```
