import pymssql


conn = pymssql.connect(server='127.0.0.1', port='11434',
                       user='gorski', password='YCRW6QKf',
                       database="gorski_a")
cursor = conn.cursor()

cursor.execute("""
        DROP TABLE Rezerwacje_dni
        DROP TABLE Warsztat_uczestnik
        DROP TABLE Szczegoly_rezerwacji
        DROP TABLE Rezerwacje_warsztat
        DROP TABLE Oplaty
        DROP TABLE Rezerwacje
        DROP TABLE Uczestnik
        DROP TABLE Firma
        DROP TABLE Warsztaty
        DROP TABLE Dni_Konferencji
        DROP TABLE Konferencja
        DROP TABLE Progi_Cenowe
""")


cursor.execute("""
    CREATE TABLE Firma (
        IDFirma INT IDENTITY(1,1)  PRIMARY KEY,
        nazwa VARCHAR(100) NOT NULL,
        dane VARCHAR(100),
    )
    """)


cursor.execute("""
    CREATE TABLE Uczestnik (
        IDUczestnik INT IDENTITY(1,1)  PRIMARY KEY,
        imie VARCHAR(100) NOT NULL,
        nazwisko VARCHAR(100) NOT NULL,
        dane VARCHAR(100),
        legitymacja_studencka int,
        identyfikator VARCHAR(100),
        FirmaID INT NULL FOREIGN KEY REFERENCES Firma (IDFirma),
    )
    """)

cursor.execute("""
    CREATE TABLE Konferencja (
        IDKonferencja INT IDENTITY(1,1)  PRIMARY KEY,
        cena real NOT NULL,
        cena_dnia real NOT NULL,
        data DATE UNIQUE NOT NULL,
        organizator VARCHAR(100) NOT NULL,
        temat VARCHAR(100) NOT NULL,
        miejsce VARCHAR(100) NOT NULL,
    )
    """)

cursor.execute("""
    CREATE TABLE Dni_Konferencji (
        IDKonferencji_Dni INT IDENTITY(1,1)  PRIMARY KEY,
        KonferencjaID INT NOT NULL FOREIGN KEY Konferencja (IDKonferencja),
        data DATE NOT NULL,
        opis VARCHAR(100),
        limit_miejsc INT NOT NULL CHECK ([limit_miejsc]>(0)),
    )
    """)

cursor.execute("""
     CREATE TABLE Progi_Cenowe (
        dwa_tygodnie REAL NOT NULL,
        miesiąc REAL NOT NULL,
        trzy_miesiace REAL NOT NULL,
        student REAL NOT NULL
    )
    """)
cursor.execute("""
    CREATE TABLE Warsztaty (
        IDWarsztaty INT IDENTITY(1,1)  PRIMARY KEY,
        Kon_DniID INT NOT NULL  FOREIGN KEY REFERENCES Dni_Konferencji (IDKonferencji_Dni),
        rozpoczecie time NOT NULL,
        zakonczenie time NOT NULL,
        opłata real not null,
        limit_uczestnikow INT not null CHECK ([limit_uczestnikow]>(0)),
    )
    """)

cursor.execute("""
    CREATE TABLE Rezerwacje (
        IDRezerwacje INT IDENTITY(1,1)  PRIMARY KEY,
        FirID INT FOREIGN KEY REFERENCES Firma (IDFirma),
        UczesID INT FOREIGN KEY REFERENCES Uczestnik (IDUczestnik),
        data_złożenia_rezerwacji date NULL,
        liczba_studentow INT NOT NULL,
        ile_osob INT NOT NULL CHECK ([ile_osob]>(0))
    )
    """)

cursor.execute("""
    CREATE TABLE Oplaty (
        IDOpłaty INT PRIMARY KEY ,
        zapłacono MONEY NOT NULL,
        data_zapłaty DATE,
        data_do_zapłaty DATE NOT NULL,
        do_zapłaty MONEY not null
    )
    """)
cursor.execute("""
    CREATE TABLE Rezerwacje_warsztat (
        IDRezWar INT IDENTITY(1,1)  PRIMARY KEY,
        IDofRez INT FOREIGN KEY REFERENCES Rezerwacje (IDRezerwacje),
        IDofWar int FOREIGN KEY REFERENCES Warsztaty (IDWarsztaty),
        ilosc_osob int not null CHECK ([ilosc_osob]>(0)),
    """)

cursor.execute("""
    CREATE TABLE Szczegoly_rezerwacji (
        idRez INT FOREIGN KEY Rezerwacje (IDRezerwacje),
        idUcze int FOREIGN KEY Uczestnik (IDUczestnik),
    )
    """)

cursor.execute("""
    CREATE TABLE Warsztat_uczestnik (
        idWar INT FOREIGN KEY Rezerwacje_warsztat (IDRezWar),
        idUczest int FOREIGN KEY Uczestnik (IDUczestnik),
    )
    """)

cursor.execute("""
    CREATE TABLE Rezerwacje_dni (
        idRezerw INT FOREIGN KEY Rezerwacje (IDRezerwacje),
        idDni int FOREIGN KEY Dni_Konferencji (IDKonferencji_Dni),
    )
    """)
conn.commit()

conn.close()