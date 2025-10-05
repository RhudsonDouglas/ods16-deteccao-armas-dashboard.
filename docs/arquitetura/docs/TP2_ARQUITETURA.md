\documentclass[a4paper,12pt,Times]{article}

% --- PACOTES ESSENCIAIS ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[brazil]{babel}
\usepackage{graphicx}
\usepackage{url}
\usepackage{hyperref}
\usepackage{setspace}
\usepackage[margin=2.5cm]{geometry}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{float}
\usepackage{caption}

% --- METADADOS ---
\newcommand{\tituloDoc}{Engenharia de Software \\ \vspace{0.5cm} Trabalho Prático 2 (TP2): Projeto de Software (Versão com foco em Dados)}
\newcommand{\AutorA}{Rhudson Douglas Mota Sampaio}
\newcommand{\matriculaA}{860221}
\newcommand{\curso}{Ciência de Dados e Inteligência Artificial}
\newcommand{\univ}{Pontifícia Universidade Católica de Minas Gerais}
\newcommand{\keyword}[1]{\textsf{#1}}

\begin{document}

% --- CAPA ---
\begin{titlepage}
    \centering
    % Substitua as imagens abaixo por arquivos válidos ou remova estes blocos
    \begin{minipage}{0.4\textwidth}
        \centering
        \includegraphics[width=0.8\linewidth]{figuras/brasao.jpg}
    \end{minipage}\hfill
    \begin{minipage}{0.5\textwidth}
        \centering
        \includegraphics[width=\linewidth]{figuras/Eng.de Software.png}
    \end{minipage}

    \vspace{2cm}
    {\Huge \univ\par}
    \vspace{1.5cm}
    {\Large \curso\par}
    \vspace{2cm}
    {\huge\bfseries \tituloDoc\par}
    \vspace{3cm}
    {\Large \AutorA\par}
    {\normalsize Matrícula: \matriculaA\par}

    \vfill
    {\large Belo Horizonte\par}
    {\large Outubro de 2025\par}
\end{titlepage}

% --- RESUMO (PT-BR) ---
\begin{abstract}
\noindent
Neste TP2 eu defino e justifico um \textbf{dashboard local no Briefer} que roda no meu computador e consome a base de dados do repositório GitHub do projeto. Eu valido previamente que \textbf{a rede neural não deve rodar dentro do Briefer}; em vez disso, implemento um \textbf{pipeline offline em Python} que gera tabelas e \emph{snapshots} consumidos pelo Briefer. Essa divisão atende ao requisito de não ser apenas frontend e mantém meu foco de \textbf{estudante de Ciência de Dados}: treino/avaliação da rede neural e aplicação de princípios de Engenharia de Software. Eu documento a arquitetura com o \textbf{C4 Model} (Context e Container) e adiciono um \textbf{Component} opcional do pipeline.
\\\textbf{\keyword{Palavras-chave:}} ODS 16; Briefer; Dashboard local; C4 Model; Engenharia de Software; Rede Neural.
\end{abstract}

\newpage
\selectlanguage{english}
\begin{abstract}
\noindent
In this TP2 I define and justify a \textbf{local dashboard in Briefer} running on my computer and consuming the dataset from my GitHub repository. I validate that the \textbf{neural network should not run inside Briefer}; instead, I implement an \textbf{offline Python pipeline} that produces tables and snapshots consumed by Briefer. This split meets the “not frontend-only” requirement and keeps my \textbf{Data Science} focus on model training/evaluation and the application of Software Engineering principles. I document the architecture using the \textbf{C4 Model} (Context and Container), with an optional \textbf{Component} for the pipeline.
\\\textbf{\keyword{Keywords:}} SDG 16; Briefer; Local dashboard; C4 Model; Software Engineering; Neural Network.
\end{abstract}

\selectlanguage{brazilian}
\newpage
\onehalfspace
\setlength{\parindent}{1.25cm}
\tableofcontents
\newpage

% ============================
\section{Introdução e escopo}
No TP1 (\url{https://github.com/RhudsonDouglas/ods16-deteccao-armas-dashboard}) eu defini o problema e o objetivo ligados ao \textbf{ODS 16}: apoiar vigilância responsável por meio de detecção de armas com rede neural e visualização de evidências. Para simplificar a entrega e maximizar meu aprendizado em \textbf{Ciência de Dados}, neste TP2 eu formalizo que a solução final será um \textbf{dashboard local no Briefer}, que consome dados e artefatos gerados por um \textbf{pipeline offline em Python} desenvolvido por mim.

% ============================
\section{Validação prévia: rede neural e aderência à disciplina}
\subsection*{Rede neural no Briefer}
Eu avalio a viabilidade técnica e concluo que o Briefer opera como \textbf{consumidor/visualizador de dados tabulares e imagens} e não como ambiente de execução de modelos de ML. Rodar inferência dentro do frontend traria acoplamento, dependências complexas, exigência de GPU e problemas de reprodutibilidade. Assim, a \textbf{inferência roda fora}, no meu pipeline offline; o Briefer apenas \textbf{lê} os resultados.

\subsection*{Aderência à disciplina}
A disciplina exige que a solução não seja apenas frontend. O meu desenho atende a isso:
\begin{itemize}[leftmargin=1.1cm]
    \item \textbf{Backend local (pipeline em Python):} leitura da base, pré-processamento, inferência (rede neural), pós-processamento e exportação de tabelas/imagens.
    \item \textbf{Frontend local (Briefer):} leitura e visualização dos resultados, filtros, métricas e evidências.
\end{itemize}

% ============================
\section{Tipo de solução e justificativa}
Eu escolho \textbf{Dashboard local (Briefer) + Pipeline offline (Python)} para priorizar:
\begin{enumerate}[leftmargin=1.1cm]
    \item \textbf{Foco em ML:} treino, ajuste e avaliação da rede neural (ex.: YOLO).
    \item \textbf{Engenharia de Software aplicada:} requisitos claros, arquitetura C4, configuração versionada, qualidade de dados, testes e documentação, conforme boas práticas consolidadas \cite{pressman-maxim}.
    \item \textbf{Simplicidade operacional:} tudo roda na minha máquina, sem nuvem, com \textit{time-to-value} rápido.
\end{enumerate}
A documentação arquitetural segue o \textbf{C4 Model} \cite{brown-c4}, iniciando por \textit{Context} e \textit{Container} e detalhando apenas quando agrega valor.

% ============================
\section{Requisitos}
\subsection{Requisitos Funcionais (RF)}
\begin{enumerate}[label=RF\arabic*.,leftmargin=1.1cm]
    \item Importar a base do repositório (ou a saída do pipeline) no ambiente local.
    \item Exibir \textbf{alertas} com filtros por data, fonte, \emph{score} e classe.
    \item Mostrar \textbf{métricas agregadas}: contagens por período/fonte e estatísticas de qualidade (ex.: taxa de FP/FN se houver rótulos).
    \item Exibir \emph{snapshots} e metadados por alerta.
    \item Exportar seleções (\emph{CSV}/PDF simples) para relatórios.
\end{enumerate}

\subsection{Requisitos Não Funcionais (RNF)}
\begin{itemize}[leftmargin=1.1cm]
    \item \textbf{Simplicidade de implantação:} uso local, sem nuvem.
    \item \textbf{Desempenho percebido:} abertura do dashboard em $<5$ s e filtros responsivos.
    \item \textbf{Reprodutibilidade:} \texttt{requirements.txt} + \texttt{config.yaml}.
    \item \textbf{Confiabilidade de dados:} checagem de esquemas/colunas e integridade de arquivos.
    \item \textbf{Privacidade:} dados e imagens permanecem no disco local, com retenção configurável.
\end{itemize}

% ============================
\section{Arquitetura (C4 Model)}
A arquitetura é documentada com o \textbf{C4 Model} \cite{brown-c4}. Para este escopo, \textbf{Context} e \textbf{Container} são suficientes; incluo um \textbf{Component} opcional do pipeline.

\subsection{C4 — Nível 1: \textit{System Context}}
\textbf{Atores e sistemas (locais):}
\begin{itemize}[leftmargin=1.1cm]
    \item \textbf{Usuário (eu):} interajo com o Briefer para explorar os resultados.
    \item \textbf{Sistema em foco:} \emph{ODS16 Dashboard (Local, Briefer)}.
    \item \textbf{Fontes locais:} dataset do GitHub e artefatos do pipeline.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\linewidth]{figuras/c4_context_briefer.png}
    \caption{C4 — Nível 1 (Context): Usuário, Dashboard (Briefer) e dados locais.}
\end{figure}

\subsection{C4 — Nível 2: \textit{Container}}
\textbf{Contêineres (todos locais):}
\begin{enumerate}[leftmargin=1.1cm]
    \item \textbf{Briefer (App local):} carrega tabelas e exibe dashboards e \emph{snapshots}.
    \item \textbf{Pipeline Offline (CLI Python):} loader $\rightarrow$ pré-processamento $\rightarrow$ inferência (rede neural) $\rightarrow$ pós-processamento $\rightarrow$ exportação (CSV/Parquet/SQLite + imagens).
    \item \textbf{Armazenamento Local:} sistema de arquivos e/ou \textbf{SQLite} com tabelas de eventos/alertas e metadados.
\end{enumerate}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\linewidth]{figuras/c4_container_briefer.png}
    \caption{C4 — Nível 2 (Container): Briefer, Pipeline Offline e Armazenamento Local.}
\end{figure}

\subsection{C4 — Nível 3 (Opcional): \textit{Component} do Pipeline Offline}
\textbf{Componentes principais:}
\begin{itemize}[leftmargin=1.1cm]
    \item \textbf{Config Loader:} lê \texttt{config.yaml} (paths, limiares).
    \item \textbf{Data Loader \& Frame Extractor:} lê o dataset e extrai quadros.
    \item \textbf{Detector (NN):} rede neural (ex.: YOLO) com \emph{bounding boxes} e \emph{scores}.
    \item \textbf{Post-Processor:} NMS, filtros por \emph{score}, seleção de \emph{snapshots}.
    \item \textbf{Exporter:} grava \texttt{alerts.parquet}/\texttt{alerts.csv} e imagens.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\linewidth]{figuras/c4_component_etl.png}
    \caption{C4 — Nível 3 (Opcional): Componentes do Pipeline Offline.}
\end{figure}

% ============================
\section{Decisões e racional}
\textbf{Separação frontend/backend local.} O Briefer fica responsável por visualização e interação; o pipeline, por processamento e inferência. Essa separação melhora testabilidade, manutenção, desempenho e segurança \cite{pressman-maxim}.  
\textbf{Documentação enxuta.} Eu uso C4 para comunicar “\textit{overview first}” e detalhar apenas o necessário \cite{brown-c4}.  
\textbf{Qualidade.} Reprodutibilidade com \texttt{requirements.txt} e \texttt{config.yaml}; validação de esquema; testes básicos do pipeline.

% ============================
\section{Plano para o TP3 (backlog objetivo)}
\begin{enumerate}[leftmargin=1.1cm]
    \item Estruturar repositório: \texttt{/pipeline}, \texttt{/data}, \texttt{/briefer}, \texttt{/docs}, \texttt{/figuras}.
    \item Implementar \textbf{pipeline offline}: \texttt{python -m pipeline.run --config config.yaml} gerando \texttt{alerts.parquet}/\texttt{alerts.csv} e \emph{snapshots}.
    \item Integrar a \textbf{rede neural} (ex.: YOLO), definir \emph{thresholds} e NMS.
    \item Montar \textbf{dashboard no Briefer}: páginas \emph{Visão Geral}, \emph{Alertas}, \emph{Evidências}, \emph{Métricas}.
    \item Empacotar: \texttt{requirements.txt}, \texttt{README} com passo a passo (pipeline $\rightarrow$ abrir Briefer $\rightarrow$ importar dados).
    \item Qualidade: checagem de esquemas (colunas obrigatórias), \texttt{pytest} básico para o pipeline.
\end{enumerate}

% ============================
\section{Gerência de configuração}
Uso GitHub para código e documentação; GitHub Projects com \emph{Project Backlog}, \emph{TODO} (TP3), \emph{In Progress} e \emph{Done}; branches curtos por tarefa e \emph{pull requests}. A versão do pipeline é registrada no campo \texttt{pipeline\_version} salvo no \texttt{alerts.parquet}.

% ============================
\section{Conclusão}
Eu simplifico a solução para um \textbf{dashboard local no Briefer} com \textbf{pipeline offline em Python}, mantendo foco pedagógico em \textbf{rede neural} e aplicação de \textbf{Engenharia de Software}. A documentação C4 comunica o desenho e prepara a execução do TP3 com baixo atrito.

\newpage
\bibliographystyle{abntex2-alf}
\bibliography{bibliografia}

\end{document}
