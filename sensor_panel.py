import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Zeytinlik Ar-Ge | Akıllı Su Yönetimi", page_icon="💧", layout="wide")

# --- SİSTEM DEĞİŞKENLERİ (İleride Veritabanından Gelecek) ---
if "depo_seviyesi" not in st.session_state:
    st.session_state.depo_seviyesi = 65  # Başlangıçta %65 dolu
if "hidrofor_calisiyor" not in st.session_state:
    st.session_state.hidrofor_calisiyor = False

AGAC_BOLGE_SAYISI = 20
PIL_YUZDE = 88 

# --- SIDEBAR: KONTROL VE DURUM ---
with st.sidebar:
    st.title("🎛️ Sistem Sağlığı")
    
    # Konum Bilgisi
    st.info("📍 **Konum:** İzmir / Bergama")
    
    # Pil Seviyesi
    st.write(f"### 🔋 Batarya Durumu: %{PIL_YUZDE}")
    st.progress(PIL_YUZDE / 100)
    
    st.divider()
    
    # Toplam Sensör Bilgisi
    st.write(f"📡 **Toplam Sensör:** {AGAC_BOLGE_SAYISI + 1} Adet")
    
    # DEPO GÖSTERGESİ (Görselleştirilmiş)
    st.write("### 💧 Su Deposu Seviyesi")
    # Depo doluluk oranına göre renk değiştirme
    depo_renk = "green" if st.session_state.depo_seviyesi > 30 else "red"
    st.subheader(f":{depo_renk}[%{st.session_state.depo_seviyesi}]")
    st.progress(st.session_state.depo_seviyesi / 100)
    st.caption("5000 Litrelik Ana Depo")

    st.divider()

    # HİDROFOR KONTROLÜ (Yeraltı Suyu Çekme)
    st.write("### ⚙️ Hidrofor Kontrolü")
    if st.session_state.hidrofor_calisiyor:
        st.warning("⚡ Hidrofor Çalışıyor: Su Çekiliyor...")
        if st.button("🔴 HİDROFORU DURDUR", use_container_width=True):
            st.session_state.hidrofor_calisiyor = False
            st.rerun()
    else:
        st.success("💤 Hidrofor Beklemede")
        if st.button("🟢 HİDROFORU BAŞLAT", use_container_width=True):
            st.session_state.hidrofor_calisiyor = True
            st.rerun()
    
    st.divider()
    st.caption(f"Son Veri Akışı: {datetime.now().strftime('%H:%M:%S')}")

# --- ANA EKRAN ---
st.title("🚜 Akıllı Saha Gözlem Merkezi")
st.markdown("Ana hat akışı, depo yönetimi ve 20 bölgedeki toprak nemi durumu.")

# Üst Özet Kartları
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Ana Boru Durumu", "AKIŞ VAR", delta="120 L/dk")
with c2:
    st.metric("Ortalama Nem", "%34", delta="-%2", delta_color="inverse")
with c3:
    status_text = "ÇALIŞIYOR" if st.session_state.hidrofor_calisiyor else "KAPALI"
    st.metric("Hidrofor Durumu", status_text)

st.divider()

# --- SENSÖR VERİ TABLOSU ---
tabs = st.tabs(["🏗️ Hat ve Depo Analizi", "🌱 Toprak Nemi (20 Bölge)"])

with tabs[0]:
    col_a1, col_a2, col_a3 = st.columns([1, 1, 2])
    col_a1.write("**Birim**")
    col_a2.write("**Durum**")
    col_a3.write("**Sistem Mesajı**")
    st.divider()
    
    # Ana Hat Bilgisi
    row1_c1, row1_c2, row1_c3 = st.columns([1, 1, 2])
    row1_c1.write("📍 **ANA HAT - 01**")
    row1_c2.info("✅ AKIŞ AKTİF")
    row1_c3.write("Basınç dengeli, filtreler temiz.")

    # Depo Bilgisi
    row2_c1, row2_c2, row2_c3 = st.columns([1, 1, 2])
    row2_c1.write("💧 **ANA DEPO**")
    if st.session_state.depo_seviyesi < 20:
        row2_c2.error("❌ SEVİYE DÜŞÜK")
    else:
        row2_c2.success("✅ SEVİYE YETERLİ")
    row2_c3.write(f"Mevcut miktar: {5000 * (st.session_state.depo_seviyesi/100):.0f} Litre")

with tabs[1]:
    # 20 Bölge Nem Verileri
    col_h1, col_h2, col_h3 = st.columns([1, 1, 2])
    col_h1.write("**Bölge No**")
    col_h2.write("**Nem Seviyesi**")
    col_h3.write("**Durum Analizi**")
    st.write("---")

    for i in range(1, AGAC_BOLGE_SAYISI + 1):
        ch1, ch2, ch3 = st.columns([1, 1, 2])
        ch1.write(f"📍 Bölge {i:02d}")
        nem_degeri = np.random.randint(25, 45) # Simülasyon verisi
        ch2.write(f"**%{nem_degeri}**")
        
        if nem_degeri < 30:
            ch3.warning("⚠️ KRİTİK: Sulama önerilir.")
        else:
            ch3.success("🟢 İDEAL: Nem yeterli.")
