import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import io
import os
import plotly.graph_objects as go
import plotly.io as pio
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

os.environ["BROWSER_PATH"] = "/usr/bin/chromium"

st.set_page_config(page_title="Finanças", layout="wide")

@st.cache_data
def load_data():
    cards = [
        "Santander Platinum Visa 1132",
        "SMILES BANCO DO BRASIL 4208",
        "AmericanExpress_51000_Green",
        "AmericanExpress_78006_Platinum",
        "ITAU MASTERCARD GOLD 0655",
        "ITAU MASTERCARD PLATINUM 5798",
        "ITAU VISA GOLD 1267",
        "Santander_Master",
        "CETELEM",
    ]

    months = [
        "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
        "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO",
    ]

    invoice_data = {
        "Santander Platinum Visa 1132": [4776.08, 4702.96, 4018.79, 5355.41, 12891.46, 14475.42, 10418.53, 24263.48, 26094.44, 25777.71, 25930.09, 21569.50],
        "SMILES BANCO DO BRASIL 4208": [0, 5227.03, 5142.01, 5109.55, 5170.39, 5647.50, 12640.19, 7820.56, 13390.90, 8290.93, 9735.91, 10091.23],
        "AmericanExpress_51000_Green": [856.14, 1668.47, 1620.65, 2443.82, 2159.28, 2832.88, 2530.23, 2665.81, 3337.78, 13149.55, 4772.24, 4640.23],
        "AmericanExpress_78006_Platinum": [3216.16, 2161.00, 1306.88, 1687.32, 1737.33, 2180.21, 2565.49, 1456.03, 1687.74, 518.44, 868.26, 1906.62],
        "ITAU MASTERCARD GOLD 0655": [4112.93, 4858.84, 3207.03, 4270.97, 597.91, 2683.87, 757.79, 780.79, 4915.61, 757.15, 6644.63, 6768.34],
        "ITAU MASTERCARD PLATINUM 5798": [0, 0, 5449.79, 1864.01, 5587.77, 5905.30, 5805.90, 6029.51, 5981.60, 5631.74, 4297.92, 4371.36],
        "ITAU VISA GOLD 1267": [0, 3979.97, 4448.83, 1094.33, 4942.18, 281.46, 4693.33, 1804.56, 5179.27, 1571.66, 2441.26, 2163.54],
        "Santander_Master": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 936.38],
        "CETELEM": [151.63, 0, 361.36, 0, 268.96, 192.42, 167.33, 0, 180.63, 0, 102.34, 141.28],
    }

    payment_data = {
        "Santander Platinum Visa 1132": [4100.00, 1600.00, 0, 5355.41, 4780.00, 12075.42, 9918.53, 15040.42, 12800.00, 13328.21, 14000.00, 15800.00],
        "SMILES BANCO DO BRASIL 4208": [0, 4000.00, 1142.00, 5109.55, 5170.39, 5647.50, 7640.19, 20850.00, 0, 8010.93, 8335.91, 11261.14],
        "AmericanExpress_51000_Green": [0, 1668.47, 665.67, 1908.82, 2036.82, 1654.53, 2440.23, 2665.81, 3000.00, 6007.83, 4534.03, 4633.58],
        "AmericanExpress_78006_Platinum": [0, 2161.00, 1306.88, 1687.32, 1737.33, 2180.21, 2565.49, 1456.03, 1687.74, 0, 868.26, 1906.62],
        "ITAU MASTERCARD GOLD 0655": [0, 4858.84, 0, 4270.97, 0, 2683.87, 757.79, 780.79, 4915.61, 6349.50, 6000.00, 6700.00],
        "ITAU MASTERCARD PLATINUM 5798": [0, 0, 2000.00, 1864.01, 5587.77, 5905.30, 805.90, 5000.00, 5400.00, 3281.72, 3732.61, 4738.75],
        "ITAU VISA GOLD 1267": [0, 0, 3500.00, 1094.33, 4943.67, 0, 0,1804.56, 0, 2928.56, 1822.79, 12223.62],
        "Santander_Master": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4100.00],
        "CETELEM": [0] * 12,
    }

    third_party_data = {
        "Santander Platinum Visa 1132": [1380.90, 638.52, 638.52, 739.43, 1444.19, 2757.34, 461.87, 2201.39, 2475.85, 0, 6119.82, 0],
        "SMILES BANCO DO BRASIL 4208": [0, 1518.71, 0, 0, 321.00, 360.00, 800.06, 0, 1460.87, 389.10, 389.10, 389.10],
        "AmericanExpress_51000_Green": [370.77, 481.02, 370.77, 1029.39, 523.36, 725.69, 997.75, 1024.75, 1613.12, 10456.54, 3122.68, 2725.68],
        "AmericanExpress_78006_Platinum": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 615.52, 426.36],
        "ITAU MASTERCARD GOLD 0655": [0] * 12,
        "ITAU MASTERCARD PLATINUM 5798": [0, 0, 0, 0, 171.44, 0, 0, 0, 0, 0, 511.67, 358.20],
        "ITAU VISA GOLD 1267": [0, 0, 0, 783.15, 0, 0, 0, 0, 833.34, 833.34, 505.63, 0],
        "Santander_Master": [0] * 12,
        "CETELEM": [0] * 12,
    }

    own_resources_data = {
        "Santander Platinum Visa 1132": [-704.82, 2464.44, 2319.23, -3200.31, 4667.76, -948.15, -380.04, 6603.50, 10718.72, 12349.63, 5810.27, 5769.50],
        "SMILES BANCO DO BRASIL 4208": [0, -291.68, 4000.01, -5491.39, -360.00, 4199.94, -13029.44, 11930.03, -109.10, 1010.90, -1559.01, 0],
        "AmericanExpress_51000_Green": [99.77, -1275.18, -370.77, -2185.58, -1617.36, -2526.62, -2077.80, -2459.87, -2578.91, -4922.65, -4017.73, -3621.12],
        "AmericanExpress_78006_Platinum": [20.51, -2139.98, -1285.86, -1640.16, -1716.31, -2159.19, -2265.33, -1433.99, -1665.70, 11.53, -1472.25, -1383.01],
        "ITAU MASTERCARD GOLD 0655": [4112.93, 0, 3207.03, 0, 597.91, 0, 0, 0, 0, -5592.35, 644.63, 68.34],
        "ITAU MASTERCARD PLATINUM 5798": [0, 0, 3449.79, 0, -171.44, 5000.00, 1029.51, 581.60, 2350.02, 53.64, -725.59, 0],
        "ITAU VISA GOLD 1267": [0, 3979.97, 948.83, -783.15, -1.49, 281.46, 4693.33, 0, 4345.93, -2190.24, 112.84, -10060.08],
        "Santander_Master": [151.63, 0, 361.36, 0, 268.96, 192.42, 167.33, 0, 180.63, 0, 102.34, 141.28],
        "CETELEM": [151.63, 0, 361.36, 0, 268.96, 192.42, 167.33, 0, 180.63, 0, 102.34, 141.28],
    }


    payment_cards_used = {
        "Santander Platinum Visa 1132": [
            "Itaú Master Gold",
            "Itaú Visa Gold",
            "-",
            "Cartão Smiles / Itaú Master Platinum",
            "Cartão Smiles / Itaú Master Platinum",
            "Cartão Smiles / Itaú Master Platinum",
            "Cartão Smiles / Itaú Master Platinum",
            "Itaú Visa Gold / Cartão Smiles / Itaú Master Platinum",
            "Cartão Smiles / Itaú Master Platinum",
            "Itaú Master Gold / Cartão Smiles",
            "Cartão Smiles / Itaú Master Gold",
            "Cartão Smiles / Itaú Master Gold",
        ],
        "SMILES BANCO DO BRASIL 4208": [
            "-",
            "Itaú Master Platinum",
            "Itaú Master Gold",
            "Itaú Visa Gold / Santander Platinum",
            "Santander Platinum",
            "Itaú Visa Gold / Santander Platinum",
            "Santander Platinum / Santander Platinum Visa",
            "Itaú Master Gold / Santander Platinum Visa",
            "Santander Platinum Visa",
            "Santander Platinum",
            "Santander Platinum",
            "Santander Platinum Master / Itaú Visa Gold",
        ],
        "AmericanExpress_51000_Green": [
            "-",
            "Itaú Visa Gold",
            "Itaú Master Platinum",
            "Santander Platinum",
            "Santander Platinum",
            "Santander Platinum",
            "Santander Platinum",
            "Santander Platinum",
            "Santander Platinum",
            "Santander Platinum / Cartão Smiles / Itaú Master Platinum",
            "Santander Platinum",
            "Itaú Visa Gold",
        ],
        "AmericanExpress_78006_Platinum": [
            "-",
            "Itaú Master Gold",
            "Cartão Smiles",
            "Santander Platinum",
            "Itaú Master Platinum",
            "Santander Platinum",
            "Itaú Master Platinum",
            "Santander Platinum",
            "Santander Platinum Visa",
            "-",
            "Itaú Visa Gold",
            "Santander Platinum Visa",
        ],
        "ITAU MASTERCARD GOLD 0655": [
            "-",
            "Cartão Smiles",
            "-",
            "Santander Platinum Visa",
            "Itaú Master Platinum",
            "Santander Platinum Visa",
            "Santander Platinum Visa",
            "Santander Platinum Visa",
            "Santander Platinum Visa",
            "Santander Platinum Visa",
            "Santander Platinum Visa",
            "Santander Platinum Visa",
        ],
        "ITAU MASTERCARD PLATINUM 5798": [
            "-",
            "-",
            "Itaú Master Gold",
            "Santander Platinum Visa",
            "Cartão Smiles / Itaú Master Gold",
            "Santander Platinum Visa / Cartão Smiles",
            "Santander Platinum Visa",
            "Cartao Smiles",
            "Santander Platinum Visa",
            "Santander Platinum Visa",
            "Santander Platinum Visa / Cartão Smiles",
            "Santander Platinum Visa / Santander Platinum Master",
        ],
        "ITAU VISA GOLD 1267": [
            "-",
            "-",
            "Cartão Smiles",
            "Santander Platinum Visa",
            "Santander Platinum Visa",
            "-",
            "-",
            "Santander Platinum Visa",
            "-",
            "Santander Platinum Visa / Cartão Smiles",
            "Santander Platinum Visa",
            "Santander Platinum Master / Santander Platinum Visa",
        ],
        "Santander_Master": [
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "Itaú Master Platinum",
        ],
        "CETELEM": ["-"] * 12,
    }


    recs = []
    for card in cards:
        for i, m in enumerate(months):
            inv  = invoice_data.get(card, [0]*12)[i]
            pay  = payment_data.get(card, [0]*12)[i]
            thr  = third_party_data.get(card, [0]*12)[i]
            own  = own_resources_data.get(card, [0]*12)[i]
            pr   = pay / inv if inv else 0
            used = payment_cards_used.get(card, ["-"]*12)[i]
            recs.append(
                dict(Card=card, Month=m,
                     Total_Invoice=inv, Total_Payments=pay,
                     Third_Party_Expenses=thr, Own_Resources=own,
                     Payment_Ratio=pr, Payment_Cards=used)
            )
    df = pd.DataFrame(recs)
    numeric = ["Total_Invoice","Total_Payments","Third_Party_Expenses","Own_Resources","Payment_Ratio"]
    df[numeric] = df[numeric].apply(pd.to_numeric).fillna(0)
    df["Month"] = pd.Categorical(df["Month"], categories=months, ordered=True)

    annual = (
        df.groupby("Card")[["Total_Invoice","Total_Payments","Third_Party_Expenses","Own_Resources"]]
        .sum().reset_index()
    )
    return df, cards, months, annual


def build_pdf(summary_df: pd.DataFrame, fig_all, card_items):
    """
    summary_df  : DataFrame resumo anual (index = Card)
    fig_all     : gráfico geral (plotly Figure)
    card_items  : lista de tuples (card_name, monthly_table_df, monthly_fig)
    """
    buf = io.BytesIO()
    pdf = canvas.Canvas(buf, pagesize=landscape(letter))
    pw, ph = landscape(letter)

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(40, ph-40, "Finanças – Resumo Anual")
    pdf.setFont("Courier", 8)

    tbl_str = summary_df.to_string(col_space=14, justify="left",
                                   formatters={c:lambda x:f"{x:,.2f}" for c in summary_df.columns})
    y = ph - 70
    for line in tbl_str.splitlines():
        pdf.drawString(40, y, line)
        y -= 10
    pdf.showPage()

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, ph-40, "Visão Geral Anual por Cartão")
    img_all = pio.to_image(fig_all, format="png", width=1400, height=600, scale=2)
    pdf.drawImage(ImageReader(io.BytesIO(img_all)),
                  40, ph-560, width=pw-80, height=520, preserveAspectRatio=True)
    pdf.showPage()

    for card, tbl_df, fig in card_items:
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(40, ph-40, f"{card} – Dados Mensais")
        pdf.setFont("Courier", 7.5)
        tbl_str = tbl_df.to_string(index=False, col_space=11,
                                   formatters={
                                       "Total_Invoice":        lambda x:f"{x:,.2f}",
                                       "Total_Payments":       lambda x:f"{x:,.2f}",
                                       "Third_Party_Expenses": lambda x:f"{x:,.2f}",
                                       "Own_Resources":        lambda x:f"{x:,.2f}",
                                   })
        y = ph - 70
        for line in tbl_str.splitlines():
            pdf.drawString(40, y, line)
            y -= 9.5
        pdf.showPage()
        
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(40, ph-40, f"{card} – Gráfico Mensal")
        img = pio.to_image(fig, format="png", width=1400, height=600, scale=2)
        pdf.drawImage(ImageReader(io.BytesIO(img)),
                      40, ph-560, width=pw-80, height=520, preserveAspectRatio=True)
        pdf.showPage()

    pdf.save()
    buf.seek(0)
    return buf

df, cards, months, annual = load_data()

st.title("Finanças")

col1, col2 = st.columns(2)
with col1:
    selected_cards = st.multiselect("Selecionar Cartões", cards, default=cards)
with col2:
    selected_months = st.multiselect("Selecionar Meses", months, default=months)

if not selected_cards or not selected_months:
    st.warning("Selecione pelo menos um cartão e um mês")
    st.stop()

f_df = df[df["Card"].isin(selected_cards) & df["Month"].isin(selected_months)]
f_annual = annual[annual["Card"].isin(selected_cards)]

st.header("Resumo Anual por Cartão")
resum = f_annual.rename(columns={
    "Card": "Cartão de Crédito",
    "Total_Invoice": "Valor total da fatura",
    "Total_Payments": "Valor pago com cartão de crédito",
    "Third_Party_Expenses": "Valor pago por terceiros",
    "Own_Resources": "Valor pago com recursos próprios",
})
num_cols = ["Valor total da fatura","Valor pago com cartão de crédito","Valor pago por terceiros","Valor pago com recursos próprios"]
st.dataframe(resum.style.format({c:"R${:,.2f}" for c in num_cols}),
             use_container_width=True)

st.header("Gráfico Geral por Cartão")
fig_all = go.Figure()
fig_all.add_trace(go.Bar(x=resum["Cartão de Crédito"], y=resum["Valor total da fatura"], name="Valor total da fatura"))
fig_all.add_trace(go.Bar(x=resum["Cartão de Crédito"], y=resum["Valor pago com cartão de crédito"], name="Pagamentos com cartão de crédito"))
fig_all.add_trace(go.Bar(x=resum["Cartão de Crédito"], y=resum["Valor pago por terceiros"], name="Valor pago por terceiros"))
fig_all.add_trace(go.Bar(x=resum["Cartão de Crédito"], y=resum["Valor pago com recursos próprios"], name="Valor pago com recursos próprios"))
fig_all.update_layout(barmode="group", template="plotly_white",
                      xaxis_title="Cartão", yaxis_title="Valor (R$)", height=500)
st.plotly_chart(fig_all, use_container_width=True)

card_items = []

for card in selected_cards:
    st.subheader(card)
    cd = f_df[f_df["Card"] == card]
    if cd.empty:
        st.write("Nenhum dado para meses selecionados")
        continue

    tbl_stream = cd[["Month","Total_Invoice","Total_Payments",
                     "Third_Party_Expenses","Own_Resources"]].rename(columns={
        "Month":"Mês","Total_Invoice":"Valor total da fatura","Total_Payments":"Valor pago com cartão de crédito",
        "Third_Party_Expenses":"Valor pago por terceiros","Own_Resources":"Valor pago com recursos próprios"})
    st.dataframe(
        tbl_stream.style.format({"Valor total da fatura":"R${:,.2f}",
                                 "Valor pago com cartão de crédito":"R${:,.2f}",
                                 "Valor pago por terceiros":"R${:,.2f}",
                                 "Valor pago com recursos próprios":"R${:,.2f}"}),
        use_container_width=True,
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(x=cd["Month"], y=cd["Total_Invoice"],
                         name="Valor total da fatura", width=0.22,
                         hovertemplate="<b>%{x}</b><br>Valor total da fatura: R$ %{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Bar(x=cd["Month"], y=cd["Total_Payments"],
                         name="Pagamentos com cartão de crédito", width=0.22,
                         customdata=cd["Payment_Cards"],
                         hovertemplate="<b>%{x}</b><br>Pagamentos: R$ %{y:,.2f}"
                                       "<br><b>Cartões usados:</b> %{customdata}<extra></extra>"))
    fig.add_trace(go.Bar(x=cd["Month"], y=cd["Third_Party_Expenses"],
                         name="Valor pago por terceiros", width=0.22,
                         hovertemplate="<b>%{x}</b><br>Terceiros: R$ %{y:,.2f}<extra></extra>"))
    fig.add_trace(go.Bar(x=cd["Month"], y=cd["Own_Resources"],
                         name="Valor pago com recursos próprios", width=0.22,
                         hovertemplate="<b>%{x}</b><br>Valor pago com recursos próprios: R$ %{y:,.2f}<extra></extra>"))
    fig.update_layout(barmode="group", template="plotly_white",
                      xaxis_tickangle=45, yaxis_title="Valor (R$)", height=550)
    st.plotly_chart(fig, use_container_width=True)

    tbl_pdf = cd[["Month","Total_Invoice","Total_Payments",
                  "Third_Party_Expenses","Own_Resources"]].copy()
    card_items.append((card, tbl_pdf, fig))

st.markdown("---")
if st.button("Exportar PDF"):
    try:
        sum_pdf = resum.set_index("Cartão de Crédito")[["Valor total da fatura","Valor pago com cartão de crédito","Valor pago por terceiros","Valor pago com recursos próprios"]]
        pdf_file = build_pdf(sum_pdf, fig_all, card_items)
        st.download_button("Baixar PDF", pdf_file,
                           file_name="financas_dashboard.pdf",
                           mime="application/pdf", use_container_width=True)
    except Exception as exc:
        st.error(f"Falha ao gerar PDF.\nVerifique se *kaleido* e *reportlab* estão instalados.\n\n{exc}")