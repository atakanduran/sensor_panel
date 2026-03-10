import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Zeytinlik Ar-Ge | Nem & Akış Takibi", page_icon="📡", layout="wide")

# --- SİSTEM AYARLARI ---
ANA_HAT_SAYISI = 1
AGAC_BOLGE_SAYISI = 20 # 20 farklı bölgeden nem verisi
PIL_YUZDE = 88 

# --- SIDEBAR: GÜÇ VE DURUM ---
with st.sidebar:
    st.title("🎛️ Sistem Sağlığı")
    
    # Pil Seviyesi
    st.write(f"### 🔋 Batarya Durumu: %{PIL_YUZDE}")
    st.progress(PIL_YUZDE / 100)
    st.info(f"📡 Toplam Sensör: {ANA_HAT_SAYISI + AGAC_BOLGE_SAYISI} Adet")
    st.caption(f"Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")
    
    st.divider()
    st.write("📍 **Konum:** İzmir / Bergama")

# --- ANA EKRAN ---
st.title("🚜 Akıllı Saha Gözlem Merkezi")
st.markdown("Ana hat akışı ve 20 farklı bölgedeki toprak nemi durumu.")

# Üst Özet Kartları
c1, c2 = st.columns(2)
with c1:
    # Ana boru akış bilgisi
    st.metric("Ana Boru Akış Durumu", "AKKIŞ VAR" if True else "AKKIŞ YOK", delta="120 L/dk")
with c2:
    # Nem ortalaması
    st.metric("Ortalama Toprak Nemi", "%34", delta="-%2 (Kritik)")

st.divider()

# --- SENSÖR VERİ TABLOSU ---
st.subheader("💧 Saha Veri Paneli")

tabs = st.tabs(["🏗️ Ana Hat Kontrolü", "🌱 Toprak Nemi (20 Bölge)"])

with tabs[0]:
    # Ana Boru Bilgi Ekranı
    ca1, ca2, ca3 = st.columns([1, 1, 2])
    ca1.write("**Hat İsmi**")
    ca2.write("**Akış Onayı**")
    ca3.write("**Sistem Mesajı**")
    
    st.divider()
    
    col_a1, col_a2, col_a3 = st.columns([1, 1, 2])
    col_a1.write("📍 **ANA HAT - 01**")
    # Bilgi kısmı: Artık kapatılabilir bir düğme değil, salt okunur bir bilgi
    col_a2.info("✅ AKIŞ AKTİF")
    col_a3.write("Pompa basıncı stabil, ana boru tam kapasite çalışıyor.")

with tabs[1]:
    # 20 Bölgenin Toprak Nem Verileri
    col_h1, col_h2, col_h3 = st.columns([1, 1, 2])
    col_h1.write("**Bölge No**")
    col_h2.write("**Nem Seviyesi**")
    col_h3.write("**Durum Analizi**")
    st.write("---")

    for i in range(1, AGAC_BOLGE_SAYISI + 1):
        ch1, ch2, ch3 = st.columns([1, 1, 2])
        ch1.write(f"📍 Bölge {i:02d}")
        
        # Simülasyon: Nem değerleri (Örn: %25 ile %45 arası)
        nem_degeri = np.random.randint(25, 45)
        ch2.write(f"**%{nem_degeri}**")
        
        # Durum Analizi (Bilgi Paneli)
        if nem_degeri < 30:
            ch3.warning("⚠️ KRİTİK: Toprak kurumuş, sulama önerilir.")
        else:
            ch3.success("🟢 İDEAL: Nem seviyesi yeterli.")
        
        st.write(" ") # Görsel boşluk

# --- ALT AKSİYONLAR ---
st.divider()
col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("🔄 Verileri Tazele", use_container_width=True):
        st.rerun()
with col_b2:
    st.button("📄 Raporu PDF Olarak İndir (Yakında)", use_container_width=True, disabled=True)
