import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Alfabetização de Mulheres - Rio de Janeiro",
    page_icon="📊",
    layout="wide",
)

CAMINHO_CSV = "alfabetizacaoMulheresRJ.csv"

@st.cache_data
def carregar_dados():
    df = pd.read_csv(CAMINHO_CSV, sep=";", encoding="latin1")

    df = df.rename(columns={
        "Pessoa responsável pelo domicílio, Sexo feminino, 15 a 29 anos, Morador sabe ler e escrever":
            "f_15_29_alfabetizada",
        "Pessoa responsável pelo domicílio, Sexo feminino, 15 a 29 anos, Morador não sabe ler e escrever":
            "f_15_29_analfabeta",
        "Pessoa responsável pelo domicílio, Sexo feminino, 30 a 59 anos, Morador sabe ler e escrever":
            "f_30_59_alfabetizada",
        "Pessoa responsável pelo domicílio, Sexo feminino, 30 a 59 anos, Morador não sabe ler e escrever":
            "f_30_59_analfabeta",
        "Pessoa responsável pelo domicílio, Sexo feminino, 60 anos ou mais, Morador sabe ler e escrever":
            "f_60mais_alfabetizada",
        "Pessoa responsável pelo domicílio, Sexo feminino, 60 anos ou mais, Morador não sabe ler e escrever":
            "f_60mais_analfabeta",
    })

    colunas_uteis = [
        "bairro", "regiao_adm", "ra",
        "f_15_29_alfabetizada", "f_15_29_analfabeta",
        "f_30_59_alfabetizada", "f_30_59_analfabeta",
        "f_60mais_alfabetizada", "f_60mais_analfabeta",
    ]
    df = df[colunas_uteis].copy()

    df["total_15_29"] = df["f_15_29_alfabetizada"] + df["f_15_29_analfabeta"]
    df["total_30_59"] = df["f_30_59_alfabetizada"] + df["f_30_59_analfabeta"]
    df["total_60mais"] = df["f_60mais_alfabetizada"] + df["f_60mais_analfabeta"]
    df["total_mulheres"] = df["total_15_29"] + df["total_30_59"] + df["total_60mais"]

    df["total_alfabetizadas"] = (
        df["f_15_29_alfabetizada"] + df["f_30_59_alfabetizada"] + df["f_60mais_alfabetizada"]
    )
    df["total_analfabetas"] = (
        df["f_15_29_analfabeta"] + df["f_30_59_analfabeta"] + df["f_60mais_analfabeta"]
    )

    df = df[df["total_mulheres"] > 0].copy()
    df["taxa_analfabetismo"] = (df["total_analfabetas"] / df["total_mulheres"]) * 100

    return df


df = carregar_dados()

# CABEÇALHO
st.title("📊 Alfabetização de Mulheres Responsáveis pelo Domicílio")
st.markdown(
    "##### Cidade do Rio de Janeiro/RJ · Atividade Extensionista II — CST em Ciência de Dados (UNINTER)"
)
st.caption(
    "Fonte dos dados: Instituto Pereira Passos (IPP) — recorte municipal por bairro. "
)
st.divider()

# BARRA LATERAL - FILTROS
st.sidebar.header("Filtros")

regioes = sorted(df["regiao_adm"].unique().tolist())
regioes_selecionadas = st.sidebar.multiselect(
    "Região Administrativa", options=regioes, default=[]
)

bairros_disponiveis = sorted(df["bairro"].unique().tolist())
bairros_selecionados = st.sidebar.multiselect(
    "Bairro", options=bairros_disponiveis, default=[]
)

min_mulheres = st.sidebar.slider(
    "Mínimo de mulheres responsáveis pelo domicílio no bairro (filtra bairros pequenos)",
    min_value=0, max_value=500, value=30, step=10,
)

df_filtrado = df[df["total_mulheres"] >= min_mulheres].copy()
if regioes_selecionadas:
    df_filtrado = df_filtrado[df_filtrado["regiao_adm"].isin(regioes_selecionadas)]
if bairros_selecionados:
    df_filtrado = df_filtrado[df_filtrado["bairro"].isin(bairros_selecionados)]

if df_filtrado.empty:
    st.warning("Nenhum bairro corresponde aos filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# INDICADORES GERAIS (KPIs)
total_mulheres = int(df_filtrado["total_mulheres"].sum())
total_analfabetas = int(df_filtrado["total_analfabetas"].sum())
taxa_geral = (total_analfabetas / total_mulheres) * 100 if total_mulheres else 0
qtd_bairros = df_filtrado["bairro"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Bairros no recorte", f"{qtd_bairros}")
col2.metric("Mulheres responsáveis pelo domicílio", f"{total_mulheres:,}".replace(",", "."))
col3.metric("Mulheres analfabetas", f"{total_analfabetas:,}".replace(",", "."))
col4.metric("Taxa de analfabetismo", f"{taxa_geral:.2f}%")

st.divider()

# GRÁFICO 1 - TAXA POR FAIXA ETÁRIA
faixas = {
    "15 a 29 anos": ("f_15_29_alfabetizada", "f_15_29_analfabeta", "total_15_29"),
    "30 a 59 anos": ("f_30_59_alfabetizada", "f_30_59_analfabeta", "total_30_59"),
    "60 anos ou mais": ("f_60mais_alfabetizada", "f_60mais_analfabeta", "total_60mais"),
}

linhas_faixa = []
for nome_faixa, (col_alf, col_analf, col_total) in faixas.items():
    total = df_filtrado[col_total].sum()
    analfabetas = df_filtrado[col_analf].sum()
    taxa = (analfabetas / total * 100) if total else 0
    linhas_faixa.append({
        "Faixa etária": nome_faixa,
        "Total de mulheres": int(total),
        "Analfabetas": int(analfabetas),
        "Taxa de analfabetismo (%)": round(taxa, 2),
    })
indicadores_faixa_df = pd.DataFrame(linhas_faixa)

col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("Taxa de analfabetismo por faixa etária")
    fig1 = px.bar(
        indicadores_faixa_df, x="Faixa etária", y="Taxa de analfabetismo (%)",
        color="Faixa etária", text="Taxa de analfabetismo (%)",
        color_discrete_sequence=["#4C72B0", "#DD8452", "#55A868"],
    )
    fig1.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig1.update_layout(showlegend=False, yaxis_title="Taxa (%)")
    st.plotly_chart(fig1, use_container_width=True)

with col_dir:
    st.subheader("Composição por faixa etária")
    fig2 = go.Figure()
    fig2.add_bar(
        name="Sabe ler e escrever",
        x=indicadores_faixa_df["Faixa etária"],
        y=indicadores_faixa_df["Total de mulheres"] - indicadores_faixa_df["Analfabetas"],
        marker_color="#4C72B0",
    )
    fig2.add_bar(
        name="Não sabe ler e escrever",
        x=indicadores_faixa_df["Faixa etária"],
        y=indicadores_faixa_df["Analfabetas"],
        marker_color="#C44E52",
    )
    fig2.update_layout(barmode="stack", yaxis_title="Número de mulheres")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# GRÁFICO 2 - RANKING DE BAIRROS
st.subheader("Ranking de bairros por taxa de analfabetismo")

qtd_top = st.slider("Quantidade de bairros no ranking", min_value=5, max_value=30, value=10)

col_top, col_bottom = st.columns(2)

with col_top:
    st.markdown(f"**{qtd_top} bairros com MAIOR taxa de analfabetismo**")
    top_maior = df_filtrado.sort_values("taxa_analfabetismo", ascending=False).head(qtd_top)
    fig3 = px.bar(
        top_maior.sort_values("taxa_analfabetismo"),
        x="taxa_analfabetismo", y="bairro", orientation="h",
        color_discrete_sequence=["#C44E52"],
        labels={"taxa_analfabetismo": "Taxa de analfabetismo (%)", "bairro": ""},
        hover_data={"regiao_adm": True, "total_mulheres": True},
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_bottom:
    st.markdown(f"**{qtd_top} bairros com MENOR taxa de analfabetismo (não nula)**")
    base_nao_zero = df_filtrado[df_filtrado["taxa_analfabetismo"] > 0]
    if base_nao_zero.empty:
        st.info("Todos os bairros do recorte selecionado têm taxa de analfabetismo igual a 0%.")
    else:
        top_menor = base_nao_zero.sort_values("taxa_analfabetismo", ascending=True).head(qtd_top)
        fig4 = px.bar(
            top_menor.sort_values("taxa_analfabetismo", ascending=False),
            x="taxa_analfabetismo", y="bairro", orientation="h",
            color_discrete_sequence=["#55A868"],
            labels={"taxa_analfabetismo": "Taxa de analfabetismo (%)", "bairro": ""},
            hover_data={"regiao_adm": True, "total_mulheres": True},
        )
        st.plotly_chart(fig4, use_container_width=True)

    qtd_zero = (df_filtrado["taxa_analfabetismo"] == 0).sum()
    if qtd_zero:
        st.caption(f"ℹ️ {qtd_zero} bairro(s) do recorte têm taxa de analfabetismo igual a 0%.")

st.divider()

# GRÁFICO 3 - POR REGIÃO ADMINISTRATIVA
st.subheader("Taxa de analfabetismo por Região Administrativa")

por_regiao = df_filtrado.groupby("regiao_adm").agg(
    total_mulheres=("total_mulheres", "sum"),
    total_analfabetas=("total_analfabetas", "sum"),
).reset_index()
por_regiao["taxa_analfabetismo"] = (
    por_regiao["total_analfabetas"] / por_regiao["total_mulheres"] * 100
)
por_regiao = por_regiao.sort_values("taxa_analfabetismo", ascending=False)

fig5 = px.bar(
    por_regiao, x="regiao_adm", y="taxa_analfabetismo",
    labels={"regiao_adm": "Região Administrativa", "taxa_analfabetismo": "Taxa de analfabetismo (%)"},
    color="taxa_analfabetismo", color_continuous_scale="Reds",
)
fig5.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# TABELA DETALHADA E DOWNLOAD
st.subheader("Dados detalhados por bairro")

colunas_exibicao = {
    "bairro": "Bairro",
    "regiao_adm": "Região Administrativa",
    "total_mulheres": "Total de mulheres",
    "total_analfabetas": "Analfabetas",
    "taxa_analfabetismo": "Taxa de analfabetismo (%)",
}
tabela = df_filtrado[list(colunas_exibicao.keys())].rename(columns=colunas_exibicao)
tabela = tabela.sort_values("Taxa de analfabetismo (%)", ascending=False).round(2)

st.dataframe(tabela, use_container_width=True, hide_index=True)

csv_download = tabela.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Baixar dados filtrados (CSV)",
    data=csv_download,
    file_name="indicadores_alfabetizacao_mulheres_rj.csv",
    mime="text/csv",
)

st.divider()
st.caption(
    "Projeto desenvolvido para a disciplina Atividade Extensionista II: Tecnologia Aplicada à "
    "Inclusão Digital — CST em Ciência de Dados, UNINTER. ODS 04 (Educação de qualidade) e "
    "ODS 10 (Redução das desigualdades)."
)
