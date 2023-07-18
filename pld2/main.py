import tkinter as tk
import mysql.connector
import random
from tkinter import messagebox
import veri_tabani as vt
#MYSQL BAĞLANTI
mydb = mysql.connector.connect(
    host="localhost",
    user="enes",
    password="root",
    database="meta_land_6"
)
##############################ALAN OLUŞTURMA BÖLÜMÜ
def create_game_area(x_entry, y_entry):
    x=int(x_entry.get())
    y=int(y_entry.get())
    # Önce alanlar tablosundaki bütün satırları silme
    mycursor = mydb.cursor()
    sql_delete = "DELETE FROM alanlar"
    mycursor.execute(sql_delete)
    mydb.commit()
    emlak_sayisi = 1
    magaza_sayisi = 1
    market_sayisi = 1
    arsa_sayisi = x * y - (emlak_sayisi + magaza_sayisi + market_sayisi)

    alanlar = []
    arsalar = []
    isletmeler = []

    # Emlak ekleme
    for _ in range(emlak_sayisi):
        emlak = "Emlak"
        alanlar.append(emlak)

    # Mağaza ekleme
    for _ in range(magaza_sayisi):
        magaza = "Mağaza"
        alanlar.append(magaza)

    # Market ekleme
    for _ in range(market_sayisi):
        market = "Market"
        alanlar.append(market)

    # Arsa ekleme
    for _ in range(arsa_sayisi):
        arsa = "Arsa"
        alanlar.append(arsa)


    # Alanları karıştırma
    random.shuffle(alanlar)

    # Veritabanına alanları ekleme
    mycursor = mydb.cursor()
    z=1
    c=1
    v=1
    y_gelir=0
    e_gelir=0
    p_gelir=0
    for i in range(x):
        for j in range(y):
            alan_tipi = alanlar[i * y + j]
            sql = "INSERT INTO alanlar (alan_no, alan_x, alan_y, alan_tipi, alan_sahibi,gecici_alan_sahibi) VALUES (%s, %s, %s, %s, %s,%s)"
            val = (z,i, j, alan_tipi, 1,1)  # Burada kullanıcı ID'sini 1 olarak varsaydım, yöneticiye ait olduğunu belirtmek için
            mycursor.execute(sql, val)
            if alan_tipi == "Arsa":
                arsalar.append((c, z, 100,0))
                c +=1
            elif alan_tipi == "Market":
                y_gelir= 100
                p_gelir = 400
                isletmeler.append((v,z,alan_tipi,3,3,3,y_gelir,e_gelir,p_gelir,3000,200))
                v +=1
            elif alan_tipi == "Mağaza":
                e_gelir= 100
                p_gelir = 400
                isletmeler.append((v, z, alan_tipi, 3, 3, 3, y_gelir, e_gelir,p_gelir, 3000, 200))
                v+=1
            elif alan_tipi == "Emlak":
                p_gelir= 500
                isletmeler.append((v, z, alan_tipi, 3, 3, 3, y_gelir, e_gelir,p_gelir, 3000, 200))
                v+=1
            y_gelir = 0
            e_gelir = 0
            z += 1
    # Veritabanına arsaları ekleme
    # print(alanlar)
    # print(arsalar)
    # print(isletmeler)
    sql_arsa = "INSERT INTO arsalar (arsa_no, alan_no, arsa_fiyati,isgal_edildi) VALUES (%s, %s, %s,%s)"
    mycursor.executemany(sql_arsa, arsalar)
    sql_isletme = "INSERT INTO isletmeler (isletme_no, alan_no, isletme_tipi,isletme_seviyesi,isletme_kapasitesi,isletme_calisan_sayisi,market_yiyecek_getirisi,magaza_esya_getirisi,emlak_para_getirisi,isletme_fiyati,kiralik_isletme_fiyati) VALUES (%s, %s, %s,%s,%s, %s, %s,%s,%s, %s,%s)"
    mycursor.executemany(sql_isletme, isletmeler)
    mydb.commit()
    messagebox.showinfo("Başarılı", "Alanlar ve arsalar oluşturuldu!")
##############################

##############################ALAN BOYUTU GİRİŞ EKRANI
def create_area_window():
    # root.withdraw()
    game_window = tk.Toplevel()
    game_window.title("Oyun")
    game_window.geometry("300x200")

    lbl_alan_x = tk.Label(game_window, text="Alan boyutu X:")
    lbl_alan_x.pack()
    entry_alan_x_boyut= tk.Entry(game_window)
    entry_alan_x_boyut.pack()
    lbl_alan_y = tk.Label(game_window, text="Alan boyutu Y:")
    lbl_alan_y.pack()
    entry_alan_y_boyut = tk.Entry(game_window)
    entry_alan_y_boyut.pack()
    btn_area = tk.Button(game_window, text="Alan Oluştur", command=lambda:create_game_area(entry_alan_x_boyut,entry_alan_y_boyut))
    btn_area.pack()
    btn_game_kapa = tk.Button(game_window, text="Çıkış Yap",command=lambda:game_window.destroy())
    btn_game_kapa.pack()
    lbl_estate = tk.Label(game_window, text="")
    lbl_estate.pack()
    game_window.mainloop()
##############################
# def game_window_kapa():
#     game_window.destroy()
#     root.deiconify()
##############################YÖNETİCİ GİRİŞ EKRANI
def yonetici_gir():
    # root.withdraw()
    game_window1 = tk.Toplevel(root)
    game_window1.title("Oyun")
    game_window1.geometry("300x200")

    lbl_kullanici_adi = tk.Label(game_window1, text="Yönetici Adı:")
    lbl_kullanici_adi.pack()
    entry_kullanici_adi = tk.Entry(game_window1)
    entry_kullanici_adi.pack()

    lbl_password = tk.Label(game_window1, text="Parola:")
    lbl_password.pack()
    entry_kullanici_sifresi = tk.Entry(game_window1, show="*")
    entry_kullanici_sifresi.pack()

    btn_login = tk.Button(game_window1, text="Giriş Yap", command=lambda: login(entry_kullanici_adi, entry_kullanici_sifresi))
    btn_login.pack()
    btn_cikis_yap = tk.Button(game_window1, text="Çıkış Yap", command=lambda:game_window1.destroy())
    btn_cikis_yap.pack()
##############################

##############################YÖNETİCİ GİRİŞ KONTROLÜ
def login(entry_kullanici_adi, entry_kullanici_sifresi):
    kullanici_adi = entry_kullanici_adi.get()
    kullanici_sifresi = entry_kullanici_sifresi.get()
    mycursor = mydb.cursor()
    sql = "SELECT * FROM kullanicilar WHERE kullanici_adi = %s AND kullanici_sifresi = %s"
    val = (kullanici_adi, kullanici_sifresi)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    # print(kullanici_adi,kullanici_sifresi,result[1],result[3])
    if result:
        if result[1] == kullanici_adi: # isAdmin
            if result[3] == kullanici_sifresi:
                messagebox.showinfo("Başarılı", "Yönetici girişi yaptınız!")
                create_area_window()
    else:
        messagebox.showerror("Hata", "Hatalı kullanıcı adı veya şifre!")
##############################
##############################KULLANICI GİRİŞ EKRANI
def kullanici_gir():
    # root.withdraw()
    game_window1 = tk.Toplevel(root)
    game_window1.title("Oyun")
    game_window1.geometry("300x200")

    lbl_kullanici_adi = tk.Label(game_window1, text="Kullanıcı Adı:")
    lbl_kullanici_adi.pack()
    entry_kullanici_adi = tk.Entry(game_window1)
    entry_kullanici_adi.pack()

    lbl_password = tk.Label(game_window1, text="Parola:")
    lbl_password.pack()
    entry_kullanici_sifresi = tk.Entry(game_window1, show="*")
    entry_kullanici_sifresi.pack()

    btn_login = tk.Button(game_window1, text="Giriş Yap", command=lambda: login1(entry_kullanici_adi, entry_kullanici_sifresi))
    btn_login.pack()
    btn_cikis_yap = tk.Button(game_window1, text="Çıkış Yap", command=lambda:game_window1.destroy())
    btn_cikis_yap.pack()
##############################
##############################KULLANICI GİRİŞ KONTROLÜ
def login1(entry_kullanici_adi, entry_kullanici_sifresi):
    kullanici_adi = entry_kullanici_adi.get()
    kullanici_sifresi = entry_kullanici_sifresi.get()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM kullanicilar")
    results = mycursor.fetchall()
    for result in results:
        if result:
            if result[1] == kullanici_adi: # isKullanici
                if result[3] == kullanici_sifresi:
                    messagebox.showinfo("Başarılı", "Kullanıcı girişi yaptınız!")
                    global oyuncu_id
                    oyuncu_id = result[0]
                    print(oyuncu_id)
                    oyun()
        else:
            messagebox.showerror("Hata", "Hatalı kullanıcı adı veya şifre!")
##############################
############################## YÖNETİCİ EKLE
def add_yonetici():

    kullanici_adi = 'admin'
    kullanici_soyadi = 'admin'
    kullanici_sifresi = '123'
    kullanici_yemek_miktari = 1000
    kullanici_esya_miktari = 1000
    kullanici_para_miktari = 1000
    calisan_mi = 0
    mycursor = mydb.cursor()
    sql_delete = "DELETE FROM alanlar"
    mycursor.execute(sql_delete)
    sql_delete = "DELETE FROM kullanicilar"
    mycursor.execute(sql_delete)
    sql = "INSERT INTO kullanicilar (kullanici_adi, kullanici_soyadi, kullanici_sifresi, kullanici_yemek_miktari, kullanici_esya_miktari, kullanici_para_miktari,calisan_mi,game_over) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s)"
    val = (kullanici_adi, kullanici_soyadi, kullanici_sifresi, kullanici_yemek_miktari, kullanici_esya_miktari, kullanici_para_miktari,calisan_mi,0)
    mycursor.execute(sql, val)
    mydb.commit()
##############################
##############################Kullanıcı ekleme ekranı
def add_kullanici():
    def kayit_yap():
        kullanici_yemek_miktari = 200
        kullanici_esya_miktari = 200
        kullanici_para_miktari = 200
        kullanici_adi = entry_kullanici_adi.get()
        kullanici_soyadi = entry_kullanici_soyadi.get()
        kullanici_sifresi = entry_kullanici_sifresi.get()
        calisan_mi=0
        if not kullanici_adi or not kullanici_soyadi or not kullanici_sifresi:
            messagebox.showwarning("Hata", "Kullanıcı adı ve şifre alanları boş olamaz!")
            return

        try:
            mycursor = mydb.cursor()
            sql = "INSERT INTO kullanicilar (kullanici_adi, kullanici_soyadi, kullanici_sifresi, kullanici_yemek_miktari, kullanici_esya_miktari, kullanici_para_miktari,calisan_mi,game_over) " \
                  "VALUES (%s, %s, %s, %s, %s, %s,%s,%s) "
            val = (kullanici_adi, kullanici_soyadi, kullanici_sifresi, kullanici_yemek_miktari, kullanici_esya_miktari, kullanici_para_miktari,calisan_mi,0)
            mycursor.execute(sql, val)
            mydb.commit()

            messagebox.showinfo("Başarılı", "Kullanıcı başarıyla eklendi!")

            entry_kullanici_adi.delete(0, tk.END)
            entry_kullanici_soyadi.delete(0, tk.END)
            entry_kullanici_sifresi.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Hata", "Kullanıcı eklenirken bir hata oluştu:\n{}".format(err))

    # root.withdraw()
    global game_window1
    global oyuncu_id
    oyuncu_id=0
    game_window1 = tk.Toplevel(root)
    game_window1.title("Kullanıcı Kayıt")
    game_window1.geometry("300x200")
    lbl_kullanici_adi = tk.Label(game_window1, text="Kullanıcı Adı:")
    lbl_kullanici_adi.pack()
    entry_kullanici_adi = tk.Entry(game_window1)
    entry_kullanici_adi.pack()
    lbl_kullanici_soyadi = tk.Label(game_window1, text="Kullanıcı Soyadı:")
    lbl_kullanici_soyadi.pack()
    entry_kullanici_soyadi = tk.Entry(game_window1)
    entry_kullanici_soyadi.pack()
    lbl_password = tk.Label(game_window1, text="Parola:")
    lbl_password.pack()
    entry_kullanici_sifresi = tk.Entry(game_window1, show="*")
    entry_kullanici_sifresi.pack()
    btn_kayit_yap = tk.Button(game_window1, text="Kayıt Yap", command=kayit_yap)
    btn_kayit_yap.pack()
    btn_cikis_yap = tk.Button(game_window1, text="Çıkış Yap", command=game_window1.withdraw)
    btn_cikis_yap.pack()
    game_window1.mainloop()
##############################

##############################
# def game_window1_kapa():
#     game_window1.destroy()
#     root.deiconify()
##############################

##############################Reset kullanıcı
# def reset_tables():
#     try:
#         mycursor = mydb.cursor()
#         tables = ["alanlar", "kullanicilar", "arsalar", "isletmeler","emlak_islemleri","isletme_gelir_gider","isletme_calisma_saati"]
#         for table in tables:
#             sql = f"DELETE FROM {table}"
#             mycursor.execute(sql)
#         mydb.commit()
#         print("Tablolar sıfırlandı.")
#     except mysql.connector.Error as error:
#         print("Hata oluştu:", error)
##############################
# reset_tables()

##############################
def oyun():
    mycursor = mydb.cursor()

    # Alanlar tablosundan verileri çek
    mycursor.execute("SELECT * FROM alanlar")
    alanlar = mycursor.fetchall()
    global gun
    # Oyun alanı oluştur
    game_window = tk.Tk()
    game_window.title("Gün " + str(gun))
    game_window.geometry("1280x720")
    def ise_gir():
        global son_tiklanan_alan,oyuncu_id,a # son tıklanan alanda işe girmesine sağlamalıyım XXXXXXXXXXXXXXXXXXXX
        mycursor.execute("SELECT calisan_mi FROM kullanicilar WHERE kullanici_no = %s",(oyuncu_id,))
        calisan_mi = mycursor.fetchone()
        mycursor.execute("SELECT isletme_no FROM isletmeler WHERE alan_no = %s",(son_tiklanan_alan,))
        isletme_no = mycursor.fetchone()
        print(isletme_no)
        print(isletme_no[0])
        print(calisan_mi[0])
        if not calisan_mi[0]:
            sql = "INSERT INTO calisanlar (kullanici_no, calisiyor_mu, calisma_gunu,isletme_no) VALUES (%s, %s, %s, %s)"
            val = (oyuncu_id, 1, 1,isletme_no[0])
            mycursor.execute(sql, val)
            mydb.commit()
            sql = "UPDATE kullanicilar SET calisan_mi = TRUE WHERE kullanici_no = %s"
            val = (oyuncu_id,)
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.execute("SELECT isletme_tipi FROM isletmeler WHERE isletme_no = %s",(isletme_no[0],))
            isletme_adi = mycursor.fetchone()
            isletme_adi_1 = isletme_adi[0].capitalize()
            messagebox.showinfo("Tebrikler", f"{isletme_adi_1} işine girdiniz")
        else:
            messagebox.showerror("Hata","Aynı andan birden fazla yerde çalışamazsınız")

    def yemek_al():
        global oyuncu_id
        print(oyuncu_id)
        sql = "SELECT * FROM kullanicilar WHERE kullanici_no = %s"
        val = (oyuncu_id,)
        mycursor.execute(sql, val)
        oyuncu = mycursor.fetchone()
        if oyuncu[6] > 50:
            sql = "UPDATE kullanicilar SET kullanici_para_miktari = kullanici_para_miktari - 25 WHERE kullanici_no = %s"
            val = (oyuncu_id,)
            mycursor.execute(sql, val)
            mydb.commit()
            sql = "UPDATE kullanicilar SET kullanici_yemek_miktari = kullanici_yemek_miktari + 50 WHERE kullanici_no = %s"
            val = (oyuncu_id,)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("YEMEK","50 Yemek aldınız")
        else:
            messagebox.showerror("Hata","Yemek almak için yeterli paranız yok.")

    def esya_al():
        global oyuncu_id
        sql = "SELECT * FROM kullanicilar WHERE kullanici_no = %s"
        val = (oyuncu_id,)
        mycursor.execute(sql, val)
        oyuncu = mycursor.fetchone()
        if oyuncu[6] > 50:
            sql = "UPDATE kullanicilar SET kullanici_para_miktari = kullanici_para_miktari - 25 WHERE kullanici_no = %s"
            val = (oyuncu_id,)
            mycursor.execute(sql, val)
            mydb.commit()
            sql = "UPDATE kullanicilar SET kullanici_esya_miktari = kullanici_esya_miktari + 50 WHERE kullanici_no = %s"
            val = (oyuncu_id,)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("EŞYA", "50 Eşya aldınız")
        else:
            messagebox.showerror("Hata","Eşya almak için yeterli paranız yok.")

    def gun_bitir():
        global gun, oyuncu_id
        print("Biten gün",gun)
        messagebox.showinfo("bitti","Gun bitti")
        gun += 1
        print("Başlayan Gün", gun)
        mycursor.execute("SELECT * FROM isletmeler")
        result = mycursor.fetchall()
        for i in result:
            sql = "SELECT gecici_alan_sahibi FROM alanlar WHERE alan_no = %s"
            val = (i[1],)
            mycursor.execute(sql, val)
            gecici_alan_sahibi = mycursor.fetchone()
            alan_sahibi = gecici_alan_sahibi[0]
            print(alan_sahibi)
            y_getiri = i[6]
            e_getiri = i[7]
            p_getiri = i[8]
            sql = "UPDATE kullanicilar SET kullanici_yemek_miktari = kullanici_yemek_miktari + %s WHERE kullanici_no = %s"
            val = (y_getiri, alan_sahibi)
            mycursor.execute(sql, val)
            mydb.commit()
            sql = "UPDATE kullanicilar SET kullanici_esya_miktari = kullanici_esya_miktari + %s WHERE kullanici_no = %s"
            val = (e_getiri, alan_sahibi)
            mycursor.execute(sql, val)
            mydb.commit()
            sql = "UPDATE kullanicilar SET kullanici_para_miktari = kullanici_para_miktari + %s WHERE kullanici_no = %s"
            val = (p_getiri, alan_sahibi)
            mycursor.execute(sql, val)
            mydb.commit()
        mycursor.execute("SELECT * FROM calisanlar")
        result_1 = mycursor.fetchall()
        for i in result_1:
            if i[2]:
                sql = "SELECT * FROM isletmeler WHERE isletme_no = %s"
                val = (i[4],)
                mycursor.execute(sql, val)
                isletme = mycursor.fetchone()
                y_getiri = int(isletme[6] / 10)
                e_getiri = int(isletme[7] / 10)
                p_getiri = int(isletme[8] / 10)
                sql = "UPDATE kullanicilar SET kullanici_yemek_miktari = kullanici_yemek_miktari + %s WHERE kullanici_no = %s"
                val = (y_getiri, i[1])
                print(y_getiri, i[1])
                mycursor.execute(sql, val)
                mydb.commit()
                sql = "UPDATE kullanicilar SET kullanici_esya_miktari = kullanici_esya_miktari + %s WHERE kullanici_no = %s"
                val = (e_getiri, i[1])
                print(e_getiri, i[1])
                mycursor.execute(sql, val)
                mydb.commit()
                sql = "UPDATE kullanicilar SET kullanici_para_miktari = kullanici_para_miktari + %s WHERE kullanici_no = %s"
                val = (p_getiri, i[1])
                print(p_getiri, i[1])
                mycursor.execute(sql, val)
                mydb.commit()


        mycursor.execute("UPDATE kullanicilar SET kullanici_para_miktari = kullanici_para_miktari - 25")
        mydb.commit()
        mycursor.execute("UPDATE kullanicilar SET kullanici_yemek_miktari = kullanici_yemek_miktari - 25")
        mydb.commit()
        mycursor.execute("UPDATE kullanicilar SET kullanici_esya_miktari = kullanici_esya_miktari - 25")
        mydb.commit()
        mycursor.execute("UPDATE kullanicilar SET game_over = TRUE WHERE kullanici_para_miktari <= 0")
        mydb.commit()
        mycursor.execute("UPDATE kullanicilar SET game_over = TRUE WHERE kullanici_yemek_miktari <= 0")
        mydb.commit()
        mycursor.execute("UPDATE kullanicilar SET game_over = TRUE WHERE kullanici_esya_miktari <= 0")
        mydb.commit()
        mycursor.execute("SELECT kullanici_no FROM kullanicilar WHERE game_over = TRUE")
        result = mycursor.fetchall()
        for i in result:
            kullanici_id = i[0]
            messagebox.showinfo("Game Over", f"{kullanici_id} numaralı oyuncu kaybetti")
            if kullanici_id == oyuncu_id:
                messagebox.showerror("Game Over","Kaybettiniz!")
                messagebox.showwarning("Yeniden başla","Oyuna yeniden başlamak için oyunu kapatıp açınız")
                game_window.destroy()
            sql = "DELETE FROM kullanicilar WHERE kullanici_no = %s"
            val = (kullanici_id,)
            mycursor.execute(sql, val)
            mydb.commit()
        game_window.destroy()
        oyun()
    def satin_al():
        global son_tiklanan_alan
        alan_no=son_tiklanan_alan
        sql = "SELECT * FROM alanlar WHERE alan_no = %s"
        val = (alan_no,)
        mycursor.execute(sql, val)
        alan = mycursor.fetchone()
        # print("alan_no",alan_no)
        # print("oyuncu_id",oyuncu_id)
        # print("Alan sahibi",alan[4])
        if oyuncu_id != alan[4]:
            if alan[3]== "arsa":
                sql = "SELECT * FROM arsalar WHERE alan_no = %s"
                val = (alan_no,)
                mycursor.execute(sql, val)
                arsa = mycursor.fetchone()
                arsa_fiyati = arsa[2]
                sql = "SELECT * FROM kullanicilar WHERE kullanici_no = %s"
                val = (oyuncu_id,)
                mycursor.execute(sql, val)
                oyuncu = mycursor.fetchone()
                oyuncu_para=oyuncu[6]
                if oyuncu_para > arsa_fiyati:
                    sql = "SELECT * FROM kullanicilar WHERE kullanici_no = %s"
                    val = (alan[4],)
                    mycursor.execute(sql, val)
                    sahip = mycursor.fetchone()
                    sahip_para = sahip[6]
                    sahip_para = sahip_para + arsa_fiyati
                    sql = "UPDATE kullanicilar SET kullanici_para_miktari = %s WHERE kullanici_no = %s"
                    val = (sahip_para, sahip[0])
                    mycursor.execute(sql, val)
                    mydb.commit()
                    sql = "UPDATE alanlar SET alan_sahibi = %s WHERE alan_no = %s"
                    val = (oyuncu_id, alan_no)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    oyuncu_para=oyuncu_para-arsa_fiyati
                    sql = "UPDATE kullanicilar SET kullanici_para_miktari = %s WHERE kullanici_no = %s"
                    val = (oyuncu_para, oyuncu_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    messagebox.showinfo("Başarılı","Satın alım gerçekleşmiştir.")
                else:
                    messagebox.showerror("Hata","Yeterli paranız yok!")
            else:
                sql = "SELECT * FROM isletmeler WHERE alan_no = %s"
                val = (alan_no,)
                mycursor.execute(sql, val)
                isletme = mycursor.fetchone()
                isletme_fiyati = isletme[8]
                sql = "SELECT * FROM kullanicilar WHERE kullanici_no = %s"
                val = (alan[4],)
                mycursor.execute(sql, val)
                sahip = mycursor.fetchone()
                sahip_para = sahip[6]
                sahip_para = sahip_para + isletme[8]
                sql = "UPDATE kullanicilar SET kullanici_para_miktari = %s WHERE kullanici_no = %s"
                val = (sahip_para, sahip[0])
                mycursor.execute(sql, val)
                mydb.commit()
                sql = "SELECT * FROM kullanicilar WHERE kullanici_no = %s"
                val = (oyuncu_id,)
                mycursor.execute(sql, val)
                oyuncu = mycursor.fetchone()
                oyuncu_para = oyuncu[6]
                if oyuncu_para > isletme_fiyati:
                    sql = "UPDATE alanlar SET alan_sahibi = %s WHERE alan_no = %s"
                    val = (oyuncu_id, alan_no)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    oyuncu_para = oyuncu_para - isletme_fiyati
                    sql = "UPDATE kullanicilar SET kullanici_para_miktari = %s WHERE kullanici_no = %s"
                    val = (oyuncu_para, oyuncu_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    messagebox.showinfo("Başarılı", "Satın alım gerçekleşmiştir.")
                else:
                    messagebox.showerror("Hata", "Yeterli paranız yok!")
        else:
            messagebox.showerror("Hata","Alan zaten sizin!")

    def kullanici_yaz():
        mycursor.execute("SELECT * FROM kullanicilar")
        kullanicilar = mycursor.fetchall()
        for i, kullanici in enumerate(kullanicilar):
            kullanici_str = f"Kullanıcı: {kullanici[1]} {kullanici[2]}\n Kullanici yemek: {kullanici[4]}\nKullanici eşya: {kullanici[5]}\nKullanici para: {kullanici[6]}"
            label = tk.Label(game_window, text=kullanici_str)
            label.grid(row=i, column=100)

    def alan_tiklandi(alan_no, alan_tipi, frame):
        # Veritabanından ilgili alanın verilerini çek
        frame.configure(relief="sunken")
        frame.after(100, lambda: frame.configure(relief="raised"))
        alan_2 = alan_tipi
        arsa = []
        isletme = []
        sql = "SELECT * FROM alanlar WHERE alan_no = %s"
        val = (alan_no,)
        mycursor.execute(sql, val)
        alan = mycursor.fetchone()
        message = "Alan no: " + str(alan[0]) + "\n" + "Alan x: " + str(alan[1]) + "\n" + "Alan y: " + str(alan[2]) + "\n" + "Alan tipi: " + str(alan[3]) + "\n" + "Alan sahibi: " + str(alan[4])
        messagebox.showinfo("Bilgiler",message)
        global son_tiklanan_alan
        son_tiklanan_alan=alan_no
        # if alan_2 == "arsa":
        #     sql = "SELECT * FROM arsalar WHERE alan_no = %s"
        #     val = (alan_no,)
        #     mycursor.execute(sql, val)
        #     arsa = mycursor.fetchone()
        # else:
        #     sql = "SELECT * FROM isletmeler WHERE alan_no = %s"
        #     val = (alan_no,)
        #     mycursor.execute(sql, val)
        #     isletme = mycursor.fetchone()

        # # Alanın verilerini yansıt
        # if alan:
        #     print("Alan Tipi:", alan[3])
        #     print("Alan Sahibi:", alan[4])
        #     print(alan)
        #     if isletme:
        #         print(isletme)
        #     elif arsa:
        #         print(arsa)
        # else:
        #     print("Alan bulunamadı")

    for i in range(len(alanlar)):
        alan_no = alanlar[i][0]
        alan = alanlar[i][3]

        # Alan türüne göre renk belirle
        if alan == "arsa":
            color = "green"
        elif alan == "emlak":
            color = "white"
        elif alan == "magaza":
            color = "blue"
        elif alan == "market":
            color = "red"

        # Grid tablosunda renkli kareler oluştur
        frame = tk.Frame(game_window, width=100, height=100, relief="raised", bd=1)
        frame.grid(row=alanlar[i][2], column=alanlar[i][1])
        frame.configure(bg=color)
        frame.bind("<Button-1>", lambda event, alan_no=alan_no, alan_tipi=alan,frame=frame: alan_tiklandi(alan_no, alan_tipi, frame))

    btn_satin_al = tk.Button(game_window, text="Satın Alım Yap", command=satin_al)
    btn_satin_al.grid(row=200, column=200)
    btn_satin_al = tk.Button(game_window, text="Gün bitir", command=gun_bitir)
    btn_satin_al.grid(row=210, column=200)
    btn_esya_al = tk.Button(game_window, text="Eşya Al", command=esya_al)
    btn_esya_al.grid(row=200, column=220)
    btn_yemek_al = tk.Button(game_window, text="Yemek Al", command=yemek_al)
    btn_yemek_al.grid(row=210, column=220)
    btn_ise_gir = tk.Button(game_window, text="İşe gir", command=ise_gir)
    btn_ise_gir.grid(row=200, column=240)
    kullanici_yaz()
    game_window.mainloop()


##############################

##############################Oyunun ana ekranı
global a # döngü için
a=0
add_yonetici()
root = tk.Tk()
root.title("Giriş Ekranı")
root.geometry("300x200")
# btn_login = tk.Button(root, text="Kullanıcı Giriş", command=yonetici_gir)
# btn_login.pack()
btn2_login = tk.Button(root, text="Alan boyutu giriş", command=yonetici_gir)
btn2_login.pack()
btn3_signin = tk.Button(root, text="Kullanıcı kayıt", command=add_kullanici)
btn3_signin.pack()
btn4_basla = tk.Button(root, text="Oyunu başlat", command=kullanici_gir)
btn4_basla.pack()
gun = 1
lbl_error = tk.Label(root, text="", fg="red")
lbl_error.pack()

root.mainloop()
##############################

