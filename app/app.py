from flask import Flask, render_template, request, redirect, url_for, flash
from banco import conectar
from config import SECRET_KEY, FLASK_DEBUG, API_READ_KEY, API_WRITE_KEY, CHANNEL_ID

import requests
import random
import time
import datetime
import threading
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.get("/")
def index():
    return redirect(url_for("listar_status"))


@app.get("/dados")
def listar_status():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, data_hora, temperatura, umidade, origem_dado, data_insercao "
        "FROM status_ambiente ORDER BY data_hora DESC LIMIT 10"
    )
    status_banco = cursor.fetchall()
    cursor.close()
    conexao.close()

    status_thingspeak = buscar_thingspeak()

    return render_template(
        "index.html",
        status_banco=status_banco,
        status_thingspeak=status_thingspeak,
    )


@app.get("/novodado")
def adicionar_status():
    return render_template(
        "form.html",
        modo="novo",
        status={
            "id": "",
            "data_hora": "",
            "temperatura": "",
            "umidade": "",
            "origem_dado": "",
            "data_insercao": "",
        },
    )


@app.post("/novodado")
def salvar_status():
    data_hora = request.form.get("data_hora", "").strip()
    temperatura = request.form.get("temperatura", "").strip()
    umidade = request.form.get("umidade", "").strip()
    origem_dado = request.form.get("origem_dado", "").strip()
    data_insercao = request.form.get("data_insercao", "").strip()

    if not all([data_hora, temperatura, umidade, origem_dado, data_insercao]):
        flash("Preencha todos os campos", "erro")
        return redirect(url_for("adicionar_status"))

    try:
        temperatura = float(temperatura)
        umidade = float(umidade)
        data_hora = datetime.datetime.fromisoformat(data_hora)
        data_insercao = datetime.datetime.fromisoformat(data_insercao)
    except ValueError:
        flash("Dados inválidos", "erro")
        return redirect(url_for("adicionar_status"))

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO status_ambiente (data_hora, temperatura, umidade, origem_dado, data_insercao) "
            "VALUES (%s, %s, %s, %s, %s)",
            (data_hora, temperatura, umidade, origem_dado, data_insercao),
        )
        conexao.commit()
        cursor.close()
        conexao.close()
    except Exception:
        flash("Erro ao salvar no banco", "erro")
        return redirect(url_for("adicionar_status"))

    flash("Status adicionado com sucesso", "sucesso")
    return redirect(url_for("listar_status"))

def buscar_thingspeak():
    try:
        url = (
            f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"
            f"?api_key={API_READ_KEY}&results=10"
        )
        resposta = requests.get(url, timeout=10)
        dados = resposta.json()

        entradas = []
        for feed in dados.get("feeds", []):
            entradas.append({
                "created_at": feed.get("created_at", ""),
                "temperatura": feed.get("field1", "—"),
                "umidade": feed.get("field2", "—"),
            })
        return entradas

    except Exception as e:
        print(f"Erro ThingSpeak: {e}")
        return []


def enviar_dados(temperatura, umidade, origem):
    url = (
        f"https://api.thingspeak.com/update"
        f"?api_key={API_WRITE_KEY}&field1={temperatura}&field2={umidade}"
    )

    resposta = requests.get(url, timeout=10)

    print(f"Temperatura enviada : {temperatura}")
    print(f"Umidade enviada     : {umidade}")
    print(f"Origem              : {origem}")
    print(f"Resposta ThingSpeak : {resposta.text}")
    print("=" * 40)

    agora = datetime.datetime.now()

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO status_ambiente (data_hora, temperatura, umidade, origem_dado, data_insercao) "
            "VALUES (%s, %s, %s, %s, %s)",
            (agora, temperatura, umidade, origem, agora),
        )
        conexao.commit()
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro banco: {e}")


def loop_sensor():
    origens = ["Sensor 1", "Sensor 2", "Sensor 3"]

    while True:
        print("Enviando dados...")

        temperatura = round(random.uniform(20, 90), 2)
        umidade = round(random.uniform(25, 75), 2)
        origem = random.choice(origens)

        enviar_dados(temperatura, umidade, origem)

        time.sleep(15)


if __name__ == "__main__":

    if not FLASK_DEBUG or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        thread_sensor = threading.Thread(target=loop_sensor, daemon=True)
        thread_sensor.start()

    app.run(host="0.0.0.0", port=5000, debug=FLASK_DEBUG)