from graficos_despesas.data_base.DBConnectionHandler import DBConnectionHandler
from sqlalchemy import text
import pandas as pd


class DataQuerys:

    def __init__(self):
        self.number_month = self.__get__all_months()
        self.query_main =   """ SELECT valor, data_evento
                                FROM despesas_gastos_mensais
                                WHERE data_evento IS NOT NULL
                            """
        self.query_histoty_sum = """select sum(valor) from despesas_gastos_mensais WHERE data_evento IS NOT NULL""" 
        self.query_last_12_months_sum = """ SELECT sum(valor)
                                        FROM despesas_gastos_mensais
                                        WHERE data_evento >= CURRENT_DATE - INTERVAL '12 months'
                                        AND data_evento IS NOT NULL 
                                    """
        self.query_last_6_months_sum = """ SELECT sum(valor)
                                        FROM despesas_gastos_mensais
                                        WHERE data_evento >= CURRENT_DATE - INTERVAL '6 months'
                                        AND data_evento IS NOT NULL 
                                    """

        pass


    def __get__all_months(self):
         with DBConnectionHandler() as db_connection:
            total_month = """
            SELECT  COUNT(DISTINCT DATE_TRUNC('month', data_evento)) AS numero_meses
            FROM despesas_gastos_mensais
            WHERE data_evento IS NOT NULL    
            """
            result = db_connection.session.execute(text(total_month))
            answer = result.scalar()
            return answer


    def pizza_query(self):
         with DBConnectionHandler() as db_connection:
            query = """SELECT 
                        SUM(valor) AS total_valor, 
                        CASE 
                            WHEN LOWER(categoria) IN ('farmacia', 'farmácia') THEN 'Farmácia'
                            WHEN LOWER(categoria) IN ('criancas', 'crianças') THEN 'Crianças'
                            WHEN LOWER(categoria) IN ('família', 'familia') THEN 'Familia'
                            WHEN LOWER(categoria) IN ('refeicao', 'refeição') THEN 'Refeição'
                            WHEN LOWER(categoria) IN ('Gasolina', 'gasolina') THEN 'Gasolina'
                            WHEN LOWER(categoria) IN ('mercado', 'Mercado', 'mercado ') THEN 'Mercado'
                            WHEN LOWER(categoria) IN ('saidas', 'saídas') THEN 'Saídas'
                            WHEN LOWER(categoria) IN ('estacionamento', 'outros', 'outros ') THEN 'Outros'
                            ELSE categoria
                        END AS categoria_agrupada
                        FROM despesas_gastos_mensais dgm
                        GROUP BY categoria_agrupada
                        ORDER BY total_valor DESC;
                    """
            result = db_connection.session.execute(text(query))
            data = pd.DataFrame(result.fetchall(), columns=['total_valor', 'categoria'])

            return data
    
    def pizza_query_last_year(self):
         with DBConnectionHandler() as db_connection:
            query = """SELECT 
                        SUM(valor) AS total_valor, 
                        CASE 
                            WHEN LOWER(categoria) IN ('farmacia', 'farmácia') THEN 'Farmácia'
                            WHEN LOWER(categoria) IN ('criancas', 'crianças') THEN 'Crianças'
                            WHEN LOWER(categoria) IN ('família', 'familia') THEN 'Família'
                            WHEN LOWER(categoria) IN ('refeicao', 'refeição') THEN 'Refeição'
                            WHEN LOWER(categoria) = 'gasolina' THEN 'Gasolina'
                            WHEN LOWER(categoria) = 'mercado' THEN 'Mercado'
                            WHEN LOWER(categoria) IN ('saidas', 'saídas') THEN 'Saídas'
                            WHEN LOWER(categoria) IN ('estacionamento', 'outros') THEN 'Outros'
                            ELSE categoria
                        END AS categoria_agrupada
                    FROM despesas_gastos_mensais dgm
                    WHERE 
                        data_evento >= CURRENT_DATE - INTERVAL '12 months'
                    GROUP BY categoria_agrupada
                    ORDER BY total_valor DESC;
            """
            result = db_connection.session.execute(text(query))
            data = pd.DataFrame(result.fetchall(), columns=['total_valor', 'categoria'])

            return data
    
    def pizza_query_last_month(self):
         with DBConnectionHandler() as db_connection:
            query = """ SELECT 
                        SUM(valor) AS total_valor, 
                        CASE 
                            WHEN LOWER(categoria) IN ('farmacia', 'farmácia') THEN 'Farmácia'
                            WHEN LOWER(categoria) IN ('criancas', 'crianças') THEN 'Crianças'
                            WHEN LOWER(categoria) IN ('família', 'familia') THEN 'Familia'
                            WHEN LOWER(categoria) IN ('refeicao', 'refeição') THEN 'Refeição'
                            WHEN LOWER(categoria) IN ('Gasolina', 'gasolina') THEN 'Gasolina'
                            WHEN LOWER(categoria) IN ('mercado', 'Mercado', 'mercado ') THEN 'Mercado'
                            WHEN LOWER(categoria) IN ('saidas', 'saídas') THEN 'Saídas'
                            WHEN LOWER(categoria) IN ('estacionamento', 'outros', 'outros ') THEN 'Outros'
                            ELSE categoria
                        END AS categoria_agrupada
                        FROM despesas_gastos_mensais dgm
                        WHERE 
                            data_evento >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'
                            AND data_evento < DATE_TRUNC('month', CURRENT_DATE)
                        GROUP BY categoria_agrupada
                        ORDER BY total_valor DESC;
            """
            result = db_connection.session.execute(text(query))
            data = pd.DataFrame(result.fetchall(), columns=['total_valor', 'categoria'])
            return data

    def pizza_query_actual_month(self):
         with DBConnectionHandler() as db_connection:
            query = """ SELECT 
                        SUM(valor) AS total_valor, 
                         CASE 
                            WHEN LOWER(categoria) IN ('farmacia', 'farmácia') THEN 'Farmácia'
                            WHEN LOWER(categoria) IN ('criancas', 'crianças') THEN 'Crianças'
                            WHEN LOWER(categoria) IN ('família', 'familia') THEN 'Familia'
                            WHEN LOWER(categoria) IN ('refeicao', 'refeição') THEN 'Refeição'
                            WHEN LOWER(categoria) IN ('Gasolina', 'gasolina') THEN 'Gasolina'
                            WHEN LOWER(categoria) IN ('mercado', 'Mercado', 'mercado ') THEN 'Mercado'
                            WHEN LOWER(categoria) IN ('saidas', 'saídas') THEN 'Saídas'
                            WHEN LOWER(categoria) IN ('estacionamento', 'outros', 'outros ') THEN 'Outros'
                            ELSE categoria
                        END AS categoria_agrupada
                        FROM despesas_gastos_mensais dgm
                        WHERE DATE_TRUNC('month', data_evento) = DATE_TRUNC('month', CURRENT_DATE)
                        GROUP BY categoria;
                    """
            result = db_connection.session.execute(text(query))
            data = pd.DataFrame(result.fetchall(), columns=['total_valor', 'categoria'])
            return data


    def car_month(self):
         with DBConnectionHandler() as db_connection:
            engine = db_connection.get_engine()
            query = """
            SELECT valor, data_evento
            FROM despesas_gastos_mensais
            WHERE data_evento IS NOT NULL and categoria = 'carro'
            """
            # Carregar os dados em um DataFrame
            df = pd.read_sql(query, con=engine)
            return df
                
    def make_querys(self, query_complement):
        #  query_complement = "and categoria = 'farmacia' or categoria = 'farmácia'"
         with DBConnectionHandler() as db_connection:
            # linha
            engine = db_connection.get_engine()
            query = f"{self.query_main} {query_complement}" 
            df = pd.read_sql(query, con=engine)
            # media geral
            total_sum = f"{self.query_histoty_sum} {query_complement}"
            result = db_connection.session.execute(text(total_sum))
            all_value = result.scalar()
            try:
                media_geral = all_value / self.number_month
            except:
                media_geral = 0
            # media 12 meses
            query_last_12_months = f"{self.query_last_12_months_sum} {query_complement}"
            result = db_connection.session.execute(text(query_last_12_months))
            value_from_last_months = result.scalar()
            try:
                media_last_year = value_from_last_months / 12
            except:
                media_last_year = 0
            # media 6 meses
            query_last_6_months = f"{self.query_last_6_months_sum} {query_complement}"
            result = db_connection.session.execute(text(query_last_6_months))
            value_from_last_6_months = result.scalar()
            try:
                media_last_semester = value_from_last_6_months / 6
            except:
                media_last_semester = 0
            return [df, media_geral, media_last_year, media_last_semester]