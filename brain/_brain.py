# -*- coding: utf-8 -*-
#
# Author: Felipe Junio da Rocha
# Date: 2020/04/13

from neuralnetwork._neuralnetwork import NeuralNetwork
from numpy import ones
from numpy import array

__all__ = ['Brain']


class Brain(NeuralNetwork):
    def __init__(self, inp, neurons, layers, out) -> object:
        super(Brain, self).__init__()

        self.input_layer((inp, ))
        self.hidden_layers(neurons, layers, 'relu', 'random_uniform')
        self.output_layer(out, activation='sigmoid')
        self.compile(loss='mse', metrics=['accuracy'])

    def pullWht(self) -> list:
        w = []

        for i in range(1, len(self.model.layers)):
            w.append(self.model.layers[i].get_weights())

        return w

    def pushWht(self, w: array) -> None:
        for i in range(w.shape[0]):
            self.model.layers[i + 1].set_weights([w[i][0], w[i][1]])

