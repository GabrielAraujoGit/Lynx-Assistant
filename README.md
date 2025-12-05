<!-- Banner central -->
<div align="center">
  <img src="https://img.shields.io/badge/Lynx%20Assistant-%23000000.svg?style=for-the-badge&logo=python&logoColor=white" height="32"/>
  <img src="https://img.shields.io/badge/Desktop%20Automation-%23282828.svg?style=for-the-badge&logo=windowsterminal&logoColor=white" height="32"/>
  <img src="https://img.shields.io/badge/Open%20Source-%23181717.svg?style=for-the-badge&logo=github&logoColor=white" height="32"/>
</div>

<h1 align="center">Lynx Assistant</h1>

<p align="center">
  <b>O poder dos comandos rápidos — na ponta dos seus dedos.</b><br/>
  Um assistente desktop inteligente para abrir programas, sites e ambientes com naturalidade.
</p>

<div align="center">
  <img src="https://img.shields.io/badge/License-0D1117?style=flat&logo=github&logoColor=white" />
  <img src="https://img.shields.io/github/v/release/gabriel-araujo-git/lynx-assistant?style=flat&color=0D1117&label=Release&logo=github&logoColor=white" />
  <img src="https://img.shields.io/github/last-commit/gabriel-araujo-git/lynx-assistant?style=flat&color=0D1117&label=Last%20Commit&logo=git&logoColor=F05032" />
  <img src="https://img.shields.io/github/issues/gabriel-araujo-git/lynx-assistant?style=flat&color=0D1117&label=Issues&logo=github&logoColor=white" />
  <img src="https://img.shields.io/github/issues-pr/gabriel-araujo-git/lynx-assistant?style=flat&color=0D1117&label=Pull%20Requests&logo=github&logoColor=white" />
  <img src="https://img.shields.io/github/stars/gabriel-araujo-git/lynx-assistant?style=flat&color=0D1117&label=Stars&logo=github&logoColor=FFD700" />
  <img src="https://img.shields.io/github/downloads/gabriel-araujo-git/lynx-assistant/total?style=flat&color=0D1117&label=Downloads&logo=github&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-0D1117?style=flat&logo=python&logoColor=3776AB" />
</div>



---

## Visão Geral

O **Lynx Assistant** é um assistente desktop open source criado para
**executar comandos e automações com linguagem natural**.\
Com ele, é possível abrir programas, sites ou ambientes de trabalho
usando instruções simples como:

``` bash
ln teste
abrir vscode
abrir youtube
```

Desenvolvido em **Python**, com interface moderna via **CustomTkinter**,
o Lynx combina **rapidez, modularidade e uma experiência fluida** de uso
no desktop.

------------------------------------------------------------------------

## Principais Recursos

-   **Comandos naturais** --- esqueça sintaxes complicadas; use
    linguagem comum.\
-   **Aprendizado adaptável** --- adicione e edite comandos pelo próprio
    app.\
-   **Interface moderna (CustomTkinter)** --- tema escuro, clean e
    responsivo.\
-   **Integrações locais e web** --- do VSCode ao LinkedIn.\
-   **Persistência local** --- armazenamento seguro e transparente via
    `commands.json`.\
-   **Extensível** --- pronto para receber novas engines e módulos.

------------------------------------------------------------------------
## Interface

<div align="center" style="display: flex; gap: 20px; justify-content: center;">

  <div style="text-align: center;">
    <img src="docs/screenshot_main.png" width="300" style="border-radius: 8px; box-shadow: 0 0 8px #0003;"/>
    <p><b>Tela Principal</b></p>
  </div>

  <div style="text-align: center;">
    <img src="docs/screenshot_help.png" width="300" style="border-radius: 8px; box-shadow: 0 0 8px #0003;"/>
    <p><b>Ajuda Expandida</b></p>
  </div>

  <div style="text-align: center;">
    <img src="docs/screenshot_add.png" width="300" style="border-radius: 8px; box-shadow: 0 0 8px #0003;"/>
    <p><b>Adicionar Comando</b></p>
  </div>

</div>



------------------------------------------------------------------------

## Instalação

``` bash
# Clone o repositório
git clone https://github.com/gabriel-araujo-git/lynx-assistant.git
cd lynx-assistant

# Instale as dependências
pip install -r requirements.txt

# Execute o Lynx
python assistant_ui.py
```

O aplicativo será iniciado em modo janela e adicionará um ícone na
bandeja do sistema.\
Você pode ocultá-lo e reabrir a qualquer momento.

------------------------------------------------------------------------

## Estrutura do Projeto

    lynx-assistant/
    │
    ├── assistant_ui.py        # Interface principal (UI + Command Engine)
    ├── commands.json          # Banco local de comandos
    ├── requirements.txt
    ├── LICENSE
    ├── README.md
    ├── CHANGELOG.md
    ├── CONTRIBUTING.md
    └── docs/
        ├── screenshot_main.png
        ├── screenshot_help.png
        └── screenshot_add.png

------------------------------------------------------------------------

## Adicionando Novos Comandos

No aplicativo, selecione **Adicionar** e defina:

  Campo            Descrição
  ---------------- ---------------------------------------
  Tipo             Interno (programa) ou Externo (site)
  Nome             Nome do comando
  Palavras-chave   Termos que acionam o comando
  Caminho / URL    Caminho do executável ou link do site

O Lynx salva as informações automaticamente em `commands.json`.

------------------------------------------------------------------------

## Stack Técnica

-   Python 3.10+
-   CustomTkinter
-   PyStray
-   Pillow
-   Subprocess / Webbrowser


------------------------------------------------------------------------

## Documentação Detalhada

A documentação técnica foi dividida em seções independentes dentro do diretório `docs/` para facilitar a navegação e manutenção:

- [Guia de Instalação e Configuração](docs/setup.md)
- [Guia de Uso e Exemplos](docs/usage.md)
- [Arquitetura e Estrutura Interna](docs/architecture.md)
- [Roadmap e Planejamento Futuro](docs/roadmap.md)

Esses arquivos seguem o mesmo padrão de estilo do projeto principal, utilizando badges informativas e linguagem técnica consistente.

------------------------------------------------------------------------

## Contribuição

Contribuições são bem-vindas. Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) 
antes de enviar um pull request.

------------------------------------------------------------------------

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [MIT](LICENSE). para mais
detalhes.
