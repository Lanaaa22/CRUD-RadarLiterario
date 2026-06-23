import psycopg2

def conexao():
    try:
        conexao = psycopg2.connect(database = "Integracao", host = "pg-7887337-cardosoilanna96-86c1.g.aivencloud.com", user = "avnadmin", password = "AVNS_rZetiphy6NluhJPzj8y", port= "13982", sslmode="require")
        return conexao
    except Exception as e:
        print(f"Erro ao conectar {e}")
        return None
    