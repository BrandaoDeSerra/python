
x = 1
while x < 10:
    x += 1
    print(x)
print("----------------------")

for letra in "abcdefgh":    
    print(letra)
print("----------------------")

for x in range(10):    
    print(x)
print("----------------------")

#cescente
for x in range(1,10):    
    print(x)
print("----------------------")

# Crescente de 2 em 2
for x in range(0,10,2):    
    print(x)
print("----------------------")

# Decrescente
for x in range(10,0,-1):    
    print(x)    
print("----------------------")    

numero = 22

for numero in range(1,5):
    if numero < 2:
        print("Numero menor que 2")
    else:
        print("Maior ou Igual a 2")
    print("Numero: {}".format(numero))

quantidade = 0;
for letra in "rochedo":
    if letra=="o":
        quantidade = quantidade+1
print("Quantidade de Letras o : {}".format(quantidade))


comando = input("Digite o comando SAIR ou CONTINUE : ")

while comando != "SAIR":
    comando = input("Digite o comando : ")

print("Programa encerrado")






