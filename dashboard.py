import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='Finanças', layout='wide')

@st.cache_data
def load_data():
    file_path = 'Fatura_Valor_Total_13122016.xlsx'

    cards = [
        'Santander Platinum Visa 1132',
        'SMILES BANCO DO BRASIL 4208',
        'AmericanExpress_51000_Green',
        'AmericanExpress_78006_Platinum',
        'ITAU MASTERCARD GOLD 0655',
        'ITAU MASTERCARD PLATINUM 5798',
        'ITAU VISA GOLD 1267',
        'Santander_Master',
        'CETELEM'
    ]

    months = [
        'JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
        'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'
    ]

    invoice_data = {
        'Santander Platinum Visa 1132': [
            4776.08, 4702.96, 4018.79, 5355.41, 12891.46, 14475.42,
            10418.53, 24263.48, 26094.44, 25777.71, 25930.09, 21569.50
        ],
        'SMILES BANCO DO BRASIL 4208': [
            0, 5227.03, 5142.01, 5109.55, 5170.39, 5647.50,
            12640.19, 7820.56, 13390.90, 8290.93, 9735.91, 10091.23
        ],
        'AmericanExpress_51000_Green': [
            856.14, 1668.47, 1620.65, 2443.82, 2159.28, 2832.88,
            2530.23, 2665.81, 3337.78, 13149.55, 4772.24, 4640.23
        ],
        'AmericanExpress_78006_Platinum': [
            3216.16, 2161.00, 1306.88, 1687.32, 1737.33, 2180.21,
            2565.49, 1456.03, 1687.74, 518.44, 868.26, 1906.62
        ],
        'ITAU MASTERCARD GOLD 0655': [
            4112.93, 4858.84, 3207.03, 4270.97, 597.91, 2683.87,
            757.79, 780.79, 4915.61, 757.15, 6644.63, 6768.34
        ],
        'ITAU MASTERCARD PLATINUM 5798': [
            0, 0, 5449.79, 1864.01, 5587.77, 5905.30,
            5805.90, 6029.51, 5981.60, 5631.74, 4297.92, 4371.36
        ],
        'ITAU VISA GOLD 1267': [
            0, 3979.97, 4448.83, 1094.33, 4942.18, 281.46,
            4693.33, 1804.56, 5179.27, 1571.66, 2441.26, 2163.54
        ],
        'Santander_Master': [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 936.38
        ],
        'CETELEM': [
            151.63, 0, 361.36, 0, 268.96, 192.42,
            167.33, 0, 180.63, 0, 102.34, 141.28
        ]
    }

    payment_data = {
        'Santander Platinum Visa 1132': [
            4100.00, 1600.00, 0, 5355.41, 4780.00, 12075.42,
            9918.53, 15040.42, 12800.00, 13328.21, 14000.00, 15800.00
        ],
        'SMILES BANCO DO BRASIL 4208': [
            0, 4000.00, 1142.00, 5109.55, 5170.39, 5647.50,
            7640.19, 20850.00, 0, 8010.93, 8335.91, 11261.14
        ],
        'AmericanExpress_51000_Green': [
            0, 1668.47, 665.67, 1908.82, 2036.82, 1654.53,
            2440.23, 2665.81, 3000.00, 6007.83, 4534.03, 4633.58
        ],
        'AmericanExpress_78006_Platinum': [
            0, 2161.00, 1306.88, 1687.32, 1737.33, 2180.21,
            2565.49, 1456.03, 1687.74, 0, 868.26, 1906.62
        ],
        'ITAU MASTERCARD GOLD 0655': [
            0, 4858.84, 0, 4270.97, 0, 2683.87,
            757.79, 780.79, 4915.61, 6349.50, 6000.00, 6700.00
        ],
        'ITAU MASTERCARD PLATINUM 5798': [
            0, 2000.00, 1864.01, 5587.77, 5905.30, 805.90,
            5000.00, 5400.00, 3281.72, 3732.61, 4738.75, 0
        ],
        'ITAU VISA GOLD 1267': [
            0, 0, 3500.00, 1094.33, 4943.67, 0,
            1804.56, 0, 2928.56, 1822.79, 12223.62, 0
        ],
        'Santander_Master': [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4100.00
        ],
        'CETELEM': [0]*12
    }

    third_party_data = {
        'Santander Platinum Visa 1132': [1380.90, 638.52, 638.52, 739.43, 1444.19, 2757.34, 461.87, 2201.39, 2475.85, 0, 6119.82, 0],
        'SMILES BANCO DO BRASIL 4208': [0, 1518.71, 0, 0, 321.00, 360.00, 800.06, 0, 1460.87, 389.10, 389.10, 389.10],
        'AmericanExpress_51000_Green': [370.77, 481.02, 370.77, 1029.39, 523.36, 725.69, 997.75, 1024.75, 1613.12, 10456.54, 3122.68, 2725.68],
        'AmericanExpress_78006_Platinum': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 615.52, 426.36],
        'ITAU MASTERCARD GOLD 0655': [0]*12,
        'ITAU MASTERCARD PLATINUM 5798': [0, 0, 0, 0, 171.44, 0, 0, 0, 0, 0, 511.67, 358.20],
        'ITAU VISA GOLD 1267': [0, 0, 0, 783.15, 0, 0, 0, 0, 833.34, 833.34, 505.63, 0],
        'Santander_Master': [0]*12,
        'CETELEM': [0]*12
    }

    own_resources_data = {
        'Santander Platinum Visa 1132':[ -704.82, 2464.44, 2319.23, -3200.31, 4667.76, -948.15, -380.04, 6603.50, 10718.72, 12349.63, 5810.27, 5769.50],
        'SMILES BANCO DO BRASIL 4208':[0, -291.68, 4000.01, -5491.39, -360.00, 4199.94, -13029.44, 11930.03, -109.10, 1010.90, -1559.01, 0],
        'AmericanExpress_51000_Green':[99.77, -1275.18, -370.77, -2185.58, -1617.36, -2526.62, -2077.80, -2459.87, -2578.91, -4922.65, -4017.73, -3621.12],
        'AmericanExpress_78006_Platinum':[20.51, -2139.98, -1285.86, -1640.16, -1716.31, -2159.19, -2265.33, -1433.99, -1665.70, 11.53, -1472.25, -1383.01],
        'ITAU MASTERCARD GOLD 0655': [4112.93, 0, 3207.03, 0, 597.91, 0, 0, 0, 0, -5592.35, 644.63, 68.34],
        'ITAU MASTERCARD PLATINUM 5798':[0, 0, 3449.79, 0, -171.44, 5000.00, 1029.51, 581.60, 2350.02, 53.64, -725.59, 0],
        'ITAU VISA GOLD 1267':[0, 3979.97, 948.83, -783.15, -1.49, 281.46, 4693.33, 0, 4345.93, -2190.24, 112.84, -10060.08],
        'Santander_Master': [151.63, 0, 361.36, 0, 268.96, 192.42, 167.33, 0, 180.63, 0, 102.34, 141.28],
        'CETELEM': [151.63, 0, 361.36, 0, 268.96, 192.42, 167.33, 0, 180.63, 0, 102.34, 141.28]
    }

    data = []
    for card in cards:
        for i, month in enumerate(months):
            inv = invoice_data.get(card, [0]*12)[i]
            pay = payment_data.get(card, [0]*12)[i]
            thr = third_party_data.get(card, [0]*12)[i]
            own = own_resources_data.get(card, [0]*12)[i]
            ratio = pay / inv if inv != 0 else 0
            data.append({
                'Card': card,
                'Month': month,
                'Total_Invoice': inv,
                'Total_Payments': pay,
                'Third_Party_Expenses': thr,
                'Own_Resources': own,
                'Payment_Ratio': ratio
            })

    df = pd.DataFrame(data)
    df[['Total_Invoice','Total_Payments','Third_Party_Expenses','Own_Resources','Payment_Ratio']] = df[['Total_Invoice','Total_Payments','Third_Party_Expenses','Own_Resources','Payment_Ratio']].apply(pd.to_numeric, errors='coerce').fillna(0)
    df['Month'] = pd.Categorical(df['Month'], categories=months, ordered=True)

    annual_summary = df.groupby('Card').agg({
        'Total_Invoice': 'sum',
        'Total_Payments': 'sum',
        'Third_Party_Expenses': 'sum',
        'Own_Resources': 'sum'
    }).reset_index().rename(columns={
        'Third_Party_Expenses': 'Total_Terceiros',
        'Own_Resources': 'Total_Proprios'
    })

    return df, cards, months, annual_summary

df, cards, months, annual_summary = load_data()

st.title('Finanças')
st.header('Filtros')
col1, col2 = st.columns(2)
with col1:
    selected_cards = st.multiselect('Selecionar Cartões de Crédito', options=cards, default=cards)
with col2:
    selected_months = st.multiselect('Selecionar Meses', options=months, default=months)

if not selected_cards or not selected_months:
    st.warning('Selecione pelo menos um cartão e um mês para exibir os gráficos.')
else:
    filtered_df = df[df['Card'].isin(selected_cards) & df['Month'].isin(selected_months)]

    st.header('Resumo Anual por Cartão')
    display_summary = annual_summary[annual_summary['Card'].isin(selected_cards)].rename(columns={
        'Total_Invoice': 'Total fatura',
        'Total_Payments': 'Total pago com cartão',
        'Total_Terceiros': 'Total pago com recursos de terceiros',
        'Total_Proprios': 'Total pago com recursos próprios'
    }).style.format({
        'Total fatura': 'R${:,.2f}',
        'Total pago com cartão': 'R${:,.2f}',
        'Total pago com recursos de terceiros': 'R${:,.2f}',
        'Total pago com recursos próprios': 'R${:,.2f}'
    })
    st.dataframe(display_summary, use_container_width=True)

    for card in selected_cards:
        st.header(card)
        card_data = filtered_df[filtered_df['Card'] == card]
        if card_data.empty:
            st.write('Nenhum dado disponível para os meses selecionados.')
            continue

        fig = go.Figure()
        fig.add_trace(go.Bar(x=card_data['Month'], y=card_data['Total_Invoice'], name='Fatura Total', text=[f'R${val:,.2f}' for val in card_data['Total_Invoice']], textposition='auto', width=0.2))
        fig.add_trace(go.Bar(x=card_data['Month'], y=card_data['Total_Payments'], name='Pagamentos Totais', text=[f'R${val:,.2f}' for val in card_data['Total_Payments']], textposition='auto', width=0.2))
        if card_data['Third_Party_Expenses'].sum() > 0:
            fig.add_trace(go.Bar(x=card_data['Month'], y=card_data['Third_Party_Expenses'], name='Despesas de Terceiros', text=[f'R${val:,.2f}' for val in card_data['Third_Party_Expenses']], textposition='auto', width=0.2))
        if card_data['Own_Resources'].sum() != 0:
            fig.add_trace(go.Bar(x=card_data['Month'], y=card_data['Own_Resources'], name='Recursos Próprios', text=[f'R${val:,.2f}' for val in card_data['Own_Resources']], textposition='auto', width=0.2))
        fig.add_trace(go.Scatter(x=card_data['Month'], y=card_data['Payment_Ratio'], name='Proporção Pagamento/Fatura', yaxis='y2', mode='lines+markers', line=dict(color='red', width=2), marker=dict(size=8)))

        fig.update_layout(
            title=f'{card} - Análise Financeira por Mês',
            xaxis_title='Mês', yaxis_title='Valor (R$)',
            yaxis2=dict(title='Proporção Pagamento/Fatura', overlaying='y', side='right', range=[0, max(1.5, card_data['Payment_Ratio'].max() * 1.1)]),
            barmode='group', template='plotly_white', height=600, width=1000,
            xaxis_tickangle=45, bargap=0.3, bargroupgap=0.05,
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.5)', bordercolor='black', borderwidth=1)
        )
        st.plotly_chart(fig, use_container_width=True)
