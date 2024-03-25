from threading import Thread, current_thread, Lock
from time import sleep
import keyboard
import random


# Variável global para controlar o estado de execução das threads
executando = True

# notificações e posts da rede social
messages = 0
posts = 0

# bloqueio 'Lock' para garantir que apenas uma thread modifique a variável por vez, evitando condições de corrida.
lock = Lock()


def post():     # thread que indica que foi feito um post
    global posts
    while executando:                   # Enquanto a variável 'executando' for True

        if keyboard.is_pressed('1'):    # caso a tecla 1 seja pressionada é feito um Post
            print(f"Você fez um post")
            posts += 1
            sleep(5)        # Pequeno atraso para evitar múltiplos posts se a tecla ficar pressionada


def like(nomes):     # thread que indica que 0foi feito um like
    global messages        # var global de mensagens

    while executando:                   # Enquanto a variável 'executando' for True
        chance = random.randint(1, 10)
        
        if posts > 0 and chance > 5:
            pessoa = nomes[int(random.random() * len(nomes))]  # Seleciona aleatoriamente um nome da lista
            print(f"{pessoa} deu like no seu post")
            with lock:  # Adquire o bloqueio antes de modificar a variável compartilhada
                messages += 1

        sleep(5)    # atraso do tempo de execução da thread


def message(nomes):     # thread que indica que recebeu uma mensagem
    global messages        # var global de mensagens

    while executando:  # Enquanto a variável 'executando' for True
        chance = random.randint(1, 10)
        if chance > 7:
            pessoa = nomes[int(random.random() * len(nomes))]  # Seleciona aleatoriamente um nome da lista
            print(f"Você recebeu uma mensagem de {pessoa}")
            with lock:  # Adquire o bloqueio antes de modificar a variável compartilhada
                messages += 1

        sleep(5)    # atraso do tempo de execução da thread

        
def verify():     # thread que verifica as mensagens
    global messages        # var global de mensagens

    while executando:                   # Enquanto a variável 'executando' for True

        if keyboard.is_pressed('2'):    # caso a tecla 2 seja pressionada
            with lock:  # Adquire o bloqueio antes de acessar a variável compartilhada
                messages -= 1
                if messages < 0:
                    messages = 0
                elif messages > 0:
                    print(f"Você viu uma mensagem. Agora você possui {messages} mensagens restantes.")
        
        sleep(0.15)     # atraso do tempo de execução da thread


def notification():     # thread que diz a quantidade de notificações
    currentMessages = messages
    while executando:                        # Enquanto a variável 'executando' for True
        if currentMessages != messages:     # se houver uma nova mensagem
            print(f"Você possui {messages} mensagens")
            sleep(5)    # atraso do tempo de execução da thread


def main():         # função principal
    # definindo var global
    global executando

    # Lista de nomes de pessoas
    nomes = ["Paulo", "Matheus", "Roger", "Gabriel", "Davi", "João", "Givanildo", "Marco", "Enzo", "Maria", "Aline",
             "Leticia"]

    # Criação das threads
    t1 = Thread(target=post, name='Thread-Post')
    t2 = Thread(target=like, args=(nomes,), name='Thread-Like')
    t3 = Thread(target=message, args=(nomes,), name='Thread-Message')
    t4 = Thread(target=notification, name='Thread-Notification')
    t5 = Thread(target=verify, name='Thread-Verify')

    threads = [t1, t2, t3, t4, t5]      # juntando as threads em uma lista

    # Inicia as threads
    for thread in threads:
        thread.start()

    while executando:  # Loop infinito para verificar a entrada do teclado
        if keyboard.is_pressed('0'):  # Se a tecla '0' for pressionada
            executando = False  # Altera o estado da variável 'executando' para False
            break  # Sai do loop

    for thread in threads:
        thread.join()  # Aguarda todas as threads terminarem


if __name__ == "__main__":
    main()
