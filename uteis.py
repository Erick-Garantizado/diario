import os


def color_msg(txt, cor):
    """
    txt = texto a ser exibido
    cor = numero da cor para o texto
    """

    if cor == 1:
        # vermelho
        i = '\033[;31m'

    elif cor == 2:
        # verde
        i = '\033[;32m'

    elif cor == 3:
        # amarelo
        i = '\033[;33m'

    elif cor == 4:
        # azul
        i = '\033[;34m'

    elif cor == 5:
        # lilas/roxo
        i = '\033[;35m'

    elif cor == 6:
        # ciano
        i = '\033[;36m'

    elif cor == 7:
        # cinza
        i = '\033[;37m'

    print(f"{i}{txt}\033[m")


def linha(tam=50):
    print('-' * tam)


def cabecalho(txt):
    color_msg('=' * 50, 3)
    color_msg(txt.center(50), 6)
    color_msg('=' * 50, 3)


def limpa_tela():
    """limpa a tela no prompt de comando"""

    if os.system("uname") == 0:
        os.system("clear")
    else:
        os.system("cls")


def menu():
    """Mostra o menu."""

    limpa_tela()
    while True:
        cabecalho("Meu diário")
        try:
            menu = int(input("[1] Cadastro\n"
                             "[2] Login\n"
                             "[3] Sobre\n"
                             "[4] Sair\n"))
        except ValueError:
            color_msg("Entrada inválida", 1)
            continue
        except KeyboardInterrupt:
            color_msg("Usuario cancelou a ação!", 1)
            menu = None
            break
        else:
            escolha = (1, 2, 3, 4)
            if menu not in escolha:
                color_msg("Opção inexistente", 3)
                continue
            else:
                break
    return menu


def sobre():
    color_msg("é um diario", 5)
    input()

