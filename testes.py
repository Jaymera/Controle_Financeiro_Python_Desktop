from PyQt5 import uic, QtWidgets
import mysql.connector
import requests
from reportlab.pdfgen import canvas
import re
from itertools import cycle

numero_id = 1


#Banco de dados
banco = mysql.connector.connect(
    host='150.230.82.105',
    user='vitor',
    password='VBc@834422',
    database='projeto_01'
)

vlogin = "015.219.171-24"
vsenha = "VBc@834422"

cursor = banco.cursor()
comando_SQL = "SELECT cpf_cnpj, senha FROM usuario WHERE cpf_cnpj = '{}' AND senha = '{}'".format(vlogin, vsenha)
#dados = str(vlogin)
cursor.execute(comando_SQL)

resultado = cursor.fetchall()


print(resultado)

