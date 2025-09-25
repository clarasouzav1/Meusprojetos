import streamlit as st
import re
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Análise de VT - avsvs",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Dicionário com os salários mínimos por competência
salarios_minimos = {
    # 2020
    "01/2020": 1045.00, "02/2020": 1045.00, "03/2020": 1045.00, "04/2020": 1045.00,
    "05/2020": 1045.00, "06/2020": 1045.00, "07/2020": 1045.00, "08/2020": 1045.00,
    "09/2020": 1045.00, "10/2020": 1045.00, "11/2020": 1045.00, "12/2020": 1045.00,

    # 2021
    "01/2021": 1100.00, "02/2021": 1100.00, "03/2021": 1100.00, "04/2021": 1100.00,
    "05/2021": 1100.00, "06/2021": 1100.00, "07/2021": 1100.00, "08/2021": 1100.00,
    "09/2021": 1100.00, "10/2021": 1100.00, "11/2021": 1100.00, "12/2021": 1100.00,

    # 2022
    "01/2022": 1212.00, "02/2022": 1212.00, "03/2022": 1212.00, "04/2022": 1212.00,
    "05/2022": 1212.00, "06/2022": 1212.00, "07/2022": 1212.00, "08/2022": 1212.00,
    "09/2022": 1212.00, "10/2022": 1212.00, "11/2022": 1212.00, "12/2022": 1212.00,

    # 2023
    "01/2023": 1302.00, "02/2023": 1302.00, "03/2023": 1302.00, "04/2023": 1302.00,
    "05/2023": 1302.00, "06/2023": 1302.00, "07/2023": 1302.00, "08/2023": 1302.00,
    "09/2023": 1302.00, "10/2023": 1302.00, "11/2023": 1302.00, "12/2023": 1302.00,

    # 2024
    "01/2024": 1412.00, "02/2024": 1412.00, "03/2024": 1412.00, "04/2024": 1412.00,
    "05/2024": 1412.00, "06/2024": 1412.00, "07/2024": 1412.00, "08/2024": 1412.00,
    "09/2024": 1412.00, "10/2024": 1412.00, "11/2024": 1412.00, "12/2024": 1412.00,

    # 2025 (projeção até junho)
    "01/2025": 1518.00, "02/2025": 1518.00, "03/2025": 1518.00, "04/2025": 1518.00,
    "05/2025": 1518.00, "06/2025": 1518.00,"07/2025": 1518.00, "08/2025": 1518.00,
    "09/2025": 1518.00, "10/2025": 1518.00, "11/2025": 1518.00, "12/2025": 1518.00,

    # 2026 (projeção até junho)
    "01/2026": 1518.00, "02/2025": 1518.00, "03/2025": 1518.00, "04/2025": 1518.00,
    "05/2026": 1518.00, "06/2025": 1518.00,"07/2026": 1518.00, "08/2026": 1518.00,
    "09/2026": 1518.00, "10/2026": 1518.00, "11/2026": 1518.00, "12/2026": 1518.00,
}


# Funções auxiliares
def format_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_real_sem_rs(valor):
    return "{:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

# Título e entrada
st.title("📊 Sistema de Cálculo de Adicionais Trabalhistas - AnaClara - com verificação da periculosidade")
st.write("Preencha os dados abaixo para calcular os adicionais:")

nome = st.text_input("Nome da pessoa analisada")
competencia = st.text_input("Competência (MM/AAAA)")

competencia_valida = bool(re.match(r"^(0[1-9]|1[0-2])/[0-9]{4}$", competencia))
salario_minimo_vigente = salarios_minimos.get(competencia) if competencia_valida else None

if competencia and not competencia_valida:
    st.warning("Digite a competência no formato MM/AAAA.")
elif competencia_valida and salario_minimo_vigente is None:
    st.info("Competência não encontrada na tabela. Digite o salário mínimo manualmente.")

if nome and competencia:
    st.success(f"Analisando {nome} para a competência {competencia}")

# Entradas numéricas
salario_base = st.number_input("Salário Base (R$)", min_value=0.0, step=100.0, format="%.2f")
divisor_jornada = st.number_input("Divisor da Jornada Mensal", min_value=1.0, value=220.0, step=1.0, format="%.0f")

if competencia_valida and salario_minimo_vigente:
    salario_minimo = st.number_input("Salário Mínimo Vigente (R$)", min_value=0.0, value=salario_minimo_vigente, step=10.0, format="%.2f")
else:
    salario_minimo = st.number_input("Salário Mínimo Vigente (R$)", min_value=0.0, value=0.0, step=10.0, format="%.2f")

recebe_periculosidade = st.checkbox("Recebe Periculosidade? (30% do salário base)")
adicional_periculosidade = salario_base * 0.3 if recebe_periculosidade else 0.0

grau_insalubridade = st.selectbox("Grau de Insalubridade", ["Nenhum", "10% (Leve)", "20% (Médio)", "40% (Máximo)"])
if grau_insalubridade == "10% (Leve)":
    adicional_insalubridade = salario_minimo * 0.1
elif grau_insalubridade == "20% (Médio)":
    adicional_insalubridade = salario_minimo * 0.2
elif grau_insalubridade == "40% (Máximo)":
    adicional_insalubridade = salario_minimo * 0.4
else:
    adicional_insalubridade = 0.0

# Entrada percentual adicional noturno (novo campo)
percentual_noturno = st.number_input("Percentual Adicional Noturno (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0, format="%.0f")

# Entradas de horas
horas_noturnas = st.number_input("Horas Noturnas", min_value=0.0, step=1.0)
horas_50 = st.number_input("Horas Extras 50%", min_value=0.0, step=1.0)
horas_100 = st.number_input("Horas Extras 100%", min_value=0.0, step=1.0)
horas_custom = st.number_input("Horas Extras (%) Personalizado", min_value=0.0, step=1.0)
percentual_custom = st.number_input("Percentual das Horas Extras Personalizadas (%)", min_value=0.0, max_value=200.0, value=70.0, step=1.0, format="%.0f")

# Botão de cálculo
if st.button("Calcular", key="btn_calcular"):
    operacoes = []

    base_hora = salario_base + adicional_periculosidade + adicional_insalubridade
    valor_hora_normal = base_hora / divisor_jornada if divisor_jornada > 0 else 0.0
    adicional_noturno = horas_noturnas * valor_hora_normal * (percentual_noturno / 100)

    valor_hora_50 = valor_hora_normal * 1.5
    valor_hora_100 = valor_hora_normal * 2.0
    valor_hora_custom = valor_hora_normal * (1 + percentual_custom / 100)

    total_horas_50 = horas_50 * valor_hora_50
    total_horas_100 = horas_100 * valor_hora_100
    total_horas_custom = horas_custom * valor_hora_custom

    total_adicionais = (
        adicional_periculosidade +
        adicional_insalubridade +
        adicional_noturno +
        total_horas_50 +
        total_horas_100 +
        total_horas_custom
    )

    # Detalhamento
    st.subheader("📝 Detalhamento:")
    st.write(f"🔹 Salário Base: {format_real(salario_base)}")
    st.write(f"🔹 Adicional de Periculosidade: {format_real(adicional_periculosidade)}")
    st.write(f"🔹 Adicional de Insalubridade: {format_real(adicional_insalubridade)}")
    st.write(f"🔹 Base de Cálculo da Hora: {format_real(base_hora)}")
    st.write(f"🔹 Valor da Hora Normal: {format_real(valor_hora_normal)}")

    # Cálculos exibidos de forma limpa
    st.subheader("💰 Cálculos:")
    st.write(f"🌙 Adicional Noturno ({horas_noturnas:.0f}h x {percentual_noturno:.0f}%): {format_real(adicional_noturno)}" if adicional_noturno > 0 else f"🌙 Adicional Noturno: {format_real(adicional_noturno)}")
    st.write(f"⏱️ Horas Extras 50% ({horas_50:.0f}h): {format_real(total_horas_50)} ({format_real(valor_hora_50)}/hora)" if total_horas_50 > 0 else f"⏱️ Horas Extras 50%: {format_real(total_horas_50)}")
    st.write(f"⏱️ Horas Extras 100% ({horas_100:.0f}h): {format_real(total_horas_100)} ({format_real(valor_hora_100)}/hora)" if total_horas_100 > 0 else f"⏱️ Horas Extras 100%: {format_real(total_horas_100)}")
    st.write(f"⏱️ Horas Extras {percentual_custom:.0f}% ({horas_custom:.0f}h): {format_real(total_horas_custom)} ({format_real(valor_hora_custom)}/hora)" if total_horas_custom > 0 else f"⏱️ Horas Extras {percentual_custom:.0f}%: {format_real(total_horas_custom)}")

    st.success(f"💰 Total de Adicionais: {format_real(total_adicionais)}")

    # Histórico
    st.subheader("📑 Histórico de Operações Realizadas")
    operacoes.append(f"Base de cálculo da hora normal = {format_real_sem_rs(salario_base)} + {format_real_sem_rs(adicional_periculosidade)} + {format_real_sem_rs(adicional_insalubridade)} = {format_real_sem_rs(base_hora)}")
    operacoes.append(f"Valor da hora normal = {format_real_sem_rs(base_hora)} / {divisor_jornada:.0f} = {format_real_sem_rs(valor_hora_normal)}")
    operacoes.append(f"Adicional noturno = {horas_noturnas:.0f} x {format_real_sem_rs(valor_hora_normal)} x {percentual_noturno / 100:.2f} = {format_real_sem_rs(adicional_noturno)}")
    operacoes.append(f"Valor hora 50% = {format_real_sem_rs(valor_hora_normal)} x 1.5 = {format_real_sem_rs(valor_hora_50)}")
    operacoes.append(f"Valor hora 100% = {format_real_sem_rs(valor_hora_normal)} x 2 = {format_real_sem_rs(valor_hora_100)}")
    operacoes.append(f"Valor hora {percentual_custom:.0f}% = {format_real_sem_rs(valor_hora_normal)} x {(1 + percentual_custom / 100):.2f} = {format_real_sem_rs(valor_hora_custom)}")
    operacoes.append(f"Total 50% = {horas_50:.0f} x {format_real_sem_rs(valor_hora_50)} = {format_real_sem_rs(total_horas_50)}")
    operacoes.append(f"Total 100% = {horas_100:.0f} x {format_real_sem_rs(valor_hora_100)} = {format_real_sem_rs(total_horas_100)}")
    operacoes.append(f"Total {percentual_custom:.0f}% = {horas_custom:.0f} x {format_real_sem_rs(valor_hora_custom)} = {format_real_sem_rs(total_horas_custom)}")
    operacoes.append(f"Total adicionais = {format_real_sem_rs(total_adicionais)}")

    # Dicionário com legendas explicativas
    legendas = {
        "Base de cálculo da hora normal": "fórmula: salário base + adicional de periculosidade + adicional de insalubridade",
        "Valor da hora normal": "fórmula: base de cálculo da hora normal / divisor da jornada mensal",
        "Adicional noturno": f"fórmula: horas noturnas × valor da hora normal × {percentual_noturno:.0f}%",
        "Valor hora 50%": "fórmula: valor da hora normal × 1,5",
        "Valor hora 100%": "fórmula: valor da hora normal × 2",
        f"Valor hora {percentual_custom:.0f}%": f"fórmula: valor da hora normal × {(1 + percentual_custom / 100):.2f}",
        "Total 50%": "fórmula: quantidade de horas extras 50% × valor hora 50%",
        "Total 100%": "fórmula: quantidade de horas extras 100% × valor hora 100%",
        f"Total {percentual_custom:.0f}%": f"fórmula: quantidade de horas extras {percentual_custom:.0f}% × valor hora extra",
        "Total adicionais": "fórmula: soma de todos os adicionais (periculosidade + insalubridade + noturno + extras)"
    }

    # Mostrar histórico com legendas
    for op in operacoes:
        st.write(f"- {op}")
        for chave, legenda in legendas.items():
            if op.startswith(chave):
                st.markdown(f"<span style='color:gray; font-size:0.85em'>  {legenda}</span>", unsafe_allow_html=True)
                break

    # Comparativo com prática alternativa (sem incluir periculosidade na base da hora)
    st.subheader("⚖️ Comparativo: Cálculo Alternativo (Prática Observada em Algumas Empresas)")

    if recebe_periculosidade:
        base_hora_alt = salario_base + adicional_insalubridade
        valor_hora_normal_alt = base_hora_alt / divisor_jornada if divisor_jornada > 0 else 0.0
        adicional_noturno_alt = horas_noturnas * valor_hora_normal_alt * (percentual_noturno / 100)

        valor_hora_50_alt = valor_hora_normal_alt * 1.5
        valor_hora_100_alt = valor_hora_normal_alt * 2.0
        valor_hora_custom_alt = valor_hora_normal_alt * (1 + percentual_custom / 100)

        total_50_alt = horas_50 * valor_hora_50_alt
        total_100_alt = horas_100 * valor_hora_100_alt
        total_custom_alt = horas_custom * valor_hora_custom_alt

        total_adicionais_alt = (
            adicional_periculosidade +  # Aqui está embutida a diferença
            adicional_insalubridade +
            adicional_noturno_alt +
            total_50_alt +
            total_100_alt +
            total_custom_alt
        )

        diff_noturno = adicional_noturno - adicional_noturno_alt
        diff_50 = total_horas_50 - total_50_alt
        diff_100 = total_horas_100 - total_100_alt
        diff_custom = total_horas_custom - total_custom_alt
        total_dif = diff_noturno + diff_50 + diff_100 + diff_custom

        # Histórico alternativo com legendas
        st.markdown("### 📄 Histórico do Cálculo Alternativo")

       


        # Histórico alternativo com legendas
        #st.markdown("### 📄 Histórico do Cálculo Alternativo")

        operacoes_alt = [
            f"Base de cálculo da hora normal = {format_real_sem_rs(salario_base)} + {format_real_sem_rs(adicional_insalubridade)} = {format_real_sem_rs(base_hora_alt)}",
            f"Valor da hora normal = {format_real_sem_rs(base_hora_alt)} / {divisor_jornada:.0f} = {format_real_sem_rs(valor_hora_normal_alt)}",
            f"Adicional noturno = {horas_noturnas:.0f} x {format_real_sem_rs(valor_hora_normal_alt)} x 0.2 = {format_real_sem_rs(adicional_noturno_alt)}",
                        f"Valor hora 50% = {format_real_sem_rs(valor_hora_normal_alt)} x 1.5 = {format_real_sem_rs(valor_hora_50_alt)}",
            f"Valor hora 100% = {format_real_sem_rs(valor_hora_normal_alt)} x 2 = {format_real_sem_rs(valor_hora_100_alt)}",
            f"Valor hora {percentual_custom:.0f}% = {format_real_sem_rs(valor_hora_normal_alt)} x {(1 + percentual_custom / 100):.2f} = {format_real_sem_rs(valor_hora_custom_alt)}",
            f"Total 50% = {horas_50:.0f} x {format_real_sem_rs(valor_hora_50_alt)} = {format_real_sem_rs(total_50_alt)}",
            f"Total 100% = {horas_100:.0f} x {format_real_sem_rs(valor_hora_100_alt)} = {format_real_sem_rs(total_100_alt)}",
            f"Total {percentual_custom:.0f}% = {horas_custom:.0f} x {format_real_sem_rs(valor_hora_custom_alt)} = {format_real_sem_rs(total_custom_alt)}",
            f"Total adicionais = {format_real_sem_rs(total_adicionais_alt)}"
        ]

        legendas_alt = {
            "Base de cálculo da hora normal": "fórmula: salário base + adicional de insalubridade",
            "Valor da hora normal": "fórmula: base de cálculo da hora normal / divisor da jornada mensal",
            "Adicional noturno": "fórmula: horas noturnas × valor da hora normal × 20%",
            "Valor hora 50%": "fórmula: valor da hora normal × 1,5",
            "Valor hora 100%": "fórmula: valor da hora normal × 2",
            f"Valor hora {percentual_custom:.0f}%": f"fórmula: valor da hora normal × {(1 + percentual_custom / 100):.2f}",
            "Total 50%": "fórmula: quantidade de horas extras 50% × valor hora 50%",
            "Total 100%": "fórmula: quantidade de horas extras 100% × valor hora 100%",
            f"Total {percentual_custom:.0f}%": f"fórmula: quantidade de horas extras {percentual_custom:.0f}% × valor hora extra",
            "Total adicionais": "fórmula: soma de todos os adicionais (insalubridade + noturno + extras + periculosidade)"
        }

        for linha in operacoes_alt:
            st.write(f"- {linha}")
            for chave, legenda in legendas_alt.items():
                if linha.startswith(chave):
                    st.markdown(f"<span style='color:gray; font-size:0.85em'>  {legenda}</span>", unsafe_allow_html=True)
                    break

        st.markdown("### 📌 Diferenças incorporadas na rubrica de Periculosidade")
        st.write(f"🌙 Diferença no Adicional Noturno: {format_real(diff_noturno)}")
        st.write(f"⏱️ Diferença nas Horas Extras 50%: {format_real(diff_50)}")
        st.write(f"⏱️ Diferença nas Horas Extras 100%: {format_real(diff_100)}")
        st.write(f"⏱️ Diferença nas Horas Extras {percentual_custom:.0f}%: {format_real(diff_custom)}")
        st.success(f"💡 Diferença total considerada como 'embutida' no Adicional de Periculosidade: {format_real(total_dif)}")

        # [Todo o código anterior permanece igual até...]

        # Detalhamento dos valores do cálculo alternativo
        st.subheader("📝 Detalhamento do Cálculo Alternativo:")

        st.write(f"🔹 Salário Base: {format_real(salario_base)}")
        st.write(f"🔹 Adicional de Insalubridade: {format_real(adicional_insalubridade)}")
        st.write(f"🔹 Base de Cálculo da Hora (sem periculosidade): {format_real(base_hora_alt)}")
        st.write(f"🔹 Valor da Hora Normal: {format_real(valor_hora_normal_alt)}")

        st.write(f"🌙 Adicional Noturno ({horas_noturnas:.0f}h): {format_real(adicional_noturno_alt)}")
        st.write(f"⏱️ Horas Extras 50% ({horas_50:.0f}h): {format_real(total_50_alt)} ({format_real(valor_hora_50_alt)}/hora)")
        st.write(f"⏱️ Horas Extras 100% ({horas_100:.0f}h): {format_real(total_100_alt)} ({format_real(valor_hora_100_alt)}/hora)")
        st.write(f"⏱️ Horas Extras {percentual_custom:.0f}% ({horas_custom:.0f}h): {format_real(total_custom_alt)} ({format_real(valor_hora_custom_alt)}/hora)")

        total_adic_alt_sem_peric = (
            adicional_insalubridade +
            adicional_noturno_alt +
            total_50_alt +
            total_100_alt +
            total_custom_alt
        )

# NOVA SEÇÃO ADICIONADA AQUI (fora do bloco if recebe_periculosidade)
# Adicione este código no final do seu script, DENTRO do bloco do botão "Calcular" mas FORA do if recebe_periculosidade


# NOVA SEÇÃO ADICIONADA AQUI (fora do bloco if recebe_periculosidade)
    # Adicione este código no final do seu script, DENTRO do bloco do botão "Calcular" mas FORA do if recebe_periculosidade

        st.divider()
st.subheader("📊 Cálculo de Percentual em Relação ao Salário Base")

valor_para_calcular = st.number_input(
    "Digite um valor monetário para calcular o percentual em relação ao salário base:",
    min_value=0.0, format="%.2f", key="valor_percentual"
)

if st.button("Apurar Percentual", key="btn_percentual"):
    if salario_base > 0 and valor_para_calcular > 0:
        percentual = (valor_para_calcular / salario_base) * 100
        st.success(f"{format_real_sem_rs(valor_para_calcular)} representa {percentual:.0f}% de {format_real_sem_rs(salario_base)}💰")
    elif valor_para_calcular > 0 and salario_base == 0:
        st.warning("Informe um salário base maior que zero para calcular o percentual.")
    else:
        st.info("Digite um valor acima de zero para calcular o percentual")
