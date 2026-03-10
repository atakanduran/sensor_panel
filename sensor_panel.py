import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Zeytinlik Ar-Ge | Sensör Ağı", page_icon="📡", layout="wide")

# --- SİSTEM AYARLARI ---
ANA_BORU_SAYISI = 1
DAL_SAYISI = 20
PIL_YUZDE = 88 # Örnek sabit değer, ileride karttan gelecek

# --- SIDEBAR: GÜÇ VE DURUM ---
with st.sidebar:
    st.title("🎛️ Sistem Sağlığı")
    
    # Pil Seviyesi Düzenlemesi
    st.write(f"### 🔋 Batarya Durumu: %{PIL_YUZDE}")
    st.progress(PIL_YUZDE / 100)
    if PIL_YUZDE > 20:
        st.success("Güç Seviyesi: Yeterli")
    else:
        st.warning("DİKKAT: Şarj Ediniz!")
    
    st.divider()
    st.info(f"📡 Toplam Sensör: {ANA_BORU_SAYISI + DAL_SAYISI} Adet")
    st.caption(f"Son Senkronizasyon: {datetime.now().strftime('%H:%M:%S')}")

# --- ANA EKRAN ---
st.title("🚜 Hidrolik Akış Gözlem Merkezi")
st.markdown("Ana boru ve bağlı 20 alt dalın anlık su geçiş kontrolü.")

# Üst Özet Kartları
c1, c2 = st.columns(2)
with c1:
    st.metric("Ana Boru Durumu", "AKKIŞ VAR", delta="120 L/dk")
with c2:
    # Simülasyon: Rastgele 3 dalda sorun varmış gibi gösterelim
    st.metric("Aktif Kılcal Dallar", f"{DAL_SAYISI - 3} / {DAL_SAYISI}", delta="-3 Hata", delta_color="inverse")

st.divider()

# --- BORU VE DAL KONTROL TABLOSU ---
st.subheader("💧 Hat Bazlı Su Onay Sistemi")

# Verileri düzenli göstermek için bir liste oluşturuyoruz
tabs = st.tabs(["🏗️ Ana Hat", "🌿 Kılcal Dallar (1-20)"])

with tabs[0]:
    # Ana Boru Kısmı
    col_a1, col_a2, col_a3 = st.columns([1, 1, 2])
    col_a1.write("**Hat İsmi**")
    col_a2.write("**Su Onayı**")
    col_a3.write("**Durum Notu**")
    
    st.divider()
    
    ca1, ca2, ca3 = st.columns([1, 1, 2])
    ca1.write("📍 **ANA BORU - 01**")
    ca2.toggle("Onay", value=True, key="ana_boru")
    ca3.write("✅ Akış Stabil - Basınç Uygun")

with tabs[1]:
    # 20 Dalın Listelenmesi
    col_h1, col_h2, col_h3 = st.columns([1, 1, 2])
    col_h1.write("**Dal No**")
    col_h2.write("**Su Geçişi**")
    col_h3.write("**Sensör Verisi**")
    st.write("---")

    for i in range(1, DAL_SAYISI + 1):
        ch1, ch2, ch3 = st.columns([1, 1, 2])
        ch1.write(f"🌿 Dal Hattı - {i:02d}")
        
        # Su Onay Butonu (Toggle)
        # Simülasyon: İlk 17 tanesi açık, son 3 tanesi kapalı başlasın
        is_active = True if i <= 17 else False
        status = ch2.toggle("Su Var", value=is_active, key=f"dal_{i}")
        
        if status:
            ch3.write("🟢 Geçiş Onaylandı (Normal)")
        else:
            ch3.write("🔴 **AKKIŞ YOK / TIKANIKLIK?**")
        
        st.write(" ") # Satır arası boşluk

# --- ALT BİLGİ ---
st.divider()
if st.button("🔄 Tüm Sensörleri Yeniden Tara"):
    st.toast("Sensör ağ taranıyor...", icon="📡")
