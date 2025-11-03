CREATE DATABASE bobsis;
USE bobsis;

CREATE TABLE Siswa(
	id INT PRIMARY KEY, 
	nim INT, 
	nama VARCHAR(20)
	);
	
CREATE TABLE Matakuliah(
	kodemk CHAR(4) PRIMARY KEY, 
	namamk VARCHAR(20), 
	sks INT
	);
	
CREATE TABLE Enroll(
	tahunajar CHAR(9), 
	periode VARCHAR(8), 
	nilai INT, 
	id INT, 
	kodemk CHAR(4),
	CONSTRAINT fk_enroll_siswa FOREIGN KEY(id) REFERENCES Siswa(id),
	CONSTRAINT fk_enroll_matkul FOREIGN KEY(kodemk) REFERENCES Matakuliah(kodemk)
	);
	
ALTER Table Siswa Add Tgllahir DATE;

INSERT INTO Siswa(id, nim, nama, tgllahir)
VALUES(2,27606,'Michael','2010-01-10'),
	(3,27808,'Budiono','2010-01-15'),
	(4,27995,'Santo','2010-02-10');
	
ALTER TABLE Matakuliah MODIFY COLUMN namamk VARCHAR(40);

INSERT INTO Matakuliah(kodemk, namamk, sks)
VALUES('MK01','Database',2),
	('MK02','ADA',4),
	('MK03','AOP',6),
	('MK04','Basic Statistic',2),
	('MK05','Algorithm and Programming',4);
	
INSERT INTO Enroll VALUES
	('2024/2025','Ganjil',80,2,'MK01'),
	('2024/2025','Ganjil',80,3,'MK01'),
	('2024/2025','Ganjil',70,2,'MK02'),
	('2024/2025','Ganjil',60,2,'MK02'),
	('2024/2025','Genap',70,2,'MK03')
	;
	
--Mengurutkan Data
SELECT * FROM Siswa ORDER BY ID ASC;
SELECT * FROM Siswa ORDER BY ID DESC;

--NATURAL JOIN
SELECT *
FROM Siswa NATURAL JOIN Enroll;

--EQUI JOIN
SELECT *
FROM Siswa JOIN Enroll
	ON Siswa.ID=Enroll.ID;
	
--JOIN LEFT OUTER JOIN
SELECT *
FROM Siswa LEFT OUTER JOIN Enroll
	ON Siswa.ID=Enroll.ID;

--RIGHT JOIN 
SELECT * FROM Enroll RIGHT JOIN Siswa ON Siswa.ID=Enroll.ID;

--SET OPERATION UNION
SELECT kodemk, id 
FROM Enroll WHERE id=2
UNION
SELECT kodemk, id
FROM Enroll WHERE id=3;

SELECT DISTINCT kodemk, id
FROM Enroll WHERE id=3 OR id=2;

--INTERSECT
SELECT kodemk
FROM Enroll WHERE id=2
INTERSECT
SELECT kodemk
FROM Enroll WHERE id=3;

SELECT kodemk
FROM Enroll WHERE id=2 AND id=3;