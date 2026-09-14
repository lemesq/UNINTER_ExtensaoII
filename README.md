# Dashboard — Alfabetização de Mulheres Responsáveis pelo Domicílio (Rio de Janeiro)

Aplicação interativa desenvolvida em **Streamlit** para a Atividade Extensionista II
(CST em Ciência de Dados — UNINTER), a partir da base `Mulheres.csv` (dados do
Instituto Pereira Passos, por bairro do município do Rio de Janeiro).

## O que o dashboard mostra

- Indicadores gerais (total de mulheres, analfabetas, taxa de analfabetismo);
- Taxa de analfabetismo por faixa etária (15–29, 30–59, 60+);
- Ranking de bairros com maior e menor taxa de analfabetismo;
- Taxa de analfabetismo por Região Administrativa;
- Filtros por região, bairro e tamanho mínimo de amostra;
- Tabela detalhada com opção de download em CSV.

## Como rodar localmente

1. Tenha Python 3.9+ instalado.
2. Nesta pasta, instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Rode o app:

   ```bash
   streamlit run app.py
   ```

4. O navegador abrirá automaticamente em `http://localhost:8501`.

## Estrutura de arquivos

```
streamlit_app/
├── app.py              # código do dashboard
├── requirements.txt    # dependências
├── Mulheres.csv         # base de dados
└── README.md            # este arquivo
```
