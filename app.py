import streamlit as st
import pandas as pd

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="ETE - Rio Incomáti",
    page_icon="🌊",
    layout="wide"
)

# ==========================================================
# TÍTULO
# ==========================================================

st.title("🌊 ETE — MONITORAMENTO E ALERTA COMUNITÁRIO")
st.subheader("RIO INCOMÁTI — MARRACUENE")

st.write("### Como está a situação neste momento?")

# ==========================================================
# CARREGAR DADOS
# ==========================================================

arquivo = "dados_incomati_marracuene.csv"

try:
    dados = pd.read_csv(arquivo)

except FileNotFoundError:
    st.error(f"Arquivo não encontrado: {arquivo}")
    st.stop()

# ==========================================================
# PREPARAR DADOS
# ==========================================================

dados["Data"] = pd.to_datetime(
    dados["Data"],
    errors="coerce"
)

dados["Nivel_Rio_m"] = pd.to_numeric(
    dados["Nivel_Rio_m"],
    errors="coerce"
)

dados["Caudal_m3s"] = pd.to_numeric(
    dados["Caudal_m3s"],
    errors="coerce"
)

dados["Precipitacao_mm"] = pd.to_numeric(
    dados["Precipitacao_mm"],
    errors="coerce"
)

# Remover registros sem data
dados = dados.dropna(subset=["Data"])

if dados.empty:
    st.warning("Ainda não existem dados disponíveis.")
    st.stop()

# ==========================================================
# ÚLTIMO REGISTRO
# ==========================================================

ultimo = dados.iloc[-1]

data = ultimo["Data"]
estacao = ultimo["Estacao"]
nivel = ultimo["Nivel_Rio_m"]
caudal = ultimo["Caudal_m3s"]
chuva = ultimo["Precipitacao_mm"]
estagio = ultimo["Estagio"]
fonte = ultimo["Fonte"]

# ==========================================================
# DETERMINAR SITUAÇÃO
# ==========================================================
#
# ATENÇÃO:
# Estes limites são apenas para DEMONSTRAÇÃO.
# Não são limites oficiais da ARA-Sul.
#
# Quando tivermos os limites oficiais,
# substituí-los aqui.
# ==========================================================

if pd.isna(nivel):

    situacao = "SEM DADO"
    emoji = "⚪"
    mensagem = (
        "Não existe neste momento um valor de nível "
        "disponível para determinar a situação."
    )

elif nivel < 2.5:

    situacao = "NORMAL"
    emoji = "🟢"
    mensagem = (
        "O nível registrado está abaixo do limite "
        "de demonstração definido para atenção."
    )

elif nivel < 3.0:

    situacao = "ATENÇÃO"
    emoji = "🟡"
    mensagem = (
        "O nível requer maior acompanhamento."
    )

elif nivel < 3.5:

    situacao = "ALERTA"
    emoji = "🟠"
    mensagem = (
        "O nível exige preparação e monitoramento frequente."
    )

else:

    situacao = "EMERGÊNCIA"
    emoji = "🔴"
    mensagem = (
        "O nível ultrapassou o limite de demonstração "
        "para situação crítica."
    )

# ==========================================================
# NÍVEIS DE SITUAÇÃO
# ==========================================================

st.write("## 🚦 Níveis de situação")

col1, col2, col3, col4 = st.columns(4)

with col1:

    if situacao == "NORMAL":

        st.success(
            "🟢 NORMAL\n\n"
            "SITUAÇÃO ATUAL"
        )

    else:

        st.info(
            "🟢 NORMAL\n\n"
            "Condições dentro do esperado."
        )


with col2:

    if situacao == "ATENÇÃO":

        st.warning(
            "🟡 ATENÇÃO\n\n"
            "SITUAÇÃO ATUAL"
        )

    else:

        st.info(
            "🟡 ATENÇÃO\n\n"
            "Requer maior observação."
        )


with col3:

    if situacao == "ALERTA":

        st.warning(
            "🟠 ALERTA\n\n"
            "SITUAÇÃO ATUAL"
        )

    else:

        st.info(
            "🟠 ALERTA\n\n"
            "Requer preparação."
        )


with col4:

    if situacao == "EMERGÊNCIA":

        st.error(
            "🔴 EMERGÊNCIA\n\n"
            "SITUAÇÃO ATUAL"
        )

    else:

        st.info(
            "🔴 EMERGÊNCIA\n\n"
            "Situação crítica."
        )

# ==========================================================
# SITUAÇÃO ATUAL
# ==========================================================

st.divider()

st.header(
    f"{emoji} SITUAÇÃO ATUAL: {situacao}"
)

st.info(mensagem)

st.write(
    f"**Estação:** {estacao}"
)

st.write(
    f"**Último registro:** "
    f"{data.strftime('%d/%m/%Y %H:%M')}"
)

st.write(
    f"**Fonte:** {fonte}"
)

# ==========================================================
# INDICADORES
# ==========================================================

st.write("## 📊 Indicadores atuais")

col1, col2, col3, col4 = st.columns(4)

with col1:

    if pd.isna(nivel):

        st.metric(
            "🌊 Nível do Rio",
            "Sem dado"
        )

    else:

        st.metric(
            "🌊 Nível do Rio",
            f"{nivel:.2f} m"
        )


with col2:

    if pd.isna(caudal):

        st.metric(
            "💧 Caudal",
            "Sem dado"
        )

    else:

        st.metric(
            "💧 Caudal",
            f"{caudal:.2f} m³/s"
        )


with col3:

    if pd.isna(chuva):

        st.metric(
            "🌧️ Precipitação",
            "Sem dado"
        )

    else:

        st.metric(
            "🌧️ Precipitação",
            f"{chuva:.1f} mm"
        )


with col4:

    if pd.isna(estagio):

        st.metric(
            "📊 Estágio",
            "Sem dado"
        )

    else:

        st.metric(
            "📊 Estágio",
            str(estagio)
        )

# ==========================================================
# GRÁFICO DO NÍVEL
# ==========================================================

st.divider()

st.write("## 📈 Evolução do nível do Rio Incomáti")

dados_nivel = dados.dropna(
    subset=["Nivel_Rio_m"]
)

if not dados_nivel.empty:

    grafico_nivel = dados_nivel.set_index(
        "Data"
    )["Nivel_Rio_m"]

    st.line_chart(grafico_nivel)

else:

    st.info(
        "O gráfico será apresentado quando "
        "existirem dados reais de nível."
    )

# ==========================================================
# GRÁFICO DO CAUDAL
# ==========================================================

st.write("## 💧 Evolução do caudal")

dados_caudal = dados.dropna(
    subset=["Caudal_m3s"]
)

if not dados_caudal.empty:

    grafico_caudal = dados_caudal.set_index(
        "Data"
    )["Caudal_m3s"]

    st.line_chart(grafico_caudal)

else:

    st.info(
        "O gráfico será apresentado quando "
        "existirem dados reais de caudal."
    )

# ==========================================================
# PRECIPITAÇÃO
# ==========================================================

st.write("## 🌧️ Precipitação")

dados_chuva = dados.dropna(
    subset=["Precipitacao_mm"]
)

if not dados_chuva.empty:

    grafico_chuva = dados_chuva.set_index(
        "Data"
    )["Precipitacao_mm"]

    st.bar_chart(grafico_chuva)

else:

    st.info(
        "O gráfico será apresentado quando "
        "existirem dados de precipitação."
    )

# ==========================================================
# TABELA
# ==========================================================

st.divider()

st.write("## 📋 Dados registrados")

st.dataframe(
    dados,
    use_container_width=True
)

# ==========================================================
# INFORMAÇÃO DA ESTAÇÃO
# ==========================================================

st.divider()

st.write("## 📍 Estação de monitoramento")

st.write(
    "**E-572 — Incomáti em Marracuene**"
)

st.write(
    "**Latitude:** -25.733"
)

st.write(
    "**Longitude:** 32.682"
)

st.write(
    "**Tipo de medição:** Nível do rio (Stage)"
)

# ==========================================================
# AVISO
# ==========================================================

st.divider()

st.caption(
    "⚠️ Os limites de alerta apresentados nesta versão "
    "são provisórios e servem apenas para desenvolvimento. "
    "Antes do uso operacional, deverão ser substituídos "
    "pelos critérios oficiais aplicáveis à estação E-572."
)
