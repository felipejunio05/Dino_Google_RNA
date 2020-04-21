# -*- utf-8 -*-

# Author: Felipe Junio da Rocha
# Date: 2020/04/13

from game import Game
from os import listdir
from os import name as os_name
from os import system as os_system

__all__ = ['Menu']


class Menu:
    aux: str = None

    def __init__(self):
        self.__game = Game()

    def run(self):
        option: int = 0
        while option != 3:
            try:
                os_system('cls' if os_name == 'nt' else 'clear')
                option = int(input("------------ DINO IA --------------\n\n"
                                   "1 - Criar uma nova população\n"
                                   "2 - Carregar uma População. \n"
                                   "3 - Sair \n\n->:"))

            except ValueError:
                os_system('cls' if os_name == 'nt' else 'clear')
                print("valor digitado não é valido")
                input()

            except TypeError:
                os_system('cls' if os_name == 'nt' else 'clear')
                print("valor digitado não é valido")
                input()

            else:
                if (option >= 1) and (option <= 3):
                    try:
                        if option == 1:
                            self.__fit(self.__fitPeg())
                        elif option == 2:
                            aux = self.__loadPeg()
                            if aux != '':
                                if self.__game.loadDNA(aux):
                                    self.__fit(self.__fitPeg(), True)
                                else:
                                    os_system('cls' if os_name == 'nt' else 'clear')
                                    print("Falha em carregar os genomas")
                                    input()
                            else:
                                os_system('cls' if os_name == 'nt' else 'clear')
                                print("falha em carregar os Genomas.")
                                input()

                    except ValueError as Error:
                        os_system('cls' if os_name == 'nt' else 'clear')
                        print("Ops! Algo errado aconteceu -> Erro: " + str(Error))
                        input()

                    except TypeError as Error:
                        os_system('cls' if os_name == 'nt' else 'clear')
                        print("Ops! Algo errado aconteceu -> Erro: " + str(Error))
                        input()
                else:
                    os_system('cls' if os_name == 'nt' else 'clear')
                    print("Opção invalida!")

    def __fit(self, ge: int, reload: bool = False):

        try:
            self.__game.open()

            if not reload:
                self.__game.createDNA(12)

            self.__game.generation(ge, 4, 20)

        finally:
            self.__game.destroyDNA()
            self.__game.close()

    # def __play(self, p: int):
    #     try:
    #         self.__game.open()
    #         self.__game.createDNA(1)
    #         self.__game.dino[0].model.load_weights('models/#/' + listdir('models/#/')[-1])
    #         self.__game.play(p)
    #
    #     finally:
    #         self.__game.close()
    #         self.__game.destroyDNA()

    @staticmethod
    def __playPeg():
        ret: int

        while True:
            try:
                os_system('cls' if os_name == 'nt' else 'clear')
                ret = int(input("Numero de Jogadas: "))
                os_system('cls' if os_name == 'nt' else 'clear')

            except ValueError:
                os_system('cls' if os_name == 'nt' else 'clear')
                print("Informação digitada está incorreta, só é permitido números inteiros.")
                input()

            except TypeError:
                os_system('cls' if os_name == 'nt' else 'clear')
                print("Valor digitado tém que ser um numero inteiro.")
                input()

            else:
                return ret

    @staticmethod
    def __fitPeg():

        ret: int

        while True:
            try:
                os_system('cls' if os_name == 'nt' else 'clear')
                ret = int(input("Numero de gerações: "))
                os_system('cls' if os_name == 'nt' else 'clear')

            except ValueError:
                os_system('cls' if os_name == 'nt' else 'clear')
                print("Informação digitada está incorreta, só é permitido números inteiros.")
                input()

            except TypeError:
                os_system('cls' if os_name == 'nt' else 'clear')
                print("Valor digitado tém que ser um numero inteiro.")
                input()

            else:
                return ret

    @staticmethod
    def __loadPeg():
        base: str = 'models/'
        content: list = [listdir(base)]
        ans: int

        ret: str = ''

        if content[0]:
            if len(content[0]) == 1:
                os_system('cls' if os_name == 'nt' else 'clear')
                content.append([listdir(base + content[0][0] + '/')])
                ans = int(input("Você possui " + str(len(content[1])) + " população com " + str(len(content[1][0])) + " gerações, escolha uma: "))

                for d in content[1][0]:
                    if int(d[-len(str(ans)):]) == ans:
                        ret = base + content[0][0] + "/" + d + "/"
                        break

            else:
                os_system('cls' if os_name == 'nt' else 'clear')
                ans = int(input("Você possui " + str(len(content[0])) + " populações, escolha uma: "))
                os_system('cls' if os_name == 'nt' else 'clear')

                for d1 in content[0]:

                    if int(d1) == ans:
                        content.append([listdir(base + d1 + '/')])
                        break

                ans = int(input("Você possui " + str(len(content[1][0])) + " gerações, escolha uma: "))

                for d2 in content[1][0]:
                    if int(d2[-len(str(ans)):]) == ans:
                        ret = base + d1 + "/" + d2 + "/"
                        break

        else:
            print("Você não possui população para ser carregada.")
            input()

        return ret