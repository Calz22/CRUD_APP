from flask import Flask, render_template, request, redirect, url_for
from database import SessionLocal, engine, Base
from models import Mahasiswa

app = Flask(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route('/')
def index():
    db = next(get_db())
    mahasiswa = db.query(Mahasiswa).all()
    db.close()
    return render_template('index.html', mahasiswa=mahasiswa)

@app.route('/add', methods=['GET', 'POST'])
def add_mahasiswa():
    if request.method == 'POST':
        db = next(get_db())
        mahasiswa_baru = Mahasiswa(
            nim=request.form['nim'],
            nama=request.form['nama'],
            jurusan=request.form['jurusan']
        )
        db.add(mahasiswa_baru)
        db.commit()
        db.close()
        return redirect(url_for('index'))
    return render_template('add_mahasiswa.html')

# @app.route('/edit', methods=['GET', 'POST'])
# def edit_mahasiswa():
#     if request.method == 'POST':
#         db = next(get_db())
#         mahasiswa_baru = Mahasiswa(
#             nim=request.form['nim'],
#             nama=request.form['nama'],
#             jurusan=request.form['jurusan']
#         )
#         db.edit(mahasiswa_baru)
#         db.commit()
#         db.close()
#         return redirect(url_for('index'))
#     return render_template('edit_mahasiswa.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_mahasiswa(id):
    db = next(get_db())  # Ambil sesi database
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id == id).first()  # Cari mahasiswa berdasarkan ID
    
    if not mahasiswa:
        db.close()
        return "Mahasiswa tidak ditemukan", 404

    if request.method == 'POST':
        mahasiswa.nim = request.form['nim']
        mahasiswa.nama = request.form['nama']
        mahasiswa.jurusan = request.form['jurusan']
        db.commit()  # Simpan perubahan
        db.close()
        return redirect(url_for('index'))

    db.close()
    return render_template('edit_mahasiswa.html', mahasiswa=mahasiswa)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_mahasiswa(id):
    db = next(get_db())  # Ambil sesi database
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id == id).first()  # Cari mahasiswa berdasarkan ID
    
    if not mahasiswa:
        db.close()
        return "Mahasiswa tidak ditemukan", 404

    if request.method == 'POST':
        db.delete(mahasiswa)  # Hapus data dari database
        db.commit()
        db.close()
        return redirect(url_for('index'))

    db.close()
    return render_template('delete_mahasiswa.html', mahasiswa=mahasiswa)


if __name__ == '__main__':
    try:
        # Buat tabel
        Base.metadata.create_all(bind=engine)
        print("Tabel berhasil dibuat")
    except Exception as e:
        print(f"Kesalahan: {e}")
    
    app.run(debug=True)