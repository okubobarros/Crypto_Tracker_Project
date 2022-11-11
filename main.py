import locale
from datetime import datetime
from classes import CoinGeckoApi, TelegramBot
from time import sleep

id_moeda = input('Enter the ID of the currency to be tracked: ')
valor_minimo = int(input('What is the minimum value to start tracking: '))
valor_maximo = int(input('What is the maximum value to start tracing: '))

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

api = CoinGeckoApi(url_base='https://api.coingecko.com/api/v3')

bot = TelegramBot(token='your_token', chat_id='your_chat_id')

while True:
    if api.ping():
        print('API on-line!')
        sleep(2)
        preco, atualizado_em = api.consulta_preco(id_moeda=id_moeda)
        print('Query performed successfully!')
        sleep(2)
        data_hora = datetime.fromtimestamp(atualizado_em).strftime('%x %X')
        mensagem = None

        if preco < valor_minimo:
            mensagem = f'*Quotation of {id_moeda}*:\n\t' \
                       f'*Price*: R$ {preco}\n\t' \
                       f'*Time*: {data_hora}\n\t' \
                       f'*Reason*: Value less than the minimum!'

        elif preco > valor_maximo:
            mensagem = f'*Quotation of {id_moeda}*:\n\t' \
                       f'*Price*: R$ {preco}\n\t' \
                       f'*Time*: {data_hora}\n\t' \
                       f'*Reason*: Value greater than the maximum!'
        else:
            mensagem = f'*Quotation of {id_moeda}*:\n\t' \
                       f'*Price*: R$ {preco}\n\t' \
                       f'*Time*: {data_hora}\n\t' \
                       f'*Reason*: The market-price is lateral!'

        if mensagem:
            bot.envia_mensagem(texto_markdown=mensagem)
    else:
        print('Server offline, try again later! ')

    sleep(300)
