'''  Array '''
meuVetor = [1,20,3,4,35]
print(meuVetor)

meuVetor.reverse()
print(meuVetor)

bkp = sorted(meuVetor)
print(bkp,meuVetor)

meuVetor.sort()
print(meuVetor)

meuVetor.sort(reverse=True)
print(meuVetor)

if 3 in meuVetor:
    print("3 Está no meu vetor")
else:
    print("3 não está no meu vetor")

del meuVetor[3:]
print(meuVetor)

del meuVetor[:]
print(meuVetor)

meuVetor = [] #vetor em branco
meuVetor.append(1)
print(meuVetor)

exit()

'''  Matriz 3x3  0,1,2 - 0,1,2  '''
matriz  = [[3,5,8],[1,7,9],[2,4,8]]
print(matriz)

print(matriz[0][0])
print(matriz[2][1])


'''  Lista '''
lista = list(range(5))
for n in lista:
    lista[n] = int(input("Digite um valor : "))
lista.append(99) #append
print(lista)   
print(len(lista))    
   
for l in lista:
   print("- lista de valores : ",l)    

print("Posição 0  do Vetor : ",meuVetor[0])
print("Posição 0  do Vetor : ",meuVetor[1])
print("Posição 0  do Vetor : ",meuVetor[2])
print("Posição 0  do Vetor : ",meuVetor[3])
print("Posição 0  do Vetor : ",meuVetor[4])

for valor in meuVetor:
   print("> Posição 0 do Vetor : ",valor)
   
meuVetor = sorted(meuVetor, reverse=True)
print(meuVetor)

meuVetor = sorted(meuVetor, reverse=False)
print(meuVetor)