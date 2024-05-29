from threading import Thread, Semaphore
from time import sleep, time
from queue import PriorityQueue
import random

# Funções para processamento de pedidos
def pedido_simples(cliente):
    print(f"Fazendo pedido SIMPLES para {cliente}")
    sleep(1)
    print(f"Pedido SIMPLES para {cliente} pronto")

def pedido_medio(cliente):
    print(f"Fazendo pedido MÉDIO para {cliente}")
    sleep(2)
    print(f"Pedido MÉDIO para {cliente} pronto")

def pedido_dificil(cliente):
    print(f"Fazendo pedido DIFÍCIL para {cliente}")
    sleep(3)
    print(f"Pedido DIFÍCIL para {cliente} pronto")

# Função para adicionar pedidos à fila de prioridade
def adicionar_pedido(cliente, tipo, tempo_processamento):
    print(f"Adicionando pedido {tipo} para {cliente} com tempo de processamento {tempo_processamento}")
    # Entrar na seção crítica
    semaforo.acquire()
    pedidos.put((tempo_processamento, cliente, tipo))
    # Sair da seção crítica
    semaforo.release()

# Inicializa a fila de prioridade e o semáforo
pedidos = PriorityQueue()
semaforo = Semaphore(1)

def main():
    random.seed(8)
    # Adiciona alguns pedidos para teste
    for _ in range(random.randint(20, 50)):
        tipo_pedido = random.choice(['simples', 'medio', 'dificil'])
        cliente = f"Cliente {_+1} - {tipo_pedido.capitalize()}"
        tempo_processamento = 5 if tipo_pedido == 'simples' else 8 if tipo_pedido == 'medio' else 12
        adicionar_pedido(cliente, tipo_pedido, tempo_processamento)
    
    # Registra o tempo inicial
    inicio = time()

    # Cria a thread para processar os pedidos
    t = Thread(target=processar_pedidos, args=(inicio,))
    t.start()

    # Espera a thread de processamento de pedidos terminar
    t.join()

def processar_pedidos(inicio):
    while True:
        # Entrar na seção crítica
        semaforo.acquire()
        if not pedidos.empty():
            tempo_processamento, cliente, tipo = pedidos.get()
            # Sair da seção crítica
            semaforo.release()
            
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
            print(f"Tempo total de processamento (SJF): {tempo_total:.2f} segundos")
            break

if __name__ == "__main__":
    main()
