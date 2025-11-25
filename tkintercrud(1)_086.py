import tkinter as tk
import sqlite3
from tkinter import messagebox

conn = sqlite3.connect("nilai_siswa.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
""")
conn.commit()


def prediksi(bio, fis, ing):
    nilai = [bio, fis, ing]
    tertinggi = max(nilai)

    if nilai.count(tertinggi) > 1:
        return "Tidak Ditemukan"

    index = nilai.index(tertinggi)

    if index == 0:
        return "Kedokteran"
    elif index == 1:
        return "Teknik"
    else:
        return "Bahasa"



root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan")
root.geometry("400x420")

judul = tk.Label(root, text="Aplikasi Prediksi Prodi Pilihan", font=("Arial", 14, "bold"))
judul.pack(pady=10)

frm = tk.Frame(root)
frm.pack(pady=10)

tk.Label(frm, text="Nama Siswa").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(frm, width=25)
entry_nama.grid(row=0, column=1)

tk.Label(frm, text="Nilai Biologi").grid(row=1, column=0, sticky="w")
entry_bio = tk.Entry(frm, width=10)
entry_bio.grid(row=1, column=1)

tk.Label(frm, text="Nilai Fisika").grid(row=2, column=0, sticky="w")
entry_fis = tk.Entry(frm, width=10)
entry_fis.grid(row=2, column=1)

tk.Label(frm, text="Nilai Inggris").grid(row=3, column=0, sticky="w")
entry_ing = tk.Entry(frm, width=10)
entry_ing.grid(row=3, column=1)


def submit():
    try:
        nama = entry_nama.get()
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())

        hasil_prediksi = prediksi(bio, fis, ing)

        cur.execute("""
            INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, bio, fis, ing, hasil_prediksi))
        conn.commit()

        hasil_label.config(text=f"Hasil Prediksi: {hasil_prediksi}")
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")

    except ValueError:
        messagebox.showerror("Error", "Masukkan nilai angka yang valid!")


def update_data():
    try:
        nama = entry_nama.get()
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())

        hasil_prediksi = prediksi(bio, fis, ing)

        cur.execute("""
            UPDATE nilai_siswa
            SET biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
            WHERE nama_siswa=?
        """, (bio, fis, ing, hasil_prediksi, nama))

        if cur.rowcount == 0:
            messagebox.showwarning("Peringatan", "Nama siswa tidak ditemukan!")
        else:
            conn.commit()
            messagebox.showinfo("Sukses", "Data berhasil diperbarui!")

    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")


def delete_data():
    nama = entry_nama.get()

    cur.execute("DELETE FROM nilai_siswa WHERE nama_siswa=?", (nama,))
    if cur.rowcount == 0:
        messagebox.showwarning("Peringatan", "Nama siswa tidak ditemukan!")
    else:
        conn.commit()
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")


btn_submit = tk.Button(root, text="Submit Nilai", command=submit, bg="lightblue", width=20)
btn_submit.pack(pady=5)

btn_update = tk.Button(root, text="Update Data", command=update_data, bg="orange", width=20)
btn_update.pack(pady=5)

btn_delete = tk.Button(root, text="Delete Data", command=delete_data, bg="red", width=20)
btn_delete.pack(pady=5)

hasil_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
hasil_label.pack(pady=10)

root.mainloop()
