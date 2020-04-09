#!/usr/bin/python3
#Codec By RyM

try:
    import requests as req, os, time, sys
    from datetime import datetime as dt
except Exception as ex:
    exit(f"Module '{ex.name}' belum diinstall bro")

w = tuple([chr(27)+'[1;0m'] + list(chr(27)+'[1;3'+str(x)+'m' for x in range(1,7)))
url = 'https://api.kawalcorona.com/'
commands = (
        'q', 'exit',
        'ls',
        'cls',
        'status',
        'h', 'help',
        'total'
        )
hari = (
        'Senin',
        'Selasa',
        'Rabu',
        'Kamis',
        'Jumat',
        'Sabtu',
        'Minggu'
        )

bulan = (
        'Januari',
        'Februari',
        'Maret',
        'April',
        'Mei',
        'Juni',
        'Juli',
        'Agustus',
        'September',
        'Oktober',
        'November',
        'Desember'
        )

def help():
    a, b = w[2], w[3]
    print(f'\t{a}- q, exit\n\t{b}- h, help\n\t{a}- cls -> hapus screen\n\t{b}- ls -> list negara/provinsi\n\t{a}- status -> status corona\n\t{b}- total -> total kasus keseluruhan')

def h(): help()

def q(): exit()

def getter():
    x = input(w[0]+'\t1. Global\n\t2. Lokal\n> ')
    if x == '2':
        return req.get(url+'indonesia/provinsi/').json(), 'Provinsi', 'provinsi'
    elif x == '1':
        return req.get(url).json(), 'Country_Region', 'negara'
    else:
        return None, None, x

def ls():
    a,b,c = getter()
    if a == None: return
    lines = os.get_terminal_size().lines
    line = 1
    try:
        for y in a:
            print(f'\t{w[3]}{a.index(y)+1}. {w[2]}{y["attributes"][b]}')
            line += 1
            if line == lines:
                line = 1
                input(w[0]+'Press Enter to continue')
                cls()
    except:
        cls()
        return

def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(w[6]+''' _____________
< Info Corona >
 -------------
 *Maulana RyM*
 ____ ____ ____ ____ ____ ____ ____ ____ 
||C |||o |||v |||i |||d |||- |||1 |||9 ||
||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|
*Thanks To Army Cyber Network*

Sumber Info: kawalcorona.com'''

def output(x):
    now = dt.now()
    now = f'{hari[now.weekday()]}, {now.day} {bulan[now.month-1]} {now.year} {now.hour}:{now.minute}:{now.second}'
    open('history.txt', 'a+').write(f'[{now}]\n{x}\n\n')
    print(f'{w[0]}{x}\nTerakhir update: {now}\nsaved: history.txt')

def total():
    g = req.get(url).json()
    positif = 0
    sembuh = 0
    mati = 0
    for x in g:
        data = x['attributes']
        positif += data['Confirmed']
        sembuh += data['Recovered']
        mati += data['Deaths']
        if data['Country_Region'] == 'Indonesia':
            idih = g.index(x)
    idn = g[idih]['attributes']
    cls()
    output(f'''Global:
\tPositif: {positif:,d}
\tSembuh: {sembuh:,d}
\tMeninggal: {mati:,d}
Indonesia:
\tPositif: {idn["Confirmed"]:,d}
\tSembuh: {idn["Recovered"]:,d}
\tMeninggal: {idn["Deaths"]:,d}''')

def status():
    x,y,z = getter()
    if x == None: return
    a = input(f'{w[0]}Masukkan no urut {z}[1-{len(x)}]\n> ')
    if a.isnumeric() and -1 < int(a)-1 < len(x):
        cls()
        data = x[int(a)-1]['attributes']
        if z == 'negara':
            output(f'''Nama {z}: {data["Country_Region"]}
terakhir update: {data["Last_Update"]}
Garis lintang: {data["Lat"]}
Garis Bujur: {data["Long_"]}
Aktif: {data["Active"]}
Positif: {data["Confirmed"]:,d}
Sembuh: {data["Recovered"]:,d}
Meninggal: {data["Deaths"]:,d}''')
        elif z == 'provinsi':
            output(f'''Nama {z}: {data["Provinsi"]}
Positif: {data["Kasus_Posi"]:,d}
Sembuh: {data["Kasus_Semb"]:,d}
Meninggal: {data["Kasus_Meni"]:,d}''')

cls()
total()
while True:
    cmd = input(w[0]+'$ ')
    if cmd in commands:
        exec(cmd+'()')
    else:
        print(f'\x1b[7;31mtidak ada command "{cmd}"{w[0]}') if cmd != '' else None
