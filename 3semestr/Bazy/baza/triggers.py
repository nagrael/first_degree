import pymssql

conn = pymssql.connect(server='127.0.0.1', port='11434',
                       user='gorski', password='YCRW6QKf',
                       database="gorski_a")
cursor = conn.cursor()

cursor.execute("""
CREATE TRIGGER [dbo].[DateNieWPrzeszlosci]
    ON [dbo].[Konferencja]
    AFTER INSERT,UPDATE
AS
BEGIN
-- SET NOCOUNT ON added to prevent extra result sets from
-- interfering with SELECT statements.
SET NOCOUNT ON;
DECLARE @Date date = (SELECT data FROM inserted)
IF((DATEDIFF(day,GETDATE(),@Date) <= 0))
BEGIN
;THROW 52000,'Konferencja nie może zaczynać się wcześniej niż następnego dnia.',1
ROLLBACK TRANSACTION
END
END


""")

cursor.execute("""
CREATE TRIGGER [dbo].[FirmaLubUczetnikNieNull]
    ON [dbo].[Rezerwacje]
    AFTER INSERT,UPDATE
AS
BEGIN
DECLARE @Firma int = (SELECT FirID FROM inserted)
DECLARE @Uczestnik int = (SELECT UczesID FROM inserted)
IF(@Firma IS NULL)
    IF(@Uczestnik IS NULL)
        BEGIN
        ;THROW 53000,'Musi byc sprecyzowane czy rezerwacja jest przez firme czy osobe prywatna.',1
        ROLLBACK TRANSACTION
        END
IF(@Firma IS NOT NULL)
    IF(@Uczestnik IS NOT NULL)
        BEGIN
        ;THROW 53000,'Musi byc sprecyzowane czy rezerwacja jest przez firme czy osobe prywatna.',1
        ROLLBACK TRANSACTION
        END

END

""")

cursor.execute("""
CREATE TRIGGER [dbo].[CzasTrwaniaWarsztat]
    ON [dbo].[Warsztaty]
    AFTER INSERT,UPDATE
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @start time = (SELECT rozpoczecie FROM inserted)
    DECLARE @end time = (SELECT zakonczenie FROM inserted)
    IF((DATEDIFF(minute,@start,@end) <= 1))
    BEGIN
        ;THROW 51000,'Warsztat musi trwac dłużej.',1
        ROLLBACK TRANSACTION
    END
END

""")

cursor.execute("""
CREATE TRIGGER [dbo].[MiejcaRezWarsztatMniejNizRezerwacja]
    ON [dbo].[Rezerwacje_warsztat]
    AFTER INSERT,UPDATE
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @numb int = (SELECT ilosc_osob FROM inserted)
    DECLARE @max_numb int = (SELECT R.ile_osob FROM inserted as I
                                join Rezerwacje as R on I.IDofRez = R.IDRezerwacje)
    IF(@numb > @max_numb)
    BEGIN
        ;THROW 50000,'Rezerwacja na warsztat nie moze liczyc wiecej niz na konferencje.',1
        ROLLBACK TRANSACTION
    END
END

""")

cursor.execute("""
CREATE TRIGGER [dbo].[LimitMiejscNaWarsztat]
    ON [dbo].[Rezerwacje_warsztat]
    AFTER INSERT,UPDATE
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @numb int = (SELECT ilosc_osob FROM inserted)
    DECLARE @max_num int = (select W.limit_uczestnikow from Warsztaty as W where W.IDWarsztaty = (SELECT IDofWar FROM inserted))
    DECLARE @rez_num int = (select sum(R.ilosc_osob) from Rezerwacje_warsztat as R
                                where R.IDOfWar = (SELECT IDofWar FROM inserted)
                                group by R.IDOfWar)
    IF(@numb > (@max_num-@rez_num))
    BEGIN
        ;THROW 49000,'Nie można tyle osob zarejestrowac na warsztat .',1
        ROLLBACK TRANSACTION
    END
END

""")

cursor.execute("""
CREATE TRIGGER [dbo].[GodzinWarsztatuMozliwa]
    ON [dbo].[Warsztat_uczestnik]
    AFTER INSERT
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @start time = (Select W.rozpoczecie from inserted as I
					join Rezerwacje_Warsztat as RW on RW.IDRezWar = I.idWar
					join Warsztaty as W on RW.IDofWar = W.IDWarsztaty)
	DECLARE @end time = (Select W.zakonczenie from inserted as I
						join Rezerwacje_Warsztat as RW on RW.IDRezWar = I.idWar
						join Warsztaty as W on RW.IDofWar = W.IDWarsztaty)
    DECLARE @person int = (SELECT idUczest FROM inserted)
    DECLARE @rez int = (SELECT W.Kon_DniID FROM inserted as I
                        join Rezerwacje_Warsztat as RW on RW.IDRezWar = I.idWar
                        join Warsztaty as W on RW.IDofWar = W.IDWarsztaty)
	DECLARE @tmpEnd time
	DECLARE @tmpStart time
	DECLARE @tmpWarID int
    DECLARE curs CURSOR FOR
    (Select W.IDWarsztaty from Warsztat_uczestnik as WU
    join Rezerwacje_Warsztat as RW on RW.IDRezWar = WU.idWar
    join Warsztaty as W on RW.IDofWar = W.IDWarsztaty
    where WU.idUczest = @person and W.Kon_DniID = @rez)
    OPEN curs
		FETCH NEXT FROM curs INTO @tmpWarID
		WHILE @@FETCH_STATUS = 0 BEGIN
			SET @tmpEnd = (Select zakonczenie from Warsztaty where IDWarsztaty = @tmpWarID)
			SET @tmpStart = (Select rozpoczecie from Warsztaty where IDWarsztaty = @tmpWarID)
			if(@start between @tmpStart and @tmpEnd)
			BEGIN
				;THROW 59000,'Kolizja warsztatow! Ta osoba nie może byc zapisana na dany warsztat! .',1
				ROLLBACK TRANSACTION
			END
			if(@end between @tmpStart and @tmpEnd)
			BEGIN
				;THROW 59000,'Kolizja warsztatow! Ta osoba nie może byc zapisana na dany warsztat! .',1
				ROLLBACK TRANSACTION
			END
			FETCH NEXT FROM curs INTO @tmpWarID
		END
		CLOSE curs
		DEALLOCATE curs
END

""")
cursor.execute("""
CREATE TRIGGER [dbo].[RezWarInnyDzienNizRezerwacja]
    ON [dbo].[Rezerwacje_warsztat]
    AFTER INSERT
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @days int = (SELECT  DK.IDKonferencji_Dni FROM inserted as R
						join Rezerwacje_dni as RD on RD.idRezerw = R.IDofRez
						join Dni_Konferencji as DK on DK.IDKonferencji_Dni = RD.idDni)
	DECLARE @war int = (Select W.Kon_DniID from inserted as I
						join Warsztaty as W on I.IDofWar = W.IDWarsztaty)

	IF ((@war not in (@days)))
	BEGIN
        ;THROW 70000,'Żeby wsiąć udział w warsztacie trzeba być tego dnia na konferencji.',1
        ROLLBACK TRANSACTION
    END
END
""")

cursor.execute("""
CREAT TRIGGER [dbo].[DwaTeSameDni]
    ON [dbo].[Rezerwacje_dni]
    AFTER INSERT
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @rez_day int = (SELECT  count(RD.idDni) FROM inserted as I
						join Rezerwacje_dni as RD on RD.idRezerw = I.idRezerw
						where RD.idDni = I.idDni
						group by RD.idDni)

	IF (@rez_day != 1)
	BEGIN
        ;THROW 71000,'Ten dzień jest już uwzględniony w tej rezerwacji.',1
        ROLLBACK TRANSACTION
    END
END
""")

cursor.execute("""
CREATE TRIGGER [dbo].[DwaTeSameDniKonf]
    ON [dbo].[Dni_Konferencji]
    AFTER INSERT,UPDATE
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @date int = (SELECT count(DK.data) FROM inserted as I
							  join Dni_Konferencji as DK on DK.KonferencjaID = I.KonferencjaID
							  where I.data = DK.data
							  group by DK.data )
	IF ((@date !=1))
	BEGIN
        ;THROW 72000,'Ten dzień jest już uwzględniony w tej konferencji.',1
        ROLLBACK TRANSACTION
    END
END
""")


cursor.execute("""
CREATE TRIGGER [dbo].[OraniczoneMiejscaNaKonferencje]
    ON [dbo].[Rezerwacje_dni]
    AFTER INSERT,UPDATE
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @numb int = (SELECT R.ile_osob FROM inserted as I
						join Rezerwacje as R on I.idRezerw = R.IDrezerwacje)
    DECLARE @max_num int = (select DK.limit_miejsc from inserted as I
							join Dni_Konferencji as DK on I.idDni = DK.IDKonferencji_Dni)
    DECLARE @rez_num int = (SELECT sum(ile_osob) FROM Rezerwacje_dni as RD
							join Rezerwacje as R on RD.idRezerw = R.IDRezerwacje
							where RD.idDni = (select I.idDni from inserted as I)
							group by idDni)
    IF(@numb > (@max_num-@rez_num))
    BEGIN
        ;THROW 71000,'Nie można tyle osob zarejestrowac na ten dzień konferencji .',1
        ROLLBACK TRANSACTION
    END
END

""")

cursor.execute("""
CREATE TRIGGER [dbo].[DwaRazyNaTaSamaKonferencjeLubRezerwacje]
   ON [dbo].[Szczegoly_rezerwacji]
    AFTER INSERT,UPDATE
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @os_list int = (SELECT  count(SR.idRez) FROM inserted as I
						join Szczegoly_rezerwacji as SR on SR.idUcze = I.idUcze and SR.idRez = I.idRez
						group by SR.idRez)
	DECLARE @day_list int = (SELECT RD.idDni FROM inserted as I
						join Szczegoly_rezerwacji as SR on SR.idUcze = I.idUcze
						join Rezerwacje_dni as RD on SR.idRez = RD.idRezerw
						where I.idRez != SR.idRez)
	DECLARE @tmpDay int

	IF (@os_list !=1)
    BEGIN
        ;THROW 72000,'Ta osoba jest juz przypisana do tej rezerwacji .',1
        ROLLBACK TRANSACTION
    END
	 DECLARE curs CURSOR FOR
    (Select RD.idDni from inserted as I
	join Rezerwacje_dni as RD on I.idRez = RD.idRezerw)
    OPEN curs
		FETCH NEXT FROM curs INTO @tmpDay
		WHILE @@FETCH_STATUS = 0 BEGIN
			if(@tmpDay in (@day_list))
			BEGIN
				;THROW 73000,'Ta osoba juz bierze udział w tym dniu konferencji! .',1
				ROLLBACK TRANSACTION
			END
			FETCH NEXT FROM curs INTO @tmpDay
		END
		CLOSE curs
		DEALLOCATE curs
END
""")

cursor.execute("""
CREATE TRIGGER [dbo].[DwaRazyTenSamaWarsztatLubRezerwacje]
    ON [dbo].[Warsztat_uczestnik]
    AFTER INSERT,UPDATE
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    DECLARE @os_list int = (SELECT  count(WU.idWar) FROM inserted as I
						join Warsztat_uczestnik as WU on WU.idUczest = I.idUczest and WU.idWar = I.idWar
						group by WU.idWar)

	DECLARE @war_list int = (SELECT RW.IDofWar FROM inserted as I
						join Warsztat_uczestnik as WU on WU.idUczest = I.idUczest
						join Rezerwacje_warsztat as RW on WU.idWar = RW.IDRezWar
						where I.idWar != WU.idWar)
	DECLARE @tmpDay int
	IF ((@os_list) != 1)
    BEGIN
        ;THROW 81000,'Ta osoba jest juz przypisana do tej rezerwaji warsztatu.',1
        ROLLBACK TRANSACTION
    END
	 DECLARE curs CURSOR FOR
    (Select RW.IDofWar from inserted as I
	join Rezerwacje_warsztat as RW on I.idWar = RW.IDRezWar)
    OPEN curs
		FETCH NEXT FROM curs INTO @tmpDay
		WHILE @@FETCH_STATUS = 0 BEGIN
			if(@tmpDay in (@war_list))
			BEGIN
				;THROW 82000,'Ta osoba juz bierze udział w tym warsztacie!',1
				ROLLBACK TRANSACTION
			END
			FETCH NEXT FROM curs INTO @tmpDay
		END
		CLOSE curs
		DEALLOCATE curs
END
""")


cursor.execute("""
CREATE TRIGGER [dbo].[IdentyfikatorImienny]
    ON [dbo].Uczestnik
    AFTER INSERT
AS
	if((select identyfikator from inserted) is null)
	BEGIN
	UPDATE [dbo].Uczestnik
    SET identyfikator = UPPER(CONCAT(SUBSTRING((SELECT imie FROM inserted),0,3),SUBSTRING((SELECT nazwisko FROM inserted),0,3)))
	END



""")
conn.commit()

conn.close()
