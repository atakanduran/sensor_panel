import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Zeytinlik Ar-Ge | Modüler Kontrol", page_icon="📡", layout="wide")

# --- SİSTEM DEĞİŞKENLERİ (Session State) ---
if "depo_seviyesi" not in st.session_state:
    st.session_state.depo_seviyesi = 65
if "hidrofor_calisiyor" not in st.session_state:
    st.session_state.hidrofor_calisiyor = False

# --- SOL MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("🚜 Sistem Yönetimi")
    st.info("📍 **Konum:** İzmir / Bergama")
    st.divider()

    # 1. ÇEKMECE: ÇİFTLİK GÖZLEM MERKEZİ (KART-1)
    with st.expander("📊 Çiftlik Gözlem Merkezi", expanded=True):
        st.write("### 🔋 Kart-1 Batarya: %88")
        st.progress(0.88)
        st.caption("Sensör Ağı Kontrol Ünitesi")
        st.write("---")
        st.write("📡 **Aktif Sensör:** 21 Adet")
        st.write("📶 **Sinyal:** Güçlü (-65 dBm)")

    # 2. ÇEKMECE: SU DEPOSU & HİDROFOR (KART-2)
    with st.expander("💧 Su Deposu ve Hidrofor", expanded=False):
        # Kart-2 Pil Durumu
        st.write("### 🔋 Kart-2 Batarya: %92")
        st.progress(0.92)
        st.caption("Depo & Pompa Kontrol Ünitesi")
        st.write("---")
        
        # Depo Görseli
        st.write("**Depo Doluluk: %" + str(st.session_state.depo_seviyesi) + "**")
        st.progress(st.session_state.depo_seviyesi / 100)
        
        st.divider()
        
        # Hidrofor Kontrolü
        st.write("⚙️ **Hidrofor Kontrolü**")
        if st.session_state.hidrofor_calisiyor:
            st.warning("⚡ Hidrofor ÇALIŞIYOR")
            if st.button("🔴 DURDUR", key="stop_h"):
                st.session_state.hidrofor_calisiyor = False
                st.rerun()
        else:
            st.success("💤 Hidrofor BEKLEMEDE")
            if st.button("🟢 BAŞLAT", key="start_h"):
                st.session_state.hidrofor_calisiyor = True
                st.rerun()

    st.divider()
    st.caption(f"Son Senkronizasyon: {datetime.now().strftime('%H:%M:%S')}")

# --- ANA EKRAN ---
st.title("🛰️ Akıllı Saha Operasyon Merkezi")

# Üst Metrikler
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Ana Hat Akışı", "120 L/dk", delta="Normal")
with m2:
    st.metric("Toprak Nemi (Ort.)", "%34", delta="-%2")
with m3:
    h_durum = "AKTİF" if st.session_state.hidrofor_calisiyor else "KAPALI"
    st.metric("Hidrofor Statüsü", h_durum)

st.divider()

# Sekmeli Detay Paneli
tab1, tab2 = st.tabs(["🌱 Bölgesel Nem Haritası", "🗠 Sistem Analizi"])

with tab1:
    st.subheader("20 Bölge Nem Raporu")
    cols = st.columns(2) # Verileri iki sütuna bölelim ki sayfa çok uzamasın
    
    for i in range(1, 21):
        target_col = cols[0] if i <= 10 else cols[1]
        with target_col:
            nem = np.random.randint(25, 45)
            status_color = "🟢" if nem >= 30 else "🟡"
            st.write(f"{status_color} **Bölge {i:02d}:** %{nem}")

with tab2:
    st.write("Burada ileride sensörlerden gelen haftalık grafikler yer alacak.")
