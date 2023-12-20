import mysql.connector
import os
import time

def clear_screen():
    # Menjalankan perintah clear screen sesuai dengan sistem operasi
    os.system('cls' if os.name == 'nt' else 'clear')

#========================== KONFIGURASI KONEKSI =============================================================================================

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'e-voting'
}

# Mendefinisikan fungsi connect() yang akan digunakan untuk membuat koneksi ke database
def connect():
    try:
        # Mencoba untuk membuat koneksi menggunakan konfigurasi yang disediakan oleh variabel db_config
        connection = mysql.connector.connect(**db_config)

        # Memeriksa apakah koneksi berhasil dilakukan
        if connection.is_connected():
            # Jika koneksi berhasil, mencetak pesan kosong (mungkin ini seharusnya pesan informatif)
            print('')

        # Mengembalikan objek koneksi ke pemanggil fungsi
        return connection

    except mysql.connector.Error as e:
        # Menangkap kesalahan yang mungkin terjadi selama proses koneksi
        print(f"Koneksi error: {e}")

        # Mengembalikan None jika terjadi kesalahan untuk menandakan kegagalan koneksi
        return None
    
#=============================================================================================================================================
    

#================== Menampilkan Data dari Kandidat ===========================================================================================

def display_kandidat():
    # Membuat koneksi ke database menggunakan fungsi connect() yang telah didefinisikan sebelumnya
    connection = connect()

    # Memeriksa apakah koneksi berhasil
    if connection:
        try:
            # Membuat objek cursor untuk mengeksekusi perintah SQL
            cursor = connection.cursor(dictionary=True)

            # Menentukan perintah SQL untuk mengambil semua data dari tabel "kandidat"
            query = "SELECT * FROM kandidat"

            # Mengeksekusi perintah SQL
            cursor.execute(query)

            # Mengambil semua baris hasil query dan menyimpannya dalam bentuk daftar kamus
            kandidat_list = cursor.fetchall()

            # Memeriksa apakah ada data kandidat
            if not kandidat_list:
                print("Tidak ada data kandidat.")
            else:
                # Jika ada data kandidat, mencetak judul dan detail kandidat
                print("Data Kandidat:")
                for kandidat in kandidat_list:
                    print(f"Nama: {kandidat['nama_kandidat']}, Visi Misi: {kandidat['visi_misi']}")

        except mysql.connector.Error as e:
            # Menangkap kesalahan yang mungkin terjadi selama eksekusi perintah SQL
            print(f"Error: {e}")

        finally:
            # Selalu menutup cursor dan koneksi, bahkan jika terjadi kesalahan
            cursor.close()
            connection.close()


#=============================================================================================================================================

#================= Fungsi untuk Registrasi User ==============================================================================================
def registrasi():
    # Membuat koneksi ke database menggunakan fungsi connect()
    connection = connect()

    # Memeriksa apakah koneksi berhasil
    if connection:
        try:
            # Membuat objek cursor untuk mengeksekusi perintah SQL
            cursor = connection.cursor()

            # Meminta pengguna untuk memasukkan NIK dan nama_user
            NIK = input("Masukkan NIK: ")
            nama_user = input("Masukkan Nama: ")

            # Menyusun perintah SQL untuk menyisipkan data baru ke dalam tabel "user"
            query = "INSERT INTO user (NIK, nama_user) VALUES (%s, %s)"
            data_user = (NIK, nama_user)
            
            # Mengeksekusi perintah SQL dengan menyertakan data pengguna
            cursor.execute(query, data_user)

            # Melakukan commit untuk menyimpan perubahan ke dalam database
            connection.commit()
            
            # Memberikan pesan bahwa registrasi berhasil
            print("Registrasi berhasil!")

            # Memberi jeda selama 2 detik menggunakan modul time
            time.sleep(2)

            # Membersihkan layar console (asumsi ada fungsi clear_screen() yang didefinisikan)
            clear_screen()

        except mysql.connector.Error as e:
            # Menangkap kesalahan yang mungkin terjadi selama eksekusi perintah SQL
            print(f"Error: {e}")

        finally:
            # Selalu menutup cursor dan koneksi, bahkan jika terjadi kesalahan
            cursor.close()
            connection.close()

#==============================================================================================================================================

#==================== Function lOGIN USER =====================================================================================================
            
def login():
    # Membuat koneksi ke database menggunakan fungsi connect()
    connection = connect()

    # Memeriksa apakah koneksi berhasil
    if connection:
        try:
            # Membuat objek cursor untuk mengeksekusi perintah SQL
            cursor = connection.cursor()

            # Meminta pengguna untuk memasukkan NIK melalui input
            NIK = input("Masukkan NIK: ")
            
            # Menyusun perintah SQL untuk mengambil data user berdasarkan NIK
            query = "SELECT id_user, nama_user FROM user WHERE NIK = %s"
            cursor.execute(query, (NIK,))
            
            # Mengambil satu baris hasil query
            user = cursor.fetchone()
            
            # Memeriksa apakah user ditemukan
            if user:
                # Jika ditemukan, mencetak pesan selamat datang dan mengembalikan ID user
                print(f"Selamat datang, {user[1]}!")
                return user[0]  # Mengembalikan ID user yang berhasil login
            else:
                # Jika tidak ditemukan, mencetak pesan bahwa login gagal
                print("Login gagal. NIK tidak ditemukan.")
                return None

        except mysql.connector.Error as e:
            # Menangkap kesalahan yang mungkin terjadi selama eksekusi perintah SQL
            print(f"Error: {e}")

        finally:
            # Selalu menutup cursor dan koneksi, bahkan jika terjadi kesalahan
            cursor.close()
            connection.close()


def login_menu():
    # Memanggil fungsi login() untuk melakukan login
    user_id = login()

    # Memeriksa apakah login berhasil (user_id tidak None)
    if user_id is not None:
        # Jika berhasil, memanggil fungsi pilih_kandidat() dengan parameter user_id
        pilih_kandidat(user_id)


#===============================================================================================================================================

#================== Fungsi untuk menyimpan data suara yang diinputkan user =====================================================================

def insert_suara(user_id, kandidat_id):
    # Membuat koneksi ke database menggunakan fungsi connect()
    connection = connect()

    # Memeriksa apakah koneksi berhasil
    if connection:
        try:
            # Membuat objek cursor untuk mengeksekusi perintah SQL
            cursor = connection.cursor()

            # Menyusun perintah SQL untuk menyisipkan data suara baru ke dalam tabel "suara"
            query = "INSERT INTO suara (id_user, id_kandidat) VALUES (%s, %s)"
            data_suara = (user_id, kandidat_id)
            
            # Mengeksekusi perintah SQL dengan menyertakan data suara
            cursor.execute(query, data_suara)

            # Melakukan commit untuk menyimpan perubahan ke dalam database
            connection.commit()

        except mysql.connector.Error as e:
            # Menangkap kesalahan yang mungkin terjadi selama eksekusi perintah SQL
            print(f"Error: {e}")

        finally:
            # Selalu menutup cursor dan koneksi, bahkan jika terjadi kesalahan
            cursor.close()
            connection.close()


#=====================================================================================================================================================

#=================== Function PILIH KANDIDAT =========================================================================================================

def pilih_kandidat(user_id):
    # Membuat koneksi ke database menggunakan fungsi connect()
    connection = connect()

    # Memeriksa apakah koneksi berhasil
    if connection:
        try:
            # Membuat objek cursor untuk mengeksekusi perintah SQL
            cursor = connection.cursor(dictionary=True)

            # Cek apakah pengguna sudah memilih sebelumnya
            check_query = "SELECT * FROM suara WHERE id_user = %s"
            cursor.execute(check_query, (user_id,))
            existing_vote = cursor.fetchone()

            if existing_vote:
                # Jika pengguna sudah memilih sebelumnya, berikan pesan dan beri jeda sebelum membersihkan layar
                print("Anda sudah memilih sebelumnya. Tidak dapat memilih lagi.")
                input("Klik ENTER untuk melanjutkan... ")
                clear_screen()
            else:
                # Jika pengguna belum memilih, tampilkan data kandidat
                query = "SELECT * FROM kandidat"
                cursor.execute(query)

                kandidat_list = cursor.fetchall()

                if not kandidat_list:
                    # Jika tidak ada data kandidat, berikan pesan
                    print("Tidak ada data kandidat.")
                else:
                    # Jika ada data kandidat, tampilkan data kandidat dan minta pengguna memilih
                    print("Data Kandidat:")
                    for kandidat in kandidat_list:
                        print(f"{kandidat['id_kandidat']}. {kandidat['nama_kandidat']} - Visi Misi: {kandidat['visi_misi']}")

                    pilihan_kandidat = input("Masukkan nomor kandidat yang dipilih: ")

                    # Memastikan pilihan adalah angka
                    if pilihan_kandidat.isdigit():
                        pilihan_kandidat = int(pilihan_kandidat)

                        # Memastikan nomor kandidat yang dipilih valid
                        if 1 <= pilihan_kandidat <= len(kandidat_list):
                            # Jika valid, memanggil fungsi insert_suara() untuk menyimpan pilihan suara
                            insert_suara(user_id, pilihan_kandidat)
                            print("Terima kasih atas partisipasi Anda dalam pemilihan.")
                            time.sleep(2)
                            clear_screen()
                        else:
                            # Jika nomor kandidat tidak valid, berikan pesan
                            print("Nomor kandidat tidak valid.")
                            time.sleep(2)
                            clear_screen()
                    else:
                        # Jika input bukan angka, berikan pesan
                        print("Masukkan nomor kandidat dengan benar.")
                        time.sleep(2)
                        clear_screen()

        except mysql.connector.Error as e:
            # Menangkap kesalahan yang mungkin terjadi selama eksekusi perintah SQL
            print(f"Error: {e}")

        finally:
            # Selalu menutup cursor dan koneksi, bahkan jika terjadi kesalahan
            cursor.close()
            connection.close()


#====================================================================================================================================

#============== Function ADMIN ======================================================================================================
            
# Data login admin 
admin_username = "admin"
admin_password = "admin"

# ...

def login_admin():
    # Meminta pengguna memasukkan username dan password admin
    input_username = input("Masukkan username admin: ")
    input_password = input("Masukkan password admin: ")

    # Memeriksa apakah input username dan password sesuai dengan data login admin
    if input_username == admin_username and input_password == admin_password:
        # Jika sesuai, memberikan pesan berhasil, memberi jeda, membersihkan layar, dan mengembalikan True
        print("Login admin berhasil.")
        time.sleep(2)
        clear_screen()
        return True
    else:
        # Jika tidak sesuai, memberikan pesan gagal dan mengembalikan False
        print("Login admin gagal. Username atau password salah.")
        return False


#======= Fungsi untuk menampilkan suara yg telah dipilih user =========================================================================

def display_suara():
    # Membuat koneksi ke database menggunakan fungsi connect()
    connection = connect()

    # Memeriksa apakah koneksi berhasil
    if connection:
        try:
            # Membuat objek cursor untuk mengeksekusi perintah SQL
            cursor = connection.cursor(dictionary=True)

            # Menyusun perintah SQL untuk mengambil semua data dari tabel "suara"
            query = "SELECT * FROM suara"
            cursor.execute(query)

            # Mengambil semua baris hasil query dan menyimpannya dalam bentuk daftar kamus
            suara_list = cursor.fetchall()

            # Memeriksa apakah ada data suara
            if not suara_list:
                print("Tidak ada data suara.")
            else:
                # Jika ada data suara, mencetak judul dan detail suara
                print("Data Suara:")
                for suara in suara_list:
                    print(f"ID User: {suara['id_user']}, Memilih Kandidat No : {suara['id_kandidat']}")

        except mysql.connector.Error as e:
            # Menangkap kesalahan yang mungkin terjadi selama eksekusi perintah SQL
            print(f"Error: {e}")

        finally:
            # Selalu menutup cursor dan koneksi, bahkan jika terjadi kesalahan
            cursor.close()
            connection.close()

            # Memberikan pengguna jeda dan membersihkan layar sebelum kembali ke menu
            input("Klik ENTER untuk melanjutkan... ")
            clear_screen()


#=============================================================================================================================================

#========= Fungsi untuk menampilkan nama dan jumlah suara yg diperolehnya ====================================================================
            
def display_kandidat_pemilih_terbanyak():
    # Membuat koneksi ke database menggunakan fungsi connect()
    connection = connect()

    # Memeriksa apakah koneksi berhasil
    if connection:
        try:
            # Membuat objek cursor untuk mengeksekusi perintah SQL
            cursor = connection.cursor(dictionary=True)

            # Menyusun perintah SQL untuk mengambil data kandidat dengan jumlah pemilih terbanyak
            query = (
                "SELECT kandidat.id_kandidat, kandidat.nama_kandidat, COUNT(suara.id_user) AS jumlah_pemilih "
                "FROM kandidat LEFT JOIN suara ON kandidat.id_kandidat = suara.id_kandidat "
                "GROUP BY kandidat.id_kandidat, kandidat.nama_kandidat "
                "ORDER BY jumlah_pemilih DESC"
            )

            # Mengeksekusi perintah SQL yang telah disusun sebelumnya
            cursor.execute(query)

            # Mengambil semua baris hasil query dan menyimpannya dalam bentuk daftar kamus
            kandidat_list = cursor.fetchall()

            # Memeriksa apakah ada data kandidat
            if not kandidat_list:
                print("Tidak ada data kandidat.")
            else:
                # Jika ada data kandidat, mencetak judul dan detail kandidat dengan pemilih terbanyak
                print("Kandidat dengan Pemilih Terbanyak:")
                print("")
                for kandidat in kandidat_list:
                    print(f"Nama: {kandidat['nama_kandidat']}, Jumlah Pemilih: {kandidat['jumlah_pemilih']}")

        except mysql.connector.Error as e:
            # Menangkap kesalahan yang mungkin terjadi selama eksekusi perintah SQL
            print(f"Error: {e}")

        finally:
            # Selalu menutup cursor dan koneksi, bahkan jika terjadi kesalahan
            cursor.close()
            connection.close()

            # Memberikan pengguna jeda, mencetak garis baru, dan menunggu sampai pengguna menekan tombol ENTER
            print("")
            input("Klik ENTER untuk melanjutkan... ")
            clear_screen()


#=============================================================================================================================================

#======== Fungsi untuk menampilkan data user Dan status user sudah memilih atau belum ========================================================

def display_data_user():
    # Membuat koneksi ke database menggunakan fungsi connect()
    connection = connect()

    # Memeriksa apakah koneksi berhasil
    if connection:
        try:
            # Membuat objek cursor untuk mengeksekusi perintah SQL
            cursor = connection.cursor(dictionary=True)

            # Menyusun perintah SQL untuk mengambil data pengguna dengan waktu pemilihan
            query = (
                "SELECT user.id_user, user.NIK, user.nama_user, suara.waktu_pilihan "
                "FROM user LEFT JOIN suara ON user.id_user = suara.id_user"
            )

            # Mengeksekusi perintah SQL yang telah disusun sebelumnya
            cursor.execute(query)

            # Mengambil semua baris hasil query dan menyimpannya dalam bentuk daftar kamus
            user_list = cursor.fetchall()

            # Memeriksa apakah ada data pengguna
            if not user_list:
                print("Tidak ada data user.")
            else:
                # Jika ada data pengguna, mencetak judul dan detail pengguna dengan waktu pemilihan
                print("Data User:")
                for user in user_list:
                    waktu_pilihan = user['waktu_pilihan'] if user['waktu_pilihan'] else "Belum memilih"
                    print(f"ID User: {user['id_user']}, NIK: {user['NIK']}, Nama: {user['nama_user']}, Waktu user memilih: {waktu_pilihan}")

        except mysql.connector.Error as e:
            # Menangkap kesalahan yang mungkin terjadi selama eksekusi perintah SQL
            print(f"Error: {e}")

        finally:
            # Selalu menutup cursor dan koneksi, bahkan jika terjadi kesalahan
            cursor.close()
            connection.close()

            # Memberikan pengguna jeda, mencetak garis baru, dan menunggu sampai pengguna menekan tombol ENTER
            print("")
            input("Klik ENTER untuk melanjutkan... ")
            clear_screen()


#=============================================================================================================================================

#============= Fungsi untuk Tampilan DASHBOARD ADMIN =========================================================================================
            
def admin_dashboard():
    # Loop tak terbatas untuk menampilkan dashboard admin
    while True:
        print("===== Dashboard Admin =====")
        print("")
        print("1. Menampilkan data suara")
        print("2. Menampilkan kandidat dengan pemilih terbanyak")
        print("3. Menampilkan data user")
        print("4. Logout")
        print("=============================")

        # Meminta admin memilih opsi
        choice = input("Pilih opsi (1/2/3/4): ")

        # Memproses pilihan admin
        if choice == '1':
            # Memanggil fungsi display_suara() untuk menampilkan data suara
            display_suara()
        elif choice == '2':
            # Memanggil fungsi display_kandidat_pemilih_terbanyak() untuk menampilkan kandidat dengan pemilih terbanyak
            display_kandidat_pemilih_terbanyak()
        elif choice == '3':
            # Memanggil fungsi display_data_user() untuk menampilkan data user
            display_data_user()
        elif choice == '4':
            # Memberikan pesan logout berhasil, memberi jeda, membersihkan layar, dan keluar dari loop
            print("Logout berhasil.")
            time.sleep(2)
            clear_screen()
            break
        else:
            # Jika pilihan tidak valid, memberikan pesan kesalahan
            print("Pilihan tidak valid. Silakan masukkan angka 1, 2, 3, atau 4.")


#=============================================================================================================================================
            
#========= Fungsi menu awal aplikasi =========================================================================================================
def show_menu():
    print("===== Aplikasi E-Voting =====")
    print("1. Registrasi")
    print("2. Pilih kandidat")
    print("3. Admin")
    print("4. Keluar")
    print("=============================")

def main_menu():
    # Loop tak terbatas untuk menampilkan menu utama
    while True:
        # Menampilkan menu utama menggunakan fungsi show_menu()
        show_menu()

        # Meminta pengguna memilih opsi
        choice = input("Pilih opsi (1/2/3/4): ")

        # Memproses pilihan pengguna
        if choice == '1':
            # Memanggil fungsi registrasi() jika pilihan adalah '1'
            registrasi()
        elif choice == '2':
            # Memanggil fungsi login_menu() jika pilihan adalah '2'
            login_menu()
        elif choice == '3':
            # Memanggil fungsi login_admin() untuk login sebagai admin dan admin_dashboard() untuk menu admin jika pilihan adalah '3'
            if login_admin():
                admin_dashboard()
        elif choice == '4':
            # Memberikan pesan aplikasi selesai, dan keluar dari loop jika pilihan adalah '4'
            print("Aplikasi selesai. Sampai jumpa!")
            break
        else:
            # Jika pilihan tidak valid, memberikan pesan kesalahan
            print("Pilihan tidak valid. Silakan masukkan angka 1, 2, 3, atau 4.")


#===============================================================================================================================================


# Panggil fungsi main_menu untuk memulai program
main_menu()


