import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Veri setini oku
df = pd.read_csv("trafik.csv")

# 2. Girdi (X) ve çıktıyı (y) ayır
X = df[["saat", "gun", "hava"]]
y = df["etiket"]

# 3. Etiketi sayıya çevir (yuksek=2, orta=1, dusuk=0)
le = LabelEncoder()
y = le.fit_transform(y)

# 4. Modeli eğit
model = DecisionTreeClassifier()
model.fit(X, y)

# 5. Modeli ve encoder'ı kaydet
joblib.dump(model, "model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("Model başarıyla eğitildi ve kaydedildi!")
print("Sınıflar:", le.classes_)