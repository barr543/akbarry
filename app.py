from flask import Flask, render_template, request, redirect, url_for, make_response
import mysql.connector
from fpdf import FPDF


app = Flask(__name__)

def hitung_nilai_akhir_akbar(tugas, uts, uas):
    return (int(tugas) + int(uts) + int(uas)) // 3

def koneksi_database_akbar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rapot_akbar"
    )
def generate_id_nilai_akbar(kursor_akbar):
    kursor_akbar.execute("""
        SELECT id_nilai 
        FROM nilai_akbar
        ORDER BY CAST(SUBSTRING(id_nilai, 2) AS UNSIGNED) DESC
        LIMIT 1
    """)
    terakhir = kursor_akbar.fetchone()

    if terakhir and terakhir["id_nilai"]:
        nomor = int(terakhir["id_nilai"][1:]) + 1
    else:
        nomor = 1

    return f"N{nomor:03d}"



@app.route('/', methods=['GET'])
def halaman_utama_akbar():
    db_akbar = koneksi_database_akbar()
    kursor_akbar = db_akbar.cursor(dictionary=True)

    nis = request.args.get('nis', '')
    id_mapel = request.args.get('id_mapel', '')
    semester = request.args.get('semester', '')
    tahun_ajaran = request.args.get('tahun_ajaran', '')

    sql_akbar = """
        SELECT n.*, s.nama, m.nama_mapel 
        FROM nilai_akbar n
        JOIN siswa_akbar s ON n.nis = s.nis
        JOIN mapel_akbar m ON n.id_mapel = m.id_mapel
        WHERE 1=1
    """
    params = []

    if nis:
        sql_akbar += " AND n.nis = %s"
        params.append(nis)

    if id_mapel:
        sql_akbar += " AND n.id_mapel = %s"
        params.append(id_mapel)

    if semester:
        sql_akbar += " AND n.semester = %s"
        params.append(semester)

    if tahun_ajaran:
        sql_akbar += " AND n.tahun_ajaran = %s"
        params.append(tahun_ajaran)

    sql_akbar += " ORDER BY n.id_nilai DESC"

    kursor_akbar.execute(sql_akbar, tuple(params))
    data_akbar = kursor_akbar.fetchall()

    kursor_akbar.execute("SELECT nis, nama FROM siswa_akbar ORDER BY nama ASC")
    siswa = kursor_akbar.fetchall()

    kursor_akbar.execute("SELECT id_mapel, nama_mapel FROM mapel_akbar ORDER BY nama_mapel ASC")
    mapel = kursor_akbar.fetchall()

    kursor_akbar.execute("SELECT DISTINCT tahun_ajaran FROM nilai_akbar ORDER BY tahun_ajaran DESC")
    tahun_raw = kursor_akbar.fetchall()

    tahun_ajaran = []
    for t in tahun_raw:
        th = int(t["tahun_ajaran"])
        tahun_ajaran.append({
            "value": th,
            "label": f"{th}/{th+1}"
        })

    kursor_akbar.close()
    db_akbar.close()

    return render_template(
        'index_akbar.html',
        daftar_nilai_akbar=data_akbar,
        filter_semester=semester,
        tahun_ajaran=tahun_ajaran
    )


@app.route('/deskripsi_otomatis/<nilai_akhir>')
def deskripsi_otomatis(nilai_akhir):
    nilai_akhir = int(nilai_akhir)

    if nilai_akhir >= 90:
        return "Sangat baik, pertahankan prestasi."
    elif nilai_akhir >= 80:
        return "Baik, tingkatkan konsistensi belajar."
    elif nilai_akhir >= 70:
        return "Cukup baik, perlu lebih giat latihan."
    elif nilai_akhir >= 60:
        return "Kurang, perlu bimbingan dan belajar lebih rutin."
    else:
        return "Sangat kurang, harus belajar lebih keras dan perlu pendampingan."


@app.route('/tambah_nilai_akbar', methods=['GET', 'POST'])
def tambah_nilai_akbar():
    db_akbar = koneksi_database_akbar()
    kursor_akbar = db_akbar.cursor(dictionary=True)

    if request.method == 'POST':
        nis = request.form['nis']
        id_mapel = request.form['id_mapel']
        n_tugas = request.form['nilai_tugas']
        n_uts = request.form['nilai_uts']
        n_uas = request.form['nilai_uas']

        n_akhir = hitung_nilai_akhir_akbar(n_tugas, n_uts, n_uas)
        deskripsi = deskripsi_otomatis(n_akhir)

        id_nilai = generate_id_nilai_akbar(kursor_akbar)

        sql_simpan = """
            INSERT INTO nilai_akbar
            (id_nilai, nis, id_mapel, nilai_tugas, nilai_uts, nilai_uas, nilai_akhir, deskripsi, semester, tahun_ajaran)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '1', 2026)
        """

        kursor_akbar.execute(sql_simpan, (
            id_nilai, nis, id_mapel, n_tugas, n_uts, n_uas, n_akhir, deskripsi
        ))
        db_akbar.commit()

        return redirect(url_for('halaman_utama_akbar'))

    kursor_akbar.execute("SELECT nis, nama FROM siswa_akbar")
    siswa = kursor_akbar.fetchall()
    kursor_akbar.execute("SELECT id_mapel, nama_mapel FROM mapel_akbar")
    mapel = kursor_akbar.fetchall()
    
    kursor_akbar.close()
    db_akbar.close()
    return render_template('tambah_nilai_akbar.html', siswa=siswa, mapel=mapel)

@app.route('/ubah_nilai_akbar/<id_nilai>', methods=['GET', 'POST'])
def ubah_nilai_akbar(id_nilai):
    db_akbar = koneksi_database_akbar()
    kursor_akbar = db_akbar.cursor(dictionary=True)
    
    if request.method == 'POST':
        n_tugas = request.form['nilai_tugas']
        n_uts = request.form['nilai_uts']
        n_uas = request.form['nilai_uas']
        deskripsi = request.form['deskripsi']
        n_akhir = hitung_nilai_akhir_akbar(n_tugas, n_uts, n_uas)
        
        sql_update = """UPDATE nilai_akbar SET nilai_tugas=%s, nilai_uts=%s, nilai_uas=%s, nilai_akhir=%s, deskripsi=%s 
                        WHERE id_nilai=%s"""
        kursor_akbar.execute(sql_update, (n_tugas, n_uts, n_uas, n_akhir, deskripsi, id_nilai))
        db_akbar.commit()
        return redirect(url_for('halaman_utama_akbar'))
    
    kursor_akbar.execute("SELECT * FROM nilai_akbar WHERE id_nilai=%s", (id_nilai,))
    data_lama = kursor_akbar.fetchone()
    kursor_akbar.close()
    db_akbar.close()
    return render_template('ubah_nilai_akbar.html', n=data_lama)

@app.route('/hapus_nilai_akbar/<id_nilai>')
def hapus_nilai_akbar(id_nilai):
    db_akbar = koneksi_database_akbar()
    kursor_akbar = db_akbar.cursor()
    kursor_akbar.execute("DELETE FROM nilai_akbar WHERE id_nilai=%s", (id_nilai,))
    db_akbar.commit()
    kursor_akbar.close()
    db_akbar.close()
    return redirect(url_for('halaman_utama_akbar'))
@app.route('/cetak_pdf/<nis>')
def cetak_pdf(nis):
    db_akbar = koneksi_database_akbar()
    kursor_akbar = db_akbar.cursor(dictionary=True)

    kursor_akbar.execute("SELECT nis, nama FROM siswa_akbar WHERE nis=%s", (nis,))
    n = kursor_akbar.fetchone()

    sql = """
        SELECT n.semester, n.tahun_ajaran, n.nilai_tugas, n.nilai_uts, n.nilai_uas,
               n.nilai_akhir, n.deskripsi, m.nama_mapel
        FROM nilai_akbar n
        JOIN mapel_akbar m ON n.id_mapel = m.id_mapel
        WHERE n.nis = %s
        ORDER BY n.tahun_ajaran DESC, n.semester DESC, m.nama_mapel ASC
    """
    kursor_akbar.execute(sql, (nis,))
    data_nilai = kursor_akbar.fetchall()

    if data_nilai:
        n["semester"] = data_nilai[0]["semester"]
        th = int(data_nilai[0]["tahun_ajaran"])
        n["tahun_ajaran"] = f"{th}/{th+1}"
        n["deskripsi"] = data_nilai[0]["deskripsi"]
    else:
        n["semester"] = "-"
        n["tahun_ajaran"] = "-"
        n["deskripsi"] = "-"

    kursor_akbar.close()
    db_akbar.close()

    return render_template("cetak_rapot_akbar.html", n=n, data_nilai=data_nilai)

@app.route('/pdf/<nis>')
def generate_pdf_akbar(nis):
    semester = request.args.get("semester", "")
    tahun_ajaran = request.args.get("tahun_ajaran", "")

    db_akbar = koneksi_database_akbar()
    kursor_akbar = db_akbar.cursor(dictionary=True)

    sql = """
        SELECT s.nis, s.nama, s.alamat,
               m.nama_mapel, n.nilai_tugas, n.nilai_uts, n.nilai_uas,
               n.nilai_akhir, n.deskripsi, n.semester, n.tahun_ajaran
        FROM nilai_akbar n
        JOIN siswa_akbar s ON n.nis = s.nis
        JOIN mapel_akbar m ON n.id_mapel = m.id_mapel
        WHERE s.nis = %s
    """
    params = [nis]

    if semester:
        sql += " AND n.semester = %s"
        params.append(semester)

    if tahun_ajaran:
        sql += " AND n.tahun_ajaran = %s"
        params.append(tahun_ajaran)

    sql += " ORDER BY m.nama_mapel ASC"

    kursor_akbar.execute(sql, tuple(params))
    data = kursor_akbar.fetchall()


    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 6, "RAPOR ONLINE SISWA", ln=True, align="C")
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, "SMK 2 CIMAHI", ln=True, align="C")
    pdf.cell(0, 6, "Alamat Sekolah: JL.Kamarung", ln=True, align="C")

    pdf.ln(3)
    pdf.set_line_width(0.6)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    if not data:
        pdf.set_font("DejaVu", "", 11)
        pdf.cell(0, 10, "Data rapor tidak ditemukan.", ln=True)
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=rapot_{nis}.pdf'
        return response

    siswa = data[0]
    semester = siswa.get("semester", "1")
    tahun_ajaran = siswa.get("tahun_ajaran", "2024")

    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 7, "A. IDENTITAS PESERTA DIDIK", ln=True)

    pdf.set_font("DejaVu", "", 10)
    x0 = 10
    y0 = pdf.get_y()
    pdf.rect(x0, y0, 190, 28)

    pdf.set_xy(x0 + 3, y0 + 3)
    pdf.cell(45, 6, "NIS", 0, 0)
    pdf.cell(0, 6, f": {siswa['nis']}", 0, 1)

    pdf.set_x(x0 + 3)
    pdf.cell(45, 6, "Nama", 0, 0)
    pdf.cell(0, 6, f": {siswa['nama']}", 0, 1)

    pdf.set_x(x0 + 3)
    pdf.cell(45, 6, "Alamat", 0, 0)
    pdf.multi_cell(0, 6, f": {siswa['alamat']}")

    pdf.set_xy(x0 + 3, y0 + 21)
    pdf.cell(45, 6, "Semester / Tahun", 0, 0)
    pdf.cell(0, 6, f": {semester} / {tahun_ajaran}", 0, 1)

    pdf.ln(8)

    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 7, "B. CAPAIAN HASIL BELAJAR", ln=True)
    pdf.ln(2)

    w_no = 10
    w_mapel = 50
    w_tugas = 18
    w_uts = 18
    w_uas = 18
    w_akhir = 18
    w_desc = 58

    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("DejaVu", "", 9)

    pdf.cell(w_no, 8, "No", 1, 0, "C", True)
    pdf.cell(w_mapel, 8, "Mata Pelajaran", 1, 0, "C", True)
    pdf.cell(w_tugas, 8, "Tugas", 1, 0, "C", True)
    pdf.cell(w_uts, 8, "UTS", 1, 0, "C", True)
    pdf.cell(w_uas, 8, "UAS", 1, 0, "C", True)
    pdf.cell(w_akhir, 8, "Akhir", 1, 0, "C", True)
    pdf.cell(w_desc, 8, "Catatan/Deskripsi", 1, 1, "C", True)

    pdf.set_font("DejaVu", "", 9)
    total_akhir = 0
    no = 1

    for d in data:
        desc = str(d["deskripsi"])

        max_char = 30
        lines = (len(desc) // max_char) + 1
        row_h = 6 * lines

        pdf.cell(w_no, row_h, str(no), 1, 0, "C")
        pdf.cell(w_mapel, row_h, str(d["nama_mapel"]), 1, 0)
        pdf.cell(w_tugas, row_h, str(d["nilai_tugas"]), 1, 0, "C")
        pdf.cell(w_uts, row_h, str(d["nilai_uts"]), 1, 0, "C")
        pdf.cell(w_uas, row_h, str(d["nilai_uas"]), 1, 0, "C")
        pdf.cell(w_akhir, row_h, str(d["nilai_akhir"]), 1, 0, "C")

        pdf.multi_cell(w_desc, 6, desc, border=1)

        total_akhir += int(d["nilai_akhir"])
        no += 1

    rata2 = total_akhir // len(data)

    pdf.ln(4)
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 7, "C. RANGKUMAN", ln=True)

    pdf.set_font("DejaVu", "", 10)
    pdf.cell(60, 7, "Jumlah Mata Pelajaran", 0, 0)
    pdf.cell(0, 7, f": {len(data)}", 0, 1)

    pdf.cell(60, 7, "Rata-rata Nilai Akhir", 0, 0)
    pdf.cell(0, 7, f": {rata2}", 0, 1)

    if rata2 >= 90:
        predikat = "A (Sangat Baik)"
    elif rata2 >= 80:
        predikat = "B (Baik)"
    elif rata2 >= 70:
        predikat = "C (Cukup)"
    elif rata2 >= 60:
        predikat = "D (Kurang)"
    else:
        predikat = "E (Sangat Kurang)"

    pdf.cell(60, 7, "Predikat", 0, 0)
    pdf.cell(0, 7, f": {predikat}", 0, 1)

    pdf.ln(8)

    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, "Mengetahui,", ln=True, align="R")
    pdf.cell(0, 6, "Wali Kelas", ln=True, align="R")
    pdf.ln(18)
    pdf.cell(0, 6, "(_________________________)", ln=True, align="R")

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=rapot_{nis}.pdf'
    return response


if __name__ == '__main__':
    app.run(debug=True)