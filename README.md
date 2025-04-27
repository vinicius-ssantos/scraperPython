# 👚 Amazon Scraper 2025 (Python + Playwright)

Scraper assíncrono desenvolvido para coletar dados da Amazon Brasil de forma resiliente, modular e escalável.

---

## 📚 O que este projeto faz?

- Pesquisa produtos na Amazon por uma palavra-chave.
- Extrai título, preço, avaliação, número de reviews, link para o produto, imagem, entrega e badge especial (ex: "Pequenas Empresas").
- Salva os dados:
  - Em um arquivo JSON
  - Em uma captura de tela (screenshot)
  - Em um arquivo HTML bruto da página

---

## 🏗️ Estrutura do Projeto

```
amazon_scraper/
├── main.py             # Ponto de entrada da aplicação
├── scraper.py          # Lógica principal de scraping e salvamento
├── selector_loader.py  # Carrega seletores de scraping de arquivo YAML
├── utils.py            # Funções auxiliares, como retry inteligente
├── model.py            # Modelos de dados (Product)
├── selectors/
│   └— selectors_amazon.yml  # Seletores de scraping configuráveis
├── output/
│   ├── JSON, HTML, screenshots (gerados dinamicamente)
└— .venv/              # Ambiente virtual Python
```

---

## ⚙️ Tecnologias Usadas

- **Python 3.12**
- **Playwright Async API** (controle do navegador headless)
- **Pydantic** (modelagem de dados)
- **Loguru** (logging profissional)
- **YAML** (configuração de seletores externos)

---

## 🚀 Como Rodar

1. Crie ambiente virtual:
   ```bash
   python -m venv .venv
   ```

2. Ative o ambiente:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

3. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Instale navegadores do Playwright:
   ```bash
   playwright install
   ```

5. Execute o projeto:
   ```bash
   python main.py
   ```

---

## 📋 Funcionalidades Implementadas

- Scraping assíncrono de produtos
- Retry automático em falhas
- Espera dinâmica de carregamento
- Exportação JSON, screenshot PNG, página HTML
- Log estruturado
- Suporte a mudanças de layout via YAML
- Código limpo, modular, extensível

---

## 📈 Melhorias Futuras (Próximos Passos)

- Scraping de múltiplas páginas de resultados
- Integração com proxies para rotação de IP
- Rodar scraping paralelo (multiprocessamento ou asyncio tasks)
- Exposição via API (FastAPI)
- Persistência em Banco de Dados (MongoDB, PostgreSQL)

---

## 📓 Documentação dos Seletores

O arquivo `selectors_amazon.yml` define quais elementos serão extraídos do HTML da Amazon, podendo ser atualizado sem mexer no código-fonte.

---


O arquivo requirements.txt foi criado no documento Requirements Scraper

 comando pip install -r requirements.tx

# 👨‍💻 Autor

- Projeto desenvolvido por Vinicius com apoio da arquitetura orientada a boas práticas de desenvolvimento moderno 🚀

