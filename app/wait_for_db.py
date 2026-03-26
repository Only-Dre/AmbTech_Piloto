import time
import sys
import mysql.connector

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

def tentar_conectar():

    conexao = mysql.connector.connect(
        host = DB_HOST,
        port = DB_PORT,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )

    conexao.close()

if __name__ == "__main__":

    max_tentativa = 30

    intervalo = 2

    for tentativa in range(1, max_tentativa + 1):

        try:
            print(f"[wait_for_db] Tentiva: {tentativa} / {max_tentativa}. Tentando conectar aoao MySQL")

            tentar_conectar()

            print("[wait_for_db] MySQL disponível!")

            sys.exit(0)

        except Exception as e:
            print(f"[wait_for_db] MySQL ainda não disponível: {e}")

            time.sleep(intervalo)
            
    print("[wait_for_db] Falha: MySQL não ficou disponível a tempo.")
    sys.exit(1)