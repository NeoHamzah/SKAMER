import psycopg2 
from tabulate import tabulate as tb
import os
from datetime import datetime, timedelta
import time
import functools

# CONNECT
def connect():
    global con
    con = psycopg2.connect(
    database="sewaKamera",
    user="postgres",
    password="admin",
    host="localhost",
    port= '5434'
    )

def loginAdmin():
    os.system('cls')
    connect()
    admin_obj = con.cursor()
    admin_obj.execute('SELECT username_admin, password_admin from admin')
    admin = admin_obj.fetchall()
    listAdmin = []
    for i in admin:
        i_list = list(i)
        listAdmin.append(i_list)
    print("------------------------------------------------------------------------")
    print("|                  SELAMAT DATANG DI LOGIN ADMIN                       |")
    print("------------------------------------------------------------------------")
    time.sleep(3)
    username = input("\nMasukkan Username anda: ")
    password = input("Masukkan Password Anda: ")
    def check():
        for i in listAdmin:
            if username != i[0]:
                continue
            elif username == i[0] and password != i[1]:
                print("\nPassword Salah!\n")
                print()
                input("Tekan Enter Untuk Coba Lagi")
                loginAdmin()
                return 1
            elif username == i[0] and password == i[1]:
                kata = "Login Sukses"
                kata2 = "Loading..."
                for i in range(0,101):
                    print("\r{0}{1}%".format(kata2,i),end="")
                    time.sleep(0.005)
                print(kata)
                return 1
    cek = check()
    if cek != 1:
        print("Login Gagal")
        for i in range(3):
            print(".")
            time.sleep(1)
        os.system('cls')
        loginAdmin()

def createPemesanan():
    connect()    
    def totalPesanan():
        global layanan
        global barangTotal
        global pilLayanan
        global pilBarang
        
        listPesanan = []
        
        lagi = 'y'
        while lagi == 'y':
            headerLayanan = ["Nomor", "Nama Layanan"]
            layanan_obj = con.cursor()
            layanan_obj.execute('SELECT id_layanan, nama_layanan from layanan order by id_layanan')
            layanan = layanan_obj.fetchall()
            print(tb(layanan, headers=headerLayanan, tablefmt="fancy_grid"))
            pilLayanan = int(input("Silahkan pilih layanan: "))
            print()
            
            headerBarang = ["ID Barang", "Nama Barang", "Harga Sewa per Hari", "Status Barang"]
            barang_obj = con.cursor()
            barang_obj.execute(f'SELECT id_barang, nama_barang, harga_sewa, status_barang from barang where layanan_id = {pilLayanan} order by id_barang')
            barang = barang_obj.fetchall()
            barangTotal_obj = con.cursor()
            barangTotal_obj.execute(f'SELECT id_barang, nama_barang, harga_sewa, status_barang from barang order by id_barang')
            barangTotal = barangTotal_obj.fetchall()
            print(tb(barang, headers = headerBarang, tablefmt="fancy_grid"))
            pilBarang = int(input("Silahkan masukkan ID Barang yang akan disewa: "))
            listPesanan.append(pilBarang)
            print()
            lagi = input("Apakah ingin memilih barang lagi? [y/n]: ")
        
        return listPesanan

    pesanan = totalPesanan()
    
    durasi_sewa = int(input("Masukkan lama pemesanan [hari]: "))
    
    tglSewa = input("Masukkan tanggal pemesanan [dd/mm/yyyy, misal: 07/12/2023]: ")
    tgl_format = datetime.strptime(f"{tglSewa}", "%d/%m/%Y")
    tgl_formatt = tgl_format.date()
    
    tglKembali = (tgl_format + timedelta(hours=durasi_sewa*24)).strftime('%d/%m/%Y')
    
    nama_pemesan = input("Masukkan nama pemesan: ")
    
    detail_pesanan_harga = [barangTotal[x-1][2] for x in pesanan]
    detail_pesanan_nama = [barangTotal[x-1][1] for x in pesanan]
    
    hitung_pesanan = functools.reduce(lambda x, y: x + y, detail_pesanan_harga)

    def biaya(harga_per_hari, hari):
        return 0 if hari == 0 else biaya(hari - 1, harga_per_hari) + harga_per_hari
    
    biaya_akhir = biaya
    
    for i in pesanan:
        pesanann_obj = con.cursor()
        pesanann_obj.execute(f"SELECT * from barang where id_barang = {i} and status_barang = 'tidak tersedia'")
        pesanann = pesanann_obj.fetchall()
    if pesanann == []:
        for i , j in zip(pesanan, detail_pesanan_harga):
            create_obj = con.cursor()
            queryCreate = f"INSERT INTO pemesanan (nama_pemesan, barang_id, durasi_sewa, tanggal_sewa, tanggal_kembali, biaya) VALUES ('{nama_pemesan}', {i}, {durasi_sewa} ,'{tgl_formatt}', '{tglKembali}', {biaya_akhir(j, durasi_sewa)}); UPDATE barang set status_barang = 'tidak tersedia' where id_barang = {i}"
            create_obj.execute(queryCreate)
            con.commit()
        print("\nCreate Pemesanan Berhasil!")
        for i in range(3):
            print(".")
            time.sleep(0.5)
        pil = int(input("[1] Cetak Nota Pembelian \n[2] Buat Pemesanan Lain \n[3] Kembali ke Menu Utama \nPilih disini >>> "))
        if pil == 1:
            print()
            print("="*50)
            print(" "*17,"NOTA DIGITAL") 
            print("="*50)
            print("Nama Unit: ")
            for (namaBarang, hargaBarang) in zip(detail_pesanan_nama, detail_pesanan_harga):
                print(f"- {namaBarang:<20} : Rp {hargaBarang:,}/hari")
            print("="*50)
            print("Tanggal Penyewaan    :", tglSewa)
            print("Nama Pelanggan       :", nama_pemesan)
            print("Lama waktu Sewa      :", durasi_sewa, "Hari")
            print("Tanggal Unit Kembali :", tglKembali)
            print(f"Total Harga          : Rp {biaya_akhir(hitung_pesanan, durasi_sewa):,}")
            print("="*50)
            print()
            input("Tekan Enter untuk kembali ke menu utama")
            mainPage()
        elif pil == 2:
            createPemesanan()
        elif pil == 3:
            mainPage()
    else:
        print("Maaf, barang sedang tidak tersedia!")
        for i in range(3):
            print(".")
            time.sleep(1)
        os.system("cls")
        createPemesanan()

def updateBarang():
    os.system('cls')
    connect()
    headerBarang = ["ID Barang", "Nama Barang", "Harga Sewa per Hari", "Status Barang"]
    barang_obj = con.cursor()
    barang_obj.execute(f'SELECT id_barang, nama_barang, harga_sewa, status_barang from barang order by id_barang')
    barang = barang_obj.fetchall()
    print(tb(barang, headers=headerBarang, tablefmt="fancy_grid"))
    pilihUpdate = int(input("Silahkan pilih nomor yang ingin di update: "))
    if pilihUpdate <= len(barang):
        print()
        pilihStatus = int(input("[1] Tersedia \n[2] Tidak Tersedia \nSilahkan pilih status barang >>> "))
        
        def prosesPilihan(x):
            return "tersedia" if x == 1 else "tidak tersedia"
        
        hasilPilihan = prosesPilihan
        
        update_obj = con.cursor()
        queryUpdate = f"UPDATE barang SET status_barang = '{hasilPilihan(pilihStatus)}' WHERE id_barang = {pilihUpdate}"
        update_obj.execute(queryUpdate)
        con.commit()
        print("\nUpdate Status Barang Berhasil!")
        for i in range(3):
            print(".")
            time.sleep(0.5)
        pilih_obj = con.cursor()
        pilih_obj.execute(f'SELECT id_barang, nama_barang, harga_sewa, status_barang from barang order by id_barang')
        pilih = pilih_obj.fetchall()
        print(tb(pilih, headers=headerBarang, tablefmt="fancy_grid"))
        lagi = input("Apakah ingin update status barang lagi? [y/n]: ").lower()
        if lagi == 'y':
            os.system('cls')
            updateBarang()
        elif lagi == 'n':
            mainPage()
    else:
        print("Maaf, barang tersebut tidak ada pada daftar")
        print()
        input("Tekan Enter untuk memilih update barang lain")
        updateBarang()

def hapusPemesanan():
    connect()
    headerPilih = ["Id Pemesanan", "Nama Pemesan", "Nama Barang", "Harga Sewa Per Hari", "Durasi Sewa [Hari]", "Biaya", "Tanggal Sewa", "Tanggal Kembali"]
    pilih_obj = con.cursor()
    pilih_obj.execute('SELECT id_pemesanan, nama_pemesan, nama_barang, harga_sewa, durasi_sewa, biaya, tanggal_sewa, tanggal_kembali FROM pemesanan INNER JOIN barang ON id_barang = barang_id INNER JOIN layanan on id_layanan = layanan_id order by id_pemesanan')
    pilih = pilih_obj.fetchall()
    print(tb(pilih, headers=headerPilih, tablefmt="fancy_grid"))
    pilihDelete = int(input("Silahkan pilih Id yang ingin dihapus: "))
    print()
    if pilihDelete <= len(pilih):
        delete_obj = con.cursor()
        queryDelete = f"DELETE FROM pemesanan WHERE id_pemesanan = {pilihDelete};"
        delete_obj.execute(queryDelete)
        con.commit()
        print("\nDelete Pemesanan Berhasil!")
        for i in range(3):
            print(".")
            time.sleep(0.5)
        pilih_obj.execute('SELECT id_pemesanan, nama_pemesan, nama_barang, harga_sewa, durasi_sewa, biaya, tanggal_sewa, tanggal_kembali FROM pemesanan INNER JOIN barang ON id_barang = barang_id INNER JOIN layanan on id_layanan = layanan_id order by id_pemesanan')
        pilih = pilih_obj.fetchall()
        print(tb(pilih, headers=headerPilih, tablefmt="fancy_grid"))
        lagi = input("Apakah Anda ingin hapus pemesanan lagi? [y/n]: ").lower()
        if lagi == 'y':
            hapusPemesanan()
        elif lagi == 'n':
            mainPage()
    else:
        print("Maaf pesanan tidak terdaftar")
        print()
        input("Tekan Enter untuk menghapus pesanan lain")
        hapusPemesanan()

def lihatPemesanan():
    pilihan = int(input("[1] Lihat Seluruh Pemesanan \n[2] Cari Data Pesanan \nSilahkan masukkan pilihan >>> "))
    if pilihan == 1:
        connect()
        headerPilih = ["Id Pemesanan", "Nama Pemesan", "Nama Barang", "Harga Sewa Per Hari", "Durasi Sewa [Hari]", "Biaya", "Tanggal Sewa", "Tanggal Kembali"]
        pilih_obj = con.cursor()
        pilih_obj.execute('SELECT id_pemesanan, nama_pemesan, nama_barang, harga_sewa, durasi_sewa, biaya, tanggal_sewa, tanggal_kembali FROM pemesanan INNER JOIN barang ON id_barang = barang_id INNER JOIN layanan on id_layanan = layanan_id order by id_pemesanan')
        pilih = pilih_obj.fetchall()
        print(tb(pilih, headers=headerPilih, tablefmt="fancy_grid"))
        print()
        lagi = int(input("[1] Pilih Menu Lihat Lain \n[2] Kembali ke Menu Utama \nPilih disini >>> "))
        if lagi == 1:
            os.system('cls')
            lihatPemesanan()
        elif lagi == 2:
            mainPage()
    elif pilihan == 2:
        cari = input("Masukkan Kata Kunci [nama pemesan/nama barang]: ")
        connect()
        headerPilih = ["Id Pemesanan", "Nama Pemesan", "Nama Barang", "Harga Sewa Per Hari", "Durasi Sewa [Hari]", "Biaya", "Tanggal Sewa", "Tanggal Kembali"]
        pilih_obj = con.cursor()
        pilih_obj.execute(f"SELECT id_pemesanan, nama_pemesan, nama_barang, harga_sewa, durasi_sewa, biaya, tanggal_sewa, tanggal_kembali FROM pemesanan INNER JOIN barang ON id_barang = barang_id INNER JOIN layanan on id_layanan = layanan_id where nama_pemesan ilike '%{cari}%' or nama_barang ilike '%{cari}%' order by id_pemesanan")
        pilih = pilih_obj.fetchall()
        print(tb(pilih, headers=headerPilih, tablefmt="fancy_grid"))
        print()
        lagi = int(input("[1] Pilih Menu Lihat Lain \n[2] Kembali ke Menu Utama \nPilih disini >>> "))
        if lagi == 1:
            os.system('cls')
            lihatPemesanan()
        elif lagi == 2:
            mainPage()

def cekDenda():
    connect()
    headerPilih = ["Id Pemesanan", "Nama Pemesan", "Nama Barang", "Harga Sewa Per Hari", "Durasi Sewa [Hari]", "Biaya", "Tanggal Sewa", "Tanggal Kembali"]
    pilih_obj = con.cursor()
    pilih_obj.execute('SELECT id_pemesanan, nama_pemesan, nama_barang, harga_sewa, durasi_sewa, biaya, tanggal_sewa, tanggal_kembali FROM pemesanan INNER JOIN barang ON id_barang = barang_id INNER JOIN layanan on id_layanan = layanan_id order by id_pemesanan')
    pilih = pilih_obj.fetchall()
    print(tb(pilih, headers=headerPilih, tablefmt="fancy_grid"))
    print()
    pilDenda = int(input("Masukkan Id yang ingin di cek: "))
    hargaDenda = pilih[pilDenda-1][5]
    tglHarusKembali = pilih[pilDenda-1][7]
    tglKembali = input("Masukkan Tanggal Barang Dikembalikan [contoh: 07/12/2023]: ")
    tglKembali_format = datetime.strptime(f"{tglKembali}", "%d/%m/%Y").date()
    lamaTelat = (tglKembali_format - tglHarusKembali).days
    if lamaTelat < 0:
        lamaTelat = 0
        
    def f(x):
        return int(hargaDenda * 10/100) 
    def g(x):
        return lamaTelat * x
    def compose(x):
        return g(f(x))
    
    totalDenda = compose(hargaDenda)
    print()
    print("**RULES: Denda 10% dari total biaya sewa per 1 hari telat!**")
    print()
    print(f"Telat: {lamaTelat} Hari")
    print(f"Biaya: Rp {totalDenda:,}")    
    lagi = input("Cek denda lain? [y/n]: ").lower()
    if lagi == 'y':
        os.system('cls')
        cekDenda()
    else:
        mainPage()

# HOMEPAGE
def mainPage():
    os.system("cls")
    print("--------------------------------------------------------------------")
    print("|                  SELAMAT DATANG DI SCAMMER                       |")
    print("|                     Sewa Camera Merdeka                          |")
    print("--------------------------------------------------------------------")
    print()    
    print("[1] Buat Pesanan")
    print("[2] Lihat Pesanan")
    print("[3] Update Status Barang")
    print("[4] Delete Pemesanan")
    print("[5] Cek Denda Telat")
    print("[6] Exit")
    pil = int(input("Pilih menu >>> "))
    if pil == 1:
        createPemesanan()
    elif pil == 2:
        lihatPemesanan()
    elif pil == 3:
        updateBarang()
    elif pil == 4:
        hapusPemesanan()
    elif pil == 5:
        cekDenda()
    elif pil == 6:
        exit
loginAdmin()
mainPage()