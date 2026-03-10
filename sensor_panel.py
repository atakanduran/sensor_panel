import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Zeytinlik Kontrol Merkezi", page_icon="🚜", layout="wide")

# --- TELEGRAM MESAJ FONKSİYONU ---
def send_telegram_msg(mesaj):
    try:
        # Secrets'tan bilgileri çekiyoruz
        token = st.secrets["TELEGRAM_TOKEN"]
        chat_id = st.secrets["CHAT_ID"]
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": mesaj}
        response = requests.get(url, params=params)
        
        # Eğer hata varsa ekranda göster (Hata ayıklama için)
        if response.status_code != 200:
            st.error(f"Telegram Hatası: {response.text}")
        else:
            st.toast("Telegram mesajı başarıyla gönderildi! ✅")
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e} - Lütfen Secrets ayarlarını kontrol edin.")

# --- SİSTEM DEĞİŞKENLERİ ---
if "depo_seviyesi" not in st.session_state:
    st.session_state.depo_seviyesi = 65
if "hidrofor_calisiyor" not in st.session_state:
    st.session_state.hidrofor_calisiyor = False

# Simülasyon Pil Değerleri (Kartlar için)
KART1_PIL = 85
KART2_PIL = 9 # Test için %10'un altında (Kritik)

# --- SOL MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("🚜 Yönetim Paneli")
    st.info("📍 **Konum:** İzmir / Bergama")
    st.divider()
    
    st.write("### 🖥️ Ekran Seçimi")
    sayfa = st.radio(
        "Görüntülemek istediğiniz merkezi seçin:",
        ["Çiftlik Gözlem Merkezi", "Su Deposu ve Hidrofor"]
    )
    
    st.divider()
    st.caption(f"Sistem Saati: {datetime.now().strftime('%H:%M')}")

# --- 1. SAYFA: ÇİFTLİK GÖZLEM MERKEZİ (KART-1) ---
if sayfa == "Çiftlik Gözlem Merkezi":
    st.title("🛰️ Çiftlik Gözlem Merkezi (Kart-1)")
    
    # Kart-1 Durum Metrikleri
    col_k1_1, col_k1_2, col_k1_3 = st.columns(3)
    with col_k1_1:
        pil_renk1 = "normal" if KART1_PIL > 10 else "inverse"
        st.metric("Kart-1 Batarya", f"%{KART1_PIL}", delta="DÜŞÜK" if KART1_PIL <= 10 else "Normal", delta_color=pil_renk1)
        st.progress(KART1_PIL / 100)
    with col_k1_2:
        st.metric("Ana Hat Akışı", "120 L/dk", delta="Stabil")
    with col_k1_3:
        st.metric("Aktif Sensör", "21/21", delta="Tam Kapasite")

    st.divider()
    
    st.subheader("🌱 Bölgesel Toprak Nemi Haritası")
    st.write("20 bölgedeki sensörlerden gelen anlık nem verileri:")
    
    # Nem Verilerini 4 Sütunda Listeleme
    nem_cols = st.columns(4)
    for i in range(1, 21):
        col_index = (i-1) % 4
        with nem_cols[col_index]:
            nem_v = np.random.randint(25, 45)
            status_icon = "🟢" if nem_v >= 30 else "🔴"
            st.write(f"{status_icon} **Bölge {i:02d}:** %{nem_v}")

# --- 2. SAYFA: SU DEPOSU VE HİDROFOR (KART-2) ---
elif sayfa == "Su Deposu ve Hidrofor":
    st.title("💧 Su Deposu ve Hidrofor Kontrolü (Kart-2)")
    
    # Kart-2 Durum Metrikleri
    col_k2_1, col_k2_2, col_k2_3 = st.columns(3)
    with col_k2_1:
        pil_renk2 = "normal" if KART2_PIL > 10 else "inverse"
        st
