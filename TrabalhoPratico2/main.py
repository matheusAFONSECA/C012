from threading import Thread, Lock
from time import sleep
import random

# Variável global para controlar o estado de execução das threads
executando = True

# Estado inicial do restaurante
mesas_disponiveis = 20      # mesas disponivéis no restaurante
pedidos_pendentes = 0       # pedidos a serem entregues
pedidos_entregues = 0       # pedidos entregues

# bloqueio 'Lock' para garantir que apenas uma thread modifique a variável por vez, evitando condições de corrida.
lock = Lock()


# Thread de mesas ocupadas
def reserva_mesa():

    global mesas_disponiveis

    while executando:                   # Enquanto a variável 'executando' for True

        with lock:  # Adquire o bloqueio antes de modificar a variável compartilhada

            if mesas_disponiveis > 0:
                mesas_disponiveis -= 1
                print(f"Uma mesa foi reservada. Mesas disponíveis: {mesas_disponiveis}")

        sleep(random.uniform(1, 3))  # Pequeno atraso para simular o tempo entre reservas


# Thread de pedidos na cozinha
def pedido_cozinha():

    global pedidos_pendentes

    while executando:                   # Enquanto a variável 'executando' for True

        with lock:  # Adquire o bloqueio antes de modificar a variável compartilhada

            pedidos_pendentes += 1
            print(f"Novo pedido na cozinha. Pedidos pendentes: {pedidos_pendentes}")

        sleep(random.uniform(1, 3))  # Pequeno atraso para simular o tempo entre novos pedidos


# Thread de entrega de pedidos
def entrega_pedido():

    global pedidos_pendentes, pedidos_entregues

    while executando:                   # Enquanto a variável 'executando' for True

        with lock:  # Adquire o bloqueio antes de modificar a variável compartilhada

            if pedidos_pendentes > 0:
                pedidos_pendentes -= 1
                pedidos_entregues += 1
                print(f"Pedido entregue. Pedidos pendentes: {pedidos_pendentes}, Pedidos entregues: {pedidos_entregues}")

        sleep(random.uniform(1, 3))  # Pequeno atraso para simular o tempo entre entregas


def verificar_status():
    while executando:                   # Enquanto a variável 'executando' for True
        sleep(10)  # Verifica o status a cada 10 segundos
        print(f"Status: Mesas disponíveis: {mesas_disponiveis}, Pedidos pendentes: {pedidos_pendentes}, Pedidos entregues: {pedidos_entregues}")


# função principal
def main():

    # definindo var global de controle de execução
    global executando

    # Criação das threads
    t1 = Thread(target=reserva_mesa, name='Thread-Reserva')
    t2 = Thread(target=pedido_cozinha, name='Thread-Pedido')
    t3 = Thread(target=entrega_pedido, name='Thread-Entrega')
    t4 = Thread(target=verificar_status, name='Thread-Status')

    threads = [t1, t2, t3, t4]      # juntando as threads em uma lista

    # Inicia as threads
    for thread in threads:
        thread.start()

    try:
        while True:  # Loop infinito para manter o programa rodando
            sleep(0.1)
    except KeyboardInterrupt:
        executando = False  # Altera o estado da variável 'executando' para False

    for thread in threads:
        thread.join()  # Aguarda todas as threads terminarem


if __name__ == "__main__":
    main()
