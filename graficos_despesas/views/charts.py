import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from graficos_despesas.data_base.DataQuerys import DataQuerys
import altair as alt
import plotly.express as px



class Charts:
    def __init__(self, data):
        self.data = data
        self.data["data_evento"] = pd.to_datetime(data["data_evento"])
        self.data["mes_ano"] = data["data_evento"].dt.to_period("M")
        self.resumo_mensal = data.groupby("mes_ano")["valor"].agg(["sum", "mean"]).reset_index()
        self.resumo_mensal["mes_ano"] = self.resumo_mensal["mes_ano"].dt.to_timestamp()

    def __enter__(self):
        # Inicialização do objeto
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Limpeza do objeto
        pass




def __make_charts_pizza():
    data = DataQuerys().pizza_query()
    data2 = DataQuerys().pizza_query()

    # Calcular o total para os percentuais
    total = data['total_valor'].sum()
    total2 = data2['total_valor'].sum()

    # Calcular o percentual de cada categoria
    data['percentual'] = (data['total_valor'] / total) * 100
    data2['percentual'] = (data2['total_valor'] / total2) * 100

    # Criar gráfico de pizza com Plotly
    fig = px.pie(data, 
                names='categoria', 
                values='total_valor', 
                hover_data=['percentual'],  # Adiciona o percentual no hover
                title='Distribuição de Despesas por Categoria',
                labels={'categoria': 'Categoria', 'total_valor': 'Valor', 'percentual': 'Percentual'}
                )

    # Criar gráfico de pizza com Plotly
    fig2 = px.pie(data2, 
                names='categoria', 
                values='total_valor', 
                hover_data=['percentual'],  # Adiciona o percentual no hover
                title='Distribuição de Despesas por Categoria',
                labels={'categoria': 'Categoria', 'total_valor': 'Valor', 'percentual': 'Percentual'}
                )

    # Usar st.columns() para dividir o layout em duas colunas
    col1, col2 = st.columns(2)

    # Exibir os gráficos nas respectivas colunas com chaves únicas
    with col1:
        st.plotly_chart(fig, use_container_width=True, key="grafico_pizza_1_{}".format(id(fig)))
    
    with col2:
         st.plotly_chart(fig2, use_container_width=True, key="grafico_pizza_2_{}".format(id(fig2)))


def __make_charts_color(color_line:str, color_point:str, title:str, data:object,  average:float, average_last_12_months:float,average_last_6_months:float):
    with Charts(data) as charts_main:
        st.subheader(title)
        st.text(f'-      Média Geral =                R$ {round(average, 2)}')
        st.text(f'-      Média dos últimos 12 meses = R$ {round(average_last_12_months, 2)}')
        st.text(f'-      Média dos últimos 6 meses =  R$ {round(average_last_6_months, 2)}')
        # Criando o gráfico com Altair
        chart = alt.Chart(charts_main.resumo_mensal).mark_line(color=color_line).encode(
            x='mes_ano:T',
            y='sum:Q',      
            tooltip=['mes_ano:T', 'sum:Q']
        )
        # Criando o gráfico com Altair
        line_chart = alt.Chart(charts_main.resumo_mensal).mark_line(color=color_line).encode(
            x='mes_ano:T',  # T significa temporal (data)
            y='sum:Q',      # Q significa quantitativo (valor)
            tooltip=['mes_ano:T', 'sum:Q']  # Exibe o mês/ano e a soma ao passar o mouse
        )
        # Criando os círculos nos pontos de cada mês
        points_chart = alt.Chart(charts_main.resumo_mensal).mark_point(shape='circle', color=color_point, size=70, filled=True).encode(
            x='mes_ano:T',  # T significa temporal (data)
            y='sum:Q',      # Q significa quantitativo (valor)
            tooltip=['mes_ano:T', 'sum:Q']  # Exibe o mês/ano e a soma ao passar o mouse
        )
        # Combinando as duas visualizações (linha + pontos)
        chart = line_chart + points_chart
        # Exibe o gráfico no Streamlit
        st.altair_chart(chart, use_container_width=True)


def make_charts():
    __make_charts_pizza()
    __make_charts_pizza()





     # Geral
    data = DataQuerys().make_querys(";")
    __make_charts_color(color_line='lightblue', color_point='lightblue', title=f'Gastos Gerais', data=data[0], average=data[1], average_last_12_months=data[2], average_last_6_months=data[3])
    # Farmacia
    farmacia_data = DataQuerys().make_querys("and (categoria = 'farmacia' OR categoria = 'farmácia')")
    __make_charts_color(color_line='green', color_point='green', title=f'Gastos com Farmácia', data=farmacia_data[0], average=farmacia_data[1], average_last_12_months=farmacia_data[2], average_last_6_months=farmacia_data[3])
    # Casa
    casa_data = DataQuerys().make_querys("and (categoria = 'casa' OR categoria = 'Casa')")
    __make_charts_color(color_line='orange', color_point='orange', title=f'Gastos com a Casa', data=casa_data[0], average=casa_data[1], average_last_12_months=casa_data[2], average_last_6_months=casa_data[3])
    # Mercado
    mercado_data = DataQuerys().make_querys("and (categoria = 'mercado' OR categoria = 'mercado')")
    __make_charts_color(color_line='purple', color_point='purple', title=f'Gastos com a Mercado', data=mercado_data[0], average=mercado_data[1], average_last_12_months=mercado_data[2], average_last_6_months=mercado_data[3])
     # Crianças
    criancas_data = DataQuerys().make_querys("and (categoria = 'criancas' OR categoria = 'crianças')")
    __make_charts_color(color_line='white', color_point='white', title=f'Gastos com a Crianças', data=criancas_data[0], average=criancas_data[1], average_last_12_months=criancas_data[2], average_last_6_months=criancas_data[3])
     # Gasolina
    gasolina_data = DataQuerys().make_querys("and (categoria = 'Gasolina' OR categoria = 'gasolina')")
    __make_charts_color(color_line='red', color_point='red', title=f'Gastos com a Gasolina', data=gasolina_data[0], average=gasolina_data[1], average_last_12_months=gasolina_data[2], average_last_6_months=gasolina_data[3])
    # Saidas
    saidas_data = DataQuerys().make_querys("and (categoria = 'saidas' OR categoria = 'saídas')")
    __make_charts_color(color_line='brown', color_point='brown', title=f'Gastos com a Saidas', data=saidas_data[0], average=saidas_data[1], average_last_12_months=saidas_data[2], average_last_6_months=saidas_data[3])
    # Familia
    familia_data = DataQuerys().make_querys("and (categoria = 'familia' OR categoria = 'família')")
    __make_charts_color(color_line='pink', color_point='pink', title=f'Gastos com a Familia', data=familia_data[0], average=familia_data[1], average_last_12_months=familia_data[2], average_last_6_months=familia_data[3])
    # refeicao
    padaria_data = DataQuerys().make_querys("and categoria = 'padaria'")
    __make_charts_color(color_line='yellow', color_point='yellow', title=f'Gastos com a padaria', data=padaria_data[0], average=padaria_data[1], average_last_12_months=padaria_data[2], average_last_6_months=padaria_data[3])
    # refeicao
    refeicao_data = DataQuerys().make_querys("and (categoria = 'refeicao' OR categoria = 'refeição')")
    __make_charts_color(color_line='orange', color_point='brown', title=f'Gastos com comida Fora', data=refeicao_data[0], average=refeicao_data[1], average_last_12_months=refeicao_data[2], average_last_6_months=refeicao_data[3])
    # Pessoal
    pessoal_data = DataQuerys().make_querys("and (categoria = 'pessoal')")
    __make_charts_color(color_line='blue', color_point='blue', title=f'Gastos Pessoais', data=pessoal_data[0], average=pessoal_data[1], average_last_12_months=pessoal_data[2], average_last_6_months=pessoal_data[3])
    # trabalho
    trabalho_data = DataQuerys().make_querys("and (categoria = 'trabalho')")
    __make_charts_color(color_line='gray', color_point='gray', title=f'Gastos com Trabalho', data=trabalho_data[0], average=trabalho_data[1], average_last_12_months=trabalho_data[2], average_last_6_months=trabalho_data[3])
    # viagem
    viagem_data = DataQuerys().make_querys("and (categoria = 'viagem')")
    __make_charts_color(color_line='yellow', color_point='yellow', title=f'Gastos Viagens', data=viagem_data[0], average=viagem_data[1], average_last_12_months=viagem_data[2], average_last_6_months=viagem_data[3])

    # outros
    outros_data = DataQuerys().make_querys("and (categoria = 'outros' or categoria = 'estacionamento')")
    __make_charts_color(color_line='black', color_point='white', title=f'Outros gastos', data=outros_data[0], average=outros_data[1], average_last_12_months=outros_data[2], average_last_6_months=outros_data[3])