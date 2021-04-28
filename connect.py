import sqlite3
from uteis import *
from getpass import getpass


def existe_banco(arquivo):
    """Verifica se existe o arquivo .db"""

    try:
        a = open(arquivo, "r")
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def db_con(db):
    """Conexão com banco de dados"""

    banco = sqlite3.connect(db)
    cursor = banco.cursor()
    return banco, cursor


def criar_banco(arquivo):
    """Cria banco de dados"""

    banco, cursor = db_con(arquivo)

    cursor.execute("CREATE TABLE usuarios ("
                   "'id' INTEGER NOT NULL UNIQUE,"
                   "'nickname'	TEXT NOT NULL UNIQUE,"
                   "'senha'TEXT NOT NULL,"
                   "PRIMARY KEY('id' AUTOINCREMENT));"
    )

    cursor.execute("CREATE TABLE depoimentos ("
                   "'id_user' INTEGER NOT NULL,"
                   "'titulo'TEXT NOT NULL UNIQUE,"
                   "'texto' TEXT NOT NULL,"
                   "'data' TEXT NOT NULL,"
                   "FOREIGN KEY('id_user') REFERENCES 'usuarios'('id'));"
    )

    cursor.close()
    banco.close()


def cadastro(db):
    """Fazer cadastro de usuarios"""

    try:
        usuario, senha = validacao()
        if usuario == senha == '00':
            return
    except Exception as e:
        limpa_tela()
        color_msg(f"Erro do tipo: [{e}]", 1)
        input("Pressione enter")
    else:
        try:
            banco, cursor = db_con(db)
            cursor.execute(f"INSERT INTO usuarios ('nickname', 'senha') VALUES('{usuario}', '{senha}');")
        except sqlite3.IntegrityError:
            limpa_tela()
            color_msg("Nome de usuario ja existe!", 3)
            input("Pressione enter")
        except Exception as e:
            limpa_tela()
            color_msg(f"Erro do tipo: [{e}]", 1)
            input("Pressione enter")
        else:
            banco.commit()
            color_msg("Cadastro feito com sucesso!", 2)
            input("Pressione enter")
        finally:
            cursor.close()
            banco.close()


def validacao():
    """validação dos dados do usuário"""

    try:
        # Validando o nick
        while True:
            color_msg("Digite o nome de usuário:\n([00] para cancelar)", 6)
            usuario = str(input()).strip()
            if usuario == '00':
                break
            if len(usuario) < 5:
                color_msg("O nome de usuário não pode ter menos de 5 caractéres!", 1)
                continue
            else:
                break

        linha()

        # Validando a senha
        while True:
            color_msg("Digite a senha:\n([00] para cancelar)", 6)
            senha = str(getpass(prompt='', stream=None)).strip()
            if senha == '00':
                break
            if len(senha) < 6:
                color_msg("A senha não pode ter menos de 6 caractéres!", 1)
                continue
            color_msg("Confirme a senha:", 6)
            senha2 = str(getpass(prompt='', stream=None)).strip()
            if senha != senha2:
                color_msg("As senhas não são iguais!", 1)
                continue
            else:
                break

    except KeyboardInterrupt:
        pass
    else:
        return usuario, senha


def login(db):
    """Faz o login do usuario"""

    try:
        color_msg("Digite o nome de usuario:", 6)
        usuario = str(input()).strip()
        color_msg("Digite a senha:", 6)
        senha = getpass(prompt='', stream=None).strip()

    except KeyboardInterrupt:
        color_msg("Operação cancelada!", 1)
    else:
        banco, cursor = db_con(db)

        try:
            cursor.execute(f"SELECT * FROM usuarios WHERE nickname = '{usuario}' AND senha = '{senha}'")
        except Exception as e:
            color_msg(f"Erro do tipo: [{e}]", 1)
        else:
            result = cursor.fetchall()
            if result:
                for i in result:
                    n = i[0]
                    nome = i[1]
                area(n, nome, db)
            else:
                print("Usuário e/ou senha não reconhecido")
                input("Pressione enter")
                limpa_tela()
        finally:
            cursor.close()
            banco.close()


def area(n, nome, db):
    """Area do usuário"""

    while True:
        try:
            limpa_tela()
            color_msg(f"Diário do(a) {nome}", 2)
            linha()

            color_msg('[1] Escrever\n'
                      '[2] Ler \n'
                      '[3] Sair', 6)
            submenu = int(input())

            if submenu == 1:
                limpa_tela()
                escrever(n, db)

            elif submenu == 2:
                ler(n, db)

            elif submenu == 3:
                break

            else:
                color_msg("Válido somente os números do menu!", 1)
                input("Pressione enter")

        except ValueError:
            color_msg("Entrada invalida!", 1)
            input("Pressione enter")

        except KeyboardInterrupt:
            color_msg("!!!", 1)
            input("Pressione enter")


def escrever(n, db):
    """Escreve no diário"""

    try:
        limpa_tela()
        color_msg("Titulo:", 3)
        titulo = str(input()).strip()

        linha()
        color_msg("Texto:\nQuerido diário,", 3)
        texto = str(input()).strip().capitalize()
    except KeyboardInterrupt:
        color_msg("Operação cancelada!", 1)
        input("Pressione enter")
        limpa_tela()
    else:
        banco, cursor = db_con(db)

        try:
            cursor.execute(f"INSERT INTO 'depoimentos' VALUES({n}, '{titulo}', '{texto}', strftime('%d/%m/%Y'));")
        except Exception as e:
            limpa_tela()
            color_msg(f"Erro! [{e}]", 1)
            input("Pressione enter")
        else:
            banco.commit()
        finally:
            cursor.close()
            banco.close()


def ler(n, db):
    """Lê os depoimentos do usuário"""

    try:
        limpa_tela()
        banco, cursor = db_con(db)
        cursor.execute(f"SELECT titulo, data FROM depoimentos WHERE id_user = {n}")
        titulos = cursor.fetchall()

    except Exception as e:
        color_msg(f"Erro! [{e}]", 1)
        print("Pressione enter")
        limpa_tela()

    else:
        while True:
            color_msg('Qual menssagem voçê deseja ver?\n', 6)
            color_msg(f"{'Número':^7}|{'titulo':^25}|{'data':^10}", 6)
            color_msg('-' * 44, 6)

            for x, y in enumerate(titulos):
                color_msg(f'{x+1:^7}|{y[0]:<25}|{y[1]:^}', 2)

            try:
                color_msg('-' * 44, 6)
                indice = int(input("[0 para sair]\n"))
            except ValueError:
                color_msg("Entrada inválida", 1)
                input("Pressione enter")
                limpa_tela()
                continue

            if indice == 00:
                break

            try:
                indice = indice - 1
                titulo = titulos[indice][0]
                cursor.execute(f"SELECT texto FROM depoimentos WHERE id_user = {n} AND titulo = '{titulo}'")
                msg = cursor.fetchall()
            except IndexError:
                color_msg("Número de menssagem inexistente", 2)
                input("pressione enter")
                limpa_tela()
            else:
                menssagem(titulo, msg[0][0])
                color_msg("Deseja ver outra menssagem? S/N", 6)
                try:
                    resp = str(input()).strip().lower()[0]
                except:
                    color_msg("Ops! houve algum erro", 3)
                    input("pressione enter")
                    limpa_tela()
                else:
                    if resp == 'n':
                        break
                    else:
                        limpa_tela()


    finally:
        cursor.close()
        banco.close()


def menssagem(title, msg):
    """"""

    # Mostrar titulo e abaixo a menssagem correspondente
    limpa_tela()
    title = str(title).title()
    msg = str(msg).capitalize()
    color_msg(f"\n{title:^50}", 6)
    linha(66)
    print(f"{msg:<50}")
    linha(66)



