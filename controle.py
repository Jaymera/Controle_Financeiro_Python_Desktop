from PyQt5 import uic, QtWidgets
import requests
import re
from itertools import cycle  # Validação de CNPJ/CPF da receita
from datetime import datetime # Valição de data
import pandas as pd
import openpyxl
import matplotlib
import locale


from banco_matriz import cadastro_banco_matriz, mostra_view_banco_matriz, exclui_banco_matriz
from conexao import banco


matriz_cpf_cnpj = ''
id = '' #Cadastro de Classe/Grupo/Subgrupo
tela = ''


def cad_usuario():
    vnome = frmcad_login.edtNome.text()
    vemail = frmcad_login.edtEmail.text()
    vcpf_cnpj = frmcad_login.edtCPF.text()
    vendereco = frmcad_login.edtEndereco.text()
    vsexo = frmcad_login.cbbSexo.currentText()
    vtelefone = frmcad_login.edtTelefone.text()
    vcep = frmcad_login.edtCep.text()
    vbairro = frmcad_login.edtBairro.text()
    vcomplemento = frmcad_login.edtComplemento.text()
    vuf = frmcad_login.edtUF.text()
    vusuario = frmcad_login.edtUsuario.text()
    vsenha = frmcad_login.edtSenha.text()
    vtipo = ""

    if telefone_validador(vtelefone) == False:
        print('Favor inserir um número de telefone correto')
        mensagem('Favor inserir um número de telefone correto')
        return None

    if (cpf_validador(vcpf_cnpj) == False):
        print('CPF/CNPJ inválido!')
        mensagem('Favor inserir um CPF/CNPJ valido')
        return None

    if (email_validador(vemail) == False):
        print('Email inválido!')
        mensagem('Favor inserir um email válido')
        return None

    if (nome_validador(vnome) == False):
        print('Nome inválido!')
        mensagem('Favor inserir um nome válido')
        return None

    if buscar_cep == False:
        print('Cep inválido')
        mensagem('Favor inserir um cep válido')
        return None

    if len(vcep) != 9:
        print('Insira um CEP válido')
        mensagem('Favor inserir um CEP válido')
        return None

    if vusuario == '' or vsenha == '':
        print('Insira um usuário e/ou senha')
        mensagem('Favor inserir usuário e/ou senha')
        return None

    if vendereco == '':
        print('Insira um endereço')
        mensagem('Favor inserir um endereço')
        return None

    cursor = banco.cursor()
    comando_SQL = 'INSERT INTO usuario (cpf_cnpj, nome, email, telefone, cep, endereco, sexo, tipo, usuario, senha, bairro, complemento, uf) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    dados = (str(vcpf_cnpj), str(vnome), str(vemail), str(vtelefone), str(vcep), str(vendereco), str(vsexo), str(vtipo),
             str(vusuario), str(vsenha), str(vbairro), str(vcomplemento), str(vuf))
    cursor.execute(comando_SQL, dados)
    banco.commit()
    cad_usuario_limpa()
    print('Usuário Cadastrado!')

    frmcad_login.close()

    mensagem('Cadastrado com sucesso')


# Log in Sistema
def verificacao_entrada():
    global matriz_cpf_cnpj
    vlogin = frmlogin.edtUsuario.text()
    vsenha = frmlogin.edtSenha.text()

    cursor = banco.cursor()
    try:
        comando_SQL = "SELECT cpf_cnpj, senha FROM usuario WHERE cpf_cnpj = '{}' and senha = '{}'".format(vlogin,
                                                                                                          vsenha)
        cursor.execute(comando_SQL)

        resultado = cursor.fetchone()

        if resultado:
            mostra_principal()
            mostra_lancamento_principal()
            login_limpa()
            frmlogin.close()
            matriz_cpf_cnpj = vlogin
        else:
            frmlogin.txtMsgerro.setText('Usuário e/ou senha não cadastrados')

        cursor.close()

    except:
        mensagem("ERRO na conexão")
        cursor.close()

# validação de data
def valida_data(data):
    formato = "%d/%m/%Y"
    res = True

    try:
        res = bool(datetime.strptime(data, formato))

    except ValueError:
        res = False

    return res

# validação de data para p SQL
def valida_data_sql(data):
    formato = "%Y-%m-%d"
    res = datetime(day=int(data[0:2]),month=int(data[3:5]),year=int(data[6:]))
    teste = res.strftime(formato)
    return teste

########################################################################################
#FORMULARIO CADASTRO DE BANCO

# Cadastro Banco
def cadastro_banco():
    global matriz_cpf_cnpj
    try:
        cadastro_banco_matriz(frmcad_banco.edtBanco.text(), frmcad_banco.edtAgencia.text(), frmcad_banco.edtConta.text(), matriz_cpf_cnpj)
        cad_banco_limpa()
        mensagem('Banco Cadastrado')
    except:
        mensagem('Erro de conexão')

#Mostra view da tela de bancos
def mostra_view_banco():
    frmview_bancos.show()
    try:
        dados = mostra_view_banco_matriz()
        frmview_bancos.tbview_bancos.setRowCount(len(dados))
        frmview_bancos.tbview_bancos.setColumnCount(4)

        i = 0
        j = 0
        for i in range(0, len(dados)):
            for j in range(0,4):
                frmview_bancos.tbview_bancos.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
    except:
        mensagem('Erro de Conexão')

def exclui_banco():
    global inf_excluir

    for currentQTableWidgetItem in frmview_bancos.tbview_bancos.selectedItems():
        if currentQTableWidgetItem.column() == 0:
            inf_excluir = currentQTableWidgetItem.text()
            exclui_banco_matriz(inf_excluir)
            mensagem("Banco excluido com sucesso")
        else:
            mensagem("Favor selecionar o código do banco")
            return None

# def print_row_bancos():
#     global inf_excluir
#
#     for currentQTableWidgetItem in frmview_bancos.tbview_bancos.selectedItems():
#         if currentQTableWidgetItem.column() == 0:
#             inf_excluir = currentQTableWidgetItem.text()
#         else:
#             return None
#
#     print(inf_excluir)

def mostra_cadastro_banco():
    frmcad_banco.show()

def cad_banco_cancela():
    cad_banco_limpa()
    frmcad_banco.close()

def view_bancos_sair():
    frmview_bancos.close()

def cad_banco_limpa():
    frmcad_banco.edtBanco.setText('')
    frmcad_banco.edtConta.setText('')
    frmcad_banco.edtAgencia.setText('')

####################################################################################################

# Cadastro tipo pagamento
def cadastro_tipo_pagamento():
    global matriz_cpf_cnpj

    vforma_pagamento = frmcad_tipo_pagamento.edtTipo_pagamento.text()

    cursor = banco.cursor()
    try:
        comando_SQL = (
            "INSERT INTO tipo_pagamento (cpf_cnpj, forma_pagamento) VALUES ('{}','{}')".format(matriz_cpf_cnpj,
                                                                                               vforma_pagamento))
        cursor.execute(comando_SQL)
        banco.commit()
        mensagem('Tipo de pagamento Cadastrado')
        cad_forma_pagamento_limpa()
        frmcad_tipo_pagamento.close()
        cursor.close()

    except:
        mensagem('Erro de conexão')
        cursor.close()


############################################################

def busca_nome(nome_coluna, nome_tabela, nome_pesquisa):

    cursor = banco.cursor()
    comando_sql = "SELECT " + nome_coluna + " FROM " + nome_tabela + " WHERE " + nome_coluna + " = '{}' ".format(nome_pesquisa)
    cursor.execute(comando_sql)
    return cursor.fetchone()


def cad_classe():
    global matriz_cpf_cnpj
    vnome_classe = frmcad_classe.edtClasse.text()

    valida_nome_repetido = busca_nome('nome_classe', 'classe', vnome_classe)
    if valida_nome_repetido == None:

        cursor = banco.cursor()
        try:
            comando_SQL = ("INSERT INTO classe (cpf_cnpj, nome_classe) VALUES ('{}','{}')".format(matriz_cpf_cnpj, vnome_classe))
            cursor.execute(comando_SQL)
            banco.commit()
            mensagem('Classe cadastrada com sucesso')
            cad_classe_limpa()
            cad_classe_sair()
            cursor.close()
        except:
            mensagem('Erro de conexão')
            cursor.close()

    else:
        mensagem("Nome da classe não pode ser repetido")

def cad_grupo():
    global matriz_cpf_cnpj
    global id

    vnome_grupo = frmcad_grupo.edtGrupo.text()

    cursor = banco.cursor()
    try:
        comando_SQL = ("INSERT INTO grupo (cpf_cnpj, nome_grupo, codigo_classe) VALUES ('{}','{}','{}')".format(matriz_cpf_cnpj, vnome_grupo, id))
        cursor.execute(comando_SQL)
        banco.commit()
        mensagem("Grupo cadastrado com sucesso")
        cad_grupo_limpa()
        cad_grupo_sair()

    except:
        mensagem("Erro de conexão")

    cursor.close()

def cad_subgrupo():
    global matriz_cpf_cnpj
    global id

    vnome_subgrupo = frmcad_subgrupo.edtSubgrupo.text()

    cursor = banco.cursor()
    try:
        comando_SQL = ("INSERT INTO subgrupo (cpf_cnpj, nome_subgrupo) VALUES ('{}', '{}')".format(matriz_cpf_cnpj, vnome_subgrupo))
        cursor.execute(comando_SQL)
        banco.commit()

        cursor.execute("SELECT MAX(codigo) FROM subgrupo")
        dado_codigo = cursor.fetchone()
        codigo_subgupo = dado_codigo[0]


        cursor2 = banco.cursor()
        comando_SQL2 = ("INSERT INTO grupo_subgrupo (cpf_cnpj, cod_grupo, cod_subgrupo) VALUES ('{}',{},{})".format(matriz_cpf_cnpj, id, codigo_subgupo))
        cursor2.execute(comando_SQL2)
        banco.commit()
        mensagem('Subgrupo cadastrado com sucesso')
        cad_subgrupo_limpa()
        cad_subgrupo_sair()

    except:
        mensagem('Dados inválidos')


##########################################################################


def mostra_view_pagamento():
    frmviewtipo_pagamento.show()

    try:
        cursor = banco.cursor()
        comando_sql = "SELECT codigo, forma_pagamento FROM tipo_pagamento"
        cursor.execute(comando_sql)
        dados = cursor.fetchall()

        frmviewtipo_pagamento.tbtipo_pagamento.setRowCount(len(dados))
        frmviewtipo_pagamento.tbtipo_pagamento.setColumnCount(2)

        for i in range (0, len(dados)):
            for j in range (0,2):
                frmviewtipo_pagamento.tbtipo_pagamento.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
    except:
        mensagem("Erro de conexão")

def mostra_view_usuario():
    frmview_usuario.show()

    try:
        cursor = banco.cursor()
        comando_sql = "SELECT cpf_cnpj, nome, email, endereco, tipo, sexo, telefone, cep, bairro, uf, usuario, senha FROM usuario"
        cursor.execute(comando_sql)
        dados = cursor.fetchall()

        frmview_usuario.tbview_usuario.setRowCount(len(dados))
        frmview_usuario.tbview_usuario.setColumnCount(12)

        for i in range (0, len(dados)):
            for j in range (0,12):
                frmview_usuario.tbview_usuario.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
    except:
        mensagem("Erro de conexão")


# Chama tela principal
def mostra_principal():
    frmPrincipal.show()



# Chama Cadastro de usuários
def mostra_cad_usuario():
    frmcad_login.show()


def mostra_cad_pagamento():
    frmcad_tipo_pagamento.show()

def mostra_lancamento_principal():
    cursor = banco.cursor()
    try:
        i = 0
        j = 0
        comando_sql = '''SELECT fluxo_caixa.codigo, fluxo_caixa.data_transacao, fluxo_caixa.descricao, banco.nome_banco, tipo_pagamento.forma_pagamento, classe.nome_classe, 
                        grupo.nome_grupo, subgrupo.nome_subgrupo, fluxo_caixa.entrada, fluxo_caixa.saida FROM fluxo_caixa
                        LEFT JOIN banco
                        ON banco.codigo = fluxo_caixa.codigo_banco
                        LEFT JOIN tipo_pagamento 
                        ON tipo_pagamento.codigo = fluxo_caixa.codigo_tipo_pagamento                   
                        LEFT JOIN classe 
                        ON classe.codigo = fluxo_caixa.codigo_classe
                        LEFT JOIN grupo 
                        ON grupo.codigo = fluxo_caixa.codigo_grupo
                        LEFT JOIN subgrupo
                        ON subgrupo.codigo = fluxo_caixa.codigo_subgrupo
                                                                        '''
        cursor.execute(comando_sql)
        dados = cursor.fetchall()

        frmPrincipal.tb_Lancamento.setRowCount(len(dados))
        frmPrincipal.tb_Lancamento.setColumnCount(10)
        for i in range(0, len(dados)):
            for j in range(0,10):
                frmPrincipal.tb_Lancamento.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))

    except:
        mensagem("Erro de banco")

    comando_sql = "SELECT SUM(entrada) FROM fluxo_caixa"
    cursor.execute(comando_sql)
    entrada = cursor.fetchone()

    print(entrada)

    frmPrincipal.totalEntrada.setText(str(entrada))


def somatoria_entrada():
    cursor = banco.cursor()
    try:
        comando_sql = 'SELECT SUM(entrada) FROM fluxo_caixa'
        cursor.execute(comando_sql)
        somatiria_entrada = cursor.fetchall()

        frmPrincipal.totalEntrada.setText(somatiria_entrada)


    except:
        mensagem("Erro de banco")

    cursor.close()

def mostra_view_classe():
    frmview_classe.show()

    cursor = banco.cursor()
    try:
        i = 0
        j = 0
        comando_SQL = "SELECT codigo, nome_classe FROM classe"
        cursor.execute(comando_SQL)
        dados = cursor.fetchall()

        frmview_classe.tb_Classeview.setRowCount(len(dados))
        frmview_classe.tb_Classeview.setColumnCount(2)

        for i in range(0, len(dados)):
            for j in range(0, 2):
                frmview_classe.tb_Classeview.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))

    except:
        mensagem('Erro de conexão')

    cursor.close()

def print_row():
    global id
    global tela

    if tela == 'tela_classe':
        for currentQTableWidgetItem in frmview_classe.tb_Classeview.selectedItems():
            id = currentQTableWidgetItem.text()
    elif tela == 'tela_grupo':
        for currentQTableWidgetItem in frmview_grupo.tb_Grupoview.selectedItems():
            id = currentQTableWidgetItem.text()



def mostra_view_grupo():
    global id
    global tela

    tela = 'tela_classe'

    print_row()

    cursor = banco.cursor()
    print("SELECT codigo, nome_classe FROM classe WHERE codigo = {} OR nome_classe = '{}'".format(id, id))
    cursor.execute("SELECT codigo, nome_classe FROM classe WHERE codigo = '{}' OR nome_classe = '{}'".format(id, id))
    dados = cursor.fetchone()
    valor_id = dados[0]
    id = valor_id

    frmview_grupo.show()

    cursor = banco.cursor()
    try:
        i = 0
        j = 0
        comando_SQL = ("SELECT codigo, nome_grupo FROM grupo WHERE codigo_classe = {}").format(id)
        cursor.execute(comando_SQL)
        dados_grupo = cursor.fetchall()

        frmview_grupo.tb_Grupoview.setRowCount(len(dados_grupo))
        frmview_grupo.tb_Grupoview.setColumnCount(2)

        for i in range(0, len(dados_grupo)):
            for j in range(0,2):
                frmview_grupo.tb_Grupoview.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_grupo[i][j])))

    except:
        mensagem('Erro de conexão')


def mostra_view_subgrupo():
    global id
    global tela

    tela = "tela_grupo"

    print_row()

    cursor = banco.cursor()
    cursor.execute("SELECT codigo, nome_grupo FROM grupo WHERE codigo = '{}' OR nome_grupo = '{}'".format(id,id))
    dados = cursor.fetchone()
    valor_id = dados[0]
    id = valor_id

    frmview_subgrupo.show()

    cursor = banco.cursor()
    try:
        comando_SQL = ("SELECT subgrupo.codigo, subgrupo.nome_subgrupo FROM subgrupo " +
                       "INNER JOIN grupo_subgrupo " +
                       "ON grupo_subgrupo.cod_subgrupo = subgrupo.codigo " +
                       "WHERE grupo_subgrupo.cod_grupo = {}".format(id))

        cursor.execute(comando_SQL)
        dados_subgrupo = cursor.fetchall()

        frmview_subgrupo.tb_Subgrupoview.setRowCount(len(dados_subgrupo))
        frmview_subgrupo.tb_Subgrupoview.setColumnCount(2)

        for i in range(0, len(dados_subgrupo)):
            for j in range (0,2):
                frmview_subgrupo.tb_Subgrupoview.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_subgrupo[i][j])))

    except:
        mensagem('Erro de conexão')


def mostra_cad_classe():
    frmcad_classe.show()

def mostra_cad_grupo():
    frmcad_grupo.show()

def mostra_cad_subgrupo():
    frmcad_subgrupo.show()

def mostra_lancamento():
    cursor = banco.cursor()
    comando_sql = 'SELECT nome_banco FROM banco'
    cursor.execute(comando_sql)
    dados = cursor.fetchall()

    for i in range(0, len(dados)):
        frmcadfluxo_caixa.cbbBanco.addItem(removeCaracterEspecial(str(dados[i])))

    frmcadfluxo_caixa.cbbBanco.setCurrentIndex(-1)
    cursor.close()

    cursor = banco.cursor()
    comando_sql2 = 'SELECT forma_pagamento FROM tipo_pagamento'
    cursor.execute(comando_sql2)
    dados2 = cursor.fetchall()

    for j in range (0, len(dados2)):
        frmcadfluxo_caixa.cbbTipo_pagamento.addItem(removeCaracterEspecial((str(dados2[j]))))

    frmcadfluxo_caixa.cbbTipo_pagamento.setCurrentIndex(-1)
    cursor.close()

    cursor = banco.cursor()
    comando_sql3 = 'SELECT nome_classe FROM classe'
    cursor.execute(comando_sql3)
    dados3 = cursor.fetchall()

    for y in range(0, len(dados3)):
        frmcadfluxo_caixa.cbbClasse.addItem(removeCaracterEspecial(str(dados3[y])))

    frmcadfluxo_caixa.cbbClasse.setCurrentIndex(-1)
    cursor.close()

    frmcadfluxo_caixa.show()

# def real_br_money_mask(my_value):
#     locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
#     valor_em_Real_formatado = locale.currency(my_value)
#     return valor_em_Real_formatado


def exportar_planilha_principal():
    # cursor = banco.cursor()
    # comando_sql = 'SELECT codigo, descricao, DATE_FORMAT(data_transacao, "%d/%m/%Y"), format(entrada,2), format(saida,2) FROM fluxo_caixa'
    # cursor.execute(comando_sql)
    # dados = cursor.fetchall()
    #
    # criar_lista = pd.DataFrame(dados, columns=['codigo','descrição','data', 'entrada', 'saída'])
    #
    # criar_lista.to_excel('lancamentos.xlsx', index=False)
    # mensagem("Lançamento exportado com sucesso")
    # cursor.close()

    cursor = banco.cursor()
    comando_sql = 'SELECT codigo, descricao, DATE_FORMAT(data_transacao, "%d/%m/%Y"), format(entrada,2), format(saida,2) FROM fluxo_caixa'
    cursor.execute(comando_sql)
    dados = cursor.fetchall()

    criar_lista = pd.DataFrame(dados, columns=['codigo','descrição','data', 'entrada', 'saída'])

    criar_lista.to_excel(salvar_arquivo() + '.xlsx', index=False)
    mensagem("Lançamento exportado com sucesso")
    cursor.close()



def importar_planilha_principal():
    global matriz_cpf_cnpj

    planilha = pd.read_excel(ler_arquivo(), None)

    cursor = banco.cursor()
    print(planilha['Planilha1']['DATA'])

    for i in range(len(planilha['Planilha1'])):
        if planilha['Planilha1']['VALOR'][i] >=0:
            comando_sql = 'INSERT INTO fluxo_caixa (cpf_cnpj, data_transacao, descricao, entrada) VALUES (%s, %s, %s, %s)'
        else:
            comando_sql = 'INSERT INTO fluxo_caixa (cpf_cnpj, data_transacao, descricao, saida) VALUES (%s, %s, %s, %s)'

        try:
            dados = (str(matriz_cpf_cnpj), str(valida_data_sql(planilha['Planilha1']['DATA'][i])), str(planilha['Planilha1']['DESCRICAO'][i]),
                    str(planilha['Planilha1']['VALOR'][i]))
        except:
            dados = (str(matriz_cpf_cnpj), str(planilha['Planilha1']['DATA'][i]),
                     str(planilha['Planilha1']['DESCRICAO'][i]), str(planilha['Planilha1']['VALOR'][i]))

        cursor.execute(comando_sql, dados)

    banco.commit()
    mensagem('Lançamentos importados com sucesso')
    cursor.close()

def ler_arquivo():
    arquivo = QtWidgets.QFileDialog.getOpenFileName()[0]

    # with open(arquivo, 'r') as a:
    #     return a.read()

    return arquivo

def salvar_arquivo():

    arquivo = QtWidgets.QFileDialog.getSaveFileName()[0]

    return arquivo

def carrega_grupo():
    vclickclasse = frmcadfluxo_caixa.cbbClasse.currentText()
    frmcadfluxo_caixa.cbbGrupo.clear()

    cursor = banco.cursor()
    comando_SQL = 'SELECT nome_grupo FROM grupo INNER JOIN classe ON classe.codigo = grupo.codigo_classe WHERE nome_classe = "{}"'.format(vclickclasse)
    cursor.execute(comando_SQL)
    dados = cursor.fetchall()

    for i in range(0, len(dados)):
        frmcadfluxo_caixa.cbbGrupo.addItem(removeCaracterEspecial(str(dados[i])))

    cursor.close()


def carrega_subgrupo():
    vclick_grupo = frmcadfluxo_caixa.cbbGrupo.currentText()
    frmcadfluxo_caixa.cbbSubgrupo.clear()

    cursor = banco.cursor()
    comando_sql =("SELECT subgrupo.nome_subgrupo FROM subgrupo " +
                "INNER JOIN grupo_subgrupo ON grupo_subgrupo.cod_subgrupo = subgrupo.codigo "+
                "INNER JOIN grupo ON grupo.codigo = grupo_subgrupo.cod_grupo " +
                "WHERE grupo.nome_grupo = '{}'".format(vclick_grupo))

    cursor.execute(comando_sql)
    dados = cursor.fetchall()

    for i in range (0, len(dados)):
        frmcadfluxo_caixa.cbbSubgrupo.addItem(removeCaracterEspecial(str(dados[i])))
    cursor.close()


##################################################################
# Botões de sair e cancelar

def cad_usuario_cancelar():
    cad_usuario_limpa()
    frmcad_login.close()


def principal_sair():
    frmPrincipal.close()
    frmlogin.show()


def login_cancela():
    login_limpa()
    frmlogin.close()


def cad_forma_pagamento_cancela():
    cad_forma_pagamento_limpa()
    frmcad_tipo_pagamento.close()


def cad_classe_sair():
    frmcad_classe.close()

def view_classe_sair():
    frmview_classe.close()

def cad_grupo_sair():
    frmcad_grupo.close()

def view_grupo_sair():
    frmview_grupo.close()

def cad_subgrupo_sair():
    frmcad_subgrupo.close()

def view_subgrupo_sair():
    frmview_subgrupo.close()


def viewtipo_pagamento_sair():
    frmviewtipo_pagamento.close()

def view_usuarios_sair():
    frmview_usuario.close()

def cad_fluxo_caixa():
    global matriz_cpf_cnpj

    vdata_transacao = frmcadfluxo_caixa.edtData_transacao.text()
    vdescricao      = frmcadfluxo_caixa.edtDescricao.text()
    vbanco          = frmcadfluxo_caixa.cbbBanco.currentText()
    vtipo_pagamento = frmcadfluxo_caixa.cbbTipo_pagamento.currentText()
    vclasse         = frmcadfluxo_caixa.cbbClasse.currentText()
    vgrupo          = frmcadfluxo_caixa.cbbGrupo.currentText()
    vsubgrupo       = frmcadfluxo_caixa.cbbSubgrupo.currentText()
    ventrada        = frmcadfluxo_caixa.edtEntrada.text()
    vsaida          = frmcadfluxo_caixa.edtSaida.text()

    if valida_data(vdata_transacao) == False:
        mensagem('Data inválida')
        return None

    if vdescricao == '':
        mensagem('Favor informar a descrição da despesa/receita')
        return None

    if vbanco == '':
        mensagem('Favor informar banco')
        return None

    if vtipo_pagamento == '':
        mensagem('Favor informar tipo de pagamento/recebimento')
        return None

    if vclasse == '':
        mensagem('Favor informar a classe da despesa/receita')
        return None

    if vgrupo == '':
        mensagem('Favor informar o grupo da despesa/receita')
        return None

    if vsubgrupo == '':
        mensagem('Favor informar subgrupo da despesa/receita')
        return None

    cursor = banco.cursor()

    vcod_classe = busca_codigo_classe(vclasse)

    vcod_banco = busca_codigo_banco(vbanco)

    vcod_tipo_pagamento = busca_codigo_tipo_pagamento(vtipo_pagamento)

    vcod_grupo = busca_codigo_grupo(vgrupo)

    vcod_subgrupo = busca_codigo_subgrupo(vsubgrupo)

    vdata_transacao_sql = valida_data_sql(vdata_transacao)

    ventrada = troca_virgula_por_ponto(ventrada)
    vsaida = troca_virgula_por_ponto(vsaida)

    if (ventrada != '' and vsaida == '') or (ventrada == '' and vsaida != ''):
        try:
            if ventrada != '':
                comando_sql  = 'INSERT INTO fluxo_caixa (cpf_cnpj, descricao, data_transacao, entrada, codigo_classe, codigo_banco, codigo_tipo_pagamento, codigo_grupo, codigo_subgrupo) ' \
                               'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                par = (str(matriz_cpf_cnpj), str(vdescricao), str(vdata_transacao_sql), str(ventrada), str(vcod_classe),
                       str(vcod_banco), str(vcod_tipo_pagamento),
                       str(vcod_grupo), str(vcod_subgrupo))
            else:
                comando_sql = 'INSERT INTO fluxo_caixa (cpf_cnpj, descricao, data_transacao, saida, codigo_classe, codigo_banco, codigo_tipo_pagamento, codigo_grupo, codigo_subgrupo) ' \
                              'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                par = (str(matriz_cpf_cnpj), str(vdescricao), str(vdata_transacao_sql), str(vsaida), str(vcod_classe),
                       str(vcod_banco), str(vcod_tipo_pagamento),
                       str(vcod_grupo), str(vcod_subgrupo))

            cursor.execute(comando_sql,par)
            banco.commit()
            mensagem('Lançamento cadastrado com sucesso!')
            cursor.close()
        except:
            mensagem('Erro de banco de dados')

    elif (ventrada != '' and vsaida != ''):
        mensagem('Favor não inserir valores de estrada e saida ao mesmo tempo')
        return None
    else:
        mensagem('Favor não inserir dois valores de despesa/receita no mesmo lançamento')
        return None


def busca_codigo_classe(var1):
    cursor = banco.cursor()
    comando_sql = "SELECT codigo FROM classe WHERE nome_classe = '{}'".format(var1)
    cursor.execute(comando_sql)
    dados = cursor.fetchone()
    vcod_classe = dados[0]
    cursor.close()
    return vcod_classe


def busca_codigo_banco(var1):
    cursor = banco.cursor()
    comando_sql = "SELECT codigo FROM banco WHERE nome_banco ='{}'".format(var1)
    cursor.execute(comando_sql)
    dados = cursor.fetchone()
    vcod_banco = dados[0]
    cursor.close()
    return vcod_banco


def busca_codigo_tipo_pagamento(var1):
    cursor = banco.cursor()
    comando_sql = "SELECT codigo FROM tipo_pagamento WHERE forma_pagamento = '{}'".format(var1)
    cursor.execute(comando_sql)
    dados = cursor.fetchone()
    vcod_tipo_pagamento = dados[0]
    cursor.close()
    return vcod_tipo_pagamento


def busca_codigo_grupo(var1):
    cursor = banco.cursor()
    comando_sql = "SELECT codigo FROM grupo WHERE nome_grupo = '{}'".format(var1)
    cursor.execute(comando_sql)
    dados = cursor.fetchone()
    vcod_grupo = dados[0]
    cursor.close()
    return vcod_grupo


def busca_codigo_subgrupo(var1):
    cursor = banco.cursor()
    comando_sql = "SELECT codigo FROM subgrupo WHERE nome_subgrupo = '{}'".format(var1)
    cursor.execute(comando_sql)
    dados = cursor.fetchone()
    vcod_subgrupo = dados[0]
    cursor.close()
    return vcod_subgrupo

####################################################################
# #Limpeza
def cad_usuario_limpa():
    frmcad_login.edtNome.setText('')
    frmcad_login.edtEmail.setText('')
    frmcad_login.edtCPF.setText('')
    frmcad_login.edtEndereco.setText('')
    frmcad_login.edtTelefone.setText('')
    frmcad_login.edtCep.setText('')
    frmcad_login.edtUsuario.setText('')
    frmcad_login.edtSenha.setText('')
    frmcad_login.edtBairro.setText('')
    frmcad_login.edtComplemento.setText('')
    frmcad_login.edtUF.setText('')




def login_limpa():
    frmlogin.edtUsuario.setText('')
    frmlogin.edtSenha.setText('')


def cad_forma_pagamento_limpa():
    frmcad_tipo_pagamento.edtTipo_pagamento.setText('')


def cad_classe_limpa():
    frmcad_classe.edtClasse.setText('')

def cad_grupo_limpa():
    frmcad_grupo.edtGrupo.setText('')

def cad_subgrupo_limpa():
    frmcad_subgrupo.edtSubgrupo.setText('')



#################################################### Validadores de dados de cadastro e entrada
# Função de validar cpf
def cpf_validador(numero):
    # Botar os números do cpf e ignora outros caracteres
    if frmcad_login.rbCPF.isChecked():
        cpf = [int(char) for char in numero if char.isdigit()]

        # Verifica se o cpf tem 11 digitos
        if len(cpf) != 11:
            return False

        # Verifica se o CPF tem todos os números iguais  ex: 111.111.111-11
        # Verifica se o CPF são considerados invalidos mas passam na validação dos digitos
        if cpf == cpf[::-1]:
            return False

        # Valida os dois últimos digitos verificadores
        for i in range(9, 11):
            value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                return False


    elif frmcad_login.rbCNPJ.isChecked():
        numero = removeCaracter(frmcad_login.edtCPF.text())
        if len(numero) != 14:
            return False

        if numero in (c * 14 for c in "1234567890"):
            return False

        cnpj_r = numero[::-1]
        for i in range(2, 0, -1):
            cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
            dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
            if cnpj_r[i - 1:i] != str(dv % 10):
                return False


# Função de validar email - Precisa melhorar
def email_validador(email):
    if (re.search(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', email)):
        print("Email válido")
        return True

    else:
        print("E-mail inválido")
        return False


# Função de validar nome
def nome_validador(nome):
    if len(nome) > 2:
        return True
    else:
        return False


# Função de validar mascara do telefone
def telefone_validador(numero):
    if len(numero) != 15:
        return False
    else:
        frmcad_login.edtTelefone.inputMask = '(00)0 0000-0000'


# Função de mensagem
def mensagem(msg):
    frmmsg.txtMsg.setText(msg)
    frmmsg.show()


# Função sair mensagem
def sair_mensagem():
    frmmsg.close()


# Função buscar cep
def buscar_cep():
    cep = frmcad_login.edtCep.text()

    if len(cep) != 9:
        return False

    request = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep))

    dados = request.json()

    if 'erro' not in dados:
        frmcad_login.edtEndereco.setText((dados['logradouro']))
        frmcad_login.edtBairro.setText((dados['bairro']))
        frmcad_login.edtComplemento.setText(dados['complemento'])
        frmcad_login.edtUF.setText(dados['localidade'] + ' - ' + dados['uf'])
    else:
        return False


# Função busca CNPJ
def busca_cnpj():
    if frmcad_login.rbCPF.isChecked():
        mensagem('Essa pesquisa não é valida para CPF')
        return None

    cnpj = frmcad_login.edtCPF.text()

    filtro_cnpj = filter(str.isdigit, cnpj)

    filtro_final = "".join(filtro_cnpj)

    if len(filtro_final) != 14:
        return False

    request = requests.get('https://publica.cnpj.ws/cnpj/{}'.format(filtro_final))

    dados = request.json()

    if dados['cnpj_raiz'] != '':
        frmcad_login.edtNome.setText(dados['razao_social'])
        frmcad_login.edtCep.setText(dados['estabelecimento']['cep'])
    else:
        return False


# Função de ativar mascara CPF
def ativaCPF():
    if frmcad_login.rbCPF.isChecked():
        frmcad_login.edtCPF.setInputMask('000.000.000-00')


# Função de ativar mascara CPF
def ativaCNPJ():
    if frmcad_login.rbCNPJ.isChecked():
        frmcad_login.edtCPF.setInputMask('00.000.000/0000-00')


def ativaCPF_login():
    if frmlogin.rbCPF.isChecked():
        frmlogin.edtUsuario.setInputMask('000.000.000-00')


def ativaCPNJ_login():
    if frmlogin.rbCNPJ.isChecked():
        frmlogin.edtUsuario.setInputMask('00.000.000/0000-00')


# Função de remoção de caracter do Jayme - tem que usar o import re
def removeCaracter(texto):
    texto = re.sub('[^0-9]', '', texto)

    return texto


def removeCaracterEspecial(texto):
    objeto_remocao = texto
    simbolos_remocao = "'()!?,/"

    for x in range(len(simbolos_remocao)):
        objeto_remocao = objeto_remocao.replace(simbolos_remocao[x],"")
    return objeto_remocao

#    texto = re.sub(r"[^a-zA-Z0-9]","", texto) # retirei pois não retirava os espaços
#    return texto

def troca_virgula_por_ponto(texto):
    objeto_remocao = texto
    simbolos_remocao = ","

    for x in range(len(simbolos_remocao)):
        objeto_remocao = objeto_remocao.replace(simbolos_remocao[x],".")
    return objeto_remocao


# Formulários
app = QtWidgets.QApplication([])
frmcad_login = uic.loadUi('ucad_login.ui')
frmlogin = uic.loadUi('ulogin.ui')
frmview_usuario = uic.loadUi('uview_cad_usuario.ui')
frmcadfluxo_caixa = uic.loadUi('ucadfluxo_caixa.ui')
frmview_fluxo_caixa = uic.loadUi('uview_fluxo_caixa.ui')
frmcad_classe = uic.loadUi('ucad_classe.ui')
frmcad_grupo = uic.loadUi('ucad_grupo.ui')
frmcad_subgrupo = uic.loadUi('ucad_subgrupo.ui')
frmviewcad_classe = uic.loadUi('uview_classe.ui')
frmcad_banco = uic.loadUi('ucad_banco.ui')
frmview_bancos = uic.loadUi('uview_bancos.ui')
frmcad_tipo_pagamento = uic.loadUi('ucad_tipo_pagamento.ui')
frmviewtipo_pagamento = uic.loadUi('uview_tipo_pagamento.ui')
frmmsg = uic.loadUi('uMsg.ui')
frmPrincipal = uic.loadUi('uPrincipal.ui')
frmview_classe = uic.loadUi('uselecao_classe.ui')
frmview_grupo = uic.loadUi('uselecao_grupo.ui')
frmview_subgrupo = uic.loadUi('uselecao_subgrupo.ui')

# botões
frmlogin.btnCadastrar.clicked.connect(mostra_cad_usuario)
frmcad_login.btnCadastrar.clicked.connect(cad_usuario)
frmcad_login.btnCancelar.clicked.connect(cad_usuario_cancelar)
frmmsg.btnFechar.clicked.connect(sair_mensagem)
frmcad_login.btnConsultar.clicked.connect(buscar_cep)
frmcad_login.rbCPF.clicked.connect(ativaCPF)
frmcad_login.rbCNPJ.clicked.connect(ativaCNPJ)
frmcad_login.btnConsultar_CNPJ.clicked.connect(busca_cnpj)
frmlogin.btnEntrar.clicked.connect(verificacao_entrada)
frmPrincipal.btnCadastro_banco.clicked.connect(mostra_view_banco)
frmPrincipal.btnSair.clicked.connect(principal_sair)
frmPrincipal.btnCadastro_pagamento.clicked.connect(mostra_view_pagamento)
frmPrincipal.btnLancamento.clicked.connect(mostra_lancamento)
frmPrincipal.btnCadastro_usuario.clicked.connect(mostra_view_usuario)
frmPrincipal.btnImportar.clicked.connect(importar_planilha_principal)
frmPrincipal.btnExportar.clicked.connect(exportar_planilha_principal)
frmcad_banco.btnCadastrar.clicked.connect(cadastro_banco)
frmcad_banco.btnCancelar.clicked.connect(cad_banco_cancela)
frmview_bancos.btnCadastrar.clicked.connect(mostra_cadastro_banco)
frmview_bancos.btnCancelar.clicked.connect(view_bancos_sair)
frmview_bancos.btnExcluir.clicked.connect(exclui_banco)
frmlogin.rbCPF.clicked.connect(ativaCPF_login)
frmlogin.rbCNPJ.clicked.connect(ativaCPNJ_login)
frmlogin.btnCancelar.clicked.connect(login_cancela)
frmcad_tipo_pagamento.btnCadastrar.clicked.connect(cadastro_tipo_pagamento)
frmcad_tipo_pagamento.btnCancelar.clicked.connect(cad_forma_pagamento_cancela)
frmviewtipo_pagamento.btnCadastrar.clicked.connect(mostra_cad_pagamento)
frmviewtipo_pagamento.btnCancelar.clicked.connect(viewtipo_pagamento_sair)
frmPrincipal.btnCadastro_classe.clicked.connect(mostra_view_classe)
frmview_classe.btnCadastrar.clicked.connect(mostra_cad_classe)
frmview_classe.btnCancelar.clicked.connect(view_classe_sair)
frmcad_classe.btnCadastrar.clicked.connect(cad_classe)
frmcad_classe.btnCancelar.clicked.connect(cad_classe_sair)
frmview_classe.tb_Classeview.doubleClicked.connect(mostra_view_grupo)
frmview_grupo.btnCadastrar.clicked.connect(mostra_cad_grupo)
frmview_grupo.btnCancelar.clicked.connect(view_grupo_sair)
frmcad_grupo.btnCadastrar.clicked.connect(cad_grupo)
frmcad_grupo.btnCancelar.clicked.connect(cad_grupo_sair)
frmview_grupo.tb_Grupoview.doubleClicked.connect(mostra_view_subgrupo)
frmview_subgrupo.btnCadastrar.clicked.connect(mostra_cad_subgrupo)
frmview_subgrupo.btnCancelar.clicked.connect(view_subgrupo_sair)
frmcad_subgrupo.btnCadastrar.clicked.connect(cad_subgrupo)
frmcad_subgrupo.btnCancelar.clicked.connect(cad_subgrupo_sair)
frmcadfluxo_caixa.cbbClasse.activated.connect(carrega_grupo)
frmcadfluxo_caixa.cbbGrupo.activated.connect(carrega_subgrupo)
frmcadfluxo_caixa.btnCadastro.clicked.connect(cad_fluxo_caixa)
frmview_usuario.btnCancelar.clicked.connect(view_usuarios_sair)



# Inicializar
frmlogin.show()
app.exec()
