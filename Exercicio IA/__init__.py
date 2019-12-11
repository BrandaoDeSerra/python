# arrayX = [-1,-0.5,0,0.5,1]
# for x in arrayX:
#    y = x**2 + x + 1
#    print('x='+str(x)+' => f(x)='+str(y))

# carrega bibliotecas
import numpy as np
import matplotlib.pyplot as plt

# dados de cada estado
SP = (0.9 * np.random.rand(20), 0.9 * np.random.rand(20))
MG = (0.2 * np.random.rand(20), 0.2 * np.random.rand(20))

# agrupa tabela
tabela_completa = (SP, MG)

# determina cor de cada estado no grafico
cores = ("blue", "green")

# cria um label para os grupos
estados = ("SP", "MG")

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
ax.scatter(1, 1, alpha=0.8, c='red', edgecolors='none', s=30, label='SP')
for data, color, group in zip(tabela_completa, cores, estados):
    x, y = data
    ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)

# titulo do grafico
plt.title('Evolução PSO')

arrayX = [-1, -0.5, 0, 0.5, 1]
soma1 = 0
soma2 = 0
soma3 = 0
soma4 = 0
somaf1 = 0
somaf2 = 0
for x in arrayX:
    y1 = x + 1 - 0
    soma1 = soma1 + y1
    print('x=' + str(x) + ' => y1=' + str(y1))
    y2 = 1 + (x * x)
    soma2 = soma2 + y2
    print('x=' + str(x) + ' => y2=' + str(y2))
    y3 = 2 + 0
    soma3 = soma3 + y3
    print('x=' + str(x) + ' => y3=' + str(y3))
    y4 = x * ((-1) - (-2))
    soma4 = soma4 + y4
    print('x=' + str(x) + ' => y4=' + str(y4))
    print('------------------------------')

print('soma1=' + str(soma1))
print('soma2=' + str(soma2))
print('soma3=' + str(soma3))
print('soma4=' + str(soma4))

for x in arrayX:
    y1 = 1 + (2 * (5 - (-1)))
    somaf1 = somaf1 + y1
    print('x=' + str(x) + ' => y1=' + str(y1))
    y2 = x + (x * x)
    somaf2 = somaf2 + y2
    print('x=' + str(x) + ' => y2=' + str(y2))
    print('------------------------------')

print('somaf1=' + str(somaf1))
print('somaf2=' + str(somaf2))

somaf1 = 0
somaf2 = 0
for x in arrayX:
    y1 = x - x
    somaf1 = somaf1 + y1
    print('x=' + str(x) + ' => y1=' + str(y1))
    y2 = (x + 1) * ((-1) + (-2))
    somaf2 = somaf2 + y2
    print('x=' + str(x) + ' => y2=' + str(y2))
    print('------------------------------')

print('somaf1=' + str(somaf1))
print('somaf2=' + str(somaf2))
'''
print("Wello World")
a = 2
b = 0
try:
    print(a/b)
except:
    print("Divisão por zero não pode");    

b = 1    
try:
    print(a/b)
except:
    print("Divisão por zero não pode");        
'''