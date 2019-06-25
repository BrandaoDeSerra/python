''' chamando função importando de outro arquivo '''

''' Import '''
from src.functions import somaValores2, somaValores1

# tipos de dados int / float / String / booleano
var1 = 1
var2 = 1.1
var3 = "Texto "+"\n"
print(len(var3))
print(var3[0])
print(var3[1:4]) #uma parte
print(var3[1:]) #Até o final

print(var3.lower())
print(var3.upper())

var3 = var3.strip() #tira a quebra de linha \n e Espaço
print(var3)

busca = var3.find("ex") #se não achou retorna -1
print(busca)

print(var3.replace("ex","@"))

lista = var3.splint();
print(lista)



var4 = True
var5 = False

# conversão de tipos de dados 
var6 = int("10")
var7 = str(10)
var8 = bool("True")
var9 = float(10)

print("Brandão"+" "+"Rochedo")
print("Brandão"+" "+str(10))
print("Brandão {}".format(10))

valor = somaValores2(1,1)
print("Soma Def retorn : ",valor)

somaValores1(1,2)

numero1 = 16 #float(input("Número 1 : "))

numero2 = 4 #float(input("Número 2 : "))

print("Soma : ",(numero1 + numero2))

print("Subtração : ",(numero1 - numero2))

print("Multiplicação : ",(numero1 * numero2))

print("Divisão : ",(numero1 / numero2))

print("Resto Divisão : ",(numero1 % numero2))

print("Potência ² número1 : ",(numero1**2))

print("Potência ² número2 : ",(numero2**2))

''' A radiciação, matematicamente falando, é o inverso da potenciação. '''
print("Raiz ² número1 : ",(numero1**(1/2)))

if ( numero1 > numero2 ):
   print("Número 1 é MAIOR que o Número2")

if ( numero1 < numero2 ):
   print("Número 1 é MENOR que o Número2")

if ( numero1 >= numero2 ):
   print("Número 1 é MAIOR ou IGUAL ao Número2")

if ( numero1 <= numero2 ):
   print("Número 1 é MENOR ou IGUAL ao Número2")
   
if ( numero1 == numero2 ):
   print("Número 1 é IGUAL ao Número2")

if ( numero1 != numero2 ):
   print("Número 1 é IGUAL ao Número2")
   
if (numero1 != numero2 and numero1 < numero2 ):
   print("Número 1 é DIFERENTE e MENOR do que o Número 2")
   
if (numero1 != numero2 or numero1 == numero2 ):
   print("Número 1 é DIFERENTE ou IGUAL ao Número 2")   

if (numero1 != numero2 or numero1 == numero2) and (not var5):
   print("Número 1 é DIFERENTE ou IGUAL ao Número 2 e Var5 é FALSO")   
 
if (not var5):
    print("Varíavel var5 é :",var5)   
      
total1 = 1
total2 = 1
for sequenca in range(0,5):
    total1 =+ 1
    total2 += 1
    
print("Total1 : {} / Total2 : {} ".format(total1,total2))
