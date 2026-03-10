import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Zeytinlik Kontrol Merkezi", page_icon="🚜", layout="wide")

# --- SİSTEM DEĞİŞKENLERİ ---
if "depo_seviyesi" not in st.session_state:
    st.session_state.depo_seviyesi = 65
if "hidrofor_calisiyor" not in st.session_state:
    st.session_state.hidrofor_calisiyor = False

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

# --- 1. SAYFA: ÇİFTLİK GÖZLEM MERKEZİ ---
if sayfa == "Çiftlik Gözlem Merkezi":
    st.title("🛰️ Çiftlik Gözlem Merkezi (Kart-1)")
    
    col_k1_1, col_k1_2, col_k1_3 = st.columns(3)
    with col_k1_1:
        st.metric("Kart-1 Batarya", "%88", delta="Güneşli")
        st.progress(0.88)
    with col_k1_2:
        st.metric("Ana Hat Akışı", "120 L/dk", delta="Stabil")
    with col_k1_3:
        st.metric("Aktif Sensör", "21/21", delta="Tam Kapasite")

    st.divider()
    st.subheader("🌱 Bölgesel Toprak Nemi Haritası")
    
    nem_cols = st.columns(4)
    for i in range(1, 21):
        col_index = (i-1) % 4
        with nem_cols[col_index]:
            nem_degeri = np.random.randint(25, 45)
            status = "🟢" if nem_degeri >= 30 else "🔴"
            st.write(f"{status} **Bölge {i:02d}:** %{nem_degeri}")

# --- 2. SAYFA: SU DEPOSU VE HİDROFOR ---
elif sayfa == "Su Deposu ve Hidrofor":
    st.title("💧 Su Deposu ve Hidrofor Kontrolü (Kart-2)")
    
    col_k2_1, col_k2_2, col_k2_3 = st.columns(3)
    with col_k2_1:
        st.metric("Kart-2 Batarya", "%92", delta="Şarj Oluyor")
        st.progress(0.92)
    with col_k2_2:
        depo_durum = "YETERLİ" if st.session_state.depo_seviyesi > 25 else "DÜŞÜK"
        st.metric("Depo Seviyesi", f"%{st.session_state.depo_seviyesi}", delta=depo_durum)
    with col_k2_3:
        h_text = "ÇALIŞIYOR" if st.session_state.hidrofor_calisiyor else "KAPALI"
        st.metric("Hidrofor Statüsü", h_text)

    st.divider()

    c_sol, c_sag = st.columns([1, 2])
    
    with c_sol:
        st.subheader("💧 Depo Durum Analizi")
        # DİKEY DEPO GÖSTERGESİ (HTML/CSS ile dik hale getirdik)
        st.write(f"Mevcut: **%{st.session_state.depo_seviyesi}**")
        st.markdown(f"""
            <div style="background-color: #e0e0e0; border-radius: 10px; width: 60px; height: 250px; position: relative; margin: auto; border: 2px solid #555;">
                <div style="background-color: #2196F3; width: 100%; height: {st.session_state.depo_seviyesi}%; position: absolute; bottom: 0; border-radius: 0 0 8px 8px; transition: height 0.5s;">
                </div>
            </div>
            <p style="text-align: center; margin-top: 10px;">5000L Depo</p>
        """, unsafe_allow_html=True)

    with c_sag:
        st.subheader("⚙️ Hidrofor Operasyonu")
        if st.session_state.hidrofor_calisiyor:
            st.error("⚡ HİDROFOR ŞU AN AKTİF")
            if st.button("🔴 HİDROFORU DURDUR", use_container_width=True):
                st.session_state.hidrofor_calisiyor = False
                st.rerun()
        else:
            st.success("💤 HİDROFOR BEKLEMEDE")
            if st.button("🟢 HİDROFORU BAŞLAT", use_container_width=True):
                st.session_state.hidrofor_calisiyor = True
                st.rerun()
        
        st.divider()
        st.subheader("📜 Depo Doldurma Geçmişi")
        # Örnek geçmiş verisi tablosu
        gecmis_data = pd.DataFrame({
            "Tarih": ["09.03.2026", "07
