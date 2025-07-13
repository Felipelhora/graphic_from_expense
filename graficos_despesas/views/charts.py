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
    data_geral = DataQuerys().pizza_query()
    data_last_year = DataQuerys().pizza_query_last_year()
    data_last_month = DataQuerys().pizza_query_last_month()
    data_before_last_month = DataQuerys().pizza_query_before_last_month()
    data_actual_month = DataQuerys().pizza_query_actual_month()
    

    # Calcular o total para os percentuais
    total_geral = data_geral['total_valor'].sum()
    total_last_year = data_last_year['total_valor'].sum()
    total_data_before_last_month=data_before_last_month['total_valor'].sum()
    total_last_month = data_last_month['total_valor'].sum()
    total_actual_month = data_actual_month['total_valor'].sum()

    # Calcular o percentual de cada categoria
    data_geral['percentual'] = (data_geral['total_valor'] / total_geral) * 100
    data_last_year['percentual'] = (data_last_year['total_valor'] / total_last_year) * 100
    data_last_month['percentual'] = (data_last_month['total_valor'] / total_last_month) * 100
    data_before_last_month['percentual'] = (data_last_month['total_valor'] / total_data_before_last_month) * 100
    data_actual_month['percentual'] = (data_actual_month['total_valor'] / total_actual_month) * 100

    # Criar gráfico de pizza Geral
    geral = px.pie(data_geral, 
                names='categoria', 
                values='total_valor', 
                hover_data=['percentual'],  
                title='Despesas por Categoria Histórico',
                labels={'categoria': 'Categoria', 'total_valor': 'Valor', 'percentual': 'Percentual'}
                )

   
    last_year = px.pie(data_last_year, 
                names='categoria', 
                values='total_valor', 
                hover_data=['percentual'],  
                title='Despesas por Categoria 12 meses',
                labels={'categoria': 'Categoria', 'total_valor': 'Valor', 'percentual': 'Percentual'}
                )
    
    # Criar gráfico de pizza com Plotly
    data_before_last_month = px.pie(data_before_last_month, 
                names='categoria', 
                values='total_valor', 
                hover_data=['percentual'],  # Adiciona o percentual no hover
                title=f"<b>Despesas por Categoria - penúltimo mês </b><br><span style='font-size:12px'>Total: R$ {round(total_data_before_last_month, 2):,.2f}</span>",
                labels={'categoria': 'Categoria', 'total_valor': 'Valor', 'percentual': 'Percentual'}
                )

    # Criar gráfico de pizza com Plotly
    data_last_month = px.pie(data_last_month, 
                names='categoria', 
                values='total_valor', 
                hover_data=['percentual'],  # Adiciona o percentual no hover
                title=f"<b>Despesas por Categoria - último mês </b><br><span style='font-size:12px'>Total: R$ {round(total_last_month, 2):,.2f}</span>",
                labels={'categoria': 'Categoria', 'total_valor': 'Valor', 'percentual': 'Percentual'}
                )

     # Criar gráfico de pizza com Plotly
    actual_month = px.pie(data_actual_month, 
                names='categoria', 
                values='total_valor', 
                hover_data=['percentual'],  # Adiciona o percentual no hover
                title=f"<b>Despesas por Categoria - mês atual</b><br><span style='font-size:12px'>Total: R$ {round(total_actual_month, 2):,.2f}</span>",
                labels={'categoria': 'Categoria', 'total_valor': 'Valor', 'percentual': 'Percentual'}
                )
    
    data_before_last_month.update_layout(
    title={
        'x': 0.2,
        'xanchor': 'left'
    }
    )
    data_last_month.update_layout(
    title={
        'x': 0.2,
        'xanchor': 'left'
    }
    )
    actual_month.update_layout(
    title={
        'x': 0.2,
        'xanchor': 'left'
    }
    )
    geral.update_layout(title={'x': 0.2})
    last_year.update_layout(title={'x': 0.2})
    data_last_month.update_layout(title={'x': 0.2})
    actual_month.update_layout(title={'x': 0.2})

     # Adicionando um título grande no topo
    st.markdown("<h1 style='text-align: center;'>Relatório de Despesas</h1>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(geral, use_container_width=True, key="grafico_pizza_1")
        with col2:
            st.plotly_chart(last_year, use_container_width=True, key="grafico_pizza_2")
    
    with st.container():
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(data_before_last_month, use_container_width=True, key="grafico_pizza_3")
        with col4:
            st.plotly_chart(data_last_month, use_container_width=True, key="grafico_pizza_4")
    
    with st.container():
        col5 = st.columns(1)[0]
        with col5:
            st.plotly_chart(actual_month, use_container_width=True, key="grafico_pizza_5")
        


def __make_charts_color(color_line:str, color_point:str, title:str, data:object,  average:float, average_last_12_months:float,average_last_6_months:float):
    with Charts(data) as charts_main:
        st.markdown(f"<h2 style='text-align: center;'>{title}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>- Média Geral = R$ {round(average, 2)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>- Média dos últimos 12 meses = R$ {round(average_last_12_months, 2)}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>- Média dos últimos 6 meses = R$ {round(average_last_6_months, 2)}</p>", unsafe_allow_html=True)

        chart = alt.Chart(charts_main.resumo_mensal).mark_line(color=color_line).encode(
            x='mes_ano:T',
            y='sum:Q',      
            tooltip=['mes_ano:T', 'sum:Q']
        ).properties(
            title={
                "text": title, 
                "anchor": "middle",   # Título centralizado
                "fontSize": 18
            }
        )
        line_chart = alt.Chart(charts_main.resumo_mensal).mark_line(color=color_line).encode(
            x='mes_ano:T',
            y='sum:Q',    
            tooltip=['mes_ano:T', 'sum:Q']  
        )
        points_chart = alt.Chart(charts_main.resumo_mensal).mark_point(shape='circle', color=color_point, size=70, filled=True).encode(
            x='mes_ano:T',  
            y='sum:Q',      
            tooltip=['mes_ano:T', 'sum:Q']  
        )
        chart = line_chart + points_chart
        st.altair_chart(chart, use_container_width=True)


def make_charts():
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
    # carro
    carro_data = DataQuerys().make_querys("and (categoria = 'Carro' or categoria = 'carro')")
    __make_charts_color(color_line='blue', color_point='white', title=f'Gastos com carro', data=carro_data[0], average=carro_data[1], average_last_12_months=carro_data[2], average_last_6_months=carro_data[3])

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
    refeicao_data = DataQuerys().make_querys("and (categoria = 'refeicao' OR categoria = 'refeição' OR categoria = 'almoco' OR categoria = 'almoço' OR categoria = 'Almoco' OR categoria = 'Almoço'  )")
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

    # não classificados
    nao_classificados_data = DataQuerys().make_querys("""
    and categoria NOT IN (
        'farmacia', 'farmácia',
        'casa', 'Casa', 'carro', 'Carro', 'almoço', 'Almoço', 'almoco', 'Almoco',
        'mercado',
        'criancas', 'crianças',
        'Gasolina', 'gasolina',
        'saidas', 'saídas',
        'familia', 'família',
        'padaria',
        'refeicao', 'refeição',
        'pessoal',
        'trabalho',
        'viagem',
        'outros',
        'estacionamento'
    )
    """)
    __make_charts_color(
    color_line='cyan',
    color_point='cyan',
    title='Gastos não classificados',
    data=nao_classificados_data[0],
    average=nao_classificados_data[1],
    average_last_12_months=nao_classificados_data[2],
    average_last_6_months=nao_classificados_data[3]
)