FROM python:3.12.5

WORKDIR /graficos
COPY . .

ARG PORT


RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

RUN pip install -r requeriments.txt

EXPOSE $PORT

CMD ["streamlit", "run", "main.py"]