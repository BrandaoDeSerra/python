# -*- coding: utf-8 -*-

arq = open("arquivo.txt","r",encoding="utf-8")
print(arq)
arq.close
print("----------------------")

arq = open("arquivo.txt","r",encoding="utf-8")
textoCompleto = arq.read()
print(textoCompleto)
arq.close
print("----------------------")

arq = open("arquivo.txt","r",encoding="utf-8")
linhasDoArquivo = arq.readlines()
print(linhasDoArquivo)
arq.close()
print("----------------------")

arq = open("arquivo_new.txt","w",encoding="utf-8") #apaga se já exite
arq.write("Eu sei Python \nVamos em frente")
arq.close()
print("----------------------")

arq = open("arquivo_new.txt","a",encoding="utf-8") #náo apaga se já exite, só complementa ao fim
arq.write("Eu sei Python \nVamos em frente")
arq.close()
print("----------------------")


