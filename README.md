ODS 16 — Sistema Inteligente de Detecção e Dashboard
Este projeto tem como objetivo o desenvolvimento de um sistema inteligente para detecção de itens de interesse em imagens e vídeos. O produto consiste em uma aplicação web completa, dotada de uma API REST para realizar as inferências a partir de um modelo de Rede Neural Convolucional (CNN), e um frontend com um dashboard interativo para a visualização de métricas de desempenho.

O sistema está alinhado ao ODS 16 — Paz, Justiça e Instituições Eficazes.

Integrantes
Rhudson Sampaio

Instruções de utilização
Assim que a primeira versão do sistema estiver disponível, esta seção será complementada com as instruções de utilização. Abaixo, descrevemos como instalar as dependências e executar a aplicação.

Instalação e Execução
Clone o repositório:

git clone [https://github.com/RhudsonDouglas/ods16-deteccao-armas-dashboard.git](https://github.com/RhudsonDouglas/ods16-deteccao-armas-dashboard.git)
cd ods16-deteccao-armas-dashboard

Crie e ative um ambiente virtual:

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
# python -m venv .venv
# .venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

Execute a API:

uvicorn app.main:app --reload

A API estará disponível em http://127.0.0.1:8000 e a documentação interativa em http://127.0.0.1:8000/docs.

Histórico de versões
0.1.1

CHANGE: Atualização da documentação. Código permaneceu inalterado.

0.1.0

Indução do primeiro modelo do agente inteligente.

0.0.1

Trabalhando na preparação dos dados.
