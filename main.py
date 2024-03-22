from threading import current_thread
from time import sleep
from random import random


def post():
    print(f"{current_thread().getName()} fez um post")
    sleep(1)


def like():
    print(f"{current_thread().getName()} deu um like no post")
    sleep(1)


def message():
    print(f"{current_thread().getName()} mandou uma mensagem")
    sleep(1)


def notification():
    mensagens = 0
    print(f"Você possui {mensagens} mensagens")
    sleep(1)


def main():
    threads = 4


if __name__ == "__main__":
    main()
