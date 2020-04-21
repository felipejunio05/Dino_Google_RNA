# -*- coding: utf-8 -*-
#
# Author: Felipe Junio da Rocha
# Date: 2020/04/13

from dna import Dna

from selenium import webdriver
from chromedriver_binary import chromedriver_filename
from selenium.common.exceptions import JavascriptException

from numpy import array
from numpy import empty
from time import sleep

from os import mkdir
from os import listdir
from os.path import isdir
from os.path import exists
from os import name as os_name
from os import system as os_system

from keyboard import is_pressed


__all__ = ["Game"]


class Game(Dna):
    def __init__(self) -> object:
        super(Game, self).__init__()

        self.__browser: webdriver = None
        self.__quit: bool = False
        self.__figure = None

    def open(self):
        self.__browser = webdriver.Chrome()
        self.__browser.set_window_position(x=-10, y=0)
        self.__browser.set_window_size(665, 1000)
        self.__browser.get('chrome://dino')

        sleep(3)

    def close(self) -> None:
        self.__browser.quit()

        del self.__browser
        self.__browser = None

    def score(self) -> int:
        score_array = self.__browser.execute_script("return Runner.instance_.distanceMeter.digits")
        score = ''.join(score_array)

        return int(score)

    def distance(self):
        d: int

        try:
            d = self.__browser.execute_script("return Runner.instance_.horizon.obstacles[0].xPos")
        except JavascriptException:
            d = 0

        return d

    def rexHeight(self):
        h: int

        try:
            h = self.__browser.execute_script("return Runner.instance_.canvas.height - Runner.instance_.tRex.yPos - 10")
        except JavascriptException:
            h = 0

        return h

    def height(self):
        h: int

        try:
            h = self.__browser.execute_script("return Runner.instance_.canvas.height - Runner.instance_.horizon.obstacles[0].yPos")
        except JavascriptException:
            h = 0

        return h

    def width(self):
        w: int

        try:
            w = self.__browser.execute_script("return Runner.instance_.horizon.obstacles[0].typeConfig['width']")
        except JavascriptException:
            w = 0

        return w

    def lenght(self):
        l: int

        try:
            l = self.__browser.execute_script("return Runner.instance_.horizon.obstacles[0].typeConfig['height']")
        except JavascriptException:
            l = 0

        return l

    def speed(self):
        s: int

        try:
            s = round(self.__browser.execute_script("return Runner.instance_.currentSpeed"), 1)
        except JavascriptException:
            s = 0

        return s

    def object(self):
        r: bool = False

        try:
            if self.__browser.execute_script("return Runner.instance_.horizon.obstacles.length") > 0:
                r = True
        except JavascriptException:
            pass

        return r

    def is_over(self):
        return self.__browser.execute_script("return Runner.instance_.crashed")

    def is_play(self):
        return self.__browser.execute_script("return Runner.instance_.playing")

    def generation(self, ge: int, pa: int, mp: float) -> None:
        try:
            self.__valid(ge, pa, mp)
            score_mean: float = 0.00

            #stack_socre: list = []
            base: list = self.__createBase()

            pop_m: array = self.pop_weights()
            pop_v: tuple = self.to_vector(pop_m)

            genomes: int = len(self.dino)
            os_system('cls' if os_name == 'nt' else 'clear')

            for g in range(ge):
                self.__printMsg(g, 0, genomes, score_mean, 0, 0, 0, 0, 0, 0)

                fitness: array = self.__loop_play(genomes, g, score_mean)
                os_system('cls' if os_name == 'nt' else 'clear')

                if is_pressed('q') or is_pressed('Q') or self.__quit:
                    break

                else:
                    print("Criando nova geração...")
                    sleep(1)

                score_mean = fitness.mean()
                #stack_socre.append(fitness.reshape((-1, 1)).copy())

                parents = self.naturalSelection(pop_v[0], fitness.copy(), pa),  \
                          self.naturalSelection(pop_v[1], fitness.copy(), pa)

                offspring = self.crossover(parents[0], size=(pop_v[0].shape[0] - parents[0].shape[0], pop_v[0].shape[1])), \
                            self.crossover(parents[1], size=(pop_v[1].shape[0] - parents[1].shape[0], pop_v[1].shape[1]))

                offspring = self.mutation(offspring[0], mp), self.mutation(offspring[1], mp)

                pop_v[0][0:parents[0].shape[0], :] = parents[0]
                pop_v[0][parents[0].shape[0]:, :] = offspring[0]

                pop_v[1][0:parents[1].shape[0], :] = parents[1]
                pop_v[1][parents[1].shape[0]:, :] = offspring[1]

                pop_m = self.to_matrix(pop_v, pop_m)

                self.__saveDNA(g, base)
                self.update_pop(pop_m)

                os_system('cls' if os_name == 'nt' else 'clear')

            if self.__quit:
                self.__quit = False
        except Exception as Error:
            raise Error
            input()

    # def play(self, p: int) -> None:
    #     b_jump: bool = False
    #     b_down: bool = False
    #
    #     for i in range(p):
    #         if not self.is_play():
    #             os_system('cls' if os_name == 'nt' else 'clear')
    #             self.__printMsg(0, 0, 0, 0, 0, 0, 0, 0, 0)
    #
    #             self.dino[0].jump(True)
    #             self.dino[0].jump(False)
    #             sleep(2)
    #
    #         while True:
    #             if self.object():
    #                 d = self.distance()
    #                 h = self.height()
    #                 w = self.width()
    #                 s = self.speed()
    #                 ht = self.rexHeight()
    #
    #                 if b_down:
    #                     ht -= 22
    #
    #                 action = self.dino[0].model.predict(array([[d, w, h, ht, s]]))
    #
    #                 os_system('cls' if os_name == 'nt' else 'clear')
    #                 self.__printMsg(0, 0, 0, 0, d, h, ht, w, s)
    #
    #                 if action[0][0] > 0.5:
    #                     self.dino[0].jump(True)
    #                     b_jump = True
    #
    #                 else:
    #                     if b_jump:
    #                         self.dino[0].jump(False)
    #                         b_jump = False
    #
    #                 if action[0][1] > 0.5:
    #                     self.dino[0].duck(True)
    #                     b_down = True
    #
    #                 else:
    #                     if b_down:
    #                         self.dino[0].duck(False)
    #                         b_down = False
    #
    #                 if is_pressed('q') or is_pressed('Q'):
    #                     self.__quit = True
    #                     break
    #
    #                 if self.is_over():
    #                     self.dino[0].score = self.score()
    #
    #                     if b_jump:
    #                         self.dino[0].jump(False)
    #                         b_jump = False
    #
    #                     if b_down:
    #                         self.dino[0].duck(False)
    #                         b_down = False
    #
    #                     break
    #
    #             else:
    #                 if is_pressed('q') or is_pressed('Q'):
    #                     self.__quit = True
    #
    #                     break
    #
    #         if self.__quit:
    #             break

    def __loop_play(self, gen: int, ge: int, me: float) -> array:
        score: array = empty(shape=(len(self.dino)))

        b_jump: bool = False
        b_down: bool = False

        for i in range(gen):
            if not self.is_play():
                os_system('cls' if os_name == 'nt' else 'clear')
                self.__printMsg(ge, i, gen, me, 0, 0, 0, 0, 0, 0)

                self.dino[i].jump(True)
                self.dino[i].jump(False)
                sleep(2)

            while True:
                if self.object():
                    d = self.distance()
                    l = self.lenght()
                    w = self.width()
                    h = self.height() - l
                    s = self.speed()
                    ht = self.rexHeight()

                    if b_down:
                        d -= 59
                        ht -= 22
                    else:
                        d -= 44

                    action = self.dino[i].model.predict(array([[d, l, w, h, s, ht]]))

                    os_system('cls' if os_name == 'nt' else 'clear')
                    self.__printMsg(ge, i, gen, me, d, l, w, h, s, ht)

                    if action[0][0] > 0.5:
                        self.dino[i].jump(True)
                        b_jump = True

                    else:
                        if b_jump:
                            self.dino[i].jump(False)
                            b_jump = False

                    if action[0][1] > 0.5:
                        self.dino[i].duck(True)
                        b_down = True

                    else:
                        if b_down:
                            self.dino[i].duck(False)
                            b_down = False

                    if is_pressed('q') or is_pressed('Q'):
                        self.__quit = True
                        break

                    if self.is_over():
                        self.dino[i].score = self.score()

                        if b_jump:
                            self.dino[i].jump(False)
                            b_jump = False

                        if b_down:
                            self.dino[i].duck(False)
                            b_down = False

                        break
                else:
                    if is_pressed('q') or is_pressed('Q'):
                        self.__quit = True

                        break

            if self.__quit:
                break

            score[i] = array([self.score()]).astype('float32')
            sleep(1)

        return score

    def __createBase(self):
        base: str = "models/"
        n_d: str = None

        if not exists(base):
            mkdir(base)

        elif not isdir(base):
            mkdir(base)

        if listdir(base):
            d_t = listdir(base)[-1]
            n_d = base + str(int(d_t) + 1).zfill(2) + "/"

            mkdir(n_d)

        else:
            n_d = base + "01/"
            mkdir(n_d)

        return n_d

    def __saveDNA(self, ge: int, base: str):
        if self.dino is not None:
            file: str = "dino_{}_{}.h5"
            directory: str = base + "G - " + str(ge + 1).zfill(2) + "/"

            mkdir(directory)
            file = directory + file

            if exists(directory):
                for i in range(len(self.dino)):
                    self.dino[i].model.save_weights(file.format(str(i + 1).zfill(2), self.dino[i].score))
            else:
                raise NotADirectoryError("Falha em criar o diretorio.")

        else:
            raise ValueError("Não há dinossauros para ser salvo, talvez seja porque eles estão extintos.")

    def __printMsg(self, ge: int, pl: int, gen: int, me: float, d: float, h: float, l: float, w: float, s: int, ht: float):
        desc: str = "-------------- Segure a tecla Q para encerrar o programa. --------------\n" \
                    "\nGeração: {} -> Avg: {}" \
                    "\n\n[Obstáculo] Distancia: {}" \
                    "\n[Obstáculo] Largura: {}" \
                    "\n[Obstáculo] Altura: {}" \
                    "\n[Obstáculo] Comprimento: {}" \
                    "\n[Cenário] Velocidade: {} Pixel/s" \
                    "\n[Dino] Altura: {}"

        print(desc.format(str(ge + 1) + ": " + str(pl + 1) + "/" + str(gen), round(me, 2), round(d, 2), round(l, 2), round(w, 2), round(h, 2), s, round(ht, 2)))

    def __valid(self, ge, p, mp):
        if self.__browser is not None:
            if self.dino is None:
                raise Exception("Os genomas não foram criados, por favor executar a função createDNA")
        else:
            raise Exception("Primeiro é preciso executar a função start para abrir o navegador.")

        if ge <= 0:
            raise ValueError("A geração deve ser maior que 0")

        if p > len(self.dino):
            raise ValueError("O numero de parentes tem que ser menor do que o da população.")

        if mp <= 0:
            raise ValueError(" O valor da mutação deve ser maior que 0")
