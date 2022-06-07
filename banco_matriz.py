from conexao import banco

#Cadastro de bancos
# class banco_geral:
#     def __init__(self):
#         self.bancos_nome = None
#         self.agencia = None
#         self.conta =None

def cadastro_banco_matriz(bancos_nome, agencia, conta, cpf_cnpj):
    vbanco = bancos_nome
    vagencia = agencia
    vconta = conta
    vmatriz_cpf_cnpj = cpf_cnpj
    cursor = banco.cursor()
    try:
        comando_sql2 = "INSERT INTO banco (nome_banco, agencia, conta, cpf_cnpj) VALUES ('{}','{}','{}','{}')".format(vbanco, vagencia, vconta, vmatriz_cpf_cnpj)
        cursor.execute(comando_sql2)
        banco.commit()
        cursor.close()
    except:
         cursor.close()

#############################################################################
def mostra_view_banco_matriz():
    cursor = banco.cursor()

    comando_sql = "SELECT codigo, nome_banco, agencia, conta FROM banco"
    cursor.execute(comando_sql)
    dados_matriz = cursor.fetchall()

    return dados_matriz

##############################################################################
def exclui_banco_matriz(dados_excluir):
    inf_excluir = dados_excluir
    cursor = banco.cursor()
    comando_sql2 = "DELETE FROM banco WHERE codigo = {}".format(inf_excluir)
    cursor.execute(comando_sql2)

    banco.commit()
    cursor.close()


