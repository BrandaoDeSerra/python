idade = input("Qual sua idade : ")

try:
    val = int(idade)
    print("A idade digitada foi: ", val)
except ValueError:
    print("Digite uma idade!")
    exit()

idade = val

if idade >= 18:
    print("Maior Idade")
else:
    print("Menor")

# 3 condições
if idade > 18:
    print("Maior que 18")
elif idade < 18:
    print("Menor que 18")
else:
    print("Igual a 18")
     
if idade <= 100 and idade >= 10:
    print("Entre 10 e 100")

if idade <= 100 and (idade == 20 or idade == 40):
    print("Idade igual a 20 ou 40")

print("Fim")