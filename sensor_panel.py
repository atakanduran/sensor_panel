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
    
    # MODÜL SEÇİMİ (Radyo Buton ile Sayfa Değiştirme)
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
    
    # Kart-1 Üst Bilgi Alanı
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
    st.write("20 farklı noktadaki sensörlerden gelen anlık nem verileri:")
    
    # Nem Verilerini 4 Sütunda Gösterelim (Daha derli toplu)
    nem_cols = st.columns(4)
    for i in range(1, 21):
        col_index = (i-1) % 4
        with nem_cols[col_index]:
            nem_degeri = np.random.randint(25, 45)
            status = "🟢" if nem_degeri >= 30 else "🔴"
            st.write(f"{status} **Bölge {i:02d}:** %{nem_degeri}")

# --- 2. SAYFA: SU DEPOSU VE HİDROFOR (KART-2) ---
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
        st.metric("Hidrofor Durumu", h_text)

    st.divider()

    # Depo Görselleştirme ve Pompa Kontrolü
    c_sol, c_sag = st.columns([1, 1])
    
    with c_sol:
        st.subheader("💧 Depo Durum Analizi")
        st.write(f"Mevcut Miktar: **{5000 * (st.session_state.depo_seviyesi/100):.0f} Litre**")
        st.progress(st.session_state.depo_seviyesi / 100)
        st.image("https://img.icons8.com/clouds/200/water-tank.png", width=150) # Temsili depo iconu

    with c_sag:
        st.subheader("⚙️ Hidrofor Operasyonu")
        if st.session_state.hidrofor_calisiyor:
            st.error("⚡ HİDROFOR ŞU AN AKTİF")
            st.info("Yeraltı suyu çekilerek ana depoya aktarılıyor.")
            if st.button("🔴 HİDROFORU DURDUR", use_container_width=True):
                st.session_state.hidrofor_calisiyor = False
                st.rerun()
        else:
            st.success("💤 HİDROFOR BEKLEMEDE")
            if st.button("🟢 HİDROFORU BAŞLAT", use_container_width=True):
                st.session_state.hidrofor_calisiyor = True
                st.rerun()

    st.divider()
    st.subheader("📊 Depo Dolum Geçmişi")
    st.line_chart([55, 58, 62, 65, 65]) # Örnek dolum grafiği
