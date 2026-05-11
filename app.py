from flask import Flask, render_template, request
import joblib
import sqlite3

app = Flask(__name__)

# Modeli yükle
model = joblib.load("model.pkl")
le = joblib.load("label_encoder.pkl")

# Veritabanını hazırla
def veritabani_olustur():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tahminler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            saat INTEGER,
            gun INTEGER,
            hava INTEGER,
            sonuc TEXT
        )
    """)
    conn.commit()
    conn.close()

veritabani_olustur()

# Ana sayfa
@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tahminler ORDER BY id DESC")
    gecmis = cursor.fetchall()
    conn.close()
    return render_template("index.html", gecmis=gecmis)

# Tahmin sayfası
@app.route("/tahmin", methods=["POST"])
def tahmin():
    saat = int(request.form["saat"])
    gun = int(request.form["gun"])
    hava = int(request.form["hava"])

    # Modelden tahmin al
    tahmin_sayisal = model.predict([[saat, gun, hava]])[0]
    sonuc = le.inverse_transform([tahmin_sayisal])[0]

    # Veritabanına kaydet
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tahminler (saat, gun, hava, sonuc) VALUES (?, ?, ?, ?)",
                   (saat, gun, hava, sonuc))
    conn.commit()

    # Geçmiş tahminleri de çek
    cursor.execute("SELECT * FROM tahminler ORDER BY id DESC")
    gecmis = cursor.fetchall()
    conn.close()

    return render_template("index.html", sonuc=sonuc, saat=saat, gun=gun, hava=hava, gecmis=gecmis)

if __name__ == "__main__":
    app.run(debug=True)