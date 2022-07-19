import sqlite3 as sq


base = sq.connect('test.db')
cur = base.cursor()

if base:
    print('DB connected')


base.execute('CREATE TABLE IF NOT EXISTS info(login PRIMARY KEY, password TEXT)')

try:
    for login_number in range(1, 26):
         cur.execute('INSERT INTO info VALUES(?, ?)', (f'login_{login_number}', '112233'))

except Exception as ex:
    print(repr(ex))
    for info in cur.execute('SELECT * FROM info').fetchall():
        print(info)


base.commit()

