from threading import Thread, current_thread, Lock
from time import sleep
import keyboard
from random import random


# Variável global para controlar o estado de execução das threads
executando = True

# notificações das ações da rede social
mensagens = 0

# bloqueio 'Lock' para garantir que apenas uma thread modifique a variável por vez, evitando condições de corrida.
lock = Lock()


def post():     # thread que indica que foi feito um post
    while executando:                   # Enquanto a variável 'executando' for True

        if keyboard.is_pressed('1'):    # caso a tecla 1 seja pressionada é feito um Post
            print(f"{current_thread().name} fez um post")
            sleep(0.5)        # Pequeno atraso para evitar múltiplos posts se a tecla ficar pressionada


def like():     # thread que indica que foi feito um like
    global mensagens        # var global de mensagens

    while executando:                   # Enquanto a variável 'executando' for True

        print(f"{current_thread().name} deu um like no post")
        with lock:  # Adquire o bloqueio antes de modificar a variável compartilhada
            mensagens += 1

        sleep(3)    # atraso do tempo de execução da thread


def message():     # thread que indica que recebeu uma mensagem
    global mensagens        # var global de mensagens

    while executando:  # Enquanto a variável 'executando' for True

        print(f"{current_thread().name} mandou uma mensagem")
        with lock:  # Adquire o bloqueio antes de modificar a variável compartilhada
            mensagens += 1

        sleep(3)    # atraso do tempo de execução da thread


def notification():     # thread que diz a quantidade de notificações
    while executando:                   # Enquanto a variável 'executando' for True
        print(f"Você possui {mensagens} mensagens")
        sleep(3)    # atraso do tempo de execução da thread


def main():         # função principal
    # definindo var global
    global executando

    # Criação das threads
    t1 = Thread(target=post, name='Thread-Post')
    t2 = Thread(target=like, name='Thread-Like')
    t3 = Thread(target=message, name='Thread-Message')
    t4 = Thread(target=notification, name='Thread-Notification')

    threads = [t1, t2, t3, t4]      # juntando as threads em uma lista

    # Inicia as threads
    for thread in threads:
        thread.start()

    while True:  # Loop infinito para verificar a entrada do teclado
        if keyboard.is_pressed('0'):  # Se a tecla '0' for pressionada
            executando = False  # Altera o estado da variável 'executando' para False
            break  # Sai do loop

    for thread in threads:
        thread.join()  # Aguarda todas as threads terminarem


if __name__ == "__main__":
    main()
