import pandas as pd
import numpy as np
import pickle
import os
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

# 1. LOAD DATA
if not os.path.exists('data/komentar_haji_bersih.csv'):
    print("❌ File data tidak ditemukan!")
else:
    df = pd.read_csv('data/komentar_haji_bersih.csv').dropna(subset=['text_clean'])
    X = df['text_clean'].astype(str)
    
    # --- STRATEGI LABELING LEBIH LUAS ---
    negatif_words = ['korupsi', 'maling', 'parah', 'kecewa', 'zalim', 'hancur', 'bobrok', 'rugi', 'penjara', 'salah', 'hakim', 'kpk', 'tangkap', 'tahanan', 'tersangka', 'jual', 'mahal', 'sulit', 'beban']
    positif_words = ['bagus', 'setuju', 'semangat', 'lancar', 'amanah', 'terima kasih', 'mantap', 'alhamdulillah', 'berkah', 'adil', 'sukses', 'baik', 'bantu', 'mudah', 'senang', 'keren']

    def berikan_label(teks):
        teks = teks.lower()
        score = 0
        for w in negatif_words:
            if w in teks: score -= 1
        for w in positif_words:
            if w in teks: score += 1
        
        if score < 0: return 0  # Negatif
        if score > 0: return 1  # Positif
        return np.random.randint(0, 2) # Netral/Random

    y = X.apply(berikan_label).values

    # 2. TOKENIZING & PADDING
    max_words = 5000
    tokenizer = Tokenizer(num_words=max_words, lower=True)
    tokenizer.fit_on_texts(X)
    X_seq = tokenizer.texts_to_sequences(X)
    X_pad = pad_sequences(X_seq, maxlen=100)

    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # 3. MODEL LSTM
    model = Sequential([
        Embedding(max_words, 128),
        LSTM(64, dropout=0.3, recurrent_dropout=0.3),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    print("🧠 Training ulang model dengan logika baru...")
    model.fit(X_pad, y, epochs=10, batch_size=32, validation_split=0.2)
    model.save('model_sentimen_haji.h5')
    print("✅ SELESAI! Jalankan app.py sekarang.")