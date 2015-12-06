#!/usr/bin/env python3
import os
import hashlib
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-creat_mode', '--c', action='store_const', const=True)
parser.add_argument('-edit_mode', '--e', action='store_const', const=True)
parser.add_argument('-read_mode', '--r', action='store_const', const=True)
parser.add_argument('-pattern', '--pt', default='stnd')
parser.add_argument('-platform', '--pf', default='null')
parser.add_argument('-login', '--lg', default='user')
parser.add_argument('-password', '--ps', default='user')
parser.add_argument('-card_number', '--nb', default='123456789000000')
parser.add_argument('-cvv', '--cvv', default='123')
parser.add_argument('-date', '--dt', default='01/15')
parser.add_argument('-name', '--nm', default='John')
parser.add_argument('-surname', '--sm', default='Titor')

def init(path=os.path.dirname(os.path.abspath(__file__))+'/'+hashlib.sha1(os.getlogin().encode()).hexdigest()):
    #print(path)
    if os.path.isfile(path):
        parsing(path)
    else:
        try:
            print('Вы еще не пользовались менеджером паролей Whitespace, хотите начать?(Д/Н)')
            new(path)
        except Exception:
            new(path)

def new(path):
    pick=str(input())
    if pick=='Н':
        raise SystemExit(1)
    elif pick=='Д':
        print('Менеджер паролей Whitespace приветствует вас. Для его использования запомните несколько команд: '+'\n'+
        '1) Создание пароля осуществляется командой --c, редактирование уже существующего --e и просмотр паролей по команде --r'+'\n'+
        '2) Программа имеет два предустановленных шаблона для паролей. --pt stnd для обычных сайтов и --pt card для банковских карт.'+'\n'+
        '3) Форма для создания пароля для сайта "--c --pf <platform> --lg <login> --ps <password>"'+'\n'+
        '4) Форма для изменения пароля для сайта "--e --pf <platform> --lg <login> --ps <password>"'+'\n'+
        '5) Форма для создания пароля для банковской карточки "--c --nb <number> --cvv <CVV> --dt <date> --nm <name> --sm surname"'+'\n'+
        '6) Форма для изменения пароля для банковской карточки "--e --nb <number> --cvv <CVV> --dt <date> --nm <name> --sm surname"'+'\n'+
        '7) Для просмотра пароля введите --r и --pt stnd/card в зависимости от ваших нужд. Вам будут показаны пароли в соответствии с указанными параметрами.')
        mine = open(path,'w')
        mine.close()
        init()

def read_pass_account(platform, login, path):
    rows=open(path,'r')
    if platform=='null' and login=='user':
        for row in rows:
            if row.split()[0]=='Platform:':
                print(row)
    elif platform=='null':
        for row in rows:
            if row.split()[3]==login:
                print(row)
    elif login=='user':
        for row in rows:
            if row.split()[1]==platform:
                print(row)
    else:
        for row in rows:
            if row.split()[1]==platform and row.split()[3]==login():
                print(row)
    rows.close()

def read_pass_creditcard(number, name, surname, path):
    rows=open(path,'r')
    if number=='123456789000000' and name=='John' and surname=='Titor':
        for row in rows:
            if row.split()[0]=='Card:':
                print(row)
    elif number=='123456789000000':
        for row in rows:
            if row.split()[7]==name and row.split()[9]==surname:
                print(row)
    else:
        for row in rows:
            if row.split()[1]==number and row.split()[7]==name and row.split()[9]==surname:
                print(row)

def parsing(path):
    global string
    string=parser.parse_args(input('Вводите команды: ').split())
    if string.c:
        if string.pt=='stnd':
            new_pass_account(string.pf, string.lg, string.ps, path)
        elif string.pt=='card':
            new_pass_creditcard(string.nb, string.dt, string.cvv, string.nm, string.sm, path)
    elif string.e:
        if string.pt=='stnd':
            edit_pass_account(string.pf, string.lg, string.ps, path)
        elif string.pt=='card':
            edit_pass_creditcard(string.nb, string.dt, string.cvv, string.nm, string.sm, path)
    elif string.r:
        if string.pt=='stnd':
            read_pass_account(string.pf, string.lg, path)
        elif string.pt=='card':
            read_pass_creditcard(string.nb, string.nm, string.sm, path)

def new_pass_account(platform, login, password, path):
    with open(path,'r') as mine:
        rows=mine.readlines()
        for row in rows:
            if platform+' '+login==row.split()[1]+' '+row.split()[3]:
                print('Подобное сочетание платформы и аккаунта уже существует. Возможно вы пытаетесь перезаписать данные. Для этого используйте форму вида "--e --pf <platform> --lg <login> --ps <password>"')
                init()
    mine.close()
    with open(path,'a') as mine:
        mine.write('Platform: '+platform+' Login: '+login+' Password: '+password+'\n')
    mine.close()
    init()

def edit_pass_account(platform, login, password, path):
    rows=open(path,'r').readlines()
    for index in range(len(rows)):
        if rows[index].split()[1]==platform and rows[index].split()[3]==login:
            rows[index]='Platform: '+platform+' Login: '+login+' Password: '+password+'\n'
            break
        if index==len(rows)-1:
            print('Подобного сочетания платформы и аккаунта не существует. Возможно вы пытаетесь записать новые данные. Для этого используйте форму вида "--c --pf <platform> --lg <login> --ps <password>"')
            init()
    with open(path,'w') as mine:
        for row in rows:
            mine.write(row)
    init()

def new_pass_creditcard(number, date, cvv, name, surname, path):
    with open(path,'r') as mine:
        rows=mine.readlines()
        for row in rows:
            if number==row.split()[1]:
                print('Подобная карта уже существует. Возможно вы пытаетесь перезаписать данные. Для этого используйте форму вида "--e --nb <number> --cvv <CVV> --dt <date> --nm <name> --sm surname"')
                init()
    mine.close()
    with open(path,'a') as mine:
        mine.write('Card: '+number+' Exp.date: '+date+' CVV: '+cvv+' Name: '+name+' Surname: '+surname+'\n')
    mine.close()
    init()

def edit_pass_creditcard(number, date, cvv, name, surname, path):
    rows=open(path,'r').readlines()
    for index in range(len(rows)):
        if rows[index].split()[1]==number:
            rows[index]='Card: '+number+' Exp.date: '+date+' CVV: '+cvv+' Name: '+name+' Surname: '+surname+'\n'
            break
        if index==len(rows)-1:
            print('Подобной карты не найдено. Возможно вы пытаетесь записать новые данные для этого используйте форму вида "--c --nb <number> --cvv <CVV> --dt <date> --nm <name> --sm surname"')
            init()
    with open(path,'w') as mine:
        for row in rows:
            mine.write(row)
    init()

init()
