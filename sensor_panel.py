import streamlit as st
import pandas as pd
import time
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Zeytinlik Sensör Ağı", page_icon="📡", layout="wide")

# --- GERÇEK VERİ ALTYAPISI (TASLAK) ---
# Burası ileride tarladaki ESP32'den gelen verileri okuyacak olan kısımdır.
def read_real_sensors():
    # Şimdilik simülasyon devam ediyor ama yapı gerçek veriye hazır
    return {
        "nemi": 32.5,  # Toprak nemi
        "akıs": 120.0, # Borudan geçen su litresi
        "pil": 85      # Kartın güneş enerjisi pil seviyesi
    }

# --- SIDEBAR: KART DURUMU ---
with st.sidebar:
    st.title("🎛️ Cihaz Durumu")
    st.success("ESP32-S3: Bağlı ✅")
    st.info("Sinyal Gücü: -65 dBm (Güçlü)")
    st.progress(85, text="🔋 Pil Seviyesi")

# --- ANA PANEL ---
st.title("🚜 Akıllı Saha Gözlem Merkezi")

c1, c2, c3 = st.columns(3)
data = read_real_sensors()

with c1:
    st.metric("Toprak Nemi", f"%{data['nemi']}", delta="-%2")
with c2:
    st.metric("Anlık Akış", f"{data['akıs']} L/dk", delta="Sabit")
with c3:
    st.metric("Sistem Voltajı", "3.7V", help="Lipo Pil Voltajı")

st.divider()

# Grafik ve Log Ekranı
col_sol, col_sag = st.columns([2, 1])

with col_sol:
    st.subheader("📈 Kritik Parametre Analizi")
    # Burada sensörlerden gelen geçmiş veriyi listeleyeceğiz
    st.line_chart({"Nem": [35, 34, 33, 32, 32.5]})

with col_sag:
    st.subheader("📜 Sistem Kayıtları (Log)")
    st.code(f"""
    [{datetime.now().strftime('%H:%M')}] Vana-1 açıldı.
    [{datetime.now().strftime('%H:%M')}] Veri sunucuya iletildi.
    [{datetime.now().strftime('%H:%M')}] Sensör kalibrasyonu OK.
    """, language="text")

# --- KRİTİK BUTONLAR ---
st.divider()
if st.button("🚨 SİSTEMİ RESETLE", use_container_width=True):
    st.warning("Uzak sunucudaki karta reset sinyali gönderiliyor...")
