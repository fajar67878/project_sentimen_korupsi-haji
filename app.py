import streamlit as st
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.set_page_config(page_title="Analisis Sentimen Haji", layout="wide")

# Fungsi Analisis Sentimen Sederhana
def get_sentiment(text):
    text = str(text).lower().strip()
    
    # 1. Daftar Kata Kunci Negatif (Sentimen Buruk/Marah)
    kata_negatif = [
        'korupsi', 'maling', 'penjara', 'buruk', 'kecewa', 'parah', 'rugi', 
        'dzalim', 'zalim', 'hancur', 'bobrok', 'mahal', 'susah', 'pungli',
        'salah', 'tidak adil', 'miris', 'memalukan', 'geram', 'usut', 'tuntas'
    ]
    
    # 2. Daftar Kata Kunci Positif (Dukungan/Harapan)
    kata_positif = [
        'bagus', 'setuju', 'mantap', 'alhamdulillah', 'baik', 'dukung', 
        'semangat', 'hebat', 'solusi', 'adil', 'transparan', 'terima kasih',
        'keren', 'positif', 'maju', 'berantas', 'amin', 'semoga'
    ]
    
    # 3. Logika Klasifikasi
    # Cek Negatif dulu
    if any(word in text for word in kata_negatif):
        return 'Negatif'
    # Cek Positif
    elif any(word in text for word in kata_positif):
        return 'Positif'
    # 4. Jika tidak ada kata kunci di atas, baru cek pakai TextBlob
    else:
        analysis = TextBlob(text)
        # Kita perkecil jangkauan Netral agar lebih sensitif
        if analysis.sentiment.polarity < -0.05:
            return 'Negatif'
        elif analysis.sentiment.polarity > 0.05:
            return 'Positif'
        else:
            # Jika benar-benar datar atau tidak terdeteksi, baru Netral
            return 'Netral'

# --- LOAD DATA ---
file_path = 'data/komentar_haji_bersih.csv'
if os.path.exists(file_path):
    df = pd.read_csv(file_path).dropna(subset=['text_clean'])
    # Hitung sentimen secara otomatis tanpa model .h5
    df['sentiment'] = df['text_clean'].apply(get_sentiment)
else:
    st.error("File CSV tidak ditemukan di folder data/")
    st.stop()

# --- TAMPILAN 5 TAB ---
st.title("Laporan Digital: Analisis Sentimen Korupsi Haji")
tabs = st.tabs([" Pendahuluan", " Statistik", " WordCloud", " Dataset", " Uji Publik"])

with tabs[0]:
    st.header("1. Pendahuluan")
    st.write(f"Analisis ini menggunakan data hasil scraping YouTube sejumlah **{len(df)} komentar**.")

with tabs[1]:
    st.header("2. Distribusi Sentimen")
    counts = df['sentiment'].value_counts().reset_index()
    fig = px.pie(counts, names='sentiment', values='count', hole=0.4,
                 color='sentiment', color_discrete_map={'Negatif':'#FF4B4B', 'Netral':'#00D4FF', 'Positif':'#00CC96'})
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.header("3. Topik Utama (WordCloud)")
    col1, col2, col3 = st.columns(3)
    for i, sent in enumerate(['Negatif', 'Netral', 'Positif']):
        data = df[df['sentiment'] == sent]['text_clean']
        if not data.empty:
            wc = WordCloud(background_color='white').generate(" ".join(data))
            fig, ax = plt.subplots()
            ax.imshow(wc)
            ax.axis('off')
            with [col1, col2, col3][i]:
                st.subheader(sent)
                st.pyplot(fig)

with tabs[3]:
    st.header("4. Rekapitulasi Data")
    st.dataframe(df[['text_clean', 'sentiment']], use_container_width=True)

with tabs[4]:
    st.header("5. Uji Sentimen Baru")
    input_user = st.text_input("Masukkan komentar untuk dicoba:")
    if input_user:
        hasil = get_sentiment(input_user)
        st.write(f"Hasil Analisis: **{hasil}**")