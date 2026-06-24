from datetime import date, datetime
import streamlit as st
import funcoes as f
import psycopg2

@st.dialog("Editar Usuário")
def editar_usuario(c, email_atual, nome_atual, data_atual):
    cursor = c.cursor()

    novo_nome = st.text_input("Nome", value=nome_atual)
    nova_data = st.date_input(
            "Data de Nascimento: ",
            min_value=date(1900,1,1),
            max_value=date.today(),
            format="DD/MM/YYYY",
            value=data_atual
        )
    
    if st.button("Salvar Alterações", type="primary"):
        cursor = c.cursor()
        cursor.execute(
            "UPDATE USUARIO SET NOME = %s, DATA_NASCIMENTO = %s WHERE E_MAIL = %s",
            (novo_nome, nova_data, email_atual)
        )
        c.commit()
        st.success("Usuário atualizado!")
        st.rerun()

def consultar(c):
    cursor = c.cursor()
    cursor.execute("SELECT NOME, E_MAIL, DATA_NASCIMENTO FROM USUARIO WHERE TIPO = 'leitor' ORDER BY NOME")
    usuarios = cursor.fetchall()
    
    if not usuarios:
        st.warning("Nenhum leitor cadastrado encontrado.")
    else:
        for usuario in usuarios:
            nome, email, data_nascimento = usuario[0], usuario[1], usuario[2]

            with st.container(border=True):
                col_info, col_actions = st.columns([0.925, 0.075], vertical_alignment="center")

            with col_info:
                st.write(f"Nome: {nome}")
                st.write(f"E-mail: {email}")
                st.write(f"Data de Nascimento: {(datetime
                                                .strptime(str(data_nascimento), '%Y-%m-%d'))
                                                .strftime('%d/%m/%Y')}")

            with col_actions:
                if st.button(label="", icon=":material/edit:", key=f"editar_{email}"):
                    editar_usuario(c, email, nome, data_nascimento)

                if st.button(label="", icon=":material/delete:", key=f"excluir_{email}"):
                    cursor.execute("DELETE FROM USUARIO WHERE E_MAIL = %s", (email,))
                    c.commit()
                    st.success(f"Usuário {nome} excluído.")
                    st.rerun() 
            
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