import pandas as pd
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# 1. Load Data
df = pd.read_csv('data/komentar_haji_10k.csv')

# 2. Inisialisasi Stemmer Sastrawi (untuk mengubah ke kata dasar)
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def bersihkan_teks(text):
    # Ubah ke huruf kecil
    text = text.lower()
    # Hapus URL/Link
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Hapus karakter khusus dan angka (hanya sisakan huruf)
    text = re.sub(r'[^a-z\s]', '', text)
    # Stemming (opsional, bisa agak lambat untuk 10rb data)
    # text = stemmer.stem(text) 
    return text

print("🧹 Sedang membersihkan teks...")
df['text_clean'] = df['text'].apply(bersihkan_teks)

# Simpan hasil bersihnya
df.to_csv('data/komentar_haji_bersih.csv', index=False)
print("✅ Preprocessing selesai! File disimpan ke data/komentar_haji_bersih.csv")