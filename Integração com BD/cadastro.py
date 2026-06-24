from datetime import date
import streamlit as st
import funcoes as f
import psycopg2

# telas que precisam fazer:
# C: cadastro
# R: ver os livro da estante?
# U: 
# D: Apagar um usuário?

# executar: python -m streamlit run cadastro.py

def inserirUsuario(c, nome, data_nascimento, e_mail, sexo):
    cursor = c.cursor()
    insert = """
        INSERT INTO USUARIO (nome, e_mail, data_nascimento, sexo, tipo)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert, (nome, e_mail, data_nascimento, sexo, "leitor"))
    c.commit()
    cursor.close()

def interface(c):
    # Cria o formulário e ativa a limpeza dos campos após o envio bem-sucedido
    with st.form("form_cadastro", clear_on_submit=True):
        st.write("Cadastro de Usuário")
        
        nome = st.text_input("Nome: ")
        email = st.text_input("E-mail: ")
        data_nasc = st.date_input(
            "Data de Nascimento: ",
            min_value=date(1900,1,1),
            max_value=date.today(),
            format="DD/MM/YYYY"
        )
        sexo = st.selectbox(
            "Sexo: ",
            ["Masculino", "Feminino", "Outro"],
            index=None,
            placeholder="Selecione o seu sexo..."
            )
        senha = st.text_input("Senha: ", type="password")

        # Botão obrigatório para submeter o formulário
        botao_cadastrar = st.form_submit_button("Cadastrar")

        if botao_cadastrar:
            if not email or not senha or not data_nasc or not nome or not sexo:
                st.warning("Tente novamente! Algum dado não foi escrito.")
            else: 
                inserirUsuario(c, nome, data_nasc, email, sexo)
                st.success("Cadastro feito com sucesso!")

    # O botão de navegação deve ficar FORA do formulário
    if st.button("Consultar Usuários Cadastrados"):
        st.switch_page("pages/consultar.py")

def main():
    try:
        c = f.conexao()
        interface(c)
    except Exception as e:
        st.error(f"O banco de dados encontrou o problema {e}")

if __name__ == "__main__":
    main()