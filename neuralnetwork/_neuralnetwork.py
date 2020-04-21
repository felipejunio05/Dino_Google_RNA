# -*- coding: utf-8 -*-

# Author: Felipe Junio da Rocha
# Date: 2020/04/13


from keras.layers.normalization import BatchNormalization
from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import Flatten
from keras.layers import Input
from keras.models import Model
from keras.layers import MaxPooling2D


__all__ = ['NeuralNetwork']


class Layers:
    def __init__(self) -> object:
        super().__init__()

        self.__x: Input = None
        self.__y: Dense = None

        self.__layers: list = [True, True, True, True]

    @property
    def x(self) -> Input:
        return self.__x

    @property
    def y(self) -> Dense:
        return self.__y

    def input_layer(self, shape: tuple) -> bool:
        ret: bool = False

        if self.__layers[0]:
            self.__x = Input(shape=shape)
            ret, self.__layers[0] = True, False

        else:
            print("Camada de entrada já foi criada")

        return ret

    def convolution(self, conv: int, pooling: int, filters: int = 64, kernel_size: tuple = (2, 2), strides: tuple = (2, 2), activation: str = 'relu') -> bool:
        ret: bool = False

        if not self.__layers[0]:
            if self.__layers[1]:
                self.__c_conv(conv, pooling, filters=filters, kernel_size=kernel_size, strides=strides, activation=activation)
                self.__y = Flatten()(self.__y)
                self.__y = BatchNormalization()(self.__y)

                ret, self.__layers[1] = True, False
            else:
                raise ValueError("Camada de convolução já foi criada.")
        else:
            raise ValueError("Camada de entrada não foi criada.")

        return ret

    def hidden_layers(self, neurons: int = 1, layers: int = 1, activation: str = 'relu', kernel_initializer: str = 'normal', bias: str = 'ones', drop: float = 0) -> bool:
        ret: bool = False

        if not self.__layers[0]:
            self.__h_layers(neurons, layers, activation, kernel_initializer, drop, bias)
            ret, self.__layers[2] = True, False

        elif self.__x is not None and self.__y is not None:
            print("Camada o oculta já foi criada")

        return ret

    def output_layer(self, neurons: int = 1, activation: str = 'sigmoid', bias: str = 'ones') -> bool:
        ret: bool = False

        if not self.__layers[2]:
            if self.__layers[3]:
                self.__y = Dense(units=neurons, activation=activation, bias_initializer=bias)(self.__y)

                ret, self.__layers[0] = True, False

            else:
                print("Camada de saida já foi criada.")
        else:
            raise ValueError("Camada Oculta não foi criada")

        return ret

    def __h_layers(self, neurons: int, layers: int, activation: str, kernel_initializer: str, drop: float, bias: str) -> None:
        if self.__layers[1]:
            self.__y = Dense(units=neurons, activation=activation, kernel_initializer=kernel_initializer, bias_initializer=bias)(self.__x)

            if drop > 0:
                self.__y = Dropout(drop)(self.__y)

            for i in range(layers - 1):
                self.__y = Dense(units=neurons, activation=activation, kernel_initializer=kernel_initializer, bias_initializer=bias)(self.__y)

                if drop > 0:
                    self.__y = Dropout(drop)(self.__y)
        else:
            for i in range(layers):
                self.__y = Dense(units=neurons, activation=activation, kernel_initializer=kernel_initializer, bias_initializer=bias)(self.__y)

                if drop > 0:
                    self.__y = Dropout(drop)(self.__y)

    def __c_conv(self, conv: int, pooling: int, filters=64, kernel_size=(2, 2), strides=(2, 2), activation='relu', pool_size=(2, 2)) -> None:

        if conv >= pooling:
            self.__y = Conv2D(filters, kernel_size=kernel_size, strides=strides, activation=activation)(self.__x)
            self.__y = MaxPooling2D(pool_size=pool_size)(self.__y)

            for i in range(conv - 1):
                if isinstance(filters, int):
                    self.__y = Conv2D(filters, kernel_size=kernel_size, strides=strides, activation=activation)(self.__y)
                elif conv > 1 and isinstance(filters, list):
                    if len(filters) == (conv + 1):
                        for j in range(len(filters)):
                            self.__y = Conv2D(j, kernel_size=kernel_size, strides=strides, activation=activation)(self.__y)

                if pooling > 0 and pooling > (i + 1):
                    self.__y = MaxPooling2D(pool_size=pool_size)(self.__y)
        else:
            raise ValueError("A quantidade de camadas de convolução tem que ser maior ou igual de Pooling")


class NeuralNetwork(Layers):
    def __init__(self) -> object:
        super(NeuralNetwork, self).__init__()

        self.__model: Model = None

    def compile(self, optimizer: str = 'adam', loss: str = 'mse', metrics: list = ['accuracy']) -> None:
        try:
            self.__model = Model(self.x, self.y)
            self.__model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        except ValueError:
            raise Exception("As camadas não foram criadas")

    @property
    def model(self) -> Model:
        return self.__model

    @model.setter
    def model(self, x: Model) -> None:
        self.__model = x
