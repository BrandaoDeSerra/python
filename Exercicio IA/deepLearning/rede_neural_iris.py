import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

base = datasets.load_iris()
previsores = base.data
classe = base.target

classe_dummy = np_utils.to_categorical(classe)

X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(previsores,
                                                                  classe_dummy,
                                                                  test_size = 0.3,
                                                                  random_state = 0)

modelo = Sequential()
modelo.add(Dense(units = 5, input_dim = 4))
modelo.add(Dense(units = 4))
modelo.add(Dense(units = 3, activation = 'softmax'))

modelo.summary()

# imprimir

modelo.compile(optimizer = 'adam', loss = 'categorical_crossentropy',
               metrics = ['accuracy'])
modelo.fit(X_treinamento, y_treinamento, epochs = 1000,
           validation_data = (X_teste, y_teste))

previsoes = modelo.predict(X_teste)
previsoes = (previsoes > 0.5)

#v = ConfusionMatrix(modelo)

y_teste_matrix = [np.argmax(t) for t in y_teste]
y_previsao_matrix = [np.argmax(t) for t in previsoes]
confusao = confusion_matrix(y_teste_matrix, y_previsao_matrix)