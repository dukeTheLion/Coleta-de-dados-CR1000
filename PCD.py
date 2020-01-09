"""
/////////////////////////////////////////////////// Selecao de dados ///////////////////////////////////////////////////


                         ______     __  __        _____     __  __     __  __     ______
                        /\  __ \   /\ \_\ \      /\  __-.  /\ \/\ \   /\ \/ /    /\  ___\
                        \ \  __<   \ \____ \     \ \ \/\ \ \ \ \_\ \  \ \  _"-.  \ \  __\
                         \ \_____\  \/\_____\     \ \____-  \ \_____\  \ \_\ \_\  \ \_____\
                          \/_____/   \/_____/      \/____/   \/_____/   \/_/\/_/   \/_____/



Feito por: Savio Goncalves Mendonca (DUKE)
Data de criacao: 2019-09-10
"Contratante": GREEN
Vercao python: 3.7

------------------------------------------------------------------------------------------------------------------------
Informacoes adicionais:

    >> Todos pacotes estao na pasta ~venv/lib/python3.7/site-packages

    >> O interpretador Python esta na pasta ~venv/bin

    >> Codigo nao comentado

------------------------------------------------------------------------------------------------------------------------
"""

from csv import DictWriter
import sys
import os

def direc():
    directorio = '/'

    temporary = sys.platform

    if temporary == 'win32':
        for root, dirs, files in os.walk("C:\\\\"):
            for file in files:
                if file.endswith('tabela_1.csv'):
                    directorio = os.path.join(root, file)
                    print('Tabela em: ', end='')
                    print(directorio.replace('\\tabela_1.csv', ''))

        directorio = directorio.replace('\\tabela_1.csv', '')

    else:
        temp = 0
        print('Loading', end='')
        for root, dirs, files in os.walk("/"):
            for file in files:
                temp += 1
                if temp > 12600:
                    temp = 0
                    print('.', end='')
                if file.endswith('tabela_1.csv'):
                    directorio = os.path.join(root, file)

        print('')
        print('Tabela em: ', end='')
        print(directorio.replace('/tabela_1.csv', ''))
        directorio = directorio.replace('/tabela_1.csv', '')

        if directorio == '/':
            print('A tabela "tabela_1.csv" nao foi encontrada')
            sys.exit()

    return directorio


def selec(directorio):
    os.chdir(directorio)

    datahora_in = 0
    datahora_fi = 0

    try:
        with open('tabela_1.csv', 'r') as tabela_csv:
            tabela_csv.readline()
            datain = tabela_csv.readline()
            datahora_in = datain.split(',')
            datahora_in = datahora_in[0]
            print(f'----------------------------------------------------------------------------------'
                  f'\n########### Uma danta entre  {datahora_in} e ', end='')

        with open('tabela_1.csv', 'r') as tabela_csv:
            ultimo = len(tabela_csv.readlines())

        with open('tabela_1.csv', 'r') as tabela_csv:
            for x in range(ultimo):
                datafi = tabela_csv.readline()
                datahora_fi = datafi.split(',')
                datahora_fi = datahora_fi[0]
            print(f'{datahora_fi} ###########\n'
                  f'----------------------------------------------------------------------------------')
    except FileNotFoundError:
        print('A tabela "tabela_1.csv" nao foi encontrada')
        sys.exit()

    datahora_in = datahora_in.split(' ')
    datahora_fi = datahora_fi.split(' ')

    datain = data(datahora_in[0])
    horain = hora(datahora_in[1])

    datafi = data(datahora_fi[0])
    horafi = hora(datahora_fi[1])

    datahora_in = datain + horain
    datahora_fi = datafi + horafi


def data__hora(data_hora):
    data_hora = data_hora.strip()

    data_hora = data_hora.split(' ')

    if len(data_hora) > 2 or len(data_hora) == 1:
        temp = len(data_hora)

        if temp != 6:
            data_hora = input('Digite a data e hora novamente, atente-se ao formato a seguir '
                              '|YYYY-MM-DD hh:mm:00| ou |YYYY-MM-DD 0| >>>')
        if len(data_hora.split(' ')) != 2:
            print('Erro: IndexError, tente novamente')
            sys.exit()

        if temp == 6:
            temp2 = [data_hora[0], data_hora[1], data_hora[2]]
            temp3 = [data_hora[3], data_hora[4], data_hora[5]]
            temp2 = '-'.join(temp2)
            temp3 = '-'.join(temp3)
            data_hora = [temp2, temp3]

    try:
        data_0 = data(data_hora[0])
    except IndexError:
        data_0 = [0, 0, 0]

    try:
        if data_hora[1] != '' or data_hora[1] != '0':
            try:
                hora_0 = hora(data_hora[1])
            except IndexError:
                hora_0 = [0, 0, 0]
        else:
            hora_0 = [0, 0, 0]
    except IndexError:
        print('Erro: IndexError, tente novamente')
        sys.exit()

    data_1 = data_0 + hora_0

    return data_1


def data(data_):
    if ':' in data_:
        data_1 = data_.split(':')
    if ';' in data_:
        data_1 = data_.split(';')
    if '.' in data_:
        data_1 = data_.split('.')
    if '-' in data_:
        data_1 = data_.split('-')
    if '/' in data_:
        data_1 = data_.split('/')

    if len(data_1[0]) == 2:
        data_1[0] = '20' + data_1[0]

    if len(data_1[0]) < 2:
        data_1[0] = 0

    try:
        data_1 = list(map(int, data_1))

        if data_1[1] > 12:
            data_1[1] = int(input('Digite o mes novamente: '))
            if data_1[1] > 12:
                print('Fora da escala, mes definido como 12')
                data_1[1] = 12

        if data_1[1] == 1 and data_1[2] > 31:
            data_1[2] = 31
        if data_1[0] % 100 != 0:
            if data_1[0] % 4 == 0 or data_1[0] % 400:
                if data_1[1] == 2 and data_1[2] > 29:
                    data_1[2] = 29
        if data_1[1] == 2 and data_1[2] > 28:
            data_1[2] = 28
        if data_1[1] == 3 and data_1[2] > 31:
            data_1[2] = 31
        if data_1[1] == 4 and data_1[2] > 30:
            data_1[2] = 30
        if data_1[1] == 5 and data_1[2] > 31:
            data_1[2] = 31
        if data_1[1] == 6 and data_1[2] > 30:
            data_1[2] = 30
        if data_1[1] == 7 and data_1[2] > 31:
            data_1[2] = 31
        if data_1[1] == 8 and data_1[2] > 31:
            data_1[2] = 31
        if data_1[1] == 9 and data_1[2] > 30:
            data_1[2] = 30
        if data_1[1] == 10 and data_1[2] > 31:
            data_1[2] = 31
        if data_1[1] == 11 and data_1[2] > 30:
            data_1[2] = 30
        if data_1[1] == 12 and data_1[2] > 31:
            data_1[2] = 31

    except ValueError:
        data_1 = 0

    return data_1


def hora(hora_):
    if ':' in hora_:
        hora_1 = hora_.split(':')
    if ';' in hora_:
        hora_1 = hora_.split(';')
    if '.' in hora_:
        hora_1 = hora_.split('.')
    if '-' in hora_:
        hora_1 = hora_.split('-')
    if '/' in hora_:
        hora_1 = hora_.split('/')
    if hora_ == '0':
        hora_1 = '0'

    if hora_1 != '0' and len(hora_1) < 3:
        hora_1 = hora_.split('-')

    try:
        while '' in hora_1:
            hora_1.remove('')
    except AttributeError:
        pass

    try:
        hora_1 = list(map(int, hora_1))
    except ValueError:
        hora_1 = 0

    try:
        if len(hora_1) == 3:
            hora_1[2] = 0
    except TypeError:
        hora_1[0] = int(input('Digite a hora novamente: '))
        if hora_1[0] > 23:
            hora_1[0] = 23
            print('Fora da escala, hora definido como 23')

    if hora_1[0] > 23:
        hora_1[0] = int(input('Digite a hora novamente: '))
        if hora_1[0] > 23:
            hora_1[0] = 23
            print('Fora da escala, hora definido como 23')

    if hora_1[1] > 59:
        hora_1[1] = int(input('Digite o minuto novamente: '))
        if hora_1[1] > 59:
            hora_1[1] = 59
            print('Fora da escala, minuto definido como 59')

    return hora_1


def coleta():
    lol = """

     ______     __  __        _____     __  __     __  __     ______    
    /\  __ \   /\ \_\ \      /\  __-.  /\ \/\ \   /\ \/ /    /\  ___\   
    \ \  __<   \ \____ \     \ \ \/\ \ \ \ \_\ \  \ \  _"-.  \ \  __\   
     \ \_____\  \/\_____\     \ \____-  \ \_____\  \ \_\ \_\  \ \_____\ 
      \/_____/   \/_____/      \/____/   \/_____/   \/_/\/_/   \/_____/ 

    """
    print(lol)


def arvore(directorio):
    os.chdir(directorio)
    selec(directorio)

    temp_in = data__hora(input('Digite a data e hora inicial |YYYY-MM-DD hh:mm:00| ou |YYYY-MM-DD 0| >>>'))
    temp_fi = data__hora(input('Digite a data e hora final |YYYY-MM-DD hh:mm:00| ou |YYYY-MM-DD 0| >>>'))

    with open('tabela_1.csv', 'r') as tabela_csv:
        tabela_csv.readline()
        tab = tabela_csv.readline()
        tab = tab.split(',')
        tab = tab[0]
        tab = tab.split(' ')
        tab_data = data(tab[0])
        tab_hora = hora(tab[1])
        tab = tab_data + tab_hora

        cont1 = 1

        try:
            while tab != temp_in:
                try:
                    tab = tabela_csv.readline()
                    tab = tabela_csv.readline()
                    tab = tab.split(',')
                    tab = tab[0]
                    tab = tab.split(' ')
                    tab_data = data(tab[0])
                    tab_hora = hora(tab[1])
                    tab = tab_data + tab_hora
                    cont1 += 1
                except IndexError:
                    cont1 = 2
        except UnboundLocalError:
            print('Dados inseridos fora do range')
            sys.exit()

    with open('tabela_1.csv', 'r') as tabela_csv:
        tabela_csv.readline()
        tab = tabela_csv.readline()
        tab = tab.split(',')
        tab = tab[0]
        tab = tab.split(' ')
        tab_data = data(tab[0])
        tab_hora = hora(tab[1])
        tab = tab_data + tab_hora

        cont2 = 1

        try:
            while tab != temp_fi:
                try:
                    tab = tabela_csv.readline()
                    tab = tabela_csv.readline()
                    tab = tab.split(',')
                    tab = tab[0]
                    tab = tab.split(' ')
                    tab_data = data(tab[0])
                    tab_hora = hora(tab[1])
                    tab = tab_data + tab_hora
                    cont2 += 1
                except IndexError:
                    cont2 = 2
        except UnboundLocalError:
            print('Dados inseridos fora do range')
            sys.exit()

    cont2 = cont2-cont1

    return cont1, cont2


def escritor(directorio):
    os.chdir(directorio)
    todos = arvore(directorio)

    start = todos[0]
    tamanho = todos[1]

    if tamanho <= 0:
        tamanho = 0

    with open('tabela_1.csv', 'r') as tabela_csv:
        try:
            os.remove('ARQUIVO_TEMPORARIO.csv')
        except FileNotFoundError:
            arquivo = open('ARQUIVO_TEMPORARIO.csv', 'a')
            arquivo.close()

        arquivo = open('ARQUIVO_TEMPORARIO.csv', 'a')
        head = ["Date_e_hora", "Numero_de_registro", "Bateria_(V)", "Pluviosidade_(mm)", "Velocidade_do_vento (m/s)",
                "Direcao_do_vento", "Temperatura_do_ar", "Umidade_relativa", "Irradiancia_(W/m2)", "Irradiancia_(Kj)"]

        escritor = DictWriter(arquivo, fieldnames=head)
        escritor.writeheader()

        for x in range(start):
            tabela_csv.readline()

        for x in range(tamanho + 1):
            tabela = tabela_csv.readline()
            tabela = tabela.split(',')
            tabela[9] = tabela[9].replace('\n', '')

            escritor.writerow({"Date_e_hora": str(tabela[0]),
                               "Numero_de_registro": str(tabela[1]),
                               "Bateria_(V)": str(tabela[2]),
                               "Pluviosidade_(mm)": str(tabela[3]),
                               "Velocidade_do_vento (m/s)": str(tabela[4]),
                               "Direcao_do_vento": str(tabela[5]),
                               "Temperatura_do_ar": str(tabela[6]),
                               "Umidade_relativa": str(tabela[7]),
                               "Irradiancia_(W/m2)": str(tabela[8]),
                               "Irradiancia_(Kj)": str(tabela[9])})
        arquivo.close()

    directorio = os.getcwd()
    print(f'\nO arquivo se encontra em: {directorio}\n'
          f'----------------------------------------------------------------------------------\n\n\n')


directorio = direc()
escritor(directorio)

resposta = input('Deseja imprimir os dados no termina? Y/N: ')

if resposta.upper() == 'Y':
    os.chdir(directorio)

    with open('ARQUIVO_TEMPORARIO.csv') as tabela:
        linhas = len(tabela.readlines())

    with open('ARQUIVO_TEMPORARIO.csv') as tabela:
        for x in range(linhas):
            print(tabela.readline(), end='')
        print('\n ----------------------------- fim -----------------------------\n\n')

if resposta.upper() == 'D':
    coleta()

    resposta = input('Deseja imprimir os dados no termina? Y/N: ')

    if resposta.upper() == 'Y':
        os.chdir(directorio)

        with open('ARQUIVO_TEMPORARIO.csv') as tabela:
            linhas = len(tabela.readlines())

        with open('ARQUIVO_TEMPORARIO.csv') as tabela:
            for x in range(linhas):
                print(tabela.readline(), end='')
            print('\n ----------------------------- fim -----------------------------\n\n')

if os.path.exists("tabela_1.csv"):
    os.remove("tabela_1.csv")

exits = input("digite qualquer coisa para sair")

