from time import sleep
from telegram.client import Telegram
import csv
import random

accounts = (
    ('Meu', 'tsts',),
    ('mee', 'tsts',),
    ('nom', 'tst ',),
)
sessions = []
for name, phone in accounts:
    tg = Telegram(
        api_id='',
        api_hash='',
        phone=phone,
        database_encryption_key='teste123',
        files_directory=f'/tmp/.tdlib_files/{phone}/'    
    )
    print(f'Login do {name}')
    tg.login()
    sessions.append([tg, name])

counter = 0
tel_num = []
values = [x.strip().replace('+', '') for x in open('lista.txt', 'r').readlines()]

with open('saida.csv', 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['NUMERO','STATUS']) 
    writer.writeheader()
    i = -1    
    for value in values:
        if (i+1) >= len(sessions):
            i = -1
        i+= 1
        tg, name = sessions[i]
        print(f'Usando a sessao do {name}')
        counter += 1
        response = tg.call_method('importContacts', {
            'contacts': [
                {'phone_number': '+'+value},
            ]
        })   
        response.wait()
        try:
            user_ids = response.update['user_ids']
        except TypeError:
            print("Erro 420 - Flood_Wait")
            sleep(1)
        if user_ids[0] == 0:
            status = 'ATIVO'
            print(f'{counter} INATIVO {value}')
            sleep(random.choice(range(2, 3)))
        else:       
            status = 'INATIVO'
            print(f'{counter} ATIVO {value}')
            tel_num.append('+'+value) 
            sleep(random.choice(range(2, 3)))
        writer.writerow({'NUMERO': value, 'STATUS': status })
        
        sleep(1)
        tg.call_method('removeContacts', {'user_ids': user_ids})
