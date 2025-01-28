import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from graficos_despesas.data_base.DataQuerys import DataQuerys
import altair as alt



# class Charts:
#     def __init__(self):

#         pass


def __charts_all_month():
    data  = DataQuerys().all_month()
    data["data_evento"] = pd.to_datetime(data["data_evento"])
    # Agrupar os valores por mês e calcular a soma e a média
    data["mes_ano"] = data["data_evento"].dt.to_period("M")
    resumo_mensal = data.groupby("mes_ano")["valor"].agg(["sum", "mean"]).reset_index()

    # Converter 'mes_ano' para datetime para uso no gráfico
    resumo_mensal["mes_ano"] = resumo_mensal["mes_ano"].dt.to_timestamp()
     # Gráfico 1: Soma dos valores ao longo do tempo
    st.subheader("Gastos Totais Mensais (Gráfico de Linhas)")
    st.line_chart(
        data=resumo_mensal.set_index("mes_ano")["sum"],
        use_container_width=True
    )



def __charts_all_month_car():
    data  = DataQuerys().car_month()
    data["data_evento"] = pd.to_datetime(data["data_evento"])
    # Agrupar os valores por mês e calcular a soma e a média
    data["mes_ano"] = data["data_evento"].dt.to_period("M")
    resumo_mensal = data.groupby("mes_ano")["valor"].agg(["sum", "mean"]).reset_index()
    # Converter 'mes_ano' para datetime para uso no gráfico
    resumo_mensal["mes_ano"] = resumo_mensal["mes_ano"].dt.to_timestamp()
     # Gráfico 1: Soma dos valores ao longo do tempo
    st.subheader("Gastos com carro")
    # Criando o gráfico com Altair
    chart = alt.Chart(resumo_mensal).mark_line(color='red').encode(
        x='mes_ano:T',  # T significa temporal (data)
        y='sum:Q',      # Q significa quantitativo (valor)
    )

    st.line_chart(
        data=resumo_mensal.set_index("mes_ano")["sum"],
        use_container_width=True
    )
    # Exibe o gráfico no Streamlit
    st.altair_chart(chart, use_container_width=True)


def make_charts():
    
    st.title("Evolução de Gastos Mensais")
    __charts_all_month()
    __charts_all_month_car()

    # if not data.empty:
    #     # Converter a coluna de data para o tipo datetime
    #     data["data_evento"] = pd.to_datetime(data["data_evento"])

    #     # Agrupar os valores por mês e calcular a soma e a média
    #     data["mes_ano"] = data["data_evento"].dt.to_period("M")
    #     resumo_mensal = data.groupby("mes_ano")["valor"].agg(["sum", "mean"]).reset_index()

    #     # Converter 'mes_ano' para datetime para uso no gráfico
    #     resumo_mensal["mes_ano"] = resumo_mensal["mes_ano"].dt.to_timestamp()

    #     # Gráfico 1: Soma dos valores ao longo do tempo
    #     st.subheader("Gastos Totais Mensais (Gráfico de Linhas)")
    #     st.line_chart(
    #         data=resumo_mensal.set_index("mes_ano")["sum"],
    #         use_container_width=True
    #     )

    #     # Gráfico 2: Média dos valores ao longo do tempo
    #     st.subheader("Média dos Gastos Mensais (Gráfico de Linhas)")
    #     st.line_chart(
    #         data=resumo_mensal.set_index("mes_ano")["mean"],
    #         use_container_width=True
    #     )

    #     # Exibir tabela de dados consolidados
    #     st.write("Dados consolidados:")
    #     st.dataframe(resumo_mensal)

    # else:
    #     st.warning("Nenhum dado disponível para exibir.")






# # Configuração inicial do Streamlit
# st.title("Evolução de Gastos Mensais")


# st.title("Evolução de Gastos Mensais")

# # Função para carregar dados do banco de dados
# def load_data():
#     try:
#         # Substitua pelas suas credenciais do banco de dados
#         db_host = "192.168.1.2"
#         db_name = "db_local"
#         db_user = "postgres"
#         db_password = ""
#         db_port = "15432"

#         # Criar a conexão com o banco de dados
#         engine = create_engine(
#             f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
#         )

#         # Consultar os dados
#         query = """
#         SELECT valor, data_evento
#         FROM despesas_gastos_mensais
#         WHERE data_evento IS NOT NULL
#         """

#         # Carregar os dados em um DataFrame
#         df = pd.read_sql(query, con=engine)
#         return df

#     except Exception as e:
#         st.error(f"Erro ao conectar ao banco de dados: {e}")
#         return pd.DataFrame()

# # Carregar os dados
# data = load_data()

# if not data.empty:
#     # Converter a coluna de data para o tipo datetime
#     data["data_evento"] = pd.to_datetime(data["data_evento"])

#     # Agrupar os valores por mês e calcular a soma e a média
#     data["mes_ano"] = data["data_evento"].dt.to_period("M")
#     resumo_mensal = data.groupby("mes_ano")["valor"].agg(["sum", "mean"]).reset_index()

#     # Converter 'mes_ano' para datetime para uso no gráfico
#     resumo_mensal["mes_ano"] = resumo_mensal["mes_ano"].dt.to_timestamp()

#     # Gráfico 1: Soma dos valores ao longo do tempo
#     st.subheader("Gastos Totais Mensais (Gráfico de Linhas)")
#     st.line_chart(
#         data=resumo_mensal.set_index("mes_ano")["sum"],
#         use_container_width=True
#     )

#     # Gráfico 2: Média dos valores ao longo do tempo
#     st.subheader("Média dos Gastos Mensais (Gráfico de Linhas)")
#     st.line_chart(
#         data=resumo_mensal.set_index("mes_ano")["mean"],
#         use_container_width=True
#     )

#     # Exibir tabela de dados consolidados
#     st.write("Dados consolidados:")
#     st.dataframe(resumo_mensal)

# else:
#     st.warning("Nenhum dado disponível para exibir.")







# streamlit run /home/escritorio/PROJETOS/PESSOAIS/grafico_python/main.py
