"""
/////////////////////////////////////// Coleta de dados da estacao meteorologica ///////////////////////////////////////

farfuz-poNjec-hinky8
                         ______     __  __        _____     __  __     __  __     ______
                        /\  __ \   /\ \_\ \      /\  __-.  /\ \/\ \   /\ \/ /    /\  ___\
                        \ \  __<   \ \____ \     \ \ \/\ \ \ \ \_\ \  \ \  _"-.  \ \  __\
                         \ \_____\  \/\_____\     \ \____-  \ \_____\  \ \_\ \_\  \ \_____\
                          \/_____/   \/_____/      \/____/   \/_____/   \/_/\/_/   \/_____/



Feito por: Savio Goncalves Mendonca (DUKE)
Data de criacao: 2019-08-28
"Contratante": GREEN
Vercao python: 3.7

------------------------------------------------------------------------------------------------------------------------
Informacoes adicionais:

    >> Todos elementos que podem ser coletados do campbell cr10000 (na data de criacao do codigo):
    "Datetime", "RecNbr", "b'BattV_Min'", "b'Rain_mm_Tot'", "b'WS_ms_Avg'", "b'WS_ms_Max'", "b'WS_ms_S_WVT'",
    "b'WindDir_D1_WVT'", "b'WindDir_SD1_WVT'", "b'AirTC_Avg'", "b'RH'", "b'Solar_Wm2_Avg'",
    "b'Solar_KJ_Tot'", "b'piranometro_dif_Avg'"

    >> Com o programa escrito desta forma, so eh possivel rodar em linux

    >> Todos pacotes estao na pasta ~venv/lib/python3.7/site-packages

    >> O interpretador Python esta na pasta ~venv/bin

------------------------------------------------------------------------------------------------------------------------
"""

import time
import os
import sys
from csv import DictWriter
from pycampbellcr1000 import CR1000
from datetime import datetime


def criar_tabela():  # Criacao da tabela
    directorio = pastas_tabelas()  # Chama a funcao que verifica as pastas e arquivos
    os.chdir(directorio)  # Muda para o directorio correto

    print('Verificando tamanho da tabela... ', end='')

    with open('tabela_1.csv', 'r') as tabela_csv:  # Verifica o tamanho da tabela principal
        tamanho = len(tabela_csv.readlines())

    print(f'OK       ({tamanho} linhas)')

    if tamanho == 0:  # Se a tabela nao tiver dados, ela vai retorna 0
        novos_dados()  # Chama a funcao que grava os dados a partir do 0

    else:  # Se a tabela tiver algum dado, ela retorna algo diferente de 0
        with open('tabela_1.csv', 'r') as tabela_csv:  # Coleta a ultima linha da tabela
            for a in range(tamanho):
                linha = tabela_csv.readline()

        # Abaixo chama duas funcoes, a externa ira salvar os dados que faltam, e a interna ajeita a data e hora
        complemento_dados(tempo(linha))


def tempo(data_hora):  # Edita a data e a hora
    print('Verificando data e hora... ', end='')
    data_hora = data_hora.split(',')  # Divide a str em uma lista
    data_hora = data_hora[0]  # Seleciona o primeiro elemento da lista

    data_hora = data_hora.split(' ')  # Divide a str em um lista [data, hora]
    data = data_hora[0]  # Seleciona a data
    data = data.split('-')  # Divide cada parte da tada em uma lista
    hora = data_hora[1]  # Seleciona a hora
    hora = hora.split(':')  # Divide cada parte da hora em uma lista

    data_hora = data + hora  # Junta as lista
    data_hora = list(map(int, data_hora))  # Cria uma lista de inteiro com a data e hora

    data_hora = datetime(year=data_hora[0], month=data_hora[1], day=data_hora[2], hour=data_hora[3],
                         minute=data_hora[4], second=data_hora[5])  # formata a data e hora
    print(f'OK             ({data_hora})')

    return data_hora  # retorna a data e hora formatados


def dado_campbell():  # Conecta com CR1000 e coleta os dados
    try:
        print('Conectando com Campbell CR1000... ', end='')
        device = CR1000.from_url('serial:/dev/ttyUSB0:38400')
        print('OK')

    except Exception:
        print('ERRO\n---------------------------- 60 min ---------------------------')
        time.sleep(1200)
        print('Conectando com Campbell CR1000', end='')
        time.sleep(3)
        print('.', end='')
        time.sleep(3)
        print('.', end='')
        time.sleep(3)
        print('. ', end='')
        try:
            device = CR1000.from_url('serial:/dev/ttyUSB0:38400')
            print('OK')
        except Exception:
            print('ERRO\n---------------------------- EXIT ----------------------------')
            sys.exit()

    return device


def pastas_tabelas():  # Verifica se tem as pastas e tabelas principais para o funcionamento do programa
    print('Verificando diretorio e pastas...', end=' ')

    os.chdir("..")  # Muda o directorio para um directorio anterior
    directorio = os.getcwd()  # Recebe o directorio atual
    teste = 'Tabela(csv)' in os.listdir(directorio)  # Testa se ha a pasta 'Tabela(CSV)'

    if teste == 1:  # Caso exista a tabela
        print('OK\nVerificando tabela principal...', end=' ')

        directorio = directorio + '/Tabela(csv)'  # Garda o directorio da tabela
        os.chdir(directorio)  # Muda para directorio da tabela
        tabela_csv = 'tabela_1.csv' in os.listdir(directorio)  # Verifica se existe o arquivo 'tabela_1.csv'

        if tabela_csv == 0:  # Caso não exista
            print('ERRO\nCriando tabela.')
            arquivo = open('tabela_1.csv', 'w')  # Cria a tabela
            arquivo.close()  # Fecha o arquivo
        else:
            print('OK')

    else:  # Caso não exista a tabela
        print('ERRO\nCriando pastas e arquivos iniciais... ')
        os.mkdir(directorio + '/Tabela(csv)')  # Cria o directorio
        directorio = directorio + '/Tabela(csv)'  # Muda para directorio da tabela
        os.chdir(directorio)
        print('OK')

        arquivo = open('tabela_1.csv', 'w')  # Cria a tabela
        arquivo.close()  # Fecha o arquivo

    return directorio  # Retorna o local onde esta a tabela


def novos_dados():  # Coleta de dados caso seja primeira coleta

    device = dado_campbell()  # Recebe o caminho dos dados

    print('Caprutando dados de Campbell CR1000... ', end='')
    data = device.get_data('Table1')  # Coleta os dados brutos
    print('OK')

    print('Escrevendo na tabela... ', end='')
    with open('tabela_1.csv', 'w') as tabela_csv:  # Inicia o arquivo .csv e cria o cabecalho (modo escrita)
        head = ["Date_e_hora", "Numero_de_registro", "Bateria_(V)", "Pluviosidade_(mm)", "Velocidade_do_vento (m/s)",
                "Direcao_do_vento", "Temperatura_do_ar", "Umidade_relativa", "Irradiancia_(W/m2)", "Irradiancia_(Kj)"]

        escritor = DictWriter(tabela_csv, fieldnames=head)
        escritor.writeheader()

        for n in range(len(data)):  # Transfere todos os dados
            escritor.writerow({"Date_e_hora": data[n]["Datetime"].strftime('%Y-%m-%d %H:%M:%S'),
                               "Numero_de_registro": str(data[n]["RecNbr"]),
                               "Bateria_(V)": str(data[n]["b'BattV_Min'"]),
                               "Pluviosidade_(mm)": str(data[n]["b'Rain_mm_Tot'"]),
                               "Velocidade_do_vento (m/s)": str(data[n]["b'WS_ms_Avg'"]),
                               "Direcao_do_vento": str(data[n]["b'WindDir_D1_WVT'"]),
                               "Temperatura_do_ar": str(data[n]["b'AirTC_Avg'"]),
                               "Umidade_relativa": str(data[n]["b'RH'"]),
                               "Irradiancia_(W/m2)": str(data[n]["b'Solar_Wm2_Avg'"]),
                               "Irradiancia_(Kj)": str(data[n]["b'Solar_KJ_Tot'"])})
    print('OK')


def complemento_dados(data_inicial):  # Coleta de dados que estao faltando

    device = dado_campbell()  # Recebe o caminho dos dados

    data = device.get_data('Table1', data_inicial)  # Coleta os dados entre o ultimo lido no arquivo e o atual

    print('Escrevendo na tabela... ', end='')
    with open('tabela_1.csv', 'a') as tabela_csv:  # Inicia o arquivo .csv e cria o cabecalho (modo escrita)
        head = ["Date_e_hora", "Numero_de_registro", "Bateria_(V)", "Pluviosidade_(mm)", "Velocidade_do_vento (m/s)",
                "Direcao_do_vento", "Temperatura_do_ar", "Umidade_relativa", "Irradiancia_(W/m2)", "Irradiancia_(Kj)"]

        escritor = DictWriter(tabela_csv, fieldnames=head)

        for n in range(len(data)):   # Transfere todos os dados
            escritor.writerow({"Date_e_hora": data[n]["Datetime"].strftime('%Y-%m-%d %H:%M:%S'),
                               "Numero_de_registro": str(data[n]["RecNbr"]),
                               "Bateria_(V)": str(data[n]["b'BattV_Min'"]),
                               "Pluviosidade_(mm)": str(data[n]["b'Rain_mm_Tot'"]),
                               "Velocidade_do_vento (m/s)": str(data[n]["b'WS_ms_Avg'"]),
                               "Direcao_do_vento": str(data[n]["b'WindDir_D1_WVT'"]),
                               "Temperatura_do_ar": str(data[n]["b'AirTC_Avg'"]),
                               "Umidade_relativa": str(data[n]["b'RH'"]),
                               "Irradiancia_(W/m2)": str(data[n]["b'Solar_Wm2_Avg'"]),
                               "Irradiancia_(Kj)": str(data[n]["b'Solar_KJ_Tot'"])})
    print('OK')


def duplicados():
    os.chdir("..")
    directorio = os.getcwd()
    directorio = directorio + '/Tabela(csv)'
    os.chdir(directorio)

    linha_anterior = ['0', '0']
    n_linha = 0
    n_linha_anterior = 0
    linha_duplicada = []

    with open('tabela_1.csv', 'r') as tab:
        linha = tab.readlines()

    with open('tabela_1.csv', 'r') as tab:
        for i in linha:
            linha = tab.readline()
            linha = linha.split(',')
            n_linha += 1

            if linha[1] == linha_anterior[1]:
                # print(linha[1], end='')
                # print(f'               -{linha}\nlinha {n_linha_anterior} e {n_linha}   -{linha_anterior}')
                linha_duplicada.append(linha[1])
            n_linha_anterior = n_linha
            linha_anterior = linha

        contador = 0

        for i in range(len(linha_duplicada)):
            with open('tabela_1.csv', 'r+') as tabela:
                tempo = tabela.readlines()
                tabela.seek(0)
                for line in tempo:
                    if linha_duplicada[contador] not in line:
                        tabela.write(line)
                tabela.truncate()

            #cprint(len(linha_duplicada) - contador)
            contador += 1

            if len(linha_duplicada) - contador == 0:
                return


ciclo = 0
ciclo_temporario = 0

while True:
    print(f'----- Iniciando o ciclo numero {ciclo:4}, desde inicio do programa -----')
    criar_tabela()

    if ciclo - ciclo_temporario == 0:
        duplicados()
        ciclo_temporario += 10

    print(f'---------------Fim do ciclo numero {ciclo:4}.... STANDBY---------------\n\n')
    ciclo += 1

    time.sleep(300)
