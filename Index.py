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

def connect():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print('')
        return connection
    except mysql.connector.Error as e:
        print(f"Koneksi error: {e}")
        return None
    
#=============================================================================================================================================
    

#================== Menampilkan Data dari Kandidat ===========================================================================================

def display_kandidat():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM kandidat"
            cursor.execute(query)
            
            kandidat_list = cursor.fetchall()
            
            if not kandidat_list:
                print("Tidak ada data kandidat.")
            else:
                print("Data Kandidat:")
                for kandidat in kandidat_list:
                    print(f"Nama: {kandidat['nama_kandidat']}, Visi Misi: {kandidat['visi_misi']}")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

#=============================================================================================================================================

#================= Fungsi untuk Registrasi User ==============================================================================================
def registrasi():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            NIK = input("Masukkan NIK: ")
            nama_user = input("Masukkan Nama: ")

            query = "INSERT INTO user (NIK, nama_user) VALUES (%s, %s)"
            data_user = (NIK, nama_user)
            
            cursor.execute(query, data_user)
            connection.commit()
            
            print("Registrasi berhasil!")
            time.sleep(2)
            clear_screen()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
#==============================================================================================================================================

#==================== Function lOGIN USER =====================================================================================================
            
def login():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            NIK = input("Masukkan NIK: ")
            
            query = "SELECT id_user, nama_user FROM user WHERE NIK = %s"
            cursor.execute(query, (NIK,))
            
            user = cursor.fetchone()
            
            if user:
                print(f"Selamat datang, {user[1]}!")
                return user[0]  # Mengembalikan ID user yang berhasil login
            else:
                print("Login gagal. NIK tidak ditemukan.")
                return None
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def login_menu():
    user_id = login()
    if user_id is not None:
        pilih_kandidat(user_id)

#===============================================================================================================================================

#================== Fungsi untuk menyimpan data suara yang diinputkan user =====================================================================

def insert_suara(user_id, kandidat_id):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            
            query = "INSERT INTO suara (id_user, id_kandidat) VALUES (%s, %s)"
            data_suara = (user_id, kandidat_id)
            
            cursor.execute(query, data_suara)
            connection.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

#=====================================================================================================================================================

#=================== Function PILIH KANDIDAT =========================================================================================================

def pilih_kandidat(user_id):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Cek apakah pengguna sudah memilih sebelumnya
            check_query = "SELECT * FROM suara WHERE id_user = %s"
            cursor.execute(check_query, (user_id,))
            existing_vote = cursor.fetchone()
            
            if existing_vote:
                print("Anda sudah memilih sebelumnya. Tidak dapat memilih lagi.")
                input("Klik ENTER untuk melanjutkan... ")
                clear_screen()
            else:
                # Jika pengguna belum memilih, tampilkan kandidat
                query = "SELECT * FROM kandidat"
                cursor.execute(query)
                
                kandidat_list = cursor.fetchall()
                
                if not kandidat_list:
                    print("Tidak ada data kandidat.")
                else:
                    print("Data Kandidat:")
                    for kandidat in kandidat_list:
                        print(f"{kandidat['id_kandidat']}. {kandidat['nama_kandidat']} - Visi Misi: {kandidat['visi_misi']}")
                    
                    pilihan_kandidat = input("Masukkan nomor kandidat yang dipilih: ")
                    
                    # Memastikan pilihan adalah angka
                    if pilihan_kandidat.isdigit():
                        pilihan_kandidat = int(pilihan_kandidat)
                       
                        # Memastikan nomor kandidat yang dipilih valid
                        if 1 <= pilihan_kandidat <= len(kandidat_list):
                            insert_suara(user_id, pilihan_kandidat)
                            print("Terima kasih atas partisipasi Anda dalam pemilihan.")
                            time.sleep(2)
                            clear_screen()
                        else:
                            print("Nomor kandidat tidak valid.")
                            time.sleep(2)
                            clear_screen()
                    else:
                        print("Masukkan nomor kandidat dengan benar.")
                        time.sleep(2)
                        clear_screen()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

#====================================================================================================================================

#============== Function ADMIN ======================================================================================================
            
# Data login admin 
admin_username = "admin"
admin_password = "admin"

# ...

def login_admin():
    input_username = input("Masukkan username admin: ")
    input_password = input("Masukkan password admin: ")

    if input_username == admin_username and input_password == admin_password:
        print("Login admin berhasil.")
        time.sleep(2)
        clear_screen()
        return True
    else:
        print("Login admin gagal. Username atau password salah.")
        return False

#======= Fungsi untuk menampilkan suara yg telah dipilih user =========================================================================

def display_suara():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM suara"
            cursor.execute(query)

            suara_list = cursor.fetchall()

            if not suara_list:
                print("Tidak ada data suara.")
            else:
                print("Data Suara:")
                for suara in suara_list:
                    print(f"ID User: {suara['id_user']}, Memilih Kandidat No : {suara['id_kandidat']}")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
            input("Klik ENTER untuk melanjutkan... ")
            clear_screen()

#=============================================================================================================================================

#========= Fungsi untuk menampilkan nama dan jumlah suara yg diperolehnya ====================================================================
            
def display_kandidat_pemilih_terbanyak():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = (
                "SELECT kandidat.id_kandidat, kandidat.nama_kandidat, COUNT(suara.id_user) AS jumlah_pemilih "
                "FROM kandidat LEFT JOIN suara ON kandidat.id_kandidat = suara.id_kandidat "
                "GROUP BY kandidat.id_kandidat, kandidat.nama_kandidat "
                "ORDER BY jumlah_pemilih DESC"
            )
            cursor.execute(query)

            kandidat_list = cursor.fetchall()

            if not kandidat_list:
                print("Tidak ada data kandidat.")
            else:
                print("Kandidat dengan Pemilih Terbanyak:")
                print("")
                for kandidat in kandidat_list:
                    print(f"Nama: {kandidat['nama_kandidat']}, Jumlah Pemilih: {kandidat['jumlah_pemilih']}")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
            print("")
            input("Klik ENTER untuk melanjutkan... ")
            clear_screen()

#=============================================================================================================================================

#======== Fungsi untuk menampilkan data user Dan status user sudah memilih atau belum ========================================================

def display_data_user():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = (
                "SELECT user.id_user, user.NIK, user.nama_user, suara.waktu_pilihan "
                "FROM user LEFT JOIN suara ON user.id_user = suara.id_user"
            )
            cursor.execute(query)

            user_list = cursor.fetchall()

            if not user_list:
                print("Tidak ada data user.")
            else:
                print("Data User:")
                for user in user_list:
                    waktu_pilihan = user['waktu_pilihan'] if user['waktu_pilihan'] else "Belum memilih"
                    print(f"ID User: {user['id_user']}, NIK: {user['NIK']}, Nama: {user['nama_user']}, Waktu user memilih: {waktu_pilihan}")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
            print("")
            input("Klik ENTER untuk melanjutkan... ")
            clear_screen()

#=============================================================================================================================================

#============= Fungsi untuk Tampilan DASHBOARD ADMIN =========================================================================================
            
def admin_dashboard():
    while True:
        print("===== Dashboard Admin =====")
        print("")
        print("1. Menampilkan data suara")
        print("2. Menampilkan kandidat dengan pemilih terbanyak")
        print("3. Menampilkan data user")
        print("4. Logout")
        print("=============================")

        choice = input("Pilih opsi (1/2/3/4): ")

        if choice == '1':
            display_suara()
        elif choice == '2':
            display_kandidat_pemilih_terbanyak()
        elif choice == '3':
            display_data_user()
        elif choice == '4':
            print("Logout berhasil.")
            time.sleep(2)
            clear_screen()
            break
        else:
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
    while True:
        show_menu()
        choice = input("Pilih opsi (1/2/3/4): ")

        if choice == '1':
            registrasi()
        elif choice == '2':
            login_menu()
        elif choice == '3':
            if login_admin():
                admin_dashboard()
        elif choice == '4':
            print("Aplikasi selesai. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan angka 1, 2, 3, atau 4.")

#===============================================================================================================================================


# Panggil fungsi main_menu untuk memulai program
main_menu()


