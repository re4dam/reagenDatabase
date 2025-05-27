-- Create main reagent table
CREATE TABLE IF NOT EXISTS Identity_new (
    id INTEGER PRIMARY KEY,
    Name TEXT,
    Description TEXT,
    Wujud TEXT,
    Stock INTEGER,
    Massa INTEGER,
    Tanggal_Expire DATE,
    Category_Hazard TEXT,
    Sifat TEXT,
    Tanggal_Produksi DATE,
    Tanggal_Pembelian DATE,
    SDS BLOB,              -- Stores the actual PDF binary
    SDS_Filename TEXT,     -- Stores the original filename of the SDS
    id_storage INTEGER,
    Image BLOB,            -- Stores image (e.g. PNG/JPG) in binary
    FOREIGN KEY (id_storage) REFERENCES Storage(id)
);

INSERT INTO Identity_new (id, Name, Description, Wujud, Stock, Massa, Tanggal_Expire, Category_Hazard, Sifat, Tanggal_Produksi, Tanggal_Pembelian, id_storage, Image)
SELECT id, Name, Description, Wujud, Stock, Massa, Tanggal_Expire, Category_Hazard, Sifat, Tanggal_Produksi, Tanggal_Pembelian, id_storage, Image FROM Identity;

DROP TABLE Identity;
ALTER TABLE Identity_new RENAME TO Identity;
