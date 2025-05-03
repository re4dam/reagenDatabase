-- Tabel Storage: Menyimpan informasi lokasi penyimpanan
CREATE TABLE Storage (
    id     INTEGER PRIMARY KEY,
    Name   TEXT,
    Level  INTEGER
);

-- Tabel Identity: Identitas lengkap bahan/reagen yang tersimpan
CREATE TABLE Identity (
    id                INTEGER PRIMARY KEY,
    Name              TEXT,
    Description       TEXT,
    Wujud             TEXT,
    Stock             INTEGER,
    Massa             INTEGER,
    Tanggal_Expire    DATE,
    Category_Hazard   TEXT,
    Sifat             TEXT,
    Tanggal_Produksi  DATE,
    Tanggal_Pembelian DATE,
    SDS               TEXT,
    id_storage        INTEGER,
    FOREIGN KEY (id_storage) REFERENCES Storage(id)
);

-- Tabel Usage: Mencatat penggunaan bahan/reagen
CREATE TABLE Usage (
    id               INTEGER PRIMARY KEY,
    Tanggal_Terpakai DATE,
    Jumlah_Terpakai  INTEGER,
    User             TEXT,
    Bahan_Pendukung  TEXT,
    id_identity      INTEGER,
    FOREIGN KEY (id_identity) REFERENCES Identity(id)
);
