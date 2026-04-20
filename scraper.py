from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT
import pandas as pd
import os

# Buat folder data jika belum ada
if not os.path.exists('data'):
    os.makedirs('data')

downloader = YoutubeCommentDownloader()

# Daftar URL video berita terkait Korupsi/Pansus Haji
video_links = [
    'https://youtu.be/1VHW1CW8Cqg?si=DYSmDnLc31tbWHWG', 
    'https://youtu.be/nBM9tN0VawU?si=Qiw44kfeM6yvJfUu',
    'https://youtu.be/dYLZc6QbpSU?si=sB8rWC5LmBkF1-hO',
    'https://youtu.be/nBM9tN0VawU?si=IdxbfPYun9XJT0QG',
    'https://youtu.be/dYLZc6QbpSU?si=X50CRHwvFT2eQVVo',
    'https://youtu.be/Fdo57B_VV7o?si=DjFDt6oaZVHwnjpF',
    'https://youtu.be/Eb7KmC6va2s?si=t51oQFr_UFLxB7WG',
    'https://youtu.be/Urh5KKq68P4?si=tfemj2nEhjAolQx_',
    'https://youtu.be/mx3juotGxjI?si=R-F7mhcK1BnbQji-',
    'https://youtu.be/PMx3y8T_k6c?si=xRxbIMrRR7wMLK9q',
    'https://youtu.be/mt1EQy4aaZc?si=CfhlVPHisTmHwyGb',
    'https://youtu.be/czrB4FP5EHM?si=sYOBVmXTymVnkjpB',
    'https://youtu.be/vxYg_daEW6E?si=T1VGptcts2etZ2Yk',
    'https://youtu.be/_sN_SaQ4kYw?si=luffqZZC9nJ2AMpI',
    'https://youtu.be/mF-PBYPYMoA?si=A_qoX-flqy_plLVH',
    'https://youtu.be/c4bB7rL-jDk?si=2GNrc4BLyvPPVALB',
    'https://youtu.be/icfZrltfcz4?si=G8itSXZbxtswAU0b',
    'https://youtu.be/MFukJf9lVWc?si=mYcT3j0Ru2TMFAAG',
    'https://youtu.be/0bNTZSaZHxE?si=O-vtGlIv7YctWZ11',
    'https://youtu.be/O0NsmvLyv2U?si=qepjYsM8pyH4Fi81',
    'https://youtu.be/JDaH3950N7I?si=ZN4P-gzuS2Hbk7vP',
    'https://youtu.be/C2Gqx1BEw5U?si=UrFbeq3fvf-POlMx',
    'https://youtu.be/_sN_SaQ4kYw?si=zi3gHzqYWKLeCLGh',
    'https://youtu.be/mF-PBYPYMoA?si=ROoR4jLPrAg5Q7HA',
    'https://youtu.be/c4bB7rL-jDk?si=-7d-0Kmgm-kIItu6',
    'https://youtu.be/D4dLXPxXOb0?si=rL0LD7t_DQSOsrJ7',
    'https://youtu.be/LeEzteTxqSY?si=sit60XX8UeQOM45V',
    'https://youtu.be/0dGDcBPnsN0?si=IIz4v6b8wvXWEEnG',
    'https://youtu.be/ETWh0VpEM4s?si=OQMVow03F_MQXL3r',
    # Silakan tambah link video lain di sini
]

all_comments = []
target_total = 10000

print(" Memulai proses scraping...")

for url in video_links:
    if len(all_comments) >= target_total:
        break
        
    print(f"Sedang mengambil komentar dari: {url}")
    try:
        comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_RECENT)
        for comment in comments:
            all_comments.append({
                'text': comment['text'],
                'author': comment['author'],
                'time': comment['time']
            })
            
            if len(all_comments) % 500 == 0:
                print(f" Terkumpul: {len(all_comments)} komentar")
                
            if len(all_comments) >= target_total:
                break
    except Exception as e:
        print(f" Gagal mengambil video {url}: {e}")

# Simpan ke CSV
df = pd.DataFrame(all_comments)
df.to_csv('data/komentar_haji_10k.csv', index=False, encoding='utf-8')
print(f" SELESAI! {len(all_comments)} data disimpan di folder data/komentar_haji_10k.csv")