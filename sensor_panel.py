import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Zeytinlik Kontrol Merkezi", page_icon="浸", layout="wide")

# --- TELEGRAM MESAJ FONKSİYONU (HATA AYIKLAMALI) ---
def send_telegram_msg(mesaj):
    try:
        # Secrets kontrolü
        if "TELEGRAM_TOKEN" not in st.secrets or "CHAT_ID" not in st.secrets:
            st.error("❌ HATA: Secrets (Token veya ID) bulunamadı!")
            return

        token = st.secrets["TELEGRAM_TOKEN"]
        chat_id = st.secrets["CHAT_ID"]
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": mesaj}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            st.toast("Telegram mesajı başarıyla gönderildi! ✅")
        else:
            # HATAYI SABİT TUTMAK İÇİN SESSION STATE KULLANIYORUZ
            st.session_state.son_hata = f"🚫 Telegram Reddeti (Hata {response.status_code}): {response.text}"
            
    except Exception as e:
        st.session_state.son_hata = f"⚠️ Bağlantı Hatası: {str(e)}"

# --- SİSTEM DEĞİŞKENLERİ ---
if "depo_seviyesi" not in st.session_state:
    st.session_state.depo_seviyesi = 65
if "hidrofor_calisiyor" not in st.session_state:
    st.session_state.hidrofor_calisiyor = False
if "son_hata" not in st.session_state:
    st.session_state.son_hata = None

# Simülasyon Pil Değerleri
KART1_PIL = 85
KART2_PIL = 9 

# --- SOL MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("🚜 Yönetim Paneli")
    st.info("📍 **Konum:** İzmir / Bergama")
    st.divider()
    
    sayfa = st.radio("Ekran Seçimi:", ["Çiftlik Gözlem Merkezi", "Su Deposu ve Hidrofor"])
    
    # HATA MESAJI VARSA BURADA GÖSTER (SABİT KALIR)
    if st.session_state.son_hata:
        st.error(st.session_state.son_hata)
        if st.button("Hata Mesajını Temizle"):
            st.session_state.son_hata = None
            st.rerun()

# --- 1. SAYFA: ÇİFTLİK GÖZLEM MERKEZİ ---
if sayfa == "Çiftlik Gözlem Merkezi":
    st.title("🛰️ Çiftlik Gözlem Merkezi (Kart-1)")
    
    col_k1_1, col_k1_2, col_k1_3 = st.columns(3)
    with col_k1_1:
        pil_renk1 = "normal" if KART1_PIL > 10 else "inverse"
        st.metric("Kart-1 Batarya", f"%{KART1_PIL}", delta="DÜŞÜK" if KART1_PIL <= 10 else "Normal", delta_color=pil_renk1)
        st.progress(KART1_PIL / 100)
    with col_k1_2:
        st.metric("Ana Hat Akışı", "120 L/dk")
    with col_k1_3:
        st.metric("Aktif Sensör", "21/21")

    st.divider()
    st.subheader("🌱 Bölgesel Toprak Nemi Haritası")
    nem_cols = st.columns(4)
    for i in range(1, 21):
        with nem_cols[(i-1) % 4]:
            nem_v = np.random.randint(25, 45)
            st.write(f"{'🟢' if nem_v >= 30 else '🔴'} **Bölge {i:02d}:** %{nem_v}")

# --- 2. SAYFA: SU DEPOSU VE HİDROFOR ---
elif sayfa == "Su Deposu ve Hidrofor":
    st.title("💧 Su Deposu ve Hidrofor Kontrolü (Kart-2)")
    
    col_k2_1, col_k2_2, col_k2_3 = st.columns(3)
    with col_k2_1:
        pil_renk2 = "normal" if KART2_PIL > 10 else "inverse"
        st.metric("Kart-2 Batarya", f"%{KART2_PIL}", delta="KRİTİK" if KART2_PIL <= 10 else "Normal", delta_color=pil_renk2)
        st.progress(KART2_PIL / 100)
            
    with col_k2_2:
        st.metric("Depo Seviyesi", f"%{st.session_state.depo_seviyesi}")
    with col_k2_3:
        st.metric("Hidrofor", "ÇALIŞIYOR" if st.session_state.hidrofor_calisiyor else "KAPALI")

    st.divider()
    c_sol, c_sag = st.columns([1, 2])
    
    with c_sol:
        st.subheader("💧 Depo Seviyesi")
        st.markdown(f"""
            <div style="background-color: #f0f0f0; border: 2px solid #555; border-radius: 10px; width: 70px; height: 250px; position: relative; margin: auto;">
                <div style="background-color: #2196F3; width: 100%; height: {st.session_state.depo_seviyesi}%; position: absolute; bottom: 0; border-radius: 0 0 8px 8px;"></div>
            </div>
            <p style="text-align: center; font-weight: bold; margin-top: 10px;">%{st.session_state.depo_seviyesi}<br>5000L Depo</p>
        """, unsafe_allow_html=True)

    with c_sag:
        st.subheader("⚙️ Hidrofor Operasyonu")
        if st.session_state.hidrofor_calisiyor:
            st.error("⚡ HİDROFOR ŞU AN AKTİF")
            if st.button("🔴 HİDROFORU DURDUR", use_container_width=True):
                st.session_state.hidrofor_calisiyor = False
                send_telegram_msg("✅ Bilgi: Hidrofor durduruldu.")
                st.rerun()
        else:
            st.success("💤 HİDROFOR BEKLEMEDE")
            if st.button("🟢 HİDROFORU BAŞLAT", use_container_width=True):
                st.session_state.hidrofor_calisiyor = True
                send_telegram_msg("⚡ Uyarı: Hidrofor başlatıldı!")
                st.rerun()
