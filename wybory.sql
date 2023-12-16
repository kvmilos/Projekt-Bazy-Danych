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