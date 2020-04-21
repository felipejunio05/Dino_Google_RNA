# -*- coding: utf-8 -*-

# Author: Felipe Junio da Rocha
# Date: 2020/04/13

import random
from dino import Dino

from numpy import array
from numpy import reshape
from numpy import empty
from numpy import uint32
from numpy import where

from time import sleep
from os import listdir
from os.path import isfile
from os.path import isdir
from os.path import exists

from keras import backend as K


__all__ = ['Dna']


class Dna:
    def __init__(self) -> object:
        self.__dino: list = None

    @property
    def dino(self):
        return self.__dino

    def createDNA(self, p: int) -> None:
        pop: list = []

        if self.__dino is None:
            for i in range(p):
                pop.append(Dino())

            self.__dino = pop
        else:
            if p > len(self.__dino):
                for i in range(len(self.__dino), p):
                    self.__dino.append(Dino())
            else:
                index = len(self.__dino) - 1

                while len(self.__dino) >= p:
                    del self.__dino[index]
                    index -= 1

    def loadDNA(self, directory: str) -> bool:
        elements: list
        ret: bool = False

        if exists(directory):
            if isdir(directory):
                elements = listdir(directory)

                aux: Dino = None
                self.__dino = []

                for i in elements:
                    if i[-2:] == 'h5':
                        try:
                            aux = Dino()
                            aux.model.load_weights(directory + i)
                            self.__dino.append(aux)

                        except ValueError as error:
                            self.destroyDNA()
                            raise ValueError(error)

                        except TypeError as error:
                            self.destroyDNA()
                            raise TypeError(error)

                        except OSError:
                            self.destroyDNA()
                            raise OSError(error)
                        else:
                            ret = True
                    else:
                        raise TypeError("este diretorio não possui arquivos que possa ser carregados para o modelo")
            else:
                raise ValueError("O destino informado não é um diretorio.")
        else:
            raise ValueError("O destino informado não existe.")

        return ret

    def destroyDNA(self) -> None:
        index = len(self.__dino) - 1

        while len(self.__dino) > 0:
            del self.__dino[index]
            index -= 1

        self.__dino: list = None
        K.clear_session()

    def pop_weights(self) -> array:
        pop_w: list = []

        for i in range(len(self.__dino)):
            pop_w.append(array(self.__dino[i].pullWht()))

        return array(pop_w)

    def update_pop(self, w) -> None:
        aux: list = []

        for i in range(len(w)):
            self.__dino[i].pushWht(w[i])

    def to_vector(self, pop) -> array:
        pop_v_h: list = []
        pop_v_b: list = []

        for p in range(pop.shape[0]):
            hidden = []
            bias = []

            for l in range(pop.shape[1]):
                h = reshape(pop[p, l][0], newshape=pop[p, l][0].size)
                b = pop[p, l][1]

                hidden.extend(h)
                bias.extend(b)

            pop_v_h.append(hidden)
            pop_v_b.append(bias)

        return array(pop_v_h), array(pop_v_b)

    def to_matrix(self, v: tuple, m: array) -> array:
        weights: list = []

        for p in range(m.shape[0]):
            start_h: int = 0
            start_b: int = 0
            end_h: int = 0
            end_b: int = 0

            for l in range(m.shape[1]):
                end_h = end_h + m[p, l][0].size
                end_b = end_b + m[p, l][1].size

                curr_h = v[0][p, start_h:end_h]
                curr_b = v[1][p, start_b:end_b]

                h = reshape(curr_h, newshape=m[p, l][0].shape)
                b = reshape(curr_b, newshape=m[p, l][1].shape)

                weights.append(h)
                weights.append(b)

                start_h = end_h
                start_b = end_b

        return reshape(weights, newshape=m.shape)

    def naturalSelection(self, pop: array, score: array, parents: int) -> array:
        p: array = empty((parents, pop.shape[1]))

        for i in range(parents):
            best_dino = where(score == score.max())
            best_dino = best_dino[0][0]

            p[i, :] = pop[best_dino, :]
            score[best_dino] = 0

        return p

    def crossover(self, p: array, size: int) -> array:
        offs: array = empty(size)
        cross: int = uint32(size[1] / 2)

        for i in range(size[0]):
            p1 = i % p.shape[0]
            p2 = (i + 1) % p.shape[0]

            offs[i, 0:cross] = p[p1, 0:cross]
            offs[i, cross:] = p[p2, cross:]

        return offs

    def mutation(self, offs: array, mut: int) -> array:
        n_m: int = uint32((mut * offs.shape[1]) / 100)
        i_m: array = array(random.sample(range(0, offs.shape[1]), n_m))

        for i in range(offs.shape[0]):
            select: int = random.choice([1, 2, 3])

            if select == 1:
                offs[i, i_m] = random.uniform(-1., 1)

            elif select == 2:
                offs[i, i_m] = offs[i, i_m] + random.uniform(-1., 1)

            elif select == 3:
                offs[i, i_m] = offs[i, i_m] * random.uniform(-1.5, 1.5)

        return offs