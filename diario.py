from connect import *


db = "diario_banco.db"
if not existe_banco(db):
    criar_banco(db)

while True:

    os.system("cls")
    cabecalho("Diário")
    try:
        color_msg('[1] Cadastro\n'
                  '[2] Login\n'
                  '[3] Sobre\n'
                  '[4] Sair', 6)
        color_msg('=' * 50, 3)
        menu = int(input())
    except ValueError:
        print('Entrada invalida!')
        continue
    except:
        print("Erro")

    if menu == 1:

        # Cadastro
        limpa_tela()
        cabecalho("Cadastro")
        cadastro(db)

    elif menu == 2:

        # Login
        limpa_tela()
        cabecalho("Login")
        login(db)

    elif menu == 3:

        # Sobre o programa
        limpa_tela()
        cabecalho("Sobre")
        sobre()

    elif menu == 4:
        # Fecha o programa        
        break

    else:
        print("Número de menu inválido!")
        continue

color_msg("Até mais!", 6)
