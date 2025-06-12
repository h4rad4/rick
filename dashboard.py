import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Finanças", layout="wide")

@st.cache_data
def load_data():
    file_path = "Fatura_Valor_Total_13122016.xlsx"
    
    cards = [
        "Santander Platinum Visa 1132",
        "SMILES BANCO DO BRASIL 4208",
        "AmericanExpress_51000_Green",
        "AmericanExpress_78006_Platinum",
        "ITAU MASTERCARD GOLD 0655",
        "ITAU MASTERCARD PLATINUM 5798",
        "ITAU VISA GOLD 1267",
        "Santander_Master",
        "CETELEM"
    ]
    
    months = [
        "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
        "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
    ]
    
    invoice_data = {
        "Santander Platinum Visa 1132": [
            4776.08, 4702.96, 4018.79, 5355.41, 12891.46, 14475.42, 10418.53, 24263.48,
            26094.44, 25777.71, 25930.09, 21569.50, 17771.14
        ],
        "SMILES BANCO DO BRASIL 4208": [
            0, 5227.03, 5142.01, 5109.55, 5170.39, 5647.50, 12640.19, 7820.56,
            13390.90, 8290.93, 9735.91, 10091.23
        ],
        "AmericanExpress_51000_Green": [
            856.14, 1668.47, 1620.65, 2443.82, 2159.28, 2832.88, 2530.23, 2665.81,
            3337.78, 13149.55, 4772.24, 4640.23
        ],
        "AmericanExpress_78006_Platinum": [
            3216.16, 2161.00, 1306.88, 1687.32, 1737.33, 2180.21, 2565.49, 1456.03,
            1687.74, 518.44, 868.26, 1906.62
        ],
        "ITAU MASTERCARD GOLD 0655": [
            4112.93, 4858.84, 3207.03, 4270.97, 597.91, 2683.87, 757.79, 780.79,
            4915.61, 757.15, 6644.63, 6768.34
        ],
        "ITAU MASTERCARD PLATINUM 5798": [
            0, 0, 5449.79, 1864.01, 5587.77, 5905.30, 5805.90, 6029.51,
            5981.60, 5631.74, 4297.92, 4371.36
        ],
        "ITAU VISA GOLD 1267": [
            0, 3979.97, 4448.83, 1094.33, 4942.18, 281.46, 4693.33, 1804.56,
            5179.27, 1571.66, 2441.26, 2163.54
        ],
        "Santander_Master": [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 936.38
        ],
        "CETELEM": [
            151.63, 0, 361.36, 0, 268.96, 192.42, 167.33, 0, 180.63, 0, 102.34, 141.28, 0
        ]
    }
    
    payment_data = {
        "Santander Platinum Visa 1132": [
            4100.00, 1600.00, 0, 5355.41, 4780.00, 12075.42, 9918.53, 15040.42,
            12800.00, 13328.21, 14000.00, 15800.00, 0
        ],
        "SMILES BANCO DO BRASIL 4208": [
            0, 4000.00, 1142.00, 5109.55, 5170.39, 5647.50, 7640.19, 20850.00,
            0, 8010.93, 8335.91, 11261.14, 0
        ],
        "AmericanExpress_51000_Green": [
            0, 1668.47, 665.67, 1908.82, 2036.82, 1654.53, 2440.23, 2665.81,
            3000.00, 6007.83, 4534.03, 4633.58, 0
        ],
        "AmericanExpress_78006_Platinum": [
            0, 2161.00, 1306.88, 1687.32, 1737.33, 2180.21, 2565.49, 1456.03,
            1687.74, 0, 868.26, 1906.62, 0
        ],
        "ITAU MASTERCARD GOLD 0655": [
            0, 4858.84, 0, 4270.97, 0, 2683.87, 757.79, 780.79,
            4915.61, 6349.50, 6000.00, 6700.00, 0
        ],
        "ITAU MASTERCARD PLATINUM 5798": [
            0, 2000.00, 1864.01, 5587.77, 5905.30, 805.90, 5000.00, 5400.00,
            3281.72, 3732.61, 4738.75, 0, 0
        ],
        "ITAU VISA GOLD 1267": [
            0, 0, 3500.00, 1094.33, 4943.67, 0, 1804.56, 0,
            2928.56, 1822.79, 12223.62, 0, 0
        ],
        "Santander_Master": [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4100.00, 0
        ],
        "CETELEM": [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
    }
    
    third_party_data: dict[str, list[float | int] | list[int]] = {
        "Santander Platinum Visa 1132": [
            1380.90, 638.52, 638.52, 739.43, 1444.19, 2757.34, 461.87, 2201.39,
            2475.85, 0, 6119.82, 0, 0
        ],
        "SMILES BANCO DO BRASIL 4208": [
            0, 1518.71, 0, 321.00, 360.00, 800.06, 0, 1460.87,
            389.10, 389.10, 389.10, 0, 0
        ],
        "AmericanExpress_51000_Green": [
            370.77, 481.02, 370.77, 1029.39, 523.36, 725.69, 997.75, 1024.75,
            1613.12, 10456.54, 3122.68, 2725.68, 0
        ],
        "AmericanExpress_78006_Platinum": [
            0, 0, 0, 0, 0, 0, 615.52, 426.36, 0, 0, 0, 0, 0
        ],
        "ITAU MASTERCARD GOLD 0655": [0]*13,
        "ITAU MASTERCARD PLATINUM 5798": [
            0, 0, 171.44, 0, 0, 0, 0, 511.67, 358.20, 0, 0, 0, 0
        ],
        "ITAU VISA GOLD 1267": [
            0, 0, 783.15, 0, 0, 0, 833.34, 833.34, 505.63, 0, 0, 0, 0
        ],
        "Santander_Master": [0]*13,
        "CETELEM": [0]*13
    }
    
    data = []
    for card in cards:
        for i, month in enumerate(months):
            invoice = invoice_data.get(card, [0]*12)[i]
            payment = payment_data.get(card, [0]*12)[i]
            third_party = third_party_data.get(card, [0]*12)[i]
            ratio = payment / invoice if invoice != 0 else 0
            data.append({
                "Card": card,
                "Month": month,
                "Total_Invoice": invoice,
                "Total_Payments": payment,
                "Third_Party_Expenses": third_party,
                "Payment_Ratio": ratio
            })
    
    df = pd.DataFrame(data)
    
    df["Total_Invoice"] = pd.to_numeric(df["Total_Invoice"], errors="coerce").fillna(0)
    df["Total_Payments"] = pd.to_numeric(df["Total_Payments"], errors="coerce").fillna(0)
    df["Third_Party_Expenses"] = pd.to_numeric(df["Third_Party_Expenses"], errors="coerce").fillna(0)
    df["Payment_Ratio"] = pd.to_numeric(df["Payment_Ratio"], errors="coerce").fillna(0)
    
    df["Month"] = pd.Categorical(df["Month"], categories=months, ordered=True)
    
    annual_summary = df.groupby("Card").agg({
        "Total_Invoice": "sum",
        "Total_Payments": "sum"
    }).reset_index()
    annual_summary["Personal_Funds"] = annual_summary["Total_Invoice"] - annual_summary["Total_Payments"]
    
    return df, cards, months, annual_summary

df, cards, months, annual_summary = load_data()

st.title("Finanças")

st.header("Filtros")
col1, col2 = st.columns(2)

with col1:
    selected_cards = st.multiselect("Selecionar Cartões de Crédito", options=cards, default=cards)
with col2:
    selected_months = st.multiselect("Selecionar Meses", options=months, default=months)

if not selected_cards or not selected_months:
    st.warning("Selecione pelo menos um cartão e um mês para exibir os gráficos.")
else:
    filtered_df = df[
        (df["Card"].isin(selected_cards)) &
        (df["Month"].isin(selected_months))
    ]
    
    st.header("Resumo Anual por Cartão")
    filtered_summary = annual_summary[annual_summary["Card"].isin(selected_cards)]
    st.dataframe(
        filtered_summary.style.format({
            "Total_Invoice": "R${:,.2f}",
            "Total_Payments": "R${:,.2f}",
            "Personal_Funds": "R${:,.2f}"
        }),
        use_container_width=True
    )
    

    for card in selected_cards:
        st.header(card)
        
        card_data = filtered_df[filtered_df["Card"] == card]
        
        if card_data.empty:
            st.write("Nenhum dado disponível para os meses selecionados.")
            continue
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                x=card_data["Month"],
                y=card_data["Total_Invoice"],
                name="Fatura Total",
                marker_color="blue",
                text=[f"R${val:,.2f}" if val > 0 else "" for val in card_data["Total_Invoice"]],
                textposition="auto",
                width=0.267
            )
        )
        
        fig.add_trace(
            go.Bar(
                x=card_data["Month"],
                y=card_data["Total_Payments"],
                name="Pagamentos Totais",
                marker_color="orange",
                text=[f"R${val:,.2f}" if val > 0 else "" for val in card_data["Total_Payments"]],
                textposition="auto",
                width=0.267
            )
        )
        
        if card_data["Third_Party_Expenses"].sum() > 0:
            fig.add_trace(
                go.Bar(
                    x=card_data["Month"],
                    y=card_data["Third_Party_Expenses"],
                    name="Despesas de Terceiros",
                    marker_color="green",
                    text=[f"R${val:,.2f}" if val > 0 else "" for val in card_data["Third_Party_Expenses"]],
                    textposition="auto",
                    width=0.267
                )
            )
        
        fig.add_trace(
            go.Scatter(
                x=card_data["Month"],
                y=card_data["Payment_Ratio"],
                name="Proporção Pagamento/Fatura",
                yaxis="y2",
                mode="lines+markers",
                line=dict(color="red", width=2),
                marker=dict(size=8)
            )
        )


        fig.update_layout(
            title=f"{card} - Análise Financeira por Mês",
            xaxis_title="Mês",
            yaxis_title="Valor (R$)",
            yaxis2=dict(
                title="Proporção Pagamento/Fatura",
                overlaying="y",
                side="right",
                range=[0, max(1.5, card_data["Payment_Ratio"].max() * 1.1)]
            ),
            barmode="group",
            template="plotly_white",
            height=600,
            width=1000,
            xaxis_tickangle=45,
            bargap=0.3,
            bargroupgap=0.05,
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor="rgba(255, 255, 255, 0.5)",
                bordercolor="black",
                borderwidth=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)