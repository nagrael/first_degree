import pymssql
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()

conn = pymssql.connect(server='127.0.0.1', port='11434',
                       user='gorski', password='YCRW6QKf',
                       database="gorski_a")
cursor = conn.cursor()

firm_numbers = [0 for x in range(0, 21)]
firm_students = [0 for x in range(0, 21)]
students = [[] for x in range(0, 21)]
for i in range(0, 20):
    company = fake.company()
    opis = fake.catch_phrase()
    cursor.execute("INSERT INTO Firma VALUES ( %s, %s)", (company, opis))

customer_comapny = [[] for x in range(0, 21)]

for i in range(1, 501):
    name = fake.first_name()
    surname = fake.last_name()
    number = random.randint(0, 20)
    student = random.randint(0, 25)
    if student == 0:
        student = random.randint(10000000, 99999999)
        students[number].append(i)
        firm_students[number] += 1
    else:
        student = None
        customer_comapny[number].append(i)
        firm_numbers[number] += 1
    if number == 0:
        number = None
    identy = name.split()[0][0:3] + surname.split()[0][0:3]
    identy = identy.upper()
    job = fake.job()
    cursor.execute("INSERT INTO Uczestnik VALUES (%s,%s,%s,%d,%s,%d)", (name, surname, job, student, identy, number))

print(firm_students)
print(firm_numbers)
for x in students:
    print(len(x), x)

onedaydel = timedelta(days=1)
mydate = date(2011, 1, 10)
paylist = [50.0, 75.0, 90.0, 100.0, 150.0, 200.0, 300.0]
threeday = [75.0, 90.0, 150.0]
fourday = [100.0, 200.0]
topics = ['Brak Danych', 'Ekonomia', 'Wojna w Syrii', 'CO', 'Nadtlenek potasu',
          'Kulinarny wybuch', "Exel i ty", 'Biuro i dom', 'Zwierzęta wśród nas',
          'Religie 21 wieku', 'Yoga dla wszystkich']
limits = [[] for x in range(0, 72)]
konf_day = [[] for x in range(0, 72)]
konf_day_index = [[] for x in range(0, 72)]
paylists = []
paylist_range = []
days = 0
days_lists = []
for i in range(1, 73):
    timedel = timedelta(days=random.randint(20, 30))
    number = random.choice(paylist)
    paylists.append(number)
    topic = random.choice(topics)
    organizator = fake.company()
    place = fake.city()
    limit = random.randrange(100, 251, 5)
    if number in threeday:
        cursor.execute("INSERT INTO Konferencja VALUES (%d,%d,%s,%s,%s,%s)",
                       (number, (number / 3), str(mydate), organizator, topic, place))
        paylist_range.append((number / 3))
        for x in range(0, 3):
            days += 1
            konf_day[i - 1].append(days)
            konf_day_index[i - 1].append(x)
            limits[i - 1].append(limit)
            cursor.execute("INSERT INTO Dni_Konferencji VALUES (%d,%s,%s,%d)",
                           (i, str(mydate + x * onedaydel), str(x + 1) + ' Day', limit))
    if number in fourday:
        cursor.execute("INSERT INTO Konferencja VALUES (%d,%d,%s,%s,%s,%s)",
                       (number, (number / 4), str(mydate), organizator, topic, place))
        paylist_range.append((number / 4))
        for x in range(0, 4):
            days += 1
            konf_day[i - 1].append(days)
            konf_day_index[i - 1].append(x)
            limits[i - 1].append(limit)
            cursor.execute("INSERT INTO Dni_Konferencji VALUES (%d,%s,%s,%d)",
                           (i, str(mydate + x * onedaydel), str(x + 1) + ' Day', limit))
    if number == 50.0:
        cursor.execute("INSERT INTO Konferencja VALUES (%d,%d,%s,%s,%s,%s)",
                       (number, (number / 2), str(mydate), organizator, topic, place))
        paylist_range.append((number / 2))
        for x in range(0, 2):
            days += 1
            konf_day[i - 1].append(days)
            konf_day_index[i - 1].append(x)
            limits[i - 1].append(limit)
            cursor.execute("INSERT INTO Dni_Konferencji VALUES (%d,%s,%s,%d)",
                           (i, str(mydate + x * onedaydel), str(x + 1) + ' Day', limit))
    if number == 300.0:
        cursor.execute("INSERT INTO Konferencja VALUES (%d,%d,%s,%s,%s,%s)",
                       (number, (number / 5), str(mydate), organizator, topic, place))
        paylist_range.append((number / 5))
        for x in range(0, 5):
            days += 1
            konf_day[i - 1].append(days)
            konf_day_index[i - 1].append(x)
            limits[i - 1].append(limit)
            cursor.execute("INSERT INTO Dni_Konferencji VALUES (%d,%s,%s,%d)",
                           (i, str(mydate + x * onedaydel), str(x + 1) + ' Day', limit))
    days_lists.append(mydate)
    mydate += timedel

cursor.execute("INSERT INTO Progi_Cenowe VALUES (0.05,0.10,0.15,0.10)")

war_info = [[] for x in range(0, days)]
z = 0
for i in range(0, days):
    for x in range(0, random.randint(4, 20)):
        z += 1
        op = random.randrange(50, 251, 10)
        lim = random.randint(15, 45)
        time = timedelta(hours=random.randint(9, 20), minutes=random.randrange(0, 55, 5))
        timeend = time + timedelta(hours=random.randint(1, 2), minutes=random.randrange(0, 55, 5))
        war_info[i].append([z, op, lim, time, timeend])
        time = str(time)
        timeend = str(timeend)
        cursor.execute("INSERT INTO Warsztaty VALUES (%d,%s,%s,%d,%d)", (i + 1, time, timeend, op, lim))

conn.commit()
zaplac = []
rez_ind = 0
rez_war = 0
for rez in range(1, 73):
    # print("I am at for\n")
    day = days_lists[rez - 1]
    kon = konf_day[rez - 1]
    ind = konf_day_index[rez - 1]
    limi = limits[rez - 1]
    open_price = paylist_range[rez - 1]
    # print(day, kon, ind, limi)
    used = []
    zeros_used = []
    con = True
    while con:
        oplata = 0
        # print("I am at beggining while\n", used)
        index = random.randint(1, 20)
        while index in used:
            index = random.randint(0, 20)
            if len(used) == 20:
                con = False
                break
        if index != 0:
            used.append(index)
        # print("while\n", con)
        timediff = timedelta(days=random.randrange(1, 121, 6))
        if (firm_numbers[index]) != 0:
            number = (firm_numbers[index]) - random.randint(0, (firm_numbers[index]) - 1)
        else:
            number = 0
        if firm_students[index] != 0:
            student_numb = (firm_students[index]) - random.randint(0, (firm_students[index]))
        else:
            student_numb = 0
        number += student_numb
        if index == 0:
            number = 1
            if student_numb > 1:
                student_numb = 1
        for lim in limi:
            # print("I am  at limi for\n")
            if (lim) < number:
                con = False

        names = random.sample(customer_comapny[index], (number - student_numb))
        stud = random.sample(students[index], student_numb)
        names.extend(stud)
        while name[0] in zeros_used:
            names = random.sample(customer_comapny[index], (number - student_numb))
            stud = random.sample(students[index], student_numb)
            names.extend(stud)
            if len(zeros_used) == firm_numbers[0]:
                if len(used) == 20:
                    con = False
                break
        if con and (number > 0):

            if index != 0:
                cursor.execute("INSERT INTO Rezerwacje VALUES (%d,%d,%s,%d,%d)",
                               (index, None, str(day - timediff), student_numb, number))
            else:
                cursor.execute("INSERT INTO Rezerwacje VALUES (%d,%d,%s,%d,%d)",
                               (None, names[0], str(day - timediff), student_numb, number))
            rez_ind += 1
            for person in names:
                cursor.execute("INSERT INTO Szczegoly_rezerwacji VALUES (%d,%d)", (rez_ind, person))
            # print("I am afte Rezerwacje\n")
            how_many = random.randint(1, len(ind))
            how_many_days = random.sample(ind, how_many)
            for x in how_many_days:
                # print("I am Rezerwacje days for\n")
                limi[x] -= number
                cursor.execute("INSERT INTO Rezerwacje_dni VALUES (%d,%d)", (rez_ind, kon[x]))
                oplata += open_price * number
                war = war_info[x]
                random.shuffle(war)
                times = []
                for w in war:
                    ispossible = True
                    num = random.randint(0, 6)
                    if num != 0:
                        for ti in times:
                            if (ti[0] < w[3] < ti[1]) or (ti[0] < w[4] < ti[1]):
                                ispossible = False
                                '''
                                times.append((w[4], w[3]))
                                if w[2] > 0:
                                    if w[2] > number:
                                        numb = random.randint(1, number)
                                    else:
                                        numb = random.randint(1, w[2])
                                    w[2] -= numb
                                    oplata += w[1] * numb
                                    rez_war += 1
                                    abc = w[0]
                                    cursor.execute("INSERT INTO Rezerwacje_warsztat VALUES (%d,%d,%d)",
                                                   (rez_ind, abc, numb))
                                    nr = random.sample(names, numb)
                                    for n in nr:
                                        cursor.execute("INSERT INTO Warsztat_uczestnik VALUES (%d,%d)", (rez_war, n))
                                        '''
                        if ispossible:
                            if w[2] > 0:
                                times.append((w[3], w[4]))
                                if w[2] > number:
                                    numb = random.randint(1, number)
                                else:
                                    numb = random.randint(1, w[2])
                                w[2] -= numb
                                abc = w[0]
                                oplata += w[1] * numb
                                rez_war += 1

                                cursor.execute("INSERT INTO Rezerwacje_warsztat VALUES (%d,%d,%d)",
                                               (rez_ind, abc, numb))
                                nr = random.sample(names, numb)
                                for n in nr:
                                    cursor.execute("INSERT INTO Warsztat_uczestnik VALUES (%d,%d)", (rez_war, n))

            timediff = timedelta(days=random.randrange(1, 81, 6))
            print(rez_ind, oplata, str(day - timediff), str(day), oplata)
            cursor.execute("INSERT INTO Oplaty VALUES (%s,%s,%s,%s,%s)",
                           (str(rez_ind), str(oplata), str(day - timediff), str(day), str(oplata)))

print(limits)

'''
cursor.execute("INSERT INTO Opłaty VALUES (500,'2012-7-11',1500)")
cursor.execute("INSERT INTO Opłaty VALUES (90,'2012-4-20',1000)")

cursor.execute("INSERT INTO Rezerwacje VALUES (1,1,'2012-9-11',0,1)")
cursor.execute("INSERT INTO Rezerwacje VALUES (2,2,'2012-7-11',1,3)")
cursor.execute("INSERT INTO Rezerwacje VALUES (NULL,3,'2012-5-11',0,0)")

cursor.execute("INSERT INTO Rezerwacje_warsztat VALUES (1,1,100,1)")
cursor.execute("INSERT INTO Rezerwacje_warsztat VALUES (2,3,100,2)")
cursor.execute("INSERT INTO Rezerwacje_warsztat VALUES (3,1,50,1)")
conn.commit()

cursor.execute('SELECT IDUczestnik FROM Uczestnik WHERE FirmaID=2')
rows = cursor.fetchall()
row = [(2, rowas[0]) for rowas in rows]
print(row)
cursor.execute('SELECT IDUczestnik FROM Uczestnik WHERE FirmaID is NULL')
user = cursor.fetchone()
print(user)
use = [3, user[0]]
print(use)
cursor.executemany("INSERT INTO Szczegoly_rezerwacji VALUES (%d,%d)", row)
cursor.execute("INSERT INTO Szczegoly_rezerwacji VALUES (%d,%d)", tuple(use))
cursor.execute("INSERT INTO Szczegoly_rezerwacji VALUES (1,1)")
del row[0]
cursor.executemany("INSERT INTO Warsztat_uczestnik VALUES (%d,%d)", row)
cursor.execute("INSERT INTO Warsztat_uczestnik VALUES (%d,%d)", tuple(use))
cursor.execute("INSERT INTO Warsztat_uczestnik VALUES (1,1)")

cursor.executemany("INSERT INTO Rezerwacje_dni VALUES (%d,%d)",
                   [(1, 1), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 1), (3, 3)])
'''
conn.commit()

conn.close()
