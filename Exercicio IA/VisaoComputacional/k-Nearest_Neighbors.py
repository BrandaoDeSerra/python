#KNN K vizinhos mais próximos - usados para classificação e regressão
# -> usa a distancia enclidiana d = raiz[ (x2-x1)² + (y2 -y1)² + (ref2 - ref1)² ]
# -> Definição do K , o ideal que seja impar 3,5,7,9,...

from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import seaborn as sb
import numpy as np

df = pd.read_csv('./arquivos/iris.csv')

sb.pairplot(df, hue='target')

X = np.array(df.drop('target',1))
y = np.array(df.target)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X,y)
print(knn.predict([[6.5,6.5,4.7,1.3]]))
