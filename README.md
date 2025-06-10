# 🚌 OniPix

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django" alt="Django Version">
  <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" alt="License">
</p>



<p align="center">
  </p>

---

## 📚 Tabela de Conteúdos

* [Sobre o Projeto](#-sobre-o-projeto)
* [✨ Funcionalidades](#-funcionalidades)
* [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
* [🚀 Rodando o Projeto Localmente](#-rodando-o-projeto-localmente)
* [🤝 Como Contribuir](#-como-contribuir)
* [📄 Licença](#-licença)

---

## 📖 Sobre o Projeto

Aplicação Web com o objetivo de disponibilizar a compra de passagens de ônibus municipais por meio de pagamento PIX.

---

## ✨ Funcionalidades

* **✅ Funcionalidade 1:** Compra de passagens rápida e com facilidade.
* **✅ Funcionalidade 2:** Validação instantânea pelo motorista.
* **✅ Funcionalidade 3:** Controle do fluxo de validações das passagens pela empresa.
* **✅ ...e muito mais!**

---

## 🛠️ Tecnologias Utilizadas

Esta aplicação foi construída utilizando as seguintes tecnologias e ferramentas:

* **Backend:** Python, Django, Django REST Framework
* **Frontend:** HTML, CSS, JavaScript
* **Banco de Dados:** [SQLite (desenvolvimento), PostgreSQL (produção)]
* **Pagamentos:** API do Mercado Pago
* **Outros:** `django-environ`, `qrcode` etc.

---

## 🚀 Rodando o Projeto Localmente

Siga estas instruções para configurar e executar o projeto em seu ambiente de desenvolvimento local.

### **Pré-requisitos**

Antes de começar, certifique-se de que você tem o seguinte instalado em sua máquina:
* [Python 3.9+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads/)

### **Passos para a Instalação**

1.  **Clone o Repositório**
    ```bash
    git clone https:/github.com/vitormarvulle/pix-onibus.git
    ```

2.  **Crie e Ative o Ambiente Virtual (`venv`)**
    * **Para macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **Para Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Instale as Dependências**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente 🔑**
    Este projeto usa um arquivo `.env` para gerenciar chaves de API e configurações sensíveis.

    * Primeiro, copie o arquivo de exemplo `.env.example` para criar seu próprio arquivo `.env`:
        ```bash
        # No macOS/Linux
        cp .env.example .env
        
        # No Windows
        copy .env.example .env
        ```
    * Depois, abra o arquivo `.env` e preencha as variáveis com suas próprias credenciais. O arquivo `.env` **não é rastreado pelo Git**, então suas credenciais estarão seguras.
        ```ini
        # Exemplo de conteúdo do .env
        SECRET_KEY="sua_chave_secreta_aqui_gerada_pelo_django"
        DEBUG=True
        MERCADOPAGO_ACCESS_TOKEN="sua_chave_de_acesso_do_mercado_pago"
        ```

5.  **Aplique as Migrações do Banco de Dados**
    ```bash
    python manage.py migrate
    ```

6.  **(Opcional) Crie um Superusuário**
    Para acessar a área administrativa do Django (`/admin`).
    ```bash
    python manage.py createsuperuser
    ```

7.  **Execute a Aplicação! 🎉**
    ```bash
    python manage.py runserver
    ```
    Acesse a aplicação em seu navegador: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---


## 🤝 Como Contribuir

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

1.  **Faça um Fork** do projeto.
2.  **Crie uma Branch** para sua nova funcionalidade (`git checkout -b feature/AmazingFeature`).
3.  **Faça o Commit** de suas alterações (`git commit -m 'Add some AmazingFeature'`).
4.  **Faça o Push** para a Branch (`git push origin feature/AmazingFeature`).
5.  **Abra um Pull Request**.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
