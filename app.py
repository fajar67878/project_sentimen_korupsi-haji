import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Analisis Sentimen Haji - 5 Slide", layout="wide")

# Daftar kata yang diabaikan dalam WordCloud
STOP = ['dan', 'yang', 'di', 'ke', 'dari', 'ini', 'itu', 'untuk', 'ada', 'adalah', 'dengan', 'yg', 'ga', 'gak', 'aja', 'ya', 'sudah', 'bisa', 'kalau', 'tak', 'banget', 'kok', 'si', 'tapi', 'sama', 'karena', 'jadi', 'mau', 'biar']

@st.cache_resource
def load_resources():
    model = load_model('model_sentimen_haji.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    return model, tokenizer

# --- 2. PROSES DATA (SENTIMEN ASLI) ---
if os.path.exists('model_sentimen_haji.h5') and os.path.exists('data/komentar_haji_bersih.csv'):
    model, tokenizer = load_resources()
    df = pd.read_csv('data/komentar_haji_bersih.csv').dropna(subset=['text_clean'])
    
    with st.spinner('AI sedang memproses data...'):
        sequences = tokenizer.texts_to_sequences(df['text_clean'].astype(str))
        padded = pad_sequences(sequences, maxlen=100)
        df['score'] = model.predict(padded)
        
        # Penentuan Kategori Berdasarkan Skor (Threshold Real)
        def klasifikasi_asli(score):
            if score < 0.48:
                return 'Negatif'
            elif score > 0.52:
                return 'Positif'
            else:
                return 'Netral'
        
        df['sentiment'] = df['score'].apply(klasifikasi_asli)
else:
    st.error("❌ File model atau CSV tidak ditemukan! Pastikan sudah menjalankan scraper dan training.")
    st.stop()

# --- 3. TAMPILAN 5 SLIDE (TAB) ---
st.title(" Laporan Digital: Analisis Sentimen Korupsi Haji")

tabs = st.tabs([
    "  Pendahuluan", 
    "  Statistik Sentimen", 
    "  Analisis Kata (WordCloud)", 
    "  Detail Dataset", 
    "  Uji Coba Model"
])

# --- SLIDE 1: PENDAHULUAN ---
with tabs[0]:
    st.header("1. Pendahuluan Proyek")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tujuan Analisis")
        st.write("""
        Proyek ini bertujuan untuk memetakan opini masyarakat di media sosial mengenai 
        isu dugaan korupsi kuota haji menggunakan algoritma Deep Learning LSTM.
        """)
    with col2:
        st.subheader("Metode Pengumpulan")
        st.write(f"Data dikumpulkan melalui teknik scraping YouTube dengan total data: **{len(df)} komentar**.")
    
    st.info("💡 Tip: Gunakan navigasi tab di atas untuk berpindah halaman laporan.")

# --- SLIDE 2: STATISTIK SENTIMEN ---
with tabs[1]:
    st.header("2. Distribusi Sentimen (Data Riil)")
    st.write("Grafik di bawah menunjukkan persentase sentimen asli hasil deteksi AI:")
    
    counts = df['sentiment'].value_counts().reset_index()
    fig_pie = px.pie(counts, names='sentiment', values='count', 
                     color='sentiment', hole=0.4,
                     color_discrete_map={'Negatif':'#FF4B4B', 'Netral':'#00D4FF', 'Positif':'#00CC96'})
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Keterangan angka
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Negatif", len(df[df['sentiment']=='Negatif']))
    c2.metric("Total Netral", len(df[df['sentiment']=='Netral']))
    c3.metric("Total Positif", len(df[df['sentiment']=='Positif']))

# --- SLIDE 3: WORDCLOUD ---
with tabs[2]:
    st.header("3. Topik yang Paling Sering Muncul")
    cols = st.columns(3)
    
    def buat_wc(data, warna, label):
        if len(data) > 2:
            txt = " ".join(data.astype(str).tolist())
            wc = WordCloud(background_color='white', stopwords=STOP, width=400, height=400, colormap=warna).generate(txt)
            fig, ax = plt.subplots()
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.warning(f"Data {label} tidak cukup untuk WordCloud")

    with cols[0]:
        st.subheader("🔴 Negatif")
        buat_wc(df[df['sentiment'] == 'Negatif']['text_clean'], 'Reds', "Negatif")
    with cols[1]:
        st.subheader("🔵 Netral")
        buat_wc(df[df['sentiment'] == 'Netral']['text_clean'], 'Blues', "Netral")
    with cols[2]:
        st.subheader("🟢 Positif")
        buat_wc(df[df['sentiment'] == 'Positif']['text_clean'], 'Greens', "Positif")

# --- SLIDE 4: DETAIL DATASET ---
with tabs[3]:
    st.header("4. Rekapitulasi Data Komentar")
    st.write("Daftar lengkap komentar beserta skor prediksi AI:")
    st.dataframe(df[['text_clean', 'sentiment', 'score']], use_container_width=True, height=500)
    
    st.download_button(
        label="📥 Download Hasil Analisis (CSV)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='hasil_sentimen_haji.csv',
        mime='text/csv'
    )

# --- SLIDE 5: UJI COBA MODEL ---
with tabs[4]:
    st.header("5. Simulator Klasifikasi Sentimen")
    st.write("Gunakan fitur ini untuk menguji kalimat baru secara langsung:")
    
    user_input = st.text_area("Masukkan Kalimat/Komentar:")
    if user_input:
        with st.spinner('AI sedang berpikir...'):
            test_seq = tokenizer.texts_to_sequences([user_input])
            test_pad = pad_sequences(test_seq, maxlen=100)
            res_score = model.predict(test_pad)[0][0]
            
            if res_score < 0.48:
                st.error(f"Prediksi: **NEGATIF** (Skor: {res_score:.2f})")
            elif res_score > 0.52:
                st.success(f"Prediksi: **POSITIF** (Skor: {res_score:.2f})")
            else:
                st.info(f"Prediksi: **NETRAL** (Skor: {res_score:.2f})")