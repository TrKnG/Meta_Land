import mysql.connector

# Veritabanı bağlantısını kur
mydb = mysql.connector.connect(
    host="localhost",
    user="enes",
    password="root"
)
mycursor = mydb.cursor()

# Veritabanını sil
mycursor.execute("DROP DATABASE IF EXISTS meta_land_6")

# print("meta_land_6 veritabanı silindi.")

# Veritabanını oluştur
mycursor.execute("CREATE DATABASE IF NOT EXISTS meta_land_6")
mycursor.execute("USE meta_land_6")

# Tabloları oluştur
sql_script = """
CREATE TABLE IF NOT EXISTS kullanicilar (
    kullanici_no INT PRIMARY KEY AUTO_INCREMENT,
    kullanici_adi VARCHAR(255) NOT NULL,
    kullanici_soyadi VARCHAR(255) NOT NULL,
    kullanici_sifresi VARCHAR(255) NOT NULL,
    kullanici_yemek_miktari INT NOT NULL DEFAULT 0,
    kullanici_esya_miktari INT NOT NULL DEFAULT 0,
    kullanici_para_miktari INT NOT NULL DEFAULT 0,
    calisan_mi INT NOT NULL DEFAULT 0,
    game_over BOOLEAN DEFAULT FALSE,
    UNIQUE(kullanici_adi)
);
CREATE TABLE IF NOT EXISTS alanlar (
    alan_no INT PRIMARY KEY AUTO_INCREMENT,
    alan_x INT NOT NULL,
    alan_y INT NOT NULL,
    alan_tipi ENUM('arsa', 'market', 'magaza','emlak') NOT NULL,
    alan_sahibi INT,
    gecici_alan_sahibi INT NOT NULL,
    FOREIGN KEY (alan_sahibi) REFERENCES kullanicilar(kullanici_no)
);
ALTER TABLE alanlar ADD CONSTRAINT alan_unicity UNIQUE (alan_x, alan_y);

CREATE TABLE IF NOT EXISTS arsalar (
    arsa_no INT PRIMARY KEY AUTO_INCREMENT,
    alan_no INT NOT NULL,
    arsa_fiyati INT NOT NULL DEFAULT 0,
    isgal_edildi BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (alan_no) REFERENCES alanlar(alan_no)
);

CREATE TABLE IF NOT EXISTS isletmeler (
    isletme_no INT PRIMARY KEY AUTO_INCREMENT,
    alan_no INT NOT NULL,
    isletme_tipi ENUM('market', 'magaza','emlak') NOT NULL,
    isletme_seviyesi INT NOT NULL DEFAULT 0,
    isletme_kapasitesi INT NOT NULL DEFAULT 0,
    isletme_calisan_sayisi INT NOT NULL DEFAULT 0,
    market_yiyecek_getirisi INT NOT NULL DEFAULT 0,
    magaza_esya_getirisi INT NOT NULL DEFAULT 0,
    emlak_para_getirisi INT NOT NULL DEFAULT 0,
    isletme_fiyati INT NOT NULL DEFAULT 0,
    kiralik_isletme_fiyati INT NOT NULL DEFAULT 0,
    FOREIGN KEY (alan_no) REFERENCES alanlar(alan_no)
);
CREATE TABLE IF NOT EXISTS emlak_islemleri (
    islem_no INT PRIMARY KEY AUTO_INCREMENT,
    islem_tipi ENUM('kiralama', 'satis') NOT NULL,
    isletme_no INT,
    alan_no INT,
    kiralama_tarihi INT NOT NULL,
    kira_bitis_tarihi INT NOT NULL,
    satis_tarihi INT NOT NULL,
    komisyon_orani FLOAT NOT NULL DEFAULT 0.0,
    FOREIGN KEY (isletme_no) REFERENCES isletmeler(isletme_no),
    FOREIGN KEY (alan_no) REFERENCES alanlar(alan_no)
);
CREATE TABLE IF NOT EXISTS calisanlar (
    calisan_no INT PRIMARY KEY AUTO_INCREMENT,
    kullanici_no INT,
    calisiyor_mu BOOLEAN DEFAULT FALSE,
    calisma_gunu INT,
    isletme_no INT,
    FOREIGN KEY (kullanici_no) REFERENCES kullanicilar(kullanici_no),
    FOREIGN KEY (isletme_no) REFERENCES isletmeler(isletme_no)
);

CREATE TABLE IF NOT EXISTS isletme_gelir_gider (
    kayit_no INT PRIMARY KEY AUTO_INCREMENT,
    isletme_no INT NOT NULL,
    tarih DATE NOT NULL,
    gelir_miktari INT NOT NULL DEFAULT 0,
    gider_miktari INT NOT NULL DEFAULT 0,
    FOREIGN KEY (isletme_no) REFERENCES isletmeler(isletme_no)
);
CREATE TABLE IF NOT EXISTS isletme_calısan (
    kayit_no INT PRIMARY KEY AUTO_INCREMENT,
    kullanici_no INT NOT NULL,
    tarih DATE NOT NULL,
    verilen_maas INT NOT NULL DEFAULT 0,
    verilen_esya INT NOT NULL DEFAULT 0,
    verilen_yemek INT NOT NULL DEFAULT 0,
    isletme_no INT NOT NULL,
    FOREIGN KEY (isletme_no) REFERENCES isletmeler(isletme_no)
);
CREATE TABLE IF NOT EXISTS isletme_calisma_saati (
    isletme_no INT NOT NULL,
    gun ENUM('Pazartesi', 'Sali', 'Carsamba', 'Persembe', 'Cuma', 'Cumartesi', 'Pazar') NOT NULL,
    calisma_baslangic_saati TIME NOT NULL,
    calisma_bitis_saati TIME NOT NULL,
    PRIMARY KEY (isletme_no, gun),
    FOREIGN KEY (isletme_no) REFERENCES isletmeler(isletme_no)
);
"""
mycursor.execute(sql_script)

# print("meta_land_6 veritabanı ve tabloları başarıyla oluşturuldu.")