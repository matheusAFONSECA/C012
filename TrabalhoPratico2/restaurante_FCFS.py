import random
from threading import Thread, Semaphore
from time import sleep, time
from queue import Queue

# Funções para processamento de pedidos
def pedido_simples(cliente):
    print(f"Fazendo pedido SIMPLES para {cliente}")
    sleep(1)
    print(f"Pedido SIMPLES para {cliente} pronto")

def pedido_medio(cliente):
    print(f"Fazendo pedido MÉDIO para {cliente}")
    sleep(3)
    print(f"Pedido MÉDIO para {cliente} pronto")

def pedido_dificil(cliente):
    print(f"Fazendo pedido DIFÍCIL para {cliente}")
    sleep(6)
    print(f"Pedido DIFÍCIL para {cliente} pronto")

# Função para adicionar pedidos à fila
def adicionar_pedido(cliente, tipo):
    print(f"Adicionando pedido {tipo} para {cliente}")
    # Entrar na seção crítica
    semaforo.acquire()
    pedidos.put((cliente, tipo, time()))
    # Sair da seção crítica
    semaforo.release()

# Inicializa a fila e o semáforo
pedidos = Queue()
semaforo = Semaphore(1)
tempos_de_espera = []

def main():
    random.seed(8)
    # Adiciona alguns pedidos para teste
    for _ in range(random.randint(20, 50)):
        tipo_pedido = random.choice(['simples', 'medio', 'dificil'])
        cliente = f"Cliente {_+1} - {tipo_pedido.capitalize()}"
        adicionar_pedido(cliente, tipo_pedido)

    # Registra o tempo inicial
    inicio = time()

    # Cria a thread para processar os pedidos
    t = Thread(target=processar_pedidos, args=(inicio,))
    t.start()

    # Espera a thread de processamento de pedidos terminar
    t.join()

    # Calcula o tempo médio de espera
    if tempos_de_espera:
        tempo_medio_espera = sum(tempos_de_espera) / len(tempos_de_espera)
        print(f"Tempo médio de espera: {tempo_medio_espera:.3f} segundos")
    else:
        print("Nenhum pedido foi processado.")

def processar_pedidos(inicio):
    while True:
        # Entrar na seção crítica
        semaforo.acquire()
        if not pedidos.empty():
            cliente, tipo, tempo_chegada = pedidos.get()
            # Sair da seção crítica
            semaforo.release()

            # Calcula o tempo de espera para o pedido atual
            tempo_espera = time() - tempo_chegada
            tempos_de_espera.append(tempo_espera)

            if tipo == 'simples':
                pedido_simples(cliente)
            elif tipo == 'medio':
                pedido_medio(cliente)
            elif tipo == 'dificil':
                pedido_dificil(cliente)
        else:
            # Sair da seção crítica
            semaforo.release()

            # Calcula o tempo total de processamento e imprime o resultado
            tempo_total = time() - inicio
            print(f"Tempo total de processamento (FCFS): {tempo_total:.3f} segundos")
            break

if __name__ == "__main__":
    main()
