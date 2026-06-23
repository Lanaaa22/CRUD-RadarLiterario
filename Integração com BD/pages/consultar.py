import streamlit as st
import funcoes as f
import psycopg2


def consultar(c):
    cursor = c.cursor()
    cursor.execute("SELECT NOME FROM USUARIO WHERE TIPO = 'leitor'")
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        with st.container(border=True):
            st.write(usuario[0])
    if st.button("Cadastrar Usuário"):
        st.switch_page("cadastro.py")

def main():
    try:
        c = f.conexao()
        consultar(c)
    except Exception as e:
        st.error(f"O banco de dados encontrou o problema {e}")
if __name__ == "__main__":
    main()