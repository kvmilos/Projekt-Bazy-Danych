CREATE TABLE Uzytkownicy (
  indeks CHAR(6) UNIQUE NOT NULL,
  haslo TEXT NOT NULL,
  czy_komisja BOOL NOT NULL DEFAULT false,
  imie TEXT NOT NULL,
  nazwisko TEXT NOT NULL,
  PRIMARY KEY (indeks)
);

CREATE TABLE Wybory (
  id INTEGER UNIQUE NOT NULL,
  nazwa TEXT NOT NULL,
  liczba_posad INTEGER NOT NULL,
  termin_zglaszania DATE NOT NULL,
  termin_rozpoczecia DATE NOT NULL,
  termin_zakonczenia DATE NOT NULL,
  czy_opublikowane BOOL NOT NULL DEFAULT false,
  PRIMARY KEY (id)
);

CREATE TABLE Kandydaci (
  indeks CHAR(6) NOT NULL,
  id_wybory INTEGER NOT NULL,
  glosy INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (indeks, id_wybory),
  FOREIGN KEY (indeks) REFERENCES Uzytkownicy (indeks),
  FOREIGN KEY (id_wybory) REFERENCES Wybory (id)
);

CREATE TABLE Glosowanie (
  indeks CHAR(6) NOT NULL,
  id_wybory INTEGER NOT NULL,
  czy_glosowal BOOL NOT NULL DEFAULT false,
  PRIMARY KEY (indeks, id_wybory),
  FOREIGN KEY (indeks) REFERENCES Uzytkownicy (indeks),
  FOREIGN KEY (id_wybory) REFERENCES Wybory (id)
);

INSERT INTO Uzytkownicy VALUES 
('000000', 'KomKomisja2024', 't', 'Komisja', 'Wyborowa'),
('123456', 'test', 'f', 'Adam', 'Testowy'), 
('222222', 'haslo', 'f', 'Jan', 'Kowalski'),
('444444', 'lol', 'f', 'Bartosz', 'Bebecki');

INSERT INTO Wybory VALUES
(1, 'Przewodniczacy SU', 1, '2024-04-01', '2022-04-02', '2022-04-20'),
(2, 'Wiceprzewodniczacy SU', 2, '2024-04-01', '2024-04-02', '2024-04-20'),
(3, 'Rada ds. rownosci', 6, '2024-03-01', '2023-03-02', '2023-03-30'),
(4, 'losowe', 4, '2024-02-01', '2024-02-02', '2024-12-31');