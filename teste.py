objeto_remocao = "('!?texto)"

simbolos_remocao = " '()!? "

for x in range(len(simbolos_remocao)):
    objeto_remocao = objeto_remocao.replace(simbolos_remocao[x], "")

print(objeto_remocao)


