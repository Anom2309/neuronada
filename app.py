import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
import math
import random
import csv
import io
import hashlib

# --- INIT SESSION STATE (PAYWALL) ---
if 'premium' not in st.session_state:
    st.session_state.premium = False

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada Ultimate OS", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- CUSTOM CSS & SOFT ANIMATION ---
st.markdown(
    """<style>
    @keyframes softFade {
        0% { opacity: 0; transform: translateY(20px); filter: blur(5px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    .soft-fade {
        animation: softFade 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; background-color: #050505; color: #e0e0e0; }
    .stApp { background: radial-gradient(circle at top, #111 0%, #000 100%); }
    
    div.stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%) !important; color: #000000 !important;
        font-weight: 900 !important; border: none !important;
        padding: 15px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3); letter-spacing: 1px;
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(255,215,0,0.5); }
    
    .cta-button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff0000 100%);
        color: white !important; padding: 15px; text-align: center; 
        border-radius: 8px; font-weight: 900; font-size: 16px; 
        box-shadow: 0 6px 15px rgba(255, 75, 75, 0.4);
        text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;
    }
    .cta-button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255, 75, 75, 0.6); }

    .ulasan-box {
        background: rgba(30, 30, 30, 0.6); backdrop-filter: blur(10px);
        padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700; 
        margin-bottom: 12px; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .glass-container {
        background: rgba(25, 25, 25, 0.5); backdrop-filter: blur(12px);
        padding: 20px; border-radius: 12px; border: 1px solid rgba(212,175,55,0.2);
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.4); margin-bottom: 15px;
    }
    
    .primbon-box {
        background: linear-gradient(135deg, rgba(43,27,5,0.8) 0%, rgba(74,48,0,0.8) 100%);
        backdrop-filter: blur(10px); padding: 25px; border-radius: 12px; 
        border: 1px solid #D4AF37; box-shadow: 0 8px 25px rgba(212,175,55,0.3); 
        margin-top: 20px; margin-bottom: 20px;
    }

    .dynamic-reading-box {
        background: rgba(20, 20, 20, 0.7); backdrop-filter: blur(5px);
        padding: 20px; border-radius: 12px; border-left: 5px solid #FFD700;
        margin-top: 15px; margin-bottom: 15px; font-size: 15px; line-height: 1.6;
    }
    
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap;
        padding: 15px; background: rgba(10,10,10,0.8); border-radius: 10px;
        border: 1px solid #333; margin-bottom: 5px; box-shadow: inset 0 2px 15px rgba(0,0,0,0.6);
    }
    .matrix-item { flex: 1; min-width: 80px; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 18px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }
    
    .list-punchy { padding-left: 20px; margin-bottom: 15px; font-size: 15px; }
    .list-punchy li { margin-bottom: 8px; }
    
    .live-badge {
        background: linear-gradient(90deg, #D4AF37, #FFD700);
        color: #000; padding: 8px 20px; border-radius: 30px;
        font-weight: 900; font-size: 14px; letter-spacing: 1px;
        display: inline-block; box-shadow: 0 4px 15px rgba(255,215,0,0.4);
    }

    .info-metric-box {
        background: rgba(255,215,0,0.05); border: 1px solid rgba(255,215,0,0.2);
        padding: 15px; border-radius: 8px; font-size: 13px; color: #ccc;
        margin-bottom: 20px; line-height: 1.5;
    }
    </style>""", unsafe_allow_html=True
)

def get_dynamic_count():
    start_date = datetime.date(2026, 4, 15) # Tanggal base
    today = datetime.date.today()
    delta = (today - start_date).days
    if delta < 0: delta = 0
    count = 1287 + (delta * 5)
    return f"{count:,}".replace(",", ".")

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa Kosmik"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

def get_planetary_hour():
    planets = [
        ("Matahari ☀️", "Fokus pada otoritas, presentasi, dan mengambil kendali.", "#FFD700"), 
        ("Venus 💖", "Waktu emas untuk negosiasi, asmara, dan melobi orang.", "#FF69B4"), 
        ("Merkurius 📝", "Eksekusi semua urusan email, naskah, dan komunikasi.", "#00FFFF"), 
        ("Bulan 🌙", "Waktu intuitif. Bagus untuk brainstorming atau istirahat.", "#F0F8FF"), 
        ("Saturnus 🪐", "Energi berat. Fokus pada pekerjaan repetitif dan audit.", "#8B4513"), 
        ("Yupiter 🍀", "Pintu rezeki terbuka. Waktu terbaik investasi/pitching.", "#32CD32"), 
        ("Mars ⚔️", "Energi agresif tinggi. Cocok untuk olahraga/eksekusi berani.", "#FF4500")
    ]
    return planets[datetime.datetime.now().hour % 7]

def get_sun_phase():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 8: return "Sunrise (Inisiasi)", "Gelombang otak beralih ke Alpha. Ideal untuk setting niat harian."
    elif 8 <= hour < 12: return "Morning (Akselerasi)", "Energi memuncak. Eksekusi tugas paling sulit sekarang."
    elif 12 <= hour < 15: return "Zenith (Konsolidasi)", "Matahari di puncak. Waktu untuk evaluasi dan re-kalibrasi."
    elif 15 <= hour < 18: return "Golden Hour (Refleksi)", "Waktu terbaik untuk kreativitas dan menyelesaikan urusan harian."
    elif 18 <= hour < 20: return "Sunset (Pelepasan)", "Tutup sistem saraf Anda dari beban kerja."
    else: return "Night Void (Regenerasi)", "Fase Delta. Dilarang mengambil keputusan besar di jam ini."

# --- DATABASE CLOUD ---
URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            decoded = response.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            return [row for row in reader][::-1]
    except: return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        req = urllib.request.Request(URL_POST, data=data)
        urllib.request.urlopen(req)
        return True
    except: return False

def generate_seed(base_str):
    return int(hashlib.md5(base_str.encode('utf-8')).hexdigest(), 16) % (10**8)

# --- PROCEDURAL TACTICAL PLAN (DYNAMIC & DEEP) ---
def proc_tactical_plan(nama, mod_harian, planet_live, planet_desc, sun_fase, sun_desc):
    random.seed(generate_seed(f"tac_{nama}_{mod_harian}_{planet_live}"))
    fase_detail = {
        0: {"nama": "🔴 FASE NADIR (Rest & Reset)", "analisa": f"Sistem saraf dan gelombang otak {nama} sedang berada di titik terendah siklusnya. Tubuh eterik Anda sedang melakukan 'reboot' sistem internal. Memaksakan ambisi besar hari ini sama dengan memacu mobil dengan gigi satu, mesin saraf Anda akan cepat aus dan *burnout*.", "do": ["Kerjakan hal-hal repetitif yang tidak butuh mikir keras (balas email biasa, rapihin file).", "Lakukan *Deep Rest*, *stretching* fisik, atau perbanyak tidur untuk regenerasi sel."], "dont": "DILARANG KERAS membuat keputusan finansial besar, mengambil risiko bisnis, atau memulai konflik emosional hari ini. Filter logika Anda sedang lemah."},
        1: {"nama": "🟢 FASE INISIASI (The Spark)", "analisa": f"Ini adalah momentum ledakan energi pertama Anda, {nama}! Pintu kosmik terbuka lebar untuk niat-niat baru. Segala sesuatu (sekecil apapun) yang Anda mulai hari ini memiliki daya dorong *momentum* 3x lipat lebih kuat dari hari biasa.", "do": ["Luncurkan ide baru, kirim proposal, atau hubungi prospek/klien target Anda sekarang.", "Lakukan gebrakan eksekusi pertama, walau hanya 5 menit, jangan tunggu sempurna."], "dont": "HINDARI sifat *over-analysis*. Hari ini adalah tentang 'Speed of Implementation', bukan tentang kesempurnaan. Bertindaklah!"},
        2: {"nama": "🔵 FASE SINKRONISASI (Kolaborasi)", "analisa": f"Energi independen (kesendirian) {nama} sedang menurun secara alami, digantikan oleh daya magnetisme sosial. Hari ini, rezeki dan solusi masalah Anda kemungkinan besar tidak datang dari diri sendiri, melainkan tersembunyi di tangan orang lain.", "do": ["Ajak negosiasi pihak yang tadinya alot, hari ini aura Anda lebih persuasif dan diterima.", "Delegasikan tugas yang bikin pusing ke tim atau orang yang lebih ahli."], "dont": "JANGAN menjadi 'Lone Wolf' (berjuang sendirian) memecahkan masalah besar hari ini. Anda akan cepat kehabisan daya dan frustrasi."},
        3: {"nama": "🟡 FASE RESONANSI (Ekspresi Diri)", "analisa": f"Cakra komunikasi {nama} sedang menyala terang. Frekuensi suara dan pilihan kata-kata tulisan Anda memiliki daya tembus alam bawah sadar yang luar biasa kepada siapapun yang mendengarnya hari ini.", "do": ["Buat konten (video/tulisan), lakukan presentasi, *pitching*, atau *Live* di sosmed.", "*Speak up*! Sampaikan keluhan, batasan, atau ide yang selama ini Anda pendam ke atasan/pasangan."], "dont": "JANGAN berdiam diri di goa atau memilih diam saat ditanya. Sangat sayang jika energi persuasi magis ini terbuang percuma."},
        4: {"nama": "🟤 FASE MATERIALISASI (Pondasi)", "analisa": f"Gelombang otak {nama} sedang sangat rasional, praktis, dan membumi. Ini bukan waktunya berkhayal masa depan. Hari ini murni tentang mengamankan dan merawat apa yang sudah Anda bangun agar tidak runtuh.", "do": ["Audit total arus kas (keuangan) Anda. Cek mutasi dan kebocoran pengeluaran minggu ini.", "Fokus pada detail operasional yang membosankan namun vital bagi bisnis."], "dont": "DILARANG mengambil risiko spekulatif (judi, trading asal, investasi tanpa data valid, foya-foya) hari ini. Pegang aset Anda erat-erat."},
        5: {"nama": "🟠 FASE EKSPANSI (Tantangan Ekstrim)", "analisa": f"Adrenalin kosmik {nama} memuncak tajam! Insting bertahan hidup dan *growth* Anda sedang sinkron. Batas-batas ketakutan (mental block) Anda melemah, memberikan celah terbuka untuk melakukan terobosan radikal.", "do": ["Eksekusi satu hal yang paling Anda takuti minggu ini (misal: *follow-up* klien kelas kakap atau *cold calling*).", "Uji coba strategi marketing/bisnis yang 'Out of the Box' dan berisiko."], "dont": "JANGAN biarkan diri Anda diam terjebak dalam kebosanan rutinitas. Diam hari ini akan berubah menjadi *Anxiety* (kecemasan parah)."},
        6: {"nama": "🟣 FASE ELEVASI (Pengayoman & Karma)", "analisa": f"Vibrasi jiwa {nama} menembus urusan duniawi hari ini. Anda memancarkan energi *Healer* (Penyembuh/Orang Tua). Alam semesta menuntut Anda sejenak kembali ke 'akar': keluarga, keikhlasan batin, dan relasi spiritual.", "do": ["Perbaiki hubungan yang retak. Minta maaf atau maafkan kesalahan pasangan/orang tua/sahabat.", "Lakukan *Charity* (sedekah nominal ekstrim) atau bantu kesulitan orang lain secara anonim."], "dont": "HINDARI debat ego, pertengkaran keras kepala, atau ambisi memanipulasi orang lain demi keuntungan uang. Karma berlaku instan hari ini."}
    }
    fd = fase_detail[mod_harian]
    buka = random.choice([f"Berdasarkan dekripsi algoritma lahir dan posisi langit saat ini, sistem mendeteksi lonjakan energi spesifik pada diri Anda, **{nama}**.", f"Peringatan Taktis! Gelombang kosmik sedang berpusat pada sektor tindakan Anda. Jika **{nama}** salah melangkah dalam jam ini, momentum akan hangus."])
    planet_murni = planet_live.split(' ')[0]
    matahari_murni = sun_fase.split(' ')[0]
    koneksi = random.choice([f"Diperkuat oleh jam {planet_murni} yang mengintervensi fase {matahari_murni} Anda, situasi ini menciptakan desakan absolut untuk bertindak.", f"Resonansi {planet_murni} yang bertabrakan dengan siklus {matahari_murni} ini mengunci otak Anda dalam mode sadar tingkat tinggi."])
    do_html = "".join([f"<li style='margin-bottom: 8px;'>{item}</li>" for item in random.sample(fd["do"], 2)])

    html_output = f"""<div class="live-engine-box soft-fade" style="background: rgba(20,20,25,0.9); border-left: 4px solid #00FFFF; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,255,255,0.1);">
<h4 style="color: #00FFFF; margin-top:0; letter-spacing: 1px; font-weight:900;">⚡ TACTICAL ACTION PLAN <span style="font-size:12px; color:#ff4b4b; font-weight:normal;">(⏳ Valid 24 Jam)</span></h4>
<p style="color: #ccc; font-size: 15px; line-height: 1.6; margin-bottom:20px;">
{buka}<br><br>
<b style="color:#FFF; font-size:16px;">STATUS BIORITME ANDA: <span style="color:#FFD700;">{fd['nama'].split('(')[0].strip()}</span></b><br>
{fd['analisa']}<br><br>
<i style="color:#888;">Sinkronisasi Kosmik:</i> {koneksi} ({planet_desc})
</p>
<div style="background: rgba(37,211,102,0.1); border: 1px solid rgba(37,211,102,0.4); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
<b style="color: #25D366; font-size:15px;">🎯 PROTOKOL EKSEKUSI (LAKUKAN SEKARANG):</b>
<ul style="color: #e0e0e0; font-size: 15px; margin-top: 10px; margin-bottom: 0; padding-left: 20px; line-height:1.5;">
{do_html}
</ul>
</div>
<div style="background: rgba(255,75,75,0.1); border: 1px solid rgba(255,75,75,0.4); padding: 15px; border-radius: 8px;">
<b style="color: #ff4b4b; font-size:15px;">🛑 RED ZONE (HINDARI MUTLAK):</b><br>
<span style="color: #ccc; font-size: 14px; display:inline-block; margin-top:5px; line-height:1.5;">{fd['dont']}</span>
</div>
<p style="font-size:12px; color:#ff4b4b; margin-top:10px; font-weight:bold;">⏳ Sistem mendeteksi perubahan energi dalam beberapa jam ke depan. Jangan tunda eksekusi!</p>
</div>"""
    return fd['nama'], html_output

# --- ENGINE FALAK RUHANI (SPIRITUAL ANCHORING) ---
def proc_falak_ruhani(total_jummal, root_num, nama):
    ruhani_data = {
        1: {"asma": "Ya Fattah (Maha Pembuka)", "vibrasi": "Mendobrak Jalan Buntu & Ego", "tujuan": "Membersihkan hambatan ego masa lalu, menaklukkan sifat keras kepala, dan mendobrak pintu rezeki yang selama ini terkunci akibat kesombongan bawah sadar."},
        2: {"asma": "Ya Salam (Maha Sejahtera)", "vibrasi": "Harmoni & Perisai Mental", "tujuan": "Menetralisir frekuensi beracun (toxic) dari lingkungan sekitar dan menyembuhkan kelelahan sistem saraf (anxiety) akibat terlalu banyak memendam perasaan."},
        3: {"asma": "Ya Mushawwir (Maha Pembentuk)", "vibrasi": "Manifestasi Ide ke Realita", "tujuan": "Menarik pikiran yang berserakan (overthinking) kembali ke pusat bumi, mengubah wacana atau ide liar menjadi sebuah karya fisik yang terstruktur."},
        4: {"asma": "Ya Muqit (Maha Pemberi Kecukupan)", "vibrasi": "Stabilitas & Nutrisi Batin", "tujuan": "Menghancurkan 'Mental Miskin' (Scarcity Mindset) hingga ke akarnya, memberikan rasa aman absolut pada kondisi finansial, dan menarik kestabilan material."},
        5: {"asma": "Ya Basith (Maha Melapangkan)", "vibrasi": "Ekspansi & Pembebasan Diri", "tujuan": "Melepaskan perasaan terkekang, menghilangkan rasa bosan kronis, dan memperluas kapasitas wadah rezeki mental Anda agar siap memanen kesuksesan besar."},
        6: {"asma": "Ya Wadud (Maha Mengasihi)", "vibrasi": "Cinta Universal & Daya Tarik", "tujuan": "Menyembuhkan trauma luka batin masa lalu, menumbuhkan Self-Love tingkat tinggi, and secara otomatis memancarkan aura pengasihan (Rapport) alami tanpa pelet."},
        7: {"asma": "Ya Batin (Maha Tersembunyi)", "vibrasi": "Intuisi & Hikmah Langit", "tujuan": "Mempertajam indra keenam, melatih kepekaan membaca bahasa tubuh dan niat tersembunyi orang lain, serta menjernihkan intuisi bisnis Anda."},
        8: {"asma": "Ya Ghaniy (Maha Kaya)", "vibrasi": "Otoritas & Kelimpahan Absolut", "tujuan": "Menyelaraskan frekuensi diri Anda menjadi magnet kekayaan material murni, serta memberikan kekuatan untuk memegang kendali tanpa terjatuh pada keserakahan."},
        9: {"asma": "Ya Hakim (Maha Bijaksana)", "vibrasi": "Pencerahan & Kesadaran", "tujuan": "Pelepasan beban karma (rasa bersalah masa lalu), menurunkan ekspektasi ego pada duniawi, dan menyelaraskan setiap tindakan fisik Anda dengan Misi Semesta (Life Purpose)."}
    }
    data = ruhani_data.get(root_num, ruhani_data[1])
    dzikir_count = total_jummal
    return data["asma"], data["vibrasi"], data["tujuan"], dzikir_count

# --- PROTOKOL TERAPI DINAMIS ---
def get_protokol_terapi(root_num, nama):
    random.seed(generate_seed(f"pt_{nama}_{root_num}"))
    b1 = random.choice([f"**Ego Supremacy & Lone Wolf Syndrome.** Anda ({nama}) memiliki program bawah sadar yang menolak bantuan karena merasa 'harus bisa sendiri'. Ujungnya? Kelelahan ekstrem (*Burnout*) dan rasa sepi di tengah keramaian karena menanggung semua beban di pundak sendiri.", f"**Ilusi Kontrol Sempurna.** Secara tidak sadar, gengsi {nama} terlalu tinggi untuk meminta tolong. Bahayanya, hal ini menciptakan pola hidup di mana Anda memforsir mesin saraf Anda melebihi kapasitas, mensabotase rezeki yang seharusnya bisa datang dari kolaborasi tim."])
    a1 = random.choice([f"Saya, {nama}, dengan penuh kesadaran menurunkan perisai ego saya malam ini. Saya paham bahwa meminta tolong adalah delegasi kecerdasan, bukan kelemahan. Saya mengizinkan energi Semesta bekerja melalui tangan orang lain.", f"Mulai tarikan napas ini, saya ({nama}) menyadari bahwa kolaborasi adalah kunci kelimpahan sejati. Saya pantas dibantu, tubuh saya pantas untuk beristirahat, dan saya membuka pintu bagi kemudahan."])
    h1 = random.choice(["Cari 1 tugas spesifik hari ini yang sebenarnya BISA Anda kerjakan sendiri, namun **mintalah tolong** orang lain untuk mengerjakannya. Latih otot 'penerimaan' Anda.", "Hubungi satu teman kompeten atau mentor Anda hari ini. Ceritakan satu kendala teknis atau mental yang sedang Anda hadapi. Dengarkan saran mereka sepenuhnya tanpa memotong."])

    b2 = random.choice([f"**People Pleaser Chronic.** {nama} secara rutin memenjarakan suara hati sendiri demi menjaga perasaan orang lain. Anda bertindak layaknya 'Spons Emosi' yang menyerap keluh kesah dan energi negatif (*toxic*) sirkel Anda.", f"**Luka Takut Ditinggalkan (Abandonment).** Anda terlalu mudah merasa *nggak enakan*. Hidup {nama} sering tersabotase karena mendahulukan kebutuhan orang yang bahkan tidak memprioritaskan Anda."])
    a2 = random.choice([f"Saya, {nama}, memegang kendali absolut atas energi dan kewarasan saya. Kebahagiaan saya adalah priority kosmik nomor satu. Mulai saat ini, batas diri (*boundaries*) saya adalah suci.", f"Saya ({nama}) melepaskan rasa bersalah palsu ini. Saya menolak bertanggung jawab atas kekecewaan atau ekspektasi orang lain. Merawat diri saya sendiri adalah priority."])
    h2 = random.choice(["Berlatih keberanian mikro: Katakan 'TIDAK' atau 'Maaf, saya tidak bisa' pada satu permintaan/ajakan hari ini. Ucapkan dengan tegas dan rileks.", "Lakukan *Digital Detoxing* parsial. Matikan notifikasi chat dari grup WhatsApp atau individu yang paling sering 'menyedot' energi Anda selama minimal 12 jam."])

    b3 = random.choice([f"**Scattered Focus (Lompatan Kera).** Otak {nama} adalah pabrik yang memproduksi ratusan ide brilian per detik, namun memiliki eksekusi nyaris nol. Energi Anda habis menguap hanya di fase *overthinking*.", f"**Impulsivitas Ide & Mudah Bosan.** Anda ({nama}) kecanduan dopamin dari sebuah 'awal yang baru'. Baru saja memulai satu hal, sistem saraf Anda sudah melompat mencari rangsangan ide lain."])
    a3 = random.choice([f"Saya, {nama}, memerintahkan pikiran saya untuk melambat dan membumi. Saya menyalurkan kreativitas liar ini ke dalam struktur yang nyata. Satu eksekusi kecil yang selesai jauh lebih berharga daripada seribu wacana.", f"Pikiran saya jernih, tajam bak sinar laser. Saya ({nama}) mengizinkan diri saya untuk duduk tenang, menghadapi rasa tidak nyaman, dan menyelesaikan apa yang sudah saya mulai."])
    h3 = random.choice(["Gunakan teknik *Timeboxing*. Pilih 1 ide/tugas spesifik saja. Tulis di kertas, pasang timer 20 menit, lalu kerjakan langkah pertamanya tanpa henti.", "Terapi Keteraturan Fisik: Rapikan meja kerja, hapus file sampah di laptop, atau bersihkan kamar Anda secara total hari ini."])

    b4 = random.choice([f"**Scarcity Mindset (Mental Miskin).** Terdapat ketakutan bawah sadar yang parah akan kegagalan dan kebangkrutan. Hal ini membuat pola pikir {nama} menjadi sangat kaku, terlalu berhati-hati, dan pelit—bahkan pada diri sendiri.", f"**Sabotase Zona Nyaman.** Anda ({nama}) sering merasionalisasi ketakutan dengan dalih 'harus nabung untuk jaga-jaga hal buruk'. Tanpa sadar, frekuensi ini justru bertindak seperti magnet yang menarik nasib buruk."])
    a4 = random.choice([f"Saya, {nama}, dengan napas ini melepaskan rasa takut akan kekurangan. Saya menyadari bahwa sumber daya Semesta tidak terbatas dan berlimpah ruah. Kondisi finansial saya aman.", f"Saya ({nama}) layak dan pantas hidup dalam kelimpahan tanpa batas. Uang adalah energi cahaya yang baik, dan saya mengizinkannya datang mengetuk pintu saya."])
    h4 = random.choice(["Latih saraf melepaskan (Letting Go): Beri hadiah fisik (reward) untuk diri sendiri hari ini. Saat membayar, tersenyumlah dan rasakan emosi kelimpahannya.", "Lakukan sedekah subuh atau transfer amal tak terduga hari ini, berapapun nominalnya. Niatkan tindakan ini untuk memutus urat ketakutan batin."])

    b5 = random.choice([f"**Escapism (Sindrom Pelarian).** {nama} memiliki kecenderungan melarikan diri (*escape*) saat dihadapkan pada tanggung jawab atau komitmen jangka panjang. Anda berlindung di balik kata 'mencari kebebasan'.", f"**Korsleting Rutinitas (Mudah Jenuh).** Saat menghadapi tekanan pekerjaan yang menuntut konsistensi tinggi, sistem saraf {nama} mendadak mati rasa. Anda tiba-tiba merasa hampa, stres tak beralasan."])
    a5 = random.choice([f"Saya, {nama}, menemukan kedalaman makna yang sejati justru di dalam komitmen yang stabil. Menetap dan konsisten bukanlah penjara bagi saya, melainkan pondasi baja untuk sukses.", f"Saya ({nama}) mengontrol penuh rasa bosan di dalam diri saya. Saya berdamai dengan proses repetitif. Saya menanam akar keringat yang kuat hari ini."])
    h5 = random.choice(["Pilih SATU pekerjaan yang paling membosankan dan sudah Anda tunda berminggu-minggu. Paksa sistem saraf Anda untuk duduk dan menyelesaikannya hingga tuntas 100% hari ini.", "Terapi Konsistensi Dasar: Rancang rutinitas pagi sederhana. Lakukan hal yang SAMA PERSIS selama 3 hari berturut-turut tanpa mengubah polanya sedikitpun."])

    b6 = random.choice([f"**Savior Complex (Penyelamat Berlebihan).** {nama} secara tidak sadar sering merasa bersalah jika menikmati hidup yang enak, sementara ada orang di sekitarnya yang masih susah. Anda menguras energi vital untuk menyelesaikan masalah orang lain.", f"**Luka Pengorbanan Tanpa Pamrih Palsu.** Anda ({nama}) memberikan 100% kapasitas emosi dan materi untuk orang-orang terdekat, namun jauh di lubuk hati terdalam diam-diam merasa kosong."])
    a6 = random.choice([f"Saya, {nama}, dengan sadar mengizinkan diri saya untuk bahagia dan berkelimpahan. Saya paham bahwa merawat dan mencintai diri sendiri secara maksimal adalah syarat mutlak.", f"Tangki cinta dan rezeki saya berlimpah, dan penerima pertama dari kelimpahan itu adalah saya sendiri. Saya ({nama}) berhak menikmati keringat saya."])
    h6 = random.choice(["Lakukan 'Isolasi Positif'. Ambil waktu minimal 45 menit hari ini murni untuk 'Me-Time'. Matikan koneksi, lakukan hobi Anda tanpa memikirkan orang lain.", "Beli makanan kesukaan yang cukup mewah hari ini. Makanlah pelan-pelan sendirian, nikmati setiap gigitannya, dan JANGAN membaginya."])

    b7 = random.choice([f"**Paralysis by Analysis (Kelumpuhan Logika).** Otak analitik {nama} terlalu tajam, namun berbalik menyerang diri sendiri. Anda menghabiskan energi menganalisa niat orang lain secara berlebihan (*over-analyzing*).", f"**Trust Issue Kronis.** Pengalaman masa lalu menciptakan sifat skeptis ekstrim di bawah sadar {nama}. Anda seringkali menolak peluang bisnis yang bagus atau cinta yang tulus karena selalu curiga."])
    a7 = random.choice([f"Saya, {nama}, menyeimbangkan ketajaman logika saya dengan kepasrahan intuisi. Saya mempercayai proses Semesta, dan saya mengizinkan hal-hal menakjubkan terjadi di hidup saya.", f"Saya ({nama}) secara sadar melepaskan kebutuhan egoistik untuk mengetahui rahasia dari segalanya. Saya memaafkan masa lalu, mempercayai perlindungan Tuhan."])
    h7 = random.choice(["Lakukan 'Silence Meditation' (meditasi hening tanpa instruksi). Duduk diam total tanpa interupsi selama 15 menit. Amati saja keluar masuknya napas.", "Latih otot kepercayaan: Percayai secara utuh satu ucapan atau tindakan niat baik dari orang di sekitar Anda hari ini, TANPA Anda *cross-check*."])

    b8 = random.choice([f"**Control Freak & Diktator Bawah Sadar.** {nama} memforsir tubuh, pikiran, dan orang lain di sekitarnya tanpa ampun demi mengejar standar kesuksesan material yang tidak ada garis finishnya.", f"**Obsesi Material Penjerat Batin.** Ambisi dan insting bisnis {nama} memang menyala terang, tapi hal ini seringkali menghancurkan kedamaian batin Anda sendiri."])
    a8 = random.choice([f"Saya, {nama}, adalah saluran tempat kelimpahan mengalir secara damai, bukan budak dari ambisi buta. Kekuatan sejati saya justru bersinar paling terang saat saya berserah.", f"Saya ({nama}) dengan ikhlas melepaskan ilusi kendali yang menyiksa saraf saya. Saya sukses, saya berkelimpahan, saya berwibawa, dan hati saya damai."])
    h8 = random.choice(["Praktik Delegasi Radikal. Serahkan satu keputusan kendali hari ini kepada orang lain (misal: biarkan bawahan/pasangan mengambil keputusan). Ikuti saja alurnya.", "Terapkan 'Hard Stop'. Berhenti bekerja dan matikan koneksi laptop/bisnis tepat pukul 17:00 hari ini. Dilarang keras menyentuh urusan pekerjaan sampai besok."])

    b9 = random.choice([f"**Toxic Empathy (Empati Penghancur).** {nama} memiliki resonansi spiritual yang terlalu peka. Anda terlalu gampang merasa kasihan, bahkan pada orang yang manipulatif dan *toxic*.", f"**Luka Ekspektasi Luluh (Patah Hati Universal).** Karena Anda memegang standar moral dan filosofi yang sangat tinggi, {nama} seringkali jatuh pada kekecewaan yang sangat parah."])
    a9 = random.choice([f"Saya, {nama}, dengan napas ini melepaskan segala hal yang berada di luar kendali otoritas saya. Saya membiarkan setiap jiwa manusia memikul karmanya sendiri.", f"Tugas suci saya ({nama}) di bumi ini BUKANLAH untuk menyelamatkan semua orang. Energi batin saya adalah pusaka yang suci."])
    h9 = random.choice(["Lakukan Detoksifikasi Frekuensi Negatif. Blokir semua asupan berita politik, gosip, tragedi, atau *scrolling* curhatan orang di sosial media selama 24 jam penuh.", "Terapi Menahan Diri: Sepanjang hari ini, berhentilah memberikan nasihat, wejangan, atau solusi kepada siapapun KECUALI jika mereka meminta."])

    protokol = {1: {"block": b1, "afirmasi": a1, "habit": h1}, 2: {"block": b2, "afirmasi": a2, "habit": h2}, 3: {"block": b3, "afirmasi": a3, "habit": h3}, 4: {"block": b4, "afirmasi": a4, "habit": h4}, 5: {"block": b5, "afirmasi": a5, "habit": h5}, 6: {"block": b6, "afirmasi": a6, "habit": h6}, 7: {"block": b7, "afirmasi": a7, "habit": h7}, 8: {"block": b8, "afirmasi": a8, "habit": h8}, 9: {"block": b9, "afirmasi": a9, "habit": h9}}
    return protokol.get(root_num, protokol[1])

# --- DATABASE BLUEPRINT ---
arketipe_punchy = {
    1: {"inti": "Sang Perintis (Dominator & Visioner Masa Depan)", "kekuatan": ["Daya dobrak tinggi & berani ambil risiko", "Mandiri secara absolut", "Fokus eksekusi"]},
    2: {"inti": "Sang Penyelaras (Negosiator & Pembaca Emosi)", "kekuatan": ["Kapasitas empati tinggi", "Negosiator ulung", "Kemampuan adaptasi emosional"]},
    3: {"inti": "Sang Visioner (Kreator Ide & Komunikator Handal)", "kekuatan": ["Komunikasi memikat", "Kreativitas tanpa batas", "Ahli mencairkan suasana"]},
    4: {"inti": "Sang Transformator (Ahli Strategi & Pembangun Sistem)", "kekuatan": ["Pola pikir sangat terstruktur", "Bisa diandalkan 100%", "Ketelitian tingkat dewa"]},
    5: {"inti": "Sang Penggerak (Eksplorator & Pemecah Kebuntuan)", "kekuatan": ["Kelincahan berpikir", "Inovator pemecah kebuntuan", "Keberanian mengeksplorasi"]},
    6: {"inti": "Sang Harmonizer (Pengayom & Pelindung Natural)", "kekuatan": ["Insting pengayom", "Tanggung jawab moral tinggi", "Loyalitas tanpa pamrih"]},
    7: {"inti": "Sang Legacy Builder (Pemikir Analitik & Spiritualis)", "kekuatan": ["Kemampuan analisa", "Intuisi sering akurat", "Sangat selektif menilai kualitas"]},
    8: {"inti": "Sang Sovereign (Eksekutor Otoritas & Magnet Material)", "kekuatan": ["Tahan banting mental", "Insting bisnis tajam", "Kemampuan memegang kendali"]},
    9: {"inti": "Sang Kesadaran Tinggi (Old Soul & Empati Universal)", "kekuatan": ["Kebijaksanaan luas", "Kepedulian universal", "Melihat 'Big Picture'"]}
}

def proc_arketipe(nama, angka, zodiak, neptu):
    random.seed(generate_seed(f"hyper_ark_{nama}_{angka}_{zodiak}_{neptu}"))
    buka = random.choice([
        f"Melalui persilangan matriks waktu dan elemen {zodiak}, DNA numerologi **{nama}** mengunci kuat pada **KODE {angka}**.",
        f"Kalkulasi semesta menyempit di **KODE {angka}**. Ini menandakan bahwa sejak lahir, alam bawah sadar **{nama}**",
        f"Sistem mendeteksi getaran **KODE {angka}** pada diri Anda. Secara genetik dan arsitektur mental, **{nama}**",
        f"Berdasarkan algoritma kepribadian {zodiak} yang melebur dengan weton, cetak biru **{nama}** adalah **KODE {angka}**."
    ])
    inti = {
        1: ["sebagai sosok perintis yang didesain untuk memimpin dan menembus batas.", "memiliki dorongan mutlak untuk mandiri dan benci didikte."],
        2: ["sebagai Sang Penyelaras yang mampu menetralisir konflik.", "memiliki radar empati tingkat dewa untuk membaca ruang dan emosi."],
        3: ["sebagai komunikator handal dengan pikiran yang meletup-letup seperti kembang api.", "memiliki anugerah kreativitas tanpa batas."],
        4: ["sebagai arsitek kehidupan yang sangat sistematis dan presisi.", "memiliki pola pikir logis yang menjadikannya pondasi kuat."],
        5: ["sebagai simbol kebebasan yang menolak keras rutinitas monoton.", "memiliki kelincahan otak untuk beradaptasi cepat."],
        6: ["sebagai pelindung sejati dengan insting pengayom yang luar biasa.", "memegang standar tanggung jawab moral yang sangat tinggi."],
        7: ["sebagai pencari kebenaran esensial dengan intuisi yang tajam.", "tidak pernah puas dengan jawaban dangkal dan selalu menganalisa."],
        8: ["sebagai eksekutor tangguh dengan insting material yang sangat presisi.", "memiliki fokus bawah sadar yang ditarik kuat menuju puncak otoritas."],
        9: ["sebagai 'Jiwa Tua' yang memandang dunia dengan kacamata kebijaksanaan.", "memiliki tingkat kepedulian universal yang melampaui ego."]
    }
    gaya = {
        1: ["Anda adalah inisiator cepat yang lebih suka bertindak daripada rapat.", "Anda memancarkan aura alpha kemanapun Anda pergi."],
        2: ["Anda adalah pendengar ulung tempat orang lain membuang keluh kesah.", "Gaya kerja Anda kolaboratif; memastikan tim merasa dihargai."],
        3: ["Anda memecahkan masalah dengan ide *out-of-the-box*.", "Anda ahli mencairkan ketegangan lewat humor spontan."],
        4: ["Anda mengeksekusi visi dengan langkah terukur dan tanpa cacat.", "Lingkungan melihat Anda sebagai sosok yang dingin namun selalu selesai tugas."],
        5: ["Anda paling bersinar saat diletakkan di situasi *chaos* yang butuh pemecahan instan.", "Gaya hidup Anda nomaden secara mental; mudah bosan."],
        6: ["Anda memimpin dengan hati, bertindak layaknya orang tua bagi teman-teman Anda.", "Loyalitas Anda tidak perlu diragukan untuk membela sirkel."],
        7: ["Anda mengobservasi dalam diam sebelum mengambil keputusan strategis.", "Gaya sosial Anda misterius; tidak banyak yang tahu isi kepala Anda."],
        8: ["Anda mengorganisir sumber daya dengan tangan besi yang elegan.", "Aura wibawa Anda sering membuat orang segan sebelum Anda bicara."],
        9: ["Anda merangkul keberagaman dan memimpin lewat contoh pengorbanan.", "Orang sering datang meminta nasihat karena kedewasaan batin Anda."]
    }
    shadow = {
        1: ["Waspadai rasa kesepian akibat ego yang membangun tembok pemisah.", "Sisi gelapnya, Anda rawan terjebak sifat arogan."],
        2: ["Waspadai memendam amarah terus-menerus yang bisa jadi bom waktu.", "Bahayanya, Anda sering menyerap energi beracun (toxic)."],
        3: ["Sisi gelapnya, rawan berbicara impulsif saat harga diri tersinggung.", "Musuh terbesar Anda adalah hilangnya fokus."],
        4: ["Bahayanya, dinilai tidak punya perasaan karena kaku pada aturan.", "Waspadai sifat over-micromanaging yang membuat gerah."],
        5: ["Waspadai 'Sindrom Cepat Bosan' yang mensabotase karir/asmara.", "Bahayanya, cenderung melarikan diri (escapism) dari komitmen berat."],
        6: ["Sangat rentan *burnout* ekstrem mengurus beban orang lain.", "Bahayanya, dihantui rasa bersalah tak masuk akal saat *me-time*."],
        7: ["Sering terjebak *Paralysis by Analysis* (overthinking tanpa aksi).", "Waspadai kecenderungan mengisolasi diri saat merasa tidak dihargai."],
        8: ["Kesulitan melepaskan kendali dan memaafkan pengkhianatan.", "Rentang mendominasi pasangan secara emosional tanpa sadar."],
        9: ["Rawan patah hati kronis karena ekspektasi luhur berbenturan realitas.", "Energi batin gampang terkuras memikirkan penderitaan dunia."]
    }
    saran = {
        1: "Belajarlah mendelegasikan tugas. Meminta tolong adalah taktik kepemimpinan.",
        2: "Berlatihlah mengatakan 'TIDAK' tanpa merasa bersalah.",
        3: "Paksa diri Anda menuntaskan satu proyek kecil hari ini sebelum melompat ke ide lain.",
        4: "Biarkan ruang untuk spontanitas. Kadang berantakan sedikit adalah terapi.",
        5: "Temukan kebebasan dalam komitmen panjang.",
        6: "Buatlah batas yang tegas. Berhenti menyelamatkan orang toxic.",
        7: "Turunkan ekspektasi Anda terhadap ketidaksempurnaan manusia.",
        8: "Latih diri berserah di momen istirahat. Kesuksesan butuh sistem saraf sehat.",
        9: "Anda tidak diutus memikul galaksi. Cintai diri sendiri dulu."
    }
    return f"{buka} Anda didesain {random.choice(inti[angka])} {random.choice(gaya[angka])} {random.choice(shadow[angka])} Pesan Semesta: {saran[angka]}"

def proc_shadow_list(nama, angka):
    random.seed(generate_seed(f"shd_{nama}_{angka}"))
    semua_shadow = {
        1: ["Gengsi minta tolong saat memikul beban", "Membangun tembok ego untuk menutupi sepi", "Overthinking merasa hasil belum sempurna", "Kesulitan menerima kritik", "Mengabaikan lelah demi target"],
        2: ["Mengorbankan kebahagiaan demi ekspektasi", "Sulit berkata TIDAK (People Pleaser)", "Memendam amarah hindari konflik", "Terlalu bergantung validasi", "Menyerap energi toxic"],
        3: ["Menyembunyikan gelisah di balik topeng ceria", "Cepat kehilangan motivasi", "Insomnia karena over-analisa", "Kesulitan fokus prioritas", "Bicara impulsif saat tersinggung"],
        4: ["Stres parah jika rencana mendadak berubah", "Terjebak zona nyaman takut risiko", "Sering dinilai terlalu dingin", "Over-micromanaging", "Menghakimi orang tak disiplin"],
        5: ["Sindrom Bosan mensabotase karya", "Kelelahan saraf otak jalan terus", "Merasa hampa hilang pijakan", "Lari (escapism) saat ditekan", "Kesulitan rutinitas panjang"],
        6: ["Burnout mengurus hidup orang lain", "Sikap Over-Protective mengekang", "Rasa bersalah jika me time", "Terlalu ikut campur keluarga", "Mengharap balasan emosional"],
        7: ["Menganalisa terus tanpa aksi (Paralysis)", "Merasa terasing/tak sepemikiran", "Mencurigai niat baik orang", "Sinis dan sarkastik", "Menutup diri saat emosi memuncak"],
        8: ["Sulit melepaskan kontrol/memaafkan", "Memaksa tubuh abaikan alarm lelah", "Menilai orang dari sisi guna/status", "Ketakutan berlebih menjadi lemah", "Mendominasi pasangan"],
        9: ["Memaklumi toxic atas nama kasihan", "Patah hati akibat ekspektasi manusia", "Kelelahan memikirkan beban semesta", "Sering merasa tidak pantas", "Kehilangan jati diri demi visi"]
    }
    return random.sample(semua_shadow[angka], 3)

def proc_couple_persona(root_c, n1, n2):
    random.seed(generate_seed(f"cp_{n1}_{n2}_{root_c}"))
    buka = random.choice([
        f"Ketika vibrasi nama **{n1}** dan **{n2}** dilebur, hasilnya mengunci di **Root {root_c}**.",
        f"Hukum resonansi mencatat persatuan **{n1}** dan **{n2}** menghasilkan gelombang **Root {root_c}**."
    ])
    desc = {
        1: ("THE POWER COUPLE", f"Kalian memancarkan simbol Alpha. {n1} dan {n2} membentuk entitas ambisius, fokus pada kemajuan karir."),
        2: ("THE SOULMATES", f"Kalian memiliki 'Wi-Fi' batin. Mudah bagi {n1} memahami emosi {n2} tanpa banyak kata. Harmoni adalah kunci."),
        3: ("THE SOCIALITES", f"Aura kalian magnetis. {n1} dan {n2} adalah pasangan menyenangkan yang selalu menghidupkan suasana sirkel."),
        4: ("THE BUILDERS", f"Hubungan ini berpijak pada bumi. Fokus {n1} dan {n2} adalah membangun aset keluarga dan kesetiaan absolut."),
        5: ("THE ADVENTURERS", f"Kalian dipenuhi energi kebebasan. {n1} maupun {n2} butuh kejutan dan tantangan agar cinta tetap menyala."),
        6: ("THE FAMILY FIRST", f"Simbol pengayoman tertinggi. Pengorbanan {n1} dan {n2} untuk merawat keutuhan rumah tangga sangat mendalam."),
        7: ("THE DEEP SEEKERS", f"Hubungan tertutup dan eksklusif. {n1} dan {n2} membangun koneksi intelektual dengan privasi yang sulit ditembus."),
        8: ("THE EMPIRE", f"Magnet kelimpahan mutlak. Penyatuan ego {n1} dan {n2} mengejar kesuksesan bisnis dan membangun kerajaan keluarga."),
        9: ("THE HEALERS", f"Puncak kedewasaan empati. Interaksi {n1} dan {n2} dipenuhi toleransi dan menjadi tempat penyembuhan bagi sirkel sekitar.")
    }
    return desc.get(root_c, ("UNCHARTED SYNERGY", "Anomali energi tak tertebak."))[0], f"{buka} {desc.get(root_c)[1]}"

def proc_weton_kombo(sisa, n1, n2, z1, z2):
    random.seed(generate_seed(f"wt_{n1}_{n2}_{sisa}_{z1}_{z2}"))
    do_list = {
        1: [f"Gunakan teknik *Pacing-Leading*. Saat argumen memanas, jangan buru-buru membantah. Validasi dulu emosi {n2} dengan mendengarkan aktif.", f"Beri jeda *Time-Out* saat perdebatan menajam. Biarkan ego bawaan {z1} dan {z2} reda terlebih dahulu."],
        2: [f"Jadikan {n2} sebagai *Partner Mastermind*. Jangan jalan sendirian! Libatkan ia dalam diskusi visi masa depan.", f"Bangun *Rapport* berbasis pencapaian. Saling memberikan apresiasi terbuka akan sangat memperkuat wibawa hubungan."],
        3: [f"Ciptakan *Pattern Interrupt* (Pola Kejutan). Lakukan kencan dadakan atau ubah rutinitas akhir pekan agar percikan dopamin tetap menyala.", f"Pancing *deep-talk* rutin minimal sebulan sekali. Obrolan filosofis akan sangat mempertajam frekuensi empati kalian."],
        4: [f"Kuasai teknik *Reframing* (Pembingkaian Ulang) saat menghadapi krisis. Pandang masalah sebagai tim solid: 'Kita berdua vs Masalah'.", f"Perkuat daya tahan mental (*Resilience*). Badai penyesuaian sifat di fase awal adalah harga tiket menuju rezeki besar."],
        5: [f"Gelar sesi 'Visi Masa Depan' bersama. Transparansi adalah kunci magnet rezeki bagi kalian.", f"Sinkronkan frekuensi kelimpahan kalian berdua. Jika salah satu sedang pesimis, tugas pasangannya menarik kembali ke mode optimis."],
        6: [f"Berikan *Space* (Ruang Pribadi) saat tensi saraf naik. Kalian memiliki filter informasi yang berbeda. Saat mulai panas, mundur selangkah.", f"Gunakan humor sebagai penetralisir racun. Ledakan tawa spontan sangat ampuh memecah ketegangan argumen ego."],
        7: [f"Komunikasi berbasis fakta (*Sensory Based*). Pastikan Anda selalu mengklarifikasi pesan: 'Maksud kamu tadi X atau Y?'.", f"Tingkatkan intensitas sentuhan fisik (*Physical Touch*) atau bahasa cinta primer pasangan untuk meredam cemburu buta."],
        8: [f"Pertahankan *Rapport* (Keakraban Bawah Sadar) dengan mengeksplorasi hobi atau proyek baru bersama untuk mencegah kebosanan.", f"Secara berkala, keluarlah dari zona nyaman rutinitas kalian berdua. Lakukan sesuatu yang memacu adrenalin bersama."]
    }
    dont_list = {
        1: [f"DILARANG KERAS melakukan *Mind-Reading* negatif. Jangan pernah mengasumsikan niat jahat {n2} tanpa klarifikasi eksplisit.", f"Pantang melakukan konfrontasi saat salah satu pihak sedang mengalami kondisi *H.A.L.T* (Hungry, Angry, Lonely, Tired)."],
        2: [f"Hindari jebakan 'Pencitraan Sempurna'. Jangan memalsukan kebahagiaan di luar padahal sedang dingin di dalam.", f"Jangan biarkan intervensi dari keluarga besar atau sirkel pertemanan luar merusak wibawa benteng rumah tangga kalian."],
        3: [f"Hati-hati terjebak dalam ilusi *Comfort Zone* (Zona Nyaman Berlebihan). Jangan sampai kalian malas berjuang untuk karir.", f"Jangan pernah mengabaikan perawatan diri (fisik dan mental) hanya karena merasa posisi Anda sudah 'aman' di hati pasangan."],
        4: [f"Jangan jadikan ego dan gengsi {n1} sebagai senjata penikam hati {n2}. Kompromi di fase adaptasi ini sangat krusial.", f"Pantang lempar handuk (menyerah) di 3 tahun pertama masa transisi. Mengucapkan kata perpisahan saat emosi memuncak akan menghancurkan pondasi."],
        5: [f"Jangan biarkan materi (uang) menjadi satu-satunya perekat jiwa antara {n1} dan {n2}.", f"Dilarang keras menyombongkan diri atau meremehkan orang lain saat pintu rezeki hasil persatuan kalian mulai terbuka lebar."],
        6: [f"Jangan pernah menyerang kelemahan fisik, masa lalu, atau harga diri fundamental {n2} secara frontal hanya karena berdebat sepele.", f"Dilarang menggunakan senjata *Silent Treatment* (mendiamkan pasangan) lebih dari 24 jam. Ini adalah manipulasi emosi."],
        7: [f"DILARANG MENGGUNAKAN kata-kata absolut saat bertengkar, seperti: 'Kamu TIDAK PERNAH peduli!'. Ini mengunci pasangan dalam mode defensif.", f"Jangan menjadi agen rahasia yang mengintai privasi ponsel atau media sosial pasangan secara diam-diam. *Trust issue* mematikan cinta."],
        8: [f"Waspadai jebakan sikap *Take it for granted* (menggampangkan pasangan). Jangan berhenti memberikan usaha lebih (*effort*) untuk membahagiakannya.", f"Jangan biarkan rutinitas mesin mematikan insting romantisme Anda. Rasa aman (*Pesthi*) butuh dirawat."]
    }
    hasil = {
        1: ("💔 PEGAT (Ujian Ego)", "Terdapat perbedaan fundamental arsitektur otak dalam memproses emosi. Sering terjadi adu argumen yang tajam karena ego defensif."),
        2: ("👑 RATU (Kharisma Pasangan)", "Memancarkan wibawa dan daya magnetis sosial yang tinggi. Kehadiran kalian memicu respek alami dari lingkungan."),
        3: ("💞 JODOH (Sinkronisasi Alami)", "Tingkat penerimaan bawah sadar yang sangat dalam. Koneksi batin terbentuk secara instan, seolah frekuensi jiwa sudah pernah terhubung."),
        4: ("🌱 TOPO (Ujian Bertumbuh)", "Awal kolaborasi akan dipenuhi gesekan adaptasi yang berat. Jika berhasil melampaui fase kritis ini, pondasi kalian takkan bisa ditembus badai."),
        5: ("💰 TINARI (Magnet Rezeki)", "Entitas pasangan ini memancarkan vibrasi kelimpahan. Kemacetan finansial mendadak terurai setelah kalian sepakat bersatu."),
        6: ("⚡ PADU (Beda Frekuensi)", "Sering muncul letupan perdebatan karena berbedanya filter informasi. Namun umumnya, yang diributkan hanyalah hal-hal teknis non-esensial."),
        7: ("👁️ SUJANAN (Rawan Asumsi)", "Vibrasi energi ini rawan menarik miskomunikasi dan cemburu buta. Asumsi negatif sering memicu salah paham jika tidak dibedah lewat komunikasi."),
        8: ("🕊️ PESTHI (Damai & Rukun)", "Interaksi batin yang adem ayem dan minim drama. Kehadiran fisik satu sama lain bertindak menetralisir racun stres kehidupan.")
    }
    return hasil[sisa][0], hasil[sisa][1], random.choice(do_list[sisa]), random.choice(dont_list[sisa])

def proc_penjelasan_matriks(n1, n2, eso_val, nep_val):
    random.seed(generate_seed(f"pm_v2_{n1}_{n2}_{eso_val}_{nep_val}"))
    header = random.choice(["⚙️ ARSITEKTUR ANALISA", "📡 DEKODE SINYAL KOSMIK", "📜 LOGIKA MESIN NEURO"])
    f_eso = random.choice([f"Fusi nama <b>{n1}</b> & <b>{n2}</b> mengunci di <b>{eso_val}</b>. Ini adalah persona yang muncul saat kalian bersama.", f"Ekstraksi sandi menghasilkan <b>{eso_val}</b>. Menentukan bagaimana kalian dipandang sebagai entitas."])
    f_nep = random.choice([f"Kalkulasi sinkronisasi waktu (Total Neptu <b>{nep_val}</b>) memetakan dinamika ego bawah sadar.", f"Analisa siklus (Parameter <b>{nep_val}</b>) menjadi radar pengukur stabilitas emosi kalian."])
    return f'<div class="info-metric-box"><b style="color:#FFD700; font-size:14px;">{header}:</b><br>• <b style="color:white;">TOTAL ESOTERIK:</b> {f_eso}<br>• <b style="color:white;">TOTAL NEPTU:</b> {f_nep}</div>'

KAMUS_ABJAD = {
    'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 
    't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 
    's': 60, 'f': 80, 'q': 100, 'r': 200, 'c': 3, 'e': 5,
    'g': 1000, 'i': 10, 'o': 6, 'p': 80, 'u': 6, 'v': 6, 'x': 60
}

def hitung_nama_esoterik(nama):
    nama_clean = ''.join(filter(str.isalpha, str(nama).lower()))
    return sum(KAMUS_ABJAD.get(huruf, 0) for huruf in nama_clean) or 1

def get_rincian_esoterik(nama):
    r = [f"{h.upper()}({KAMUS_ABJAD.get(h,0)})" for h in ''.join(filter(str.isalpha, str(nama).lower())) if KAMUS_ABJAD.get(h,0)>0]
    return " + ".join(r) if r else "0"

def generate_dynamic_reading(total_jummal):
    mod = total_jummal % 4 if total_jummal % 4 != 0 else 4
    el = {1: ("🔥 API (Nar)", "Sistem saraf eksekusi cepat, Anda inisiator."), 2: ("🌍 TANAH (Turab)", "Fondasi logis dan membumi."), 3: ("💨 UDARA (Hawa)", "Konseptor ide tanpa henti."), 4: ("💧 AIR (Ma')", "Emosional peka, empati beradaptasi.")}
    p_red = " + ".join(list(str(total_jummal)))
    s_red = sum(int(d) for d in str(total_jummal))
    r_num = s_red
    while r_num > 9: r_num = sum(int(d) for d in str(r_num))
    r_dict = {1:"Pencipta jalan baru", 2:"Penyelaras harmoni", 3:"Penyampai pesan", 4:"Pembangun sistem", 5:"Agen transformasi", 6:"Pengayom sejati", 7:"Pencari esensi", 8:"Pemegang kendali", 9:"Kesadaran universal"}
    m_note = "<div style='background:rgba(212,175,55,0.1); padding:10px; border-radius:5px;'><span style='color:#FFD700;'>⚡ <b>KODE MASTER:</b></span> Intuisi Spiritual Tinggi Terdeteksi.</div>" if any(m in str(total_jummal) for m in ["11","22","33"]) else ""
    return el[mod][0], el[mod][1], p_red, s_red, r_num, r_dict.get(r_num,""), m_note

def hitung_angka(tanggal):
    try:
        t = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
        while t > 9: t = sum(int(digit) for digit in str(t))
        return t
    except: return 1

def get_rincian_tanggal(tanggal):
    try:
        ts = tanggal.strftime("%d%m%Y")
        p = f"{' + '.join(list(ts))} = {sum(int(d) for d in ts)}"
        t = sum(int(d) for d in ts)
        while t > 9:
            p += f" ➡ {' + '.join(list(str(t)))} = {sum(int(d) for d in str(t))}"
            t = sum(int(d) for d in str(t))
        return p
    except: return "1 = 1"

def hitung_neptu_langsung(hari, pasaran):
    return {"Minggu":5,"Senin":4,"Selasa":3,"Rabu":7,"Kamis":8,"Jumat":6,"Sabtu":9}.get(hari,0) + {"Legi":5,"Pahing":9,"Pon":7,"Wage":4,"Kliwon":8}.get(pasaran,0)
 
def get_betaljemur_data(neptu, hari):
    lk = {7:("Lebu Katiup Angin","Pikiran dinamis"),8:("Lakuning Geni","Emosi meledak-ledak"),9:("Lakuning Angin","Adaptif namun labil"),10:("Pandito Mbangun Teki","Introspektif, cerdas"),11:("Aras Tuding","Pemberani, ditunjuk peluang"),12:("Aras Kembang","Menebar pesona"),13:("Lakuning Lintang","Magnetis menyendiri"),14:("Lakuning Rembulan","Penenang batin"),15:("Lakuning Srengenge","Pencerah logis"),16:("Lakuning Banyu","Ketenangan mematikan"),17:("Lakuning Bumi","Sabar membumi"),18:("Lakuning Paripurna","Pemegang kendali bijak")}
    nd = {"Minggu":"Timur", "Senin":"Selatan", "Selasa":"Barat", "Rabu":"Utara", "Kamis":"Timur", "Jumat":"Selatan", "Sabtu":"Selatan"}
    return lk.get(neptu,("Anomali",""))[0], lk.get(neptu,("Anomali",""))[1], nd.get(hari,"Netral")

def get_rezeki_usaha(neptu):
    r = {1:("Wasesa Segara","Rezeki seluas lautan"),2:("Tunggak Semi","Patah tumbuh hilang berganti"),3:("Satria Wibawa","Dihormati kolega"),4:("Sumur Sinaba","Menjadi referensi, membawa berkah"),5:("Bumi Kapetak","Kerja cerdas dan keras"),6:("Satria Wirang","Rawan rintangan"),7:("Lebu Katiup Angin","Wajib punya aset tetap")}[neptu%7 or 7]
    u = {1:("Sandang","Bisnis komoditas"),2:("Pangan","Kuliner/ritel"),3:("Beja","Instrumen investasi"),4:("Lara","Butuh partner mitigasi"),5:("Pati","Hindari spekulasi buta")}[neptu%5 or 5]
    return r, u
 
def get_zodiak(tanggal):
    d, m = tanggal.day, tanggal.month
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "Aries"
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "Taurus"
    elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "Gemini"
    elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "Cancer"
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "Leo"
    elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "Virgo"
    elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "Libra"
    elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "Scorpio"
    elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "Sagittarius"
    elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "Capricorn"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius"
    else: return "Pisces"

def get_safe_firstname(name_str, default="User"):
    return str(name_str).strip().split()[0].upper() if str(name_str).strip() else default

# Menghitung angka pengguna secara dinamis
dynamic_users = get_dynamic_count()

# --- SIDEBAR PROMOSI & LOGIN ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        try: st.image("baru.jpg.png", use_container_width=True); st.markdown("<br>", unsafe_allow_html=True)
        except: pass
 
    st.markdown(f"### {get_greeting()}")
    
    # SYSTEM LOCK / MEMBERSHIP
    st.markdown("---")
    st.markdown("### 🔓 Akses Premium")
    if not st.session_state.premium:
        kode_input = st.text_input("Punya Kode Akses? Ketik di sini:", type="password")
        if kode_input:
            if kode_input.upper() == "NEUROVIP": # BISA DIGANTI KODE APA AJA BRO
                st.session_state.premium = True
                st.success("✅ Akses Terbuka! Selamat Datang.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Kode Salah atau Kadaluarsa.")
        st.markdown("<p style='font-size:13px; color:#888;'>Dapatkan Kode Akses via <a href='https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy.' target='_blank' style='color:#25D366; font-weight:bold; text-decoration:none;'>WhatsApp</a></p>", unsafe_allow_html=True)
    else:
        st.success("👑 Status: VIP MEMBER")
        if st.button("Logout"):
            st.session_state.premium = False
            st.rerun()
    
    # WA CTA (URGENT & AGGRESSIVE)
    st.markdown("---")
    st.markdown("""<div style='background: linear-gradient(135deg, #ff0000 0%, #8b0000 100%); padding: 18px; border-radius: 10px; text-align: center; border: 1px solid #ff4b4b; box-shadow: 0 5px 15px rgba(255,0,0,0.3);'>
<b style='color: white; font-size: 16px; letter-spacing: 1px;'>🔥 BUTUH ANALISA LEBIH DALAM?</b><br>
<span style='color: #ccc; font-size: 12px; display:block; margin-top:5px;'>Beberapa hasil tidak bisa ditampilkan di sistem.</span>
<span style='color: #FFD700; font-size: 13px; display:inline-block; margin-top:5px; margin-bottom:12px;'>Konsultasi langsung dengan Coach (Slot Terbatas Hari Ini)</span><br>
<a href='https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20butuh%20sesi%20kalibrasi%20private%20hari%20ini' target='_blank' style='background: #25D366; color: white; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 900; font-size: 14px; display: inline-block; box-shadow: 0 4px 10px rgba(37,211,102,0.4);'>💬 KLIK DI SINI SEKARANG</a>
</div>""", unsafe_allow_html=True)
    st.markdown("<br><center><small style='color:#666;'>© 2026 Neuro Nada Academy</small></center>", unsafe_allow_html=True)
 
# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

cur_planet, cur_instr, cur_color = get_planetary_hour()
st.markdown(f"""<div style='text-align: right;'><div class='live-badge' style='background: {cur_color};'>🕒 LIVE PLANET: {cur_planet.upper()}</div><div style='font-size: 11px; color: #888; margin-top: 5px;'>{cur_instr}</div></div>""", unsafe_allow_html=True)
 
st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900; color:#FFD700;'>🌌 BUKA KODE HIDUP ANDA HARI INI</h1>", unsafe_allow_html=True)
st.markdown("""<p style='text-align: center; font-size: 16px; color: #ccc;'>Ini bukanlah Ramalan. Ini adalah pemetaan presisi tinggi berdasarkan cetak biru nama, garis waktu kelahiran, dan bioritme alam semesta Anda.<br><br><b style='color:#FFF;'>⚡ Dalam 10 detik, Anda akan tahu:</b><br><span style='color:#D4AF37;'>• Arah rezeki hari ini<br>• Keputusan yang HARUS diambil<br>• Risiko yang WAJIB dihindari</span></p>""", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; margin-bottom:20px;'><span style='background:rgba(255,75,75,0.2); color:#ff4b4b; padding:8px 15px; border-radius:5px; font-size:13px; font-weight:bold; letter-spacing:1px;'>⚠️ Jangan baca ini kalau belum siap tahu kebenaran tentang diri Anda.</span></div>", unsafe_allow_html=True)
st.markdown("---")
 
tgl_today = datetime.date.today()
tab1, tab2, tab5, tab3, tab4 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Matrix 🔒", "⏱️ Quantum Engine 🔒", "🌌 Falak Ruhani 🔒", "📚 FAQ"])
 
# ==========================================
# TAB 1: IDENTITAS KOSMIK (HOOK & PAYWALL)
# ==========================================
with tab1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#fff;'>👇 Masukkan data Anda sekarang</h4>", unsafe_allow_html=True)
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama asli Anda...", key="t1_nama")
    
    col_tgl, col_wt = st.columns(2)
    with col_tgl:
        st.write("📅 **Data Masehi:**")
        tgl_input = st.date_input("Tanggal Lahir", value=datetime.date(1983, 9, 23), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")
    with col_wt:
        st.write("📜 **Data Weton:**")
        hari_input = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="h_t1")
        pasaran_input = st.selectbox("Pasaran", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="p_t1")
    st.markdown("</div>", unsafe_allow_html=True)
 
    if st.button("🚀 Lihat Peluang Saya Hari Ini", key="btn_t1"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Mohon ketik nama lengkap Anda (minimal 3 huruf).")
        else:
            try:
                with st.spinner('Menyelaraskan frekuensi kosmik...'):
                    time.sleep(1.5)
                
                safe_name = get_safe_firstname(nama_user)
                angka_hasil = hitung_angka(tgl_input)
                rincian_tgl = get_rincian_tanggal(tgl_input)
                
                nilai_jummal = hitung_nama_esoterik(nama_user)
                rincian_jummal = get_rincian_esoterik(nama_user)
                el_nama, el_desc, p_reduk, s_reduk, r_num, r_desc, m_note = generate_dynamic_reading(nilai_jummal)
                
                nep = hitung_neptu_langsung(hari_input, pasaran_input)
                wet = f"{hari_input} {pasaran_input}"
                zod = get_zodiak(tgl_input)
                
                n_laku, d_laku, arah_naga = get_betaljemur_data(nep, hari_input)
                rezeki_data, usaha_data = get_rezeki_usaha(nep)
                
                punchy = arketipe_punchy.get(angka_hasil, arketipe_punchy[1])
                desk_ark_dinamis = proc_arketipe(safe_name, angka_hasil, zod, nep)
                shadow = proc_shadow_list(safe_name, angka_hasil)
                
                # --- HASIL CEPAT 10 DETIK (HOOK - SELALU MUNCUL) ---
                st.markdown(f"""<div class="soft-fade" style="background: rgba(255,215,0,0.1); border-left: 5px solid #FFD700; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,215,0,0.3);">
<h3 style="margin-top:0; color:#FFD700; font-weight:900; letter-spacing:1px;">🎯 HASIL ANDA HARI INI</h3>
<ul style="font-size: 17px; line-height: 1.8; color: #fff; list-style-type: none; padding-left: 0;">
<li style="margin-bottom: 10px;">💰 <b>REZEKI:</b> <span style="color:#25D366; font-weight:bold;">TERBUKA</span> <i style="color:#aaa; font-size:14px;">(Momentum tinggi - {rezeki_data[0]})</i></li>
<li style="margin-bottom: 10px;">⚡ <b>AKSI:</b> Hubungi seseorang yang sudah lama Anda tunda.</li>
<li style="margin-bottom: 10px;">🚫 <b>LARANGAN:</b> Jangan ambil keputusan finansial besar hari ini (Waspadai sifat {shadow[0].lower()}).</li>
</ul>
<div style="background: rgba(255,75,75,0.2); padding: 8px 15px; border-radius: 5px; display: inline-block; margin-top: 10px;">
<b style="color:#ff4b4b; font-size:13px;">⏳ Energi ini hanya berlaku sampai 24 jam ke depan</b>
</div>
</div>""", unsafe_allow_html=True)
                
                # --- PAYWALL: CEK STATUS PREMIUM ---
                if not st.session_state.premium:
                    st.markdown(f"""<div class="glass-container soft-fade" style="text-align:center; border: 2px solid #ff4b4b; padding: 30px 20px;">
<h3 style="color:#ff4b4b; margin-top:0;">🔓 Anda baru melihat 20% dari hasil Anda...</h3>
<div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: left; display: inline-block;">
<span style="color:#ccc; font-size: 15px;">Di dalam analisa lengkap:</span><br>
<b style="color:#fff;">• Blueprint kepribadian terdalam Anda</b><br>
<b style="color:#fff;">• Titik kebocoran rezeki Anda</b><br>
<b style="color:#fff;">• Strategi spesifik 60 menit ke depan</b><br>
<b style="color:#fff;">• Analisa hubungan & jodoh (jika ada pasangan)</b>
</div>
<p style="color:#FFD700; font-size: 16px;"><b>🔥 Ini bukan informasi umum.<br>Ini PERSONAL — hanya untuk Anda.</b></p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration:none;">
<div class="cta-button" style="font-size:18px; margin-top: 10px;">🚀 AKTIFKAN ANALISA LENGKAP</div>
</a>
<p style="font-size:14px; color:#ccc; margin-top:15px; margin-bottom: 5px;">Hanya <b>Rp 19.000</b><br><i style="color:#888;">(Lebih murah dari kopi, tapi bisa ubah arah hidup Anda)</i></p>
<span style="background:rgba(255,75,75,0.2); color:#ff4b4b; padding:4px 10px; border-radius:3px; font-size:12px; font-weight:bold;">⚠️ Harga bisa naik kapan saja | Akses langsung terbuka</span>
<div style="margin-top: 25px; border-top: 1px dashed #555; padding-top: 15px;">
<span style="font-size:14px; color:#25D366; font-weight:bold;">🔥 {dynamic_users} orang sudah membuka analisa mereka hari ini.</span><br>
<span style="font-size:13px; color:#888;">Jangan jadi yang ketinggalan momentum.</span>
</div>
<br><br>
<div style='background: rgba(212,175,55,0.1); padding: 15px; border-radius: 10px; border: 1px solid #D4AF37;'>
<b style='color: #D4AF37; font-size: 16px; letter-spacing: 1px;'>🚀 BONUS (VERSI SUPER VIRAL)</b><br>
<span style='color: white; font-size: 14px; display:inline-block; margin-top:5px; margin-bottom:12px;'><i>“Jangan baca ini kalau belum siap tahu kebenaran tentang diri Anda”</i></span>
</div>
</div>""", unsafe_allow_html=True)
                else:
                    # --- DEEP ANALYSIS (HANYA JIKA PREMIUM) ---
                    st.markdown(f"<h3 style='text-align:center;'>🌌 Deep Analysis: {safe_name}</h3>", unsafe_allow_html=True)
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Nilai Esoterik</div><div class="matrix-value matrix-value-special">{nilai_jummal}</div></div><div class="matrix-item"><div class="matrix-label">Elemen Dasar</div><div class="matrix-value">{el_nama.split(' ')[1] if len(el_nama.split(' '))>1 else el_nama}</div></div><div class="matrix-item"><div class="matrix-label">Meta-Program</div><div class="matrix-value matrix-value-special">KODE {angka_hasil}</div></div><div class="matrix-item"><div class="matrix-label">Filter Zodiak</div><div class="matrix-value">{zod}</div></div><div class="matrix-item"><div class="matrix-label">Energi Weton</div><div class="matrix-value">{wet} ({nep})</div></div></div>""", unsafe_allow_html=True)
                    st.markdown(f"""<div class="dynamic-reading-box soft-fade"><h4 style="color: #FFD700; margin-top:0;">🔍 Bedah DNA Angka & Waktu Lahir</h4><p><b>1. Sandi Esoterik Nama (Hisab Jummal)</b><br><code style="color:#25D366; background:transparent; padding:0;">{rincian_jummal} = <b>{nilai_jummal}</b></code></p><ul style="margin-left: -15px; margin-bottom: 20px;"><li><b>Elemen Bawah Sadar:</b> {el_nama} - <i style="color:#aaa;">{el_desc}</i></li><li><b>Inti Jiwa (Root Number):</b> {p_reduk} = {s_reduk} ➡ <b>{r_num}</b> ({r_desc})</li></ul><p><b>2. Sandi Waktu Lahir (Meta-Program NLP)</b><br><code style="color:#FFD700; background:transparent; padding:0;">{rincian_tgl}</code><br><span style="font-size:14px; color:#ccc;">Maka didapatkan <b>KODE {angka_hasil}</b>. Angka ini adalah <i>Blueprint</i> otak <b>{safe_name}</b> memproses informasi.</span></p>{m_note}</div>""", unsafe_allow_html=True)
                    st.markdown(f"""<div class="primbon-box soft-fade"><div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;"><span style="color:#D4AF37; font-size:14px; font-weight:900; letter-spacing:2px;">📜 PETHIKAN KITAB BETALJEMUR ADAMMAKNA</span></div><div style="font-size:15px; line-height:1.6; margin-bottom: 15px;"><b style="color:#FFF; font-size:18px;">{n_laku}</b> — <i style="color:#ccc;">"{d_laku}"</i></div><div style="font-size:15px; line-height:1.6; margin-bottom: 15px; border-top: 1px dashed #555; padding-top: 10px;">• <b>Rezeki (<span style="color:#FFD700;">{rezeki_data[0]}</span>):</b> <i style="color:#ccc;">{rezeki_data[1]}</i><br>• <b>Usaha (<span style="color:#25D366;">{usaha_data[0]}</span>):</b> <i style="color:#ccc;">{usaha_data[1]}</i></div><div style="font-size:15px; line-height:1.6; background: rgba(212,175,55,0.1); padding: 10px; border-radius: 8px;"><span style="color:#FFD700;">🧭 <b>NAGA DINA (Arah Kejayaan Hari {hari_input}):</b></span> <b style="font-size: 16px;">{arah_naga}</b><br><i style="color:#888; font-size:13px;">*ACTIONABLE: Posisikan diri Anda menghadap <b>{arah_naga}</b> saat mengambil keputusan penting hari ini.</i></div></div>""", unsafe_allow_html=True)
                    st.markdown(f"### 👁️ Decode Kepribadian Dinamis: {safe_name}")
                    st.info(f"Mengacu pada pola unik {safe_name}, arketipe utama dikunci sebagai:\n\n**{punchy['inti']}**")
                    st.write(desk_ark_dinamis)
                    
                    c_kekuatan, c_shadow = st.columns(2)
                    with c_kekuatan:
                        st.markdown(f"🔥 **KEKUATAN DOMINAN:**")
                        st.markdown(f"<ul class='list-punchy' style='color:#25D366;'><li>{punchy['kekuatan'][0]}</li><li>{punchy['kekuatan'][1]}</li><li>{punchy['kekuatan'][2]}</li></ul>", unsafe_allow_html=True)
                    with c_shadow:
                        st.markdown(f"⚠️ **SHADOW TERSEMBUNYI:**")
                        st.markdown(f"<ul class='list-punchy' style='color:#ff4b4b;'><li>{shadow[0]}</li><li>{shadow[1]}</li><li>{shadow[2]}</li></ul>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Sistem gagal melakukan komputasi: {e}")
 
# ==========================================
# TAB 2: COUPLE MATRIX (LOCKED)
# ==========================================
with tab2:
    if not st.session_state.premium:
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h3 style='color: #ff4b4b; font-weight: 900; margin-top:0;'>💞 CEK KECOCOKAN ANDA & DIA</h3>
<p style='color: #ccc; font-size: 16px; margin-bottom: 20px;'>Apakah hubungan ini:<br><b style='color:#ff4b4b;'>❤️ JODOH?</b> | <b style='color:#FFD700;'>⚡ Ujian?</b> | <b style='color:#888;'>💔 Atau sebenarnya tidak cocok?</b></p>
<p style='font-size: 14px; color: #aaa; margin-bottom: 30px;'>Masukkan 2 nama dan lihat hasilnya sekarang.<br><i style='color:#ff4b4b;'>⚠️ Banyak yang kaget setelah lihat hasilnya.</i></p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN KODE VIA WHATSAPP (Rp 19.000)</div>
</a>
<p style='font-size:13px; color:#25D366; font-weight:bold; margin-top:15px;'>🔥 {dynamic_users} orang sudah membuka analisa mereka hari ini.</p>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("💞 Penyatuan Esoterik & Betaljemur (Couple Matrix)")
        ca, cb = st.columns(2)
        with ca: 
            st.markdown("<h4 style='color:#FFD700;'>Pihak 1 (Pria)</h4>", unsafe_allow_html=True)
            n1 = st.text_input("Nama Anda", key="n1_c")
            d1 = st.date_input("Lahir Masehi", value=datetime.date(1995, 1, 1), format="DD/MM/YYYY", key="d1_c")
            hc1 = st.selectbox("Hari Pria", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="hc1")
            pc1 = st.selectbox("Pasaran Pria", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="pc1")
        with cb: 
            st.markdown("<h4 style='color:#FF69B4;'>Pihak 2 (Wanita)</h4>", unsafe_allow_html=True)
            n2 = st.text_input("Nama Pasangan", key="n2_c")
            d2 = st.date_input("Lahir Wanita", value=datetime.date(1995, 1, 1), format="DD/MM/YYYY", key="d2_c")
            hc2 = st.selectbox("Hari Wanita", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=2, key="hc2")
            pc2 = st.selectbox("Pasaran Wanita", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=0, key="pc2")
        st.markdown("</div>", unsafe_allow_html=True)
            
        if st.button("🚀 Lihat Nasib Saya Hari Ini", key="btn_couple"):
            if str(n1).strip() and str(n2).strip():
                try:
                    with st.spinner('Menghitung benturan energi pasangan...'):
                        time.sleep(1.5)
                    
                    safe_n1, safe_n2 = get_safe_firstname(n1, "Pria"), get_safe_firstname(n2, "Wanita")
                    zod1, zod2 = get_zodiak(d1), get_zodiak(d2)
                    nep_1, nep_2 = hitung_neptu_langsung(hc1, pc1), hitung_neptu_langsung(hc2, pc2)
                    sel = abs(hitung_angka(d1) - hitung_angka(d2))
                    
                    jummal_1, jummal_2 = hitung_nama_esoterik(n1), hitung_nama_esoterik(n2)
                    total_couple = jummal_1 + jummal_2
                    root_c = total_couple
                    while root_c > 9: root_c = sum(int(d) for d in str(root_c))
                    
                    c_title, c_desc = proc_couple_persona(root_c, safe_n1, safe_n2)
                    judul_jodoh, desk_jodoh, d_do, d_dont = proc_weton_kombo((nep_1+nep_2)%8 or 8, safe_n1, safe_n2, zod1, zod2)
                    
                    st.markdown(f"### 🔮 The Unified Resonance: {safe_n1} & {safe_n2}")
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Neptu {safe_n1}</div><div class="matrix-value">{hc1} {pc1} ({nep_1})</div></div><div class="matrix-item"><div class="matrix-label">Neptu {safe_n2}</div><div class="matrix-value">{hc2} {pc2} ({nep_2})</div></div><div class="matrix-item" style="background: rgba(212,175,55,0.2);"><div class="matrix-label" style="color:#FFD700;">TOTAL NEPTU</div><div class="matrix-value matrix-value-special">{nep_1 + nep_2}</div></div><div class="matrix-item"><div class="matrix-label">Total Esoterik</div><div class="matrix-value">{total_couple}</div></div></div>""", unsafe_allow_html=True)
                    st.markdown(proc_penjelasan_matriks(safe_n1, safe_n2, total_couple, (nep_1+nep_2)), unsafe_allow_html=True)
                    st.markdown(f'<div class="dynamic-reading-box soft-fade" style="border-left-color: #25D366;"><h4 style="color: #25D366; margin-top:0;">🧬 Persona Pasangan: {c_title}</h4><p><i>{c_desc}</i></p></div>', unsafe_allow_html=True)
                    st.info(f"**Titik Benturan Weton ({judul_jodoh}):**\n{desk_jodoh}")
                    
                    if sel in [0, 3, 6, 9]: st.success(f"💘 **SKOR META-PROGRAM (NLP): Sangat Sinkron**")
                    elif sel in [1, 2, 8]: st.warning(f"⚖️ **SKOR META-PROGRAM (NLP): Dinamis** - Butuh toleransi.")
                    else: st.error(f"🔥 **SKOR META-PROGRAM (NLP): Rawan Gesekan**")
         
                    c_do_c, c_dont_c = st.columns(2)
                    with c_do_c: st.markdown(f"<div class='soft-fade' style='background:rgba(37,211,102,0.1); padding:20px; border-radius:10px; border:1px solid #25D366; height:100%;'><b style='color:#25D366; font-size:16px;'>✅ LAKUKAN INI:</b><br><br><span style='color:#e0e0e0; line-height:1.6;'>{d_do}</span></div>", unsafe_allow_html=True)
                    with c_dont_c: st.markdown(f"<div class='soft-fade' style='background:rgba(255,75,75,0.1); padding:20px; border-radius:10px; border:1px solid #ff4b4b; height:100%;'><b style='color:#ff4b4b; font-size:16px;'>❌ HINDARI INI:</b><br><br><span style='color:#e0e0e0; line-height:1.6;'>{d_dont}</span></div>", unsafe_allow_html=True)
                except Exception as e: st.error(f"Error komputasi: {e}")

# ==========================================
# TAB 5: QUANTUM ENGINE (LOCKED)
# ==========================================
with tab5:
    if not st.session_state.premium:
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 FITUR PREMIUM DIKUNCI</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Anda sedang mengakses versi Gratis. Buka akses <b>Tactical Action Plan (Pemetaan Aksi Taktis Harian)</b> yang dikalibrasi real-time dengan energi planet Anda.</p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN KODE VIA WHATSAPP (Rp 19.000)</div>
</a>
<p style='font-size:13px; color:#25D366; font-weight:bold; margin-top:15px;'>🔥 {dynamic_users} orang sudah membuka analisa mereka hari ini.</p>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("⏱️ Live Cosmic Dashboard (Fate Hacking)")
        qe_nama = st.text_input("Nama Panggilan:", key="qe_n")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Lihat Nasib Saya Hari Ini", key="btn_qe"):
            if qe_nama:
                with st.spinner('Menarik data pergerakan planet...'):
                    time.sleep(1.2)
                
                safe_qe = get_safe_firstname(qe_nama)
                jummal_qe = hitung_nama_esoterik(qe_nama)
                mod_harian = (jummal_qe + sum(int(d) for d in tgl_today.strftime("%d%m%Y"))) % 7
                
                sun_fase, sun_desc = get_sun_phase()
                planet_live, planet_desc, planet_color = get_planetary_hour()
                
                siklus_nama, html_plan = proc_tactical_plan(safe_qe, mod_harian, planet_live, planet_desc, sun_fase, sun_desc)
                
                st.markdown(f"### 📡 Live Dashboard: {safe_qe}")
                st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Fase Harian</div><div class="matrix-value">{siklus_nama.split('(')[0].strip()}</div></div><div class="matrix-item"><div class="matrix-label">Matahari</div><div class="matrix-value matrix-value-special">{sun_fase.split(' ')[0]}</div></div><div class="matrix-item" style="border-bottom: 2px solid {planet_color};"><div class="matrix-label">Jam Planet</div><div class="matrix-value" style="color:{planet_color};">{planet_live}</div></div></div>""", unsafe_allow_html=True)
                
                st.markdown(html_plan, unsafe_allow_html=True)

# ==========================================
# TAB 3: FALAK RUHANI (LOCKED)
# ==========================================
with tab3:
    if not st.session_state.premium:
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 FITUR PREMIUM DIKUNCI</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Anda sedang mengakses versi Gratis. Buka resep <b>Terapi Falak Ruhani, Afirmasi NLP Khusus, & Penawar Mental Block</b> dengan Akses Premium.</p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN KODE VIA WHATSAPP (Rp 19.000)</div>
</a>
<p style='font-size:13px; color:#25D366; font-weight:bold; margin-top:15px;'>🔥 {dynamic_users} orang sudah membuka analisa mereka hari ini.</p>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("🌌 Terapi Falak Ruhani & Hypno-NLP")
        st.info("**Reset Ulang Saraf Anda**\n\nSistem mengonversi nama Anda menjadi angka getaran, lalu mencocokkannya dengan frekuensi Asmaul Husna dan Afirmasi Bawah Sadar untuk menghancurkan *Mental Block*.")
        nama_ruhani = st.text_input("Masukkan Nama Lengkap Anda:", placeholder="Ketik nama asli...", key="input_ruhani")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Lihat Nasib Saya Hari Ini", key="btn_ruhani"):
            if nama_ruhani and len(nama_ruhani.strip()) >= 3:
                try:
                    with st.spinner('Mengekstrak sandi penyembuhan Anda...'):
                        time.sleep(1.5)
                        
                    safe_nr = get_safe_firstname(nama_ruhani)
                    nilai_jummal_r = hitung_nama_esoterik(nama_ruhani)
                    
                    r_num_r = nilai_jummal_r
                    while r_num_r > 9: r_num_r = sum(int(d) for d in str(r_num_r))
                    
                    asma_terapi, vibrasi_asma, tujuan_ruhani, jumlah_dzikir = proc_falak_ruhani(nilai_jummal_r, r_num_r, safe_nr)
                    protokol_nlp = get_protokol_terapi(r_num_r, safe_nr)
                    
                    st.markdown(f"""<div class="soft-fade" style="background: linear-gradient(135deg, rgba(10, 20, 40, 0.9) 0%, rgba(20, 10, 40, 0.9) 100%); border-left: 5px solid #00FFFF; padding: 25px; border-radius: 12px; margin-top: 20px; box-shadow: 0 8px 25px rgba(0, 255, 255, 0.15);">
<div style="text-align:center; border-bottom:1px solid #00FFFF; padding-bottom:10px; margin-bottom:20px;">
<span style="color:#00FFFF; font-size:16px; font-weight:900; letter-spacing:2px;">🧠 PROTOKOL TERAPI KOMPREHENSIF: {safe_nr}</span>
</div>
<div style="margin-bottom: 20px;">
<b style="color:#ff4b4b; font-size:16px;">⚠️ MENTAL BLOCK (Virus Bawah Sadar):</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.6;">{protokol_nlp['block']}</span>
</div>
<div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
<b style="color:#FFF; font-size:16px;">✨ 1. ANCHOR SPIRITUAL (Falak Ruhani)</b><br>
<span style="color:#aaa; font-size:14px;">Gunakan Asma ini sebagai Dzikir penenang hati:</span><br>
<b style="color:#00FFFF; font-size:20px;">{asma_terapi}</b> <span style="color:#FFD700; font-weight:bold;">(BACA {jumlah_dzikir}x)</span><br>
<i style="color:#ccc; font-size:14px;">Fungsi: {tujuan_ruhani}</i>
</div>
<div style="background: rgba(255,215,0,0.05); border-left: 4px solid #FFD700; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
<b style="color:#FFD700; font-size:16px;">🗣️ 2. SUGESTI HYPNO-NLP (Afirmasi Diri)</b><br>
<span style="color:#aaa; font-size:14px;">Ucapkan kalimat ini berulang di dalam hati dengan penuh keyakinan menjelang tidur (Gelombang Theta):</span><br>
<i style="color:#fff; font-size:16px; line-height:1.6;">"{protokol_nlp['afirmasi']}"</i>
</div>
<div style="border-top: 1px dashed #555; padding-top: 15px; padding-bottom: 5px;">
<b style="color:#25D366; font-size:16px;">🏃‍♂️ 3. QUANTUM HABIT (Tindakan Fisik Hari Ini)</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.6;">Semesta merespons tindakan nyata. Untuk menghancurkan rantai Mental Block Anda secara instan, eksekusi satu tugas ini hari ini juga:<br>
<b style="color:#FFF;">{protokol_nlp['habit']}</b></span>
</div>
<p style="font-size:12px; color:#ff4b4b; margin-top:15px; font-weight:bold;">⏳ Sistem mendeteksi perubahan energi. Lakukan protokol ini sebelum siklus berganti!</p>
</div>""", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses sandi terapi: {e}")
                
            else:
                st.warning("⚠️ Ketik nama lengkap Anda (minimal 3 huruf) untuk sinkronisasi.")

# ==========================================
# TAB 4: FAQ
# ==========================================
with tab4:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("📚 FAQ & Navigasi Energi")
    with st.expander("🤔 1. Apa itu Jam Planet?"): st.write("Pembagian waktu astronomi kuno yang membagi siang/malam menjadi 12 fase energi.")
    with st.expander("🤔 2. Apa itu Hisab Jummal?"): st.write("Sains huruf kuno (Gematria Arab) yang memberi bobot matematika pada tiap aksara.")
    with st.expander("🤔 3. Apakah hasil ini mutlak?"): st.write("TIDAK. Ini adalah Alat Pemetaan Pola (Pattern Mapping) untuk Self-Awareness.")
    st.error("**⚠️ DISCLAIMER:** Bukan saran medis profesional.")
    st.markdown("</div>", unsafe_allow_html=True)
 
# ==========================================
# SOCIAL PROOF
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Transformasi</h3>", unsafe_allow_html=True)
daftar_ulasan = ambil_ulasan()
if daftar_ulasan:
    marquee_content = " | ".join([f"<span style='color: #FFD700;'>{u.get('Rating', '⭐⭐⭐⭐⭐')}</span> <b>{u.get('Nama', 'User')}:</b> \"{u.get('Komentar', '')[:50]}...\"" for u in daftar_ulasan[:3]])
    st.markdown(f'<div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;"><marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">{marquee_content}</marquee></div>', unsafe_allow_html=True)
    for u in daftar_ulasan[:5]:
        if u.get("Komentar", ""): st.markdown(f'<div class="ulasan-box"><span style="color: #FFD700; font-size: 12px;">{u.get("Rating", "⭐⭐⭐⭐⭐")}</span><br><b>{u.get("Nama", "Jiwa")}</b><br><i style="color: #ccc;">"{u.get("Komentar", "")}"</i></div>', unsafe_allow_html=True)

with st.expander("💬 Bagikan Pengalaman Anda"):
    with st.form("form_review"):
        rn, rr, rk = st.text_input("Nama"), st.radio("Rating", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"], horizontal=True), st.text_area("Ulasan")
        if st.form_submit_button("Kirim") and rn and rk:
            if kirim_ulasan(rn, rr, rk): 
                st.success("Terkirim!")
                time.sleep(1)
                st.rerun()
 
st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Certified NLP Trainer & Professional Hypnotherapist © 2026</small></center>", unsafe_allow_html=True)



import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
import math
import random
import csv
import io
import hashlib

# --- INIT SESSION STATE (PAYWALL) ---
if 'premium' not in st.session_state:
    st.session_state.premium = False

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada Ultimate OS", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- CUSTOM CSS & SOFT ANIMATION ---
st.markdown(
    """<style>
    @keyframes softFade {
        0% { opacity: 0; transform: translateY(20px); filter: blur(5px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    .soft-fade {
        animation: softFade 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; background-color: #050505; color: #e0e0e0; }
    .stApp { background: radial-gradient(circle at top, #111 0%, #000 100%); }
    
    div.stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%) !important; color: #000000 !important;
        font-weight: 900 !important; border: none !important;
        padding: 15px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3); letter-spacing: 1px;
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(255,215,0,0.5); }
    
    .cta-button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff0000 100%);
        color: white !important; padding: 15px; text-align: center; 
        border-radius: 8px; font-weight: 900; font-size: 16px; 
        box-shadow: 0 6px 15px rgba(255, 75, 75, 0.4);
        text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;
    }
    .cta-button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255, 75, 75, 0.6); }

    .ulasan-box {
        background: rgba(30, 30, 30, 0.6); backdrop-filter: blur(10px);
        padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700; 
        margin-bottom: 12px; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .glass-container {
        background: rgba(25, 25, 25, 0.5); backdrop-filter: blur(12px);
        padding: 20px; border-radius: 12px; border: 1px solid rgba(212,175,55,0.2);
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.4); margin-bottom: 15px;
    }
    
    .primbon-box {
        background: linear-gradient(135deg, rgba(43,27,5,0.8) 0%, rgba(74,48,0,0.8) 100%);
        backdrop-filter: blur(10px); padding: 25px; border-radius: 12px; 
        border: 1px solid #D4AF37; box-shadow: 0 8px 25px rgba(212,175,55,0.3); 
        margin-top: 20px; margin-bottom: 20px;
    }

    .dynamic-reading-box {
        background: rgba(20, 20, 20, 0.7); backdrop-filter: blur(5px);
        padding: 20px; border-radius: 12px; border-left: 5px solid #FFD700;
        margin-top: 15px; margin-bottom: 15px; font-size: 15px; line-height: 1.6;
    }
    
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap;
        padding: 15px; background: rgba(10,10,10,0.8); border-radius: 10px;
        border: 1px solid #333; margin-bottom: 5px; box-shadow: inset 0 2px 15px rgba(0,0,0,0.6);
    }
    .matrix-item { flex: 1; min-width: 80px; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 18px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }
    
    .list-punchy { padding-left: 20px; margin-bottom: 15px; font-size: 15px; }
    .list-punchy li { margin-bottom: 8px; }
    
    .live-badge {
        background: linear-gradient(90deg, #D4AF37, #FFD700);
        color: #000; padding: 8px 20px; border-radius: 30px;
        font-weight: 900; font-size: 14px; letter-spacing: 1px;
        display: inline-block; box-shadow: 0 4px 15px rgba(255,215,0,0.4);
    }

    .info-metric-box {
        background: rgba(255,215,0,0.05); border: 1px solid rgba(255,215,0,0.2);
        padding: 15px; border-radius: 8px; font-size: 13px; color: #ccc;
        margin-bottom: 20px; line-height: 1.5;
    }
    </style>""", unsafe_allow_html=True
)

def get_dynamic_count():
    start_date = datetime.date(2026, 4, 15) 
    today = datetime.date.today()
    delta = (today - start_date).days
    if delta < 0: delta = 0
    count = 1287 + (delta * 5)
    return f"{count:,}".replace(",", ".")

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa Kosmik"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

def get_planetary_hour():
    planets = [
        ("Matahari ☀️", "Fokus pada otoritas, presentasi, dan mengambil kendali.", "#FFD700"), 
        ("Venus 💖", "Waktu emas untuk negosiasi, asmara, dan melobi orang.", "#FF69B4"), 
        ("Merkurius 📝", "Eksekusi semua urusan email, naskah, dan komunikasi.", "#00FFFF"), 
        ("Bulan 🌙", "Waktu intuitif. Bagus untuk brainstorming atau istirahat.", "#F0F8FF"), 
        ("Saturnus 🪐", "Energi berat. Fokus pada pekerjaan repetitif dan audit.", "#8B4513"), 
        ("Yupiter 🍀", "Pintu rezeki terbuka. Waktu terbaik investasi/pitching.", "#32CD32"), 
        ("Mars ⚔️", "Energi agresif tinggi. Cocok untuk olahraga/eksekusi berani.", "#FF4500")
    ]
    return planets[datetime.datetime.now().hour % 7]

def get_sun_phase():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 8: return "Sunrise (Inisiasi)", "Gelombang otak beralih ke Alpha. Ideal untuk setting niat harian."
    elif 8 <= hour < 12: return "Morning (Akselerasi)", "Energi memuncak. Eksekusi tugas paling sulit sekarang."
    elif 12 <= hour < 15: return "Zenith (Konsolidasi)", "Matahari di puncak. Waktu untuk evaluasi dan re-kalibrasi."
    elif 15 <= hour < 18: return "Golden Hour (Refleksi)", "Waktu terbaik untuk kreativitas dan menyelesaikan urusan harian."
    elif 18 <= hour < 20: return "Sunset (Pelepasan)", "Tutup sistem saraf Anda dari beban kerja."
    else: return "Night Void (Regenerasi)", "Fase Delta. Dilarang mengambil keputusan besar di jam ini."

# --- DATABASE CLOUD ---
URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            decoded = response.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            return [row for row in reader][::-1]
    except: return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        req = urllib.request.Request(URL_POST, data=data)
        urllib.request.urlopen(req)
        return True
    except: return False

def generate_seed(base_str):
    return int(hashlib.md5(base_str.encode('utf-8')).hexdigest(), 16) % (10**8)

# --- PROCEDURAL TACTICAL PLAN (DYNAMIC & DEEP) ---
def proc_tactical_plan(nama, mod_harian, planet_live, planet_desc, sun_fase, sun_desc):
    random.seed(generate_seed(f"tac_{nama}_{mod_harian}_{planet_live}"))
    fase_detail = {
        0: {"nama": "🔴 FASE NADIR (Rest & Reset)", "analisa": f"Sistem saraf dan gelombang otak {nama} sedang berada di titik terendah siklusnya. Tubuh eterik Anda sedang melakukan 'reboot' sistem internal. Memaksakan ambisi besar hari ini sama dengan memacu mobil dengan gigi satu, mesin saraf Anda akan cepat aus dan *burnout*.", "do": ["Kerjakan hal-hal repetitif yang tidak butuh mikir keras (balas email biasa, rapihin file).", "Lakukan *Deep Rest*, *stretching* fisik, atau perbanyak tidur untuk regenerasi sel."], "dont": "DILARANG KERAS membuat keputusan finansial besar, mengambil risiko bisnis, atau memulai konflik emosional hari ini. Filter logika Anda sedang lemah."},
        1: {"nama": "🟢 FASE INISIASI (The Spark)", "analisa": f"Ini adalah momentum ledakan energi pertama Anda, {nama}! Pintu kosmik terbuka lebar untuk niat-niat baru. Segala sesuatu (sekecil apapun) yang Anda mulai hari ini memiliki daya dorong *momentum* 3x lipat lebih kuat dari hari biasa.", "do": ["Luncurkan ide baru, kirim proposal, atau hubungi prospek/klien target Anda sekarang.", "Lakukan gebrakan eksekusi pertama, walau hanya 5 menit, jangan tunggu sempurna."], "dont": "HINDARI sifat *over-analysis*. Hari ini adalah tentang 'Speed of Implementation', bukan tentang kesempurnaan. Bertindaklah!"},
        2: {"nama": "🔵 FASE SINKRONISASI (Kolaborasi)", "analisa": f"Energi independen (kesendirian) {nama} sedang menurun secara alami, digantikan oleh daya magnetisme sosial. Hari ini, rezeki dan solusi masalah Anda kemungkinan besar tidak datang dari diri sendiri, melainkan tersembunyi di tangan orang lain.", "do": ["Ajak negosiasi pihak yang tadinya alot, hari ini aura Anda lebih persuasif dan diterima.", "Delegasikan tugas yang bikin pusing ke tim atau orang yang lebih ahli."], "dont": "JANGAN menjadi 'Lone Wolf' (berjuang sendirian) memecahkan masalah besar hari ini. Anda akan cepat kehabisan daya dan frustrasi."},
        3: {"nama": "🟡 FASE RESONANSI (Ekspresi Diri)", "analisa": f"Cakra komunikasi {nama} sedang menyala terang. Frekuensi suara dan pilihan kata-kata tulisan Anda memiliki daya tembus alam bawah sadar yang luar biasa kepada siapapun yang mendengarnya hari ini.", "do": ["Buat konten (video/tulisan), lakukan presentasi, *pitching*, atau *Live* di sosmed.", "*Speak up*! Sampaikan keluhan, batasan, atau ide yang selama ini Anda pendam ke atasan/pasangan."], "dont": "JANGAN berdiam diri di goa atau memilih diam saat ditanya. Sangat sayang jika energi persuasi magis ini terbuang percuma."},
        4: {"nama": "🟤 FASE MATERIALISASI (Pondasi)", "analisa": f"Gelombang otak {nama} sedang sangat rasional, praktis, dan membumi. Ini bukan waktunya berkhayal masa depan. Hari ini murni tentang mengamankan dan merawat apa yang sudah Anda bangun agar tidak runtuh.", "do": ["Audit total arus kas (keuangan) Anda. Cek mutasi dan kebocoran pengeluaran minggu ini.", "Fokus pada detail operasional yang membosankan namun vital bagi bisnis."], "dont": "DILARANG mengambil risiko spekulatif (judi, trading asal, investasi tanpa data valid, foya-foya) hari ini. Pegang aset Anda erat-erat."},
        5: {"nama": "🟠 FASE EKSPANSI (Tantangan Ekstrim)", "analisa": f"Adrenalin kosmik {nama} memuncak tajam! Insting bertahan hidup dan *growth* Anda sedang sinkron. Batas-batas ketakutan (mental block) Anda melemah, memberikan celah terbuka untuk melakukan terobosan radikal.", "do": ["Eksekusi satu hal yang paling Anda takuti minggu ini (misal: *follow-up* klien kelas kakap atau *cold calling*).", "Uji coba strategi marketing/bisnis yang 'Out of the Box' dan berisiko."], "dont": "JANGAN biarkan diri Anda diam terjebak dalam kebosanan rutinitas. Diam hari ini akan berubah menjadi *Anxiety* (kecemasan parah)."},
        6: {"nama": "🟣 FASE ELEVASI (Pengayoman & Karma)", "analisa": f"Vibrasi jiwa {nama} menembus urusan duniawi hari ini. Anda memancarkan energi *Healer* (Penyembuh/Orang Tua). Alam semesta menuntut Anda sejenak kembali ke 'akar': keluarga, keikhlasan batin, dan relasi spiritual.", "do": ["Perbaiki hubungan yang retak. Minta maaf atau maafkan kesalahan pasangan/orang tua/sahabat.", "Lakukan *Charity* (sedekah nominal ekstrim) atau bantu kesulitan orang lain secara anonim."], "dont": "HINDARI debat ego, pertengkaran keras kepala, atau ambisi memanipulasi orang lain demi keuntungan uang. Karma berlaku instan hari ini."}
    }
    fd = fase_detail[mod_harian]
    buka = random.choice([f"Berdasarkan dekripsi algoritma lahir dan posisi langit saat ini, sistem mendeteksi lonjakan energi spesifik pada diri Anda, **{nama}**.", f"Peringatan Taktis! Gelombang kosmik sedang berpusat pada sektor tindakan Anda. Jika **{nama}** salah melangkah dalam jam ini, momentum akan hangus."])
    planet_murni = planet_live.split(' ')[0]
    matahari_murni = sun_fase.split(' ')[0]
    koneksi = random.choice([f"Diperkuat oleh jam {planet_murni} yang mengintervensi fase {matahari_murni} Anda, situasi ini menciptakan desakan absolut untuk bertindak.", f"Resonansi {planet_murni} yang bertabrakan dengan siklus {matahari_murni} ini mengunci otak Anda dalam mode sadar tingkat tinggi."])
    do_html = "".join([f"<li style='margin-bottom: 8px;'>{item}</li>" for item in random.sample(fd["do"], 2)])

    html_output = f"""<div class="live-engine-box soft-fade" style="background: rgba(20,20,25,0.9); border-left: 4px solid #00FFFF; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,255,255,0.1);">
<h4 style="color: #00FFFF; margin-top:0; letter-spacing: 1px; font-weight:900;">⚡ TACTICAL ACTION PLAN <span style="font-size:12px; color:#ff4b4b; font-weight:normal;">(⏳ Valid 24 Jam)</span></h4>
<p style="color: #ccc; font-size: 15px; line-height: 1.6; margin-bottom:20px;">
{buka}<br><br>
<b style="color:#FFF; font-size:16px;">STATUS BIORITME ANDA: <span style="color:#FFD700;">{fd['nama'].split('(')[0].strip()}</span></b><br>
{fd['analisa']}<br><br>
<i style="color:#888;">Sinkronisasi Kosmik:</i> {koneksi} ({planet_desc})
</p>
<div style="background: rgba(37,211,102,0.1); border: 1px solid rgba(37,211,102,0.4); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
<b style="color: #25D366; font-size:15px;">🎯 PROTOKOL EKSEKUSI (LAKUKAN SEKARANG):</b>
<ul style="color: #e0e0e0; font-size: 15px; margin-top: 10px; margin-bottom: 0; padding-left: 20px; line-height:1.5;">
{do_html}
</ul>
</div>
<div style="background: rgba(255,75,75,0.1); border: 1px solid rgba(255,75,75,0.4); padding: 15px; border-radius: 8px;">
<b style="color: #ff4b4b; font-size:15px;">🛑 RED ZONE (HINDARI MUTLAK):</b><br>
<span style="color: #ccc; font-size: 14px; display:inline-block; margin-top:5px; line-height:1.5;">{fd['dont']}</span>
</div>
<p style="font-size:12px; color:#ff4b4b; margin-top:10px; font-weight:bold;">⏳ Sistem mendeteksi perubahan energi dalam beberapa jam ke depan. Jangan tunda eksekusi!</p>
</div>"""
    return fd['nama'], html_output

# --- ENGINE FALAK RUHANI (SPIRITUAL ANCHORING) ---
def proc_falak_ruhani(total_jummal, root_num, nama):
    ruhani_data = {
        1: {"asma": "Ya Fattah (Maha Pembuka)", "vibrasi": "Mendobrak Jalan Buntu & Ego", "tujuan": "Membersihkan hambatan ego masa lalu, menaklukkan sifat keras kepala, dan mendobrak pintu rezeki yang selama ini terkunci akibat kesombongan bawah sadar."},
        2: {"asma": "Ya Salam (Maha Sejahtera)", "vibrasi": "Harmoni & Perisai Mental", "tujuan": "Menetralisir frekuensi beracun (toxic) dari lingkungan sekitar dan menyembuhkan kelelahan sistem saraf (anxiety) akibat terlalu banyak memendam perasaan."},
        3: {"asma": "Ya Mushawwir (Maha Pembentuk)", "vibrasi": "Manifestasi Ide ke Realita", "tujuan": "Menarik pikiran yang berserakan (overthinking) kembali ke pusat bumi, mengubah wacana atau ide liar menjadi sebuah karya fisik yang terstruktur."},
        4: {"asma": "Ya Muqit (Maha Pemberi Kecukupan)", "vibrasi": "Stabilitas & Nutrisi Batin", "tujuan": "Menghancurkan 'Mental Miskin' (Scarcity Mindset) hingga ke akarnya, memberikan rasa aman absolut pada kondisi finansial, dan menarik kestabilan material."},
        5: {"asma": "Ya Basith (Maha Melapangkan)", "vibrasi": "Ekspansi & Pembebasan Diri", "tujuan": "Melepaskan perasaan terkekang, menghilangkan rasa bosan kronis, dan memperluas kapasitas wadah rezeki mental Anda agar siap memanen kesuksesan besar."},
        6: {"asma": "Ya Wadud (Maha Mengasihi)", "vibrasi": "Cinta Universal & Daya Tarik", "tujuan": "Menyembuhkan trauma luka batin masa lalu, menumbuhkan Self-Love tingkat tinggi, and secara otomatis memancarkan aura pengasihan (Rapport) alami tanpa pelet."},
        7: {"asma": "Ya Batin (Maha Tersembunyi)", "vibrasi": "Intuisi & Hikmah Langit", "tujuan": "Mempertajam indra keenam, melatih kepekaan membaca bahasa tubuh dan niat tersembunyi orang lain, serta menjernihkan intuisi bisnis Anda."},
        8: {"asma": "Ya Ghaniy (Maha Kaya)", "vibrasi": "Otoritas & Kelimpahan Absolut", "tujuan": "Menyelaraskan frekuensi diri Anda menjadi magnet kekayaan material murni, serta memberikan kekuatan untuk memegang kendali tanpa terjatuh pada keserakahan."},
        9: {"asma": "Ya Hakim (Maha Bijaksana)", "vibrasi": "Pencerahan & Kesadaran", "tujuan": "Pelepasan beban karma (rasa bersalah masa lalu), menurunkan ekspektasi ego pada duniawi, dan menyelaraskan setiap tindakan fisik Anda dengan Misi Semesta (Life Purpose)."}
    }
    data = ruhani_data.get(root_num, ruhani_data[1])
    dzikir_count = total_jummal
    return data["asma"], data["vibrasi"], data["tujuan"], dzikir_count

# --- PROTOKOL TERAPI DINAMIS ---
def get_protokol_terapi(root_num, nama):
    random.seed(generate_seed(f"pt_{nama}_{root_num}"))
    b1 = random.choice([f"**Ego Supremacy & Lone Wolf Syndrome.** Anda ({nama}) memiliki program bawah sadar yang menolak bantuan karena merasa 'harus bisa sendiri'. Ujungnya? Kelelahan ekstrem (*Burnout*) dan rasa sepi di tengah keramaian karena menanggung semua beban di pundak sendiri.", f"**Ilusi Kontrol Sempurna.** Secara tidak sadar, gengsi {nama} terlalu tinggi untuk meminta tolong. Bahayanya, hal ini menciptakan pola hidup di mana Anda memforsir mesin saraf Anda melebihi kapasitas, mensabotase rezeki yang seharusnya bisa datang dari kolaborasi tim."])
    a1 = random.choice([f"Saya, {nama}, dengan penuh kesadaran menurunkan perisai ego saya malam ini. Saya paham bahwa meminta tolong adalah delegasi kecerdasan, bukan kelemahan. Saya mengizinkan energi Semesta bekerja melalui tangan orang lain.", f"Mulai tarikan napas ini, saya ({nama}) menyadari bahwa kolaborasi adalah kunci kelimpahan sejati. Saya pantas dibantu, tubuh saya pantas untuk beristirahat, dan saya membuka pintu bagi kemudahan."])
    h1 = random.choice(["Cari 1 tugas spesifik hari ini yang sebenarnya BISA Anda kerjakan sendiri, namun **mintalah tolong** orang lain untuk mengerjakannya. Latih otot 'penerimaan' Anda.", "Hubungi satu teman kompeten atau mentor Anda hari ini. Ceritakan satu kendala teknis atau mental yang sedang Anda hadapi. Dengarkan saran mereka sepenuhnya tanpa memotong."])

    b2 = random.choice([f"**People Pleaser Chronic.** {nama} secara rutin memenjarakan suara hati sendiri demi menjaga perasaan orang lain. Anda bertindak layaknya 'Spons Emosi' yang menyerap keluh kesah dan energi negatif (*toxic*) sirkel Anda.", f"**Luka Takut Ditinggalkan (Abandonment).** Anda terlalu mudah merasa *nggak enakan*. Hidup {nama} sering tersabotase karena mendahulukan kebutuhan orang yang bahkan tidak memprioritaskan Anda."])
    a2 = random.choice([f"Saya, {nama}, memegang kendali absolut atas energi dan kewarasan saya. Kebahagiaan saya adalah priority kosmik nomor satu. Mulai saat ini, batas diri (*boundaries*) saya adalah suci.", f"Saya ({nama}) melepaskan rasa bersalah palsu ini. Saya menolak bertanggung jawab atas kekecewaan atau ekspektasi orang lain. Merawat diri saya sendiri adalah priority."])
    h2 = random.choice(["Berlatih keberanian mikro: Katakan 'TIDAK' atau 'Maaf, saya tidak bisa' pada satu permintaan/ajakan hari ini. Ucapkan dengan tegas dan rileks.", "Lakukan *Digital Detoxing* parsial. Matikan notifikasi chat dari grup WhatsApp atau individu yang paling sering 'menyedot' energi Anda selama minimal 12 jam."])

    b3 = random.choice([f"**Scattered Focus (Lompatan Kera).** Otak {nama} adalah pabrik yang memproduksi ratusan ide brilian per detik, namun memiliki eksekusi nyaris nol. Energi Anda habis menguap hanya di fase *overthinking*.", f"**Impulsivitas Ide & Mudah Bosan.** Anda ({nama}) kecanduan dopamin dari sebuah 'awal yang baru'. Baru saja memulai satu hal, sistem saraf Anda sudah melompat mencari rangsangan ide lain."])
    a3 = random.choice([f"Saya, {nama}, memerintahkan pikiran saya untuk melambat dan membumi. Saya menyalurkan kreativitas liar ini ke dalam struktur yang nyata. Satu eksekusi kecil yang selesai jauh lebih berharga daripada seribu wacana.", f"Pikiran saya jernih, tajam bak sinar laser. Saya ({nama}) mengizinkan diri saya untuk duduk tenang, menghadapi rasa tidak nyaman, dan menyelesaikan apa yang sudah saya mulai."])
    h3 = random.choice(["Gunakan teknik *Timeboxing*. Pilih 1 ide/tugas spesifik saja. Tulis di kertas, pasang timer 20 menit, lalu kerjakan langkah pertamanya tanpa henti.", "Terapi Keteraturan Fisik: Rapikan meja kerja, hapus file sampah di laptop, atau bersihkan kamar Anda secara total hari ini."])

    b4 = random.choice([f"**Scarcity Mindset (Mental Miskin).** Terdapat ketakutan bawah sadar yang parah akan kegagalan dan kebangkrutan. Hal ini membuat pola pikir {nama} menjadi sangat kaku, terlalu berhati-hati, dan pelit—bahkan pada diri sendiri.", f"**Sabotase Zona Nyaman.** Anda ({nama}) sering merasionalisasi ketakutan dengan dalih 'harus nabung untuk jaga-jaga hal buruk'. Tanpa sadar, frekuensi ini justru bertindak seperti magnet yang menarik nasib buruk."])
    a4 = random.choice([f"Saya, {nama}, dengan napas ini melepaskan rasa takut akan kekurangan. Saya menyadari bahwa sumber daya Semesta tidak terbatas dan berlimpah ruah. Kondisi finansial saya aman.", f"Saya ({nama}) layak dan pantas hidup dalam kelimpahan tanpa batas. Uang adalah energi cahaya yang baik, dan saya mengizinkannya datang mengetuk pintu saya."])
    h4 = random.choice(["Latih saraf melepaskan (Letting Go): Beri hadiah fisik (reward) untuk diri sendiri hari ini. Saat membayar, tersenyumlah dan rasakan emosi kelimpahannya.", "Lakukan sedekah subuh atau transfer amal tak terduga hari ini, berapapun nominalnya. Niatkan tindakan ini untuk memutus urat ketakutan batin."])

    b5 = random.choice([f"**Escapism (Sindrom Pelarian).** {nama} memiliki kecenderungan melarikan diri (*escape*) saat dihadapkan pada tanggung jawab atau komitmen jangka panjang. Anda berlindung di balik kata 'mencari kebebasan'.", f"**Korsleting Rutinitas (Mudah Jenuh).** Saat menghadapi tekanan pekerjaan yang menuntut konsistensi tinggi, sistem saraf {nama} mendadak mati rasa. Anda tiba-tiba merasa hampa, stres tak beralasan."])
    a5 = random.choice([f"Saya, {nama}, menemukan kedalaman makna yang sejati justru di dalam komitmen yang stabil. Menetap dan konsisten bukanlah penjara bagi saya, melainkan pondasi baja untuk sukses.", f"Saya ({nama}) mengontrol penuh rasa bosan di dalam diri saya. Saya berdamai dengan proses repetitif. Saya menanam akar keringat yang kuat hari ini."])
    h5 = random.choice(["Pilih SATU pekerjaan yang paling membosankan dan sudah Anda tunda berminggu-minggu. Paksa sistem saraf Anda untuk duduk dan menyelesaikannya hingga tuntas 100% hari ini.", "Terapi Konsistensi Dasar: Rancang rutinitas pagi sederhana. Lakukan hal yang SAMA PERSIS selama 3 hari berturut-turut tanpa mengubah polanya sedikitpun."])

    b6 = random.choice([f"**Savior Complex (Penyelamat Berlebihan).** {nama} secara tidak sadar sering merasa bersalah jika menikmati hidup yang enak, sementara ada orang di sekitarnya yang masih susah. Anda menguras energi vital untuk menyelesaikan masalah orang lain.", f"**Luka Pengorbanan Tanpa Pamrih Palsu.** Anda ({nama}) memberikan 100% kapasitas emosi dan materi untuk orang-orang terdekat, namun jauh di lubuk hati terdalam diam-diam merasa kosong."])
    a6 = random.choice([f"Saya, {nama}, dengan sadar mengizinkan diri saya untuk bahagia dan berkelimpahan. Saya paham bahwa merawat dan mencintai diri sendiri secara maksimal adalah syarat mutlak.", f"Tangki cinta dan rezeki saya berlimpah, dan penerima pertama dari kelimpahan itu adalah saya sendiri. Saya ({nama}) berhak menikmati keringat saya."])
    h6 = random.choice(["Lakukan 'Isolasi Positif'. Ambil waktu minimal 45 menit hari ini murni untuk 'Me-Time'. Matikan koneksi, lakukan hobi Anda tanpa memikirkan orang lain.", "Beli makanan kesukaan yang cukup mewah hari ini. Makanlah pelan-pelan sendirian, nikmati setiap gigitannya, dan JANGAN membaginya."])

    b7 = random.choice([f"**Paralysis by Analysis (Kelumpuhan Logika).** Otak analitik {nama} terlalu tajam, namun berbalik menyerang diri sendiri. Anda menghabiskan energi menganalisa niat orang lain secara berlebihan (*over-analyzing*).", f"**Trust Issue Kronis.** Pengalaman masa lalu menciptakan sifat skeptis ekstrim di bawah sadar {nama}. Anda seringkali menolak peluang bisnis yang bagus atau cinta yang tulus karena selalu curiga."])
    a7 = random.choice([f"Saya, {nama}, menyeimbangkan ketajaman logika saya dengan kepasrahan intuisi. Saya mempercayai proses Semesta, dan saya mengizinkan hal-hal menakjubkan terjadi di hidup saya.", f"Saya ({nama}) secara sadar melepaskan kebutuhan egoistik untuk mengetahui rahasia dari segalanya. Saya memaafkan masa lalu, mempercayai perlindungan Tuhan."])
    h7 = random.choice(["Lakukan 'Silence Meditation' (meditasi hening tanpa instruksi). Duduk diam total tanpa interupsi selama 15 menit. Amati saja keluar masuknya napas.", "Latih otot kepercayaan: Percayai secara utuh satu ucapan atau tindakan niat baik dari orang di sekitar Anda hari ini, TANPA Anda *cross-check*."])

    b8 = random.choice([f"**Control Freak & Diktator Bawah Sadar.** {nama} memforsir tubuh, pikiran, dan orang lain di sekitarnya tanpa ampun demi mengejar standar kesuksesan material yang tidak ada garis finishnya.", f"**Obsesi Material Penjerat Batin.** Ambisi dan insting bisnis {nama} memang menyala terang, tapi hal ini seringkali menghancurkan kedamaian batin Anda sendiri."])
    a8 = random.choice([f"Saya, {nama}, adalah saluran tempat kelimpahan mengalir secara damai, bukan budak dari ambisi buta. Kekuatan sejati saya justru bersinar paling terang saat saya berserah.", f"Saya ({nama}) dengan ikhlas melepaskan ilusi kendali yang menyiksa saraf saya. Saya sukses, saya berkelimpahan, saya berwibawa, dan hati saya damai."])
    h8 = random.choice(["Praktik Delegasi Radikal. Serahkan satu keputusan kendali hari ini kepada orang lain (misal: biarkan bawahan/pasangan mengambil keputusan). Ikuti saja alurnya.", "Terapkan 'Hard Stop'. Berhenti bekerja dan matikan koneksi laptop/bisnis tepat pukul 17:00 hari ini. Dilarang keras menyentuh urusan pekerjaan sampai besok."])

    b9 = random.choice([f"**Toxic Empathy (Empati Penghancur).** {nama} memiliki resonansi spiritual yang terlalu peka. Anda terlalu gampang merasa kasihan, bahkan pada orang yang manipulatif dan *toxic*.", f"**Luka Ekspektasi Luluh (Patah Hati Universal).** Karena Anda memegang standar moral dan filosofi yang sangat tinggi, {nama} seringkali jatuh pada kekecewaan yang sangat parah."])
    a9 = random.choice([f"Saya, {nama}, dengan napas ini melepaskan segala hal yang berada di luar kendali otoritas saya. Saya membiarkan setiap jiwa manusia memikul karmanya sendiri.", f"Tugas suci saya ({nama}) di bumi ini BUKANLAH untuk menyelamatkan semua orang. Energi batin saya adalah pusaka yang suci."])
    h9 = random.choice(["Lakukan Detoksifikasi Frekuensi Negatif. Blokir semua asupan berita politik, gosip, tragedi, atau *scrolling* curhatan orang di sosial media selama 24 jam penuh.", "Terapi Menahan Diri: Sepanjang hari ini, berhentilah memberikan nasihat, wejangan, atau solusi kepada siapapun KECUALI jika mereka meminta."])

    protokol = {1: {"block": b1, "afirmasi": a1, "habit": h1}, 2: {"block": b2, "afirmasi": a2, "habit": h2}, 3: {"block": b3, "afirmasi": a3, "habit": h3}, 4: {"block": b4, "afirmasi": a4, "habit": h4}, 5: {"block": b5, "afirmasi": a5, "habit": h5}, 6: {"block": b6, "afirmasi": a6, "habit": h6}, 7: {"block": b7, "afirmasi": a7, "habit": h7}, 8: {"block": b8, "afirmasi": a8, "habit": h8}, 9: {"block": b9, "afirmasi": a9, "habit": h9}}
    return protokol.get(root_num, protokol[1])

# --- DATABASE BLUEPRINT (DEEP NLP PROFILING) ---
arketipe_punchy = {
    1: {"inti": "Sang Perintis (Dominator & Visioner Masa Depan)", "kekuatan": ["Daya dobrak insting tinggi & keberanian mengambil risiko ekstrim", "Kemandirian absolut (Self-Sufficient)", "Fokus eksekusi tanpa banyak wacana"]},
    2: {"inti": "Sang Penyelaras (Negosiator & Pembaca Emosi)", "kekuatan": ["Kapasitas empati dan diplomasi tingkat dewa", "Negosiator ulung yang mampu membaca ruang", "Kemampuan adaptasi emosional dalam krisis"]},
    3: {"inti": "Sang Visioner (Kreator Ide & Komunikator Handal)", "kekuatan": ["Daya tarik komunikasi yang memikat (Magnetic Charisma)", "Kreativitas lateral tanpa batas", "Ahli mencairkan suasana dan persuasi masal"]},
    4: {"inti": "Sang Transformator (Ahli Strategi & Pembangun Sistem)", "kekuatan": ["Pola pikir sangat presisi dan terstruktur", "Loyalitas dan keandalan sistematis 100%", "Ketelitian audit tingkat tinggi"]},
    5: {"inti": "Sang Penggerak (Eksplorator & Pemecah Kebuntuan)", "kekuatan": ["Kelincahan berpikir (Agility) di situasi *chaos*", "Inovator pemecah kebuntuan *out-of-the-box*", "Keberanian mengeksplorasi wilayah yang belum dipetakan"]},
    6: {"inti": "Sang Harmonizer (Pengayom & Pelindung Natural)", "kekuatan": ["Insting pengayom dan penyembuh (Healer) yang sangat kuat", "Tanggung jawab moral dan integritas tinggi", "Loyalitas tanpa pamrih pada sirkel terdekat"]},
    7: {"inti": "Sang Legacy Builder (Pemikir Analitik & Spiritualis)", "kekuatan": ["Kemampuan analisa forensik menembus kebohongan", "Intuisi batin (Indra ke-6) yang seringkali akurat", "Sangat selektif dan memegang standar kualitas tinggi"]},
    8: {"inti": "Sang Sovereign (Eksekutor Otoritas & Magnet Material)", "kekuatan": ["Tahan banting mental luar biasa terhadap tekanan", "Insting bisnis dan radar kekayaan yang sangat presisi", "Kemampuan mutlak untuk memegang dan merebut kendali"]},
    9: {"inti": "Sang Kesadaran Tinggi (Old Soul & Empati Universal)", "kekuatan": ["Kebijaksanaan pandangan (Eagle-Eye Perspective) yang luas", "Kepedulian universal yang melampaui ego pribadi", "Kemampuan memahami inti penderitaan orang lain"]}
}

def proc_arketipe(nama, angka, zodiak, neptu):
    random.seed(generate_seed(f"hyper_ark_{nama}_{angka}_{zodiak}_{neptu}"))
    buka = random.choice([
        f"Melalui persilangan matriks waktu lahir dan algoritma elemen {zodiak}, DNA numerologi dan psikologis **{nama}** mengunci kuat pada **KODE {angka}**.",
        f"Kalkulasi semesta dan kalibrasi weton menyempit presisi di **KODE {angka}**. Ini menandakan bahwa sejak tarikan napas pertama, alam bawah sadar **{nama}**",
    ])
    inti = {
        1: "sebagai arsitek pendobrak batas (Sang Perintis). Anda didesain dengan mesin mental beroktan tinggi yang menuntut kemandirian absolut dan secara alami menolak didikte atau dikontrol oleh sistem yang kaku.",
        2: "sebagai Sang Penyelaras sejati. Anda dibekali dengan radar empati tingkat dewa yang beresonansi kuat dalam mendeteksi dan memanipulasi energi ruang, menjadikan Anda seorang negosiator yang intuitif dan pembaca bahasa tubuh alami.",
        3: "sebagai komunikator magnetis. Anda memiliki mesin pikiran yang meletup-letup dengan ide visioner. Kekuatan utama Anda terletak pada lidah dan ekspresi; kata-kata Anda memiliki daya tembus hipnotik ke alam bawah sadar pendengar.",
        4: "sebagai arsitek sistem yang kokoh. Pola pikir Anda beroperasi bagaikan kode mesin yang presisi. Anda didesain untuk menjadi pondasi bagi entitas yang lebih besar, membangun kerangka dari *chaos* menjadi sebuah tatanan logis yang stabil.",
        5: "sebagai jiwa bebas yang menolak keras rutinitas monoton. Anda adalah simbol eksplorasi; otak Anda paling bersinar terang dan lincah justru ketika diletakkan di tengah situasi krisis atau saat dihadapkan pada kebosanan yang memuncak.",
        6: "sebagai pilar pengayom dan pelindung (Sang Healer). Anda memegang standar tanggung jawab moral yang sangat tinggi di pundak Anda, dengan insting alami yang secara otomatis bergerak melindungi dan menyembuhkan orang-orang di lingkar dalam Anda.",
        7: "sebagai pencari kebenaran esensial dengan mata batin yang setajam silet. Anda adalah jiwa analitik yang tidak akan pernah sudi ditipu oleh jawaban dangkal. Filter logika Anda bekerja berlapis-lapis untuk membongkar misteri dan niat tersembunyi.",
        8: "sebagai eksekutor otoritas (Sang Sovereign) dengan daya tarik gravitasi material yang mutlak. Anda memiliki fokus bawah sadar yang ditarik secara agresif menuju puncak hierarki. Wibawa bawaan Anda seringkali membuat orang lain segan atau tunduk bahkan sebelum Anda mengucapkan sepatah kata pun.",
        9: "sebagai 'Jiwa Tua' (Old Soul) yang memandang kerasnya dunia lewat kacamata kebijaksanaan tingkat tinggi. Anda didesain untuk memahami lanskap kehidupan secara utuh (Big Picture) dengan tingkat kepedulian universal yang melampaui urusan materi fana."
    }
    shadow = {
        1: "Di balik kehebatan eksekusi itu, musuh terbesar Anda adalah rasa sepi akibat tembok gengsi yang Anda bangun sendiri. Kesulitan mendelegasikan tugas rawan memicu *burnout*.",
        2: "Bahaya tersembunyinya adalah kecenderungan menjadi 'Spons Emosi'. Anda terlalu sering memenjarakan suara hati sendiri (People Pleasing) demi menjaga perasaan orang lain, yang akhirnya menjadi bom waktu.",
        3: "Sisi gelap arsitektur ini adalah 'Lompatan Kera' (Scattered Focus). Ide Anda ratusan, eksekusi nol. Selain itu, Anda rawan mengeluarkan kata-kata tajam yang impulsif saat ego sedang terluka.",
        4: "Kelemahan fatal Anda adalah *Micromanaging*. Ketakutan akan hilangnya struktur sering membuat Anda dinilai terlalu kaku, dingin, dan tidak memiliki toleransi pada ritme spontanitas manusiawi.",
        5: "Waspadai 'Sindrom Cepat Bosan' yang mensabotase hasil jerih payah Anda sendiri. Anda rawan melarikan diri secara impulsif (*escapism*) sesaat sebelum mencapai puncak kesuksesan yang butuh komitmen panjang.",
        6: "Ada kecenderungan *Toxic Empathy* dan *Savior Complex*. Anda menguras habis energi vital untuk menyelamatkan hidup orang lain, sementara Anda sendiri diam-diam merasa kosong dan tidak dipedulikan.",
        7: "Jebakan terbesar Anda adalah *Paralysis by Analysis*—berhenti bertindak karena terlalu banyak berpikir. Kekecewaan pada realitas sering membuat Anda menarik diri ke dalam goa isolasi sosial yang dingin.",
        8: "Ketakutan terdalam Anda adalah terlihat rapuh atau lemah. Sifat 'Control Freak' ini membuat Anda sangat kesulitan untuk berserah, melepaskan kendali, dan memaafkan kesalahan masa lalu tanpa dendam.",
        9: "Aura empati Anda rawan disalahgunakan oleh para manipulator. Kekecewaan kronis sering melanda karena Anda memaksakan ekspektasi keluhuran moral yang terlalu tinggi kepada manusia pada umumnya."
    }
    saran = {
        1: "Pesan Semesta: Belajarlah menurunkan perisai Anda. Meminta bantuan bawahan/rekan bukanlah tanda kelemahan, melainkan taktik pendelegasian otoritas tingkat dewa.",
        2: "Pesan Semesta: Berhentilah mensabotase kedamaian Anda demi orang lain. Berlatihlah mengucapkan kata 'TIDAK' dengan lantang tanpa secercah rasa bersalah.",
        3: "Pesan Semesta: Ikat ide liar Anda ke bumi. Paksa sistem saraf Anda untuk menyelesaikan SATU proyek kecil sampai tuntas 100% sebelum melompat memburu sensasi ide yang baru.",
        4: "Pesan Semesta: Kendurkan genggaman Anda pada kontrol obsesif. Berikan ruang untuk spontanitas; terkadang sedikit ketidakberaturan adalah terapi mental terbaik bagi Anda.",
        5: "Pesan Semesta: Temukan ruang kebebasan dan seni di dalam rutinitas jangka panjang. Kedewasaan terbesar Anda diuji saat Anda mampu menetap ketika insting menyuruh Anda lari.",
        6: "Pesan Semesta: Tangki energi Anda harus penuh sebelum menyiram orang lain. Buat batasan yang agresif. Anda tidak lahir ke dunia ini semata-mata untuk menggendong beban sirkel Anda.",
        7: "Pesan Semesta: Turunkan ekspektasi Anda terhadap kesempurnaan manusiawi. Kadang, jawaban yang paling benar tidak ditemukan di ujung analisa pikiran, melainkan pada keberanian mengambil langkah pertama.",
        8: "Pesan Semesta: Latih otot kepasrahan (*Letting Go*) Anda di momen istirahat. Kekuatan sejati justru bersinar paling terang saat Anda mampu berserah. Kesuksesan jangka panjang menuntut sistem saraf yang sehat dan damai.",
        9: "Pesan Semesta: Tugas suci Anda bukanlah untuk menyelamatkan galaksi. Selamatkanlah dan cintai diri Anda sendiri terlebih dahulu sebelum Anda kehabisan energi menghadapi kerasnya realitas."
    }
    return f"{buka} {inti[angka]} {shadow[angka]} <br><br><b style='color:#FFD700;'>Pesan Kosmik:</b> <i style='color:#ccc;'>{saran[angka]}</i>"

def proc_shadow_list(nama, angka):
    random.seed(generate_seed(f"shd_{nama}_{angka}"))
    semua_shadow = {
        1: ["**Ego Supremacy & Gengsi Absolut:** Anda membangun tembok kemandirian yang sangat tebal. Saat memikul beban berat atau stres ekstrem, Anda lebih memilih hancur sendirian daripada terlihat lemah dan harus meminta bantuan.", "**Ilusi Kesempurnaan (Overthinking Eksekusi):** Sering mensabotase karya atau langkah maju Anda sendiri dengan terus mencari detail yang kurang, mengorbankan momentum berharga demi kesempurnaan palsu.", "**Mengabaikan Alarm Fisik:** Ambisi buta yang membuat Anda sering mematikan sinyal kelelahan dari sistem saraf, mendorong tubuh melampaui batas kewajarannya hingga berujung pada *burnout* diam-diam."],
        2: ["**Sindrom Penyenang (People Pleaser Chronic):** Anda secara rutin mengorbankan batas diri dan kebahagiaan pribadi hanya untuk memenuhi ekspektasi atau menghindari konflik dengan orang di sekitar Anda.", "**Spons Energi Beracun:** Radar empati yang bocor membuat Anda tanpa sadar menyerap amarah, keluh-kesah, dan energi negatif (toxic) dari orang lain, yang akhirnya merusak *mood* harian Anda sendiri.", "**Bom Waktu Amarah Terselubung:** Terlalu banyak menekan perasaan kecewa demi menjaga 'keharmonisan palsu' yang sewaktu-waktu bisa meledak hebat pada hal sepele."],
        3: ["**Topeng Keceriaan (Hidden Anxiety):** Menyembunyikan rasa gelisah, *insecurity*, atau kebingungan yang parah di balik persona yang selalu tampil ceria, asyik, dan pandai bicara di depan publik.", "**Scattered Focus (Fokus Berserakan):** Mesin ide yang terlalu panas membuat Anda cepat kehilangan motivasi. Baru memulai satu hal, otak sudah melompat mencari rangsangan (dopamin) dari proyek baru.", "**Lidah Impulsif:** Saat ego merasa diserang atau dikhianati, Anda cenderung kehilangan filter dan menembakkan kata-kata sarkastik yang dampaknya sangat merusak secara emosional."],
        4: ["**Kelumpuhan Zona Nyaman:** Terdapat ketakutan bawah sadar untuk mengambil risiko besar, membuat Anda sering terjebak dalam rutinitas monoton dan menyabotase peluang emas yang sedikit tidak pasti.", "**Diktator Mikro (Over-Micromanaging):** Rasa cemas jika hal tidak berjalan sesuai sistem membuat Anda sering mencampuri dan mengkritik terlalu detail cara kerja orang lain, menciptakan suasana tegang.", "**Pembekuan Emosional:** Saat menghadapi krisis mendadak, Anda sering mengunci emosi dan terlihat sangat kaku atau tidak berperasaan oleh orang terdekat demi mempertahankan logika operasional."],
        5: ["**Sindrom Melarikan Diri (Escapism):** Ketakutan bawah sadar akan rasa terikat membuat Anda sering melarikan diri—baik secara mental maupun fisik—saat dihadapkan pada komitmen asmara atau bisnis jangka panjang.", "**Kelelahan Saraf Akibat Rangsangan:** Otak yang terus menerus memburu variasi dan kebebasan membuat Anda rentan mengalami kelelahan mental yang berujung pada rasa hampa dan kehilangan pijakan.", "**Sabotase Rutinitas Berharga:** Anda sering mengakhiri hal yang sudah bagus atau stabil hanya karena rasa bosan impulsif yang mendadak muncul tanpa alasan logis yang kuat."],
        6: ["**Savior Complex (Sindrom Penyelamat Beban):** Anda merasa bertanggung jawab atas kemalangan orang lain dan sering menguras habis energi material maupun spiritual Anda untuk menyelamatkan nyawa orang-orang *toxic*.", "**Penjara Rasa Bersalah:** Anda dihantui rasa bersalah yang tidak rasional jika mengambil waktu untuk menikmati hasil keringat sendiri (Me-Time) sementara ada keluarga/teman yang masih kesusahan.", "**Ekspektasi Balasan Emosional (Pamrih Batin):** Sekuat apapun Anda bilang ikhlas, jauh di lubuk hati terdapat kekecewaan parah jika pengorbanan besar Anda diabaikan atau tidak mendapat pengakuan yang setimpal."],
        7: ["**Paralysis by Analysis (Lumpuh Logika):** Ketajaman analitik Anda berbalik menjadi bumerang. Anda membedah setiap risiko secara *overthinking* hingga akhirnya kehilangan momentum dan tidak mengeksekusi apapun.", "**Skeptisisme & Trust Issue Kronis:** Luka masa lalu menciptakan filter paranoid di otak Anda, membuat Anda sering mencurigai niat baik orang lain dan menyabotase hubungan atau kerja sama potensial.", "**Arogansi Intelektual Bawah Sadar:** Karena standar kualitas yang tinggi, Anda rawan merasa terasing dan secara tidak sadar memancarkan aura sinis atau sarkastik pada lingkungan yang Anda anggap 'dangkal'."],
        8: ["**Insecurity Otoritas (Ketakutan Menjadi Lemah):** Di bawah wibawa yang kokoh, terdapat ego rapuh yang menolak keras terlihat rentan di depan siapa pun, menekan Anda untuk terus menggunakan topeng 'Si Paling Kuat'.", "**Cengkeraman Kontrol (Diktator Psikologis):** Anda sangat kesulitan melepaskan kendali dan mempercayakan hasil akhir pada orang lain, bahkan cenderung memaksakan dominasi Anda pada ranah privasi pasangan.", "**Kalkulasi Nilai Kemanusiaan:** Saat ambisi material sedang menguasai, radar empati Anda mati. Anda rawan menilai orang-orang di sekitar murni berdasarkan metrik fungsi, aset, atau keuntungan status sosio-ekonominya saja."],
        9: ["**Empati Penghancur (Toxic Empathy):** Kesadaran universal Anda membuat Anda terlalu mudah memaklumi, memaafkan, dan memberi kesempatan berkali-kali pada manipulator yang terus merugikan hidup Anda.", "**Patah Hati Paradigma (Ekspektasi Semu):** Anda memegang filosofi dan standar kemanusiaan yang sangat luhur, yang ujungnya membuat Anda kelelahan dan depresi melihat kerasnya realitas sifat asli manusia.", "**Kehilangan Jangkar Jati Diri:** Saking sibuknya memikirkan masa depan atau visi besar kehidupan sirkel Anda, Anda rawan terombang-ambing, kehilangan sentuhan pada keinginan dan kebahagiaan Anda sendiri di masa kini."]
    }
    return random.sample(semua_shadow[angka], 3)

def get_betaljemur_data(neptu, hari):
    lk = {
        7: ("Lebu Katiup Angin", "Pikiran Anda sangat dinamis dan mudah terombang-ambing. Rawan godaan impulsif yang membuat fokus terpecah. Anda membutuhkan anchor (jangkar) rutinitas yang ketat untuk menahan energi yang berhamburan hari ini."),
        8: ("Lakuning Geni", "Elemen api mendominasi. Emosi Anda bagaikan bensin yang mudah tersulut percikan kecil. Ini adalah hari di mana ambisi menyala terang, namun Anda wajib memegang kendali agar lidah Anda tidak membakar relasi yang sudah dibangun susah payah."),
        9: ("Lakuning Angin", "Kapasitas adaptasi Anda sedang berada di puncaknya, namun di sisi lain karakter Anda menjadi sulit ditebak dan cenderung labil. Sangat bagus untuk negosiasi kilat, sangat buruk untuk komitmen jangka panjang."),
        10: ("Pandito Mbangun Teki", "Energi sang pertapa menyelimuti Anda. Waktu yang luar biasa tajam untuk introspeksi mendalam, menyusun strategi sunyi, dan menajamkan intuisi. Kecerdasan analitik Anda mampu membedah masalah yang paling rumit sekalipun."),
        11: ("Aras Tuding", "Aura keberanian dan kepeloporan sedang aktif. Anda akan sering 'ditunjuk' oleh semesta—baik itu ditunjuk untuk memimpin krisis, atau ditunjuk oleh peluang rezeki emas. Jangan menunduk, ambil panggung Anda hari ini."),
        12: ("Aras Kembang", "Pesona dan kharisma alami (Magnetic Aura) Anda sedang memancar maksimal. Gelombang vibrasi ini membuat perkataan Anda lebih mudah dituruti dan kehadiran Anda didambakan. Waktu terbaik untuk melobi klien kelas kakap atau penyelesaian konflik."),
        13: ("Lakuning Lintang", "Magnetis namun menyendiri. Anda memancarkan pesona misterius yang sering menjadi pusat perhatian tanpa Anda sadari. Namun jauh di lubuk hati, Anda menyimpan dunia eksklusif. Fase ini meminta Anda untuk tidak terlalu lama mengisolasi diri saat ada peluang kolaborasi di depan mata."),
        14: ("Lakuning Rembulan", "Anda bertindak bagaikan penenang batin di tengah kekacauan. Kehadiran Anda memberikan rasa aman bagi sirkel Anda. Intuisi Anda jernih dan tajam, sangat cocok untuk mengambil keputusan yang berlandaskan empati dan harmoni."),
        15: ("Lakuning Srengenge", "Aura Anda sepanas dan seterang matahari siang. Sangat logis, pencerah, dan dominan. Kepemimpinan Anda tidak bisa dibantah hari ini. Gunakan energi raksasa ini untuk mengeksekusi *project* mandek atau menegakkan aturan dengan tegas."),
        16: ("Lakuning Banyu", "Ketenangan air yang menyimpan arus bawah mematikan. Anda terlihat sangat sabar dan fleksibel di permukaan, namun menyimpan kekuatan presisi yang luar biasa. Sangat pas untuk mengamati diam-diam lalu melakukan serangan negosiasi di saat krusial."),
        17: ("Lakuning Bumi", "Sangat membumi, sabar, dan terstruktur. Hari ini pikiran Anda tidak mentolerir angan-angan kosong. Fokus pada pondasi: audit pembukuan, merapikan aset, dan memastikan semua operasional dasar bisnis/hidup Anda tidak memiliki kebocoran."),
        18: ("Lakuning Paripurna", "Fase puncak pemegang kendali yang bijaksana. Ego telah luruh menjadi kewibawaan murni. Perkataan Anda mengandung tuah (sabda), sehingga Anda dilarang keras mengeluh atau menyumpahi hal buruk, karena potensi manifestasinya sangat cepat terjadi.")
    }
    nd = {"Minggu":"Timur", "Senin":"Selatan", "Selasa":"Barat", "Rabu":"Utara", "Kamis":"Timur", "Jumat":"Selatan", "Sabtu":"Selatan"}
    return lk.get(neptu,("Anomali","Energi tak terpetakan. Dengarkan insting dasar Anda."))[0], lk.get(neptu,("Anomali",""))[1], nd.get(hari,"Netral")

def get_rezeki_usaha(neptu):
    r = {
        1: ("Wasesa Segara (Lautan Rezeki)", "Pintu kelimpahan Anda sedang dalam fase ekspansi maksimal, seluas samudra. Aliran finansial berpotensi datang dari arah yang tidak terduga jika Anda berani melepaskan keraguan dan mengeksekusi niat besar hari ini."),
        2: ("Tunggak Semi (Tumbuh Abadi)", "Memiliki vibrasi 'Patah tumbuh hilang berganti'. Jika hari ini Anda mengalami kerugian atau penolakan, jangan panik. Algoritma rezeki Anda didesain untuk memantul kembali dengan ganti yang jauh lebih menguntungkan."),
        3: ("Satria Wibawa (Magnet Kehormatan)", "Rezeki Anda hari ini tidak datang dalam bentuk uang tunai seketika, melainkan 'Trust' atau respek dari koneksi tingkat tinggi. Kewibawaan adalah mata uang Anda hari ini; jaga penampilan dan tata bahasa Anda."),
        4: ("Sumur Sinaba (Sumber Berkah)", "Vibrasi energi Anda bertindak bagaikan oasis. Orang-orang (klien/prospek) akan datang menghampiri untuk mencari jawaban dan solusi dari Anda. Jangan pelit berbagi *value*, karena dari situlah konversi rezeki Anda tercipta."),
        5: ("Bumi Kapetak (Kerja Cerdas)", "Tidak ada keajaiban instan hari ini. Mesin rezeki Anda menuntut pembuktian berupa keringat dan strategi presisi. Jika Anda mau menurunkan ego untuk bekerja lebih keras di belakang layar, panen besar sedang menunggu Anda."),
        6: ("Satria Wirang (Ujian Kelayakan)", "Fase ini adalah kawah candradimuka. Ada potensi gesekan rintangan atau ujian mental yang muncul di permukaan. Ini bukanlah kesialan, melainkan cara Semesta memfilter kelayakan ego Anda sebelum membuka akses ke level rezeki yang jauh lebih tinggi. Tetaplah *low-profile*."),
        7: ("Lebu Katiup Angin (Rentan Bocor)", "Arus kas Anda sedang berada di zona rawan. Potensi uang masuk besar, namun angin pengeluaran impulsif bertiup sangat kencang. Anda wajib menahan keinginan foya-foya dan segera kunci rezeki Anda ke dalam bentuk aset tetap atau investasi mati.")
    }[neptu%7 or 7]
    u = {
        1: ("Sandang (Kebutuhan Dasar)", "Sektor hoki Anda terhubung erat pada komoditas, gaya hidup, atau *tools* yang menyelesaikan masalah fundamental orang lain."),
        2: ("Pangan (Nutrisi Esensial)", "Vibrasi usaha berputar kuat pada ritel, kuliner, konsumsi, atau memberikan 'asupan nutrisi mental' (seperti edukasi dan *training*)."),
        3: ("Beja (Keberuntungan Murni)", "Sektor paling resonan adalah instrumen investasi, *closing* negosiasi bernilai tinggi, atau peluncuran aset digital baru. Cuan menanti."),
        4: ("Lara (Butuh Mitigasi)", "Zona merah. Hindari mengambil keputusan ekspansi bisnis secara Solo (*Lone Wolf*). Anda wajib berkolaborasi atau mencari referensi pihak ketiga."),
        5: ("Pati (Titik Buta)", "Dilarang keras melakukan spekulasi buta, judi, atau investasi bodong. Fokuskan tenaga murni untuk memperbaiki SOP internal atau *maintenance* sistem.")
    }[neptu%5 or 5]
    return r, u
 
def get_zodiak(tanggal):
    d, m = tanggal.day, tanggal.month
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "Aries"
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "Taurus"
    elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "Gemini"
    elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "Cancer"
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "Leo"
    elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "Virgo"
    elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "Libra"
    elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "Scorpio"
    elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "Sagittarius"
    elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "Capricorn"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius"
    else: return "Pisces"

def get_safe_firstname(name_str, default="User"):
    return str(name_str).strip().split()[0].upper() if str(name_str).strip() else default

def proc_couple_persona(root_c, n1, n2):
    random.seed(generate_seed(f"cp_{n1}_{n2}_{root_c}"))
    buka = random.choice([
        f"Ketika vibrasi nama **{n1}** dan **{n2}** dilebur, hasilnya mengunci di **Root {root_c}**.",
        f"Hukum resonansi mencatat persatuan **{n1}** dan **{n2}** menghasilkan gelombang **Root {root_c}**."
    ])
    desc = {
        1: ("THE POWER COUPLE", f"Kalian memancarkan simbol Alpha. {n1} dan {n2} membentuk entitas ambisius, fokus pada kemajuan karir."),
        2: ("THE SOULMATES", f"Kalian memiliki 'Wi-Fi' batin. Mudah bagi {n1} memahami emosi {n2} tanpa banyak kata. Harmoni adalah kunci."),
        3: ("THE SOCIALITES", f"Aura kalian magnetis. {n1} dan {n2} adalah pasangan menyenangkan yang selalu menghidupkan suasana sirkel."),
        4: ("THE BUILDERS", f"Hubungan ini berpijak pada bumi. Fokus {n1} dan {n2} adalah membangun aset keluarga dan kesetiaan absolut."),
        5: ("THE ADVENTURERS", f"Kalian dipenuhi energi kebebasan. {n1} maupun {n2} butuh kejutan dan tantangan agar cinta tetap menyala."),
        6: ("THE FAMILY FIRST", f"Simbol pengayoman tertinggi. Pengorbanan {n1} dan {n2} untuk merawat keutuhan rumah tangga sangat mendalam."),
        7: ("THE DEEP SEEKERS", f"Hubungan tertutup dan eksklusif. {n1} dan {n2} membangun koneksi intelektual dengan privasi yang sulit ditembus."),
        8: ("THE EMPIRE", f"Magnet kelimpahan mutlak. Penyatuan ego {n1} dan {n2} mengejar kesuksesan bisnis dan membangun kerajaan keluarga."),
        9: ("THE HEALERS", f"Puncak kedewasaan empati. Interaksi {n1} dan {n2} dipenuhi toleransi dan menjadi tempat penyembuhan bagi sirkel sekitar.")
    }
    return desc.get(root_c, ("UNCHARTED SYNERGY", "Anomali energi tak tertebak."))[0], f"{buka} {desc.get(root_c)[1]}"

def proc_weton_kombo(sisa, n1, n2, z1, z2):
    random.seed(generate_seed(f"wt_{n1}_{n2}_{sisa}_{z1}_{z2}"))
    do_list = {
        1: [f"Gunakan teknik *Pacing-Leading*. Saat argumen memanas, jangan buru-buru membantah. Validasi dulu emosi {n2} dengan mendengarkan aktif.", f"Beri jeda *Time-Out* saat perdebatan menajam. Biarkan ego bawaan {z1} dan {z2} reda terlebih dahulu."],
        2: [f"Jadikan {n2} sebagai *Partner Mastermind*. Jangan jalan sendirian! Libatkan ia dalam diskusi visi masa depan.", f"Bangun *Rapport* berbasis pencapaian. Saling memberikan apresiasi terbuka akan sangat memperkuat wibawa hubungan."],
        3: [f"Ciptakan *Pattern Interrupt* (Pola Kejutan). Lakukan kencan dadakan atau ubah rutinitas akhir pekan agar percikan dopamin tetap menyala.", f"Pancing *deep-talk* rutin minimal sebulan sekali. Obrolan filosofis akan sangat mempertajam frekuensi empati kalian."],
        4: [f"Kuasai teknik *Reframing* (Pembingkaian Ulang) saat menghadapi krisis. Pandang masalah sebagai tim solid: 'Kita berdua vs Masalah'.", f"Perkuat daya tahan mental (*Resilience*). Badai penyesuaian sifat di fase awal adalah harga tiket menuju rezeki besar."],
        5: [f"Gelar sesi 'Visi Masa Depan' bersama. Transparansi adalah kunci magnet rezeki bagi kalian.", f"Sinkronkan frekuensi kelimpahan kalian berdua. Jika salah satu sedang pesimis, tugas pasangannya menarik kembali ke mode optimis."],
        6: [f"Berikan *Space* (Ruang Pribadi) saat tensi saraf naik. Kalian memiliki filter informasi yang berbeda. Saat mulai panas, mundur selangkah.", f"Gunakan humor sebagai penetralisir racun. Ledakan tawa spontan sangat ampuh memecah ketegangan argumen ego."],
        7: [f"Komunikasi berbasis fakta (*Sensory Based*). Pastikan Anda selalu mengklarifikasi pesan: 'Maksud kamu tadi X atau Y?'.", f"Tingkatkan intensitas sentuhan fisik (*Physical Touch*) atau bahasa cinta primer pasangan untuk meredam cemburu buta."],
        8: [f"Pertahankan *Rapport* (Keakraban Bawah Sadar) dengan mengeksplorasi hobi atau proyek baru bersama untuk mencegah kebosanan.", f"Secara berkala, keluarlah dari zona nyaman rutinitas kalian berdua. Lakukan sesuatu yang memacu adrenalin bersama."]
    }
    dont_list = {
        1: [f"DILARANG KERAS melakukan *Mind-Reading* negatif. Jangan pernah mengasumsikan niat jahat {n2} tanpa klarifikasi eksplisit.", f"Pantang melakukan konfrontasi saat salah satu pihak sedang mengalami kondisi *H.A.L.T* (Hungry, Angry, Lonely, Tired)."],
        2: [f"Hindari jebakan 'Pencitraan Sempurna'. Jangan memalsukan kebahagiaan di luar padahal sedang dingin di dalam.", f"Jangan biarkan intervensi dari keluarga besar atau sirkel pertemanan luar merusak wibawa benteng rumah tangga kalian."],
        3: [f"Hati-hati terjebak dalam ilusi *Comfort Zone* (Zona Nyaman Berlebihan). Jangan sampai kalian malas berjuang untuk karir.", f"Jangan pernah mengabaikan perawatan diri (fisik dan mental) hanya karena merasa posisi Anda sudah 'aman' di hati pasangan."],
        4: [f"Jangan jadikan ego dan gengsi {n1} sebagai senjata penikam hati {n2}. Kompromi di fase adaptasi ini sangat krusial.", f"Pantang lempar handuk (menyerah) di 3 tahun pertama masa transisi. Mengucapkan kata perpisahan saat emosi memuncak akan menghancurkan pondasi."],
        5: [f"Jangan biarkan materi (uang) menjadi satu-satunya perekat jiwa antara {n1} dan {n2}.", f"Dilarang keras menyombongkan diri atau meremehkan orang lain saat pintu rezeki hasil persatuan kalian mulai terbuka lebar."],
        6: [f"Jangan pernah menyerang kelemahan fisik, masa lalu, atau harga diri fundamental {n2} secara frontal hanya karena berdebat sepele.", f"Dilarang menggunakan senjata *Silent Treatment* (mendiamkan pasangan) lebih dari 24 jam. Ini adalah manipulasi emosi."],
        7: [f"DILARANG MENGGUNAKAN kata-kata absolut saat bertengkar, seperti: 'Kamu TIDAK PERNAH peduli!'. Ini mengunci pasangan dalam mode defensif.", f"Jangan menjadi agen rahasia yang mengintai privasi ponsel atau media sosial pasangan secara diam-diam. *Trust issue* mematikan cinta."],
        8: [f"Waspadai jebakan sikap *Take it for granted* (menggampangkan pasangan). Jangan berhenti memberikan usaha lebih (*effort*) untuk membahagiakannya.", f"Jangan biarkan rutinitas mesin mematikan insting romantisme Anda. Rasa aman (*Pesthi*) butuh dirawat."]
    }
    hasil = {
        1: ("💔 PEGAT (Ujian Ego)", "Terdapat perbedaan fundamental arsitektur otak dalam memproses emosi. Sering terjadi adu argumen yang tajam karena ego defensif."),
        2: ("👑 RATU (Kharisma Pasangan)", "Memancarkan wibawa dan daya magnetis sosial yang tinggi. Kehadiran kalian memicu respek alami dari lingkungan."),
        3: ("💞 JODOH (Sinkronisasi Alami)", "Tingkat penerimaan bawah sadar yang sangat dalam. Koneksi batin terbentuk secara instan, seolah frekuensi jiwa sudah pernah terhubung."),
        4: ("🌱 TOPO (Ujian Bertumbuh)", "Awal kolaborasi akan dipenuhi gesekan adaptasi yang berat. Jika berhasil melampaui fase kritis ini, pondasi kalian takkan bisa ditembus badai."),
        5: ("💰 TINARI (Magnet Rezeki)", "Entitas pasangan ini memancarkan vibrasi kelimpahan. Kemacetan finansial mendadak terurai setelah kalian sepakat bersatu."),
        6: ("⚡ PADU (Beda Frekuensi)", "Sering muncul letupan perdebatan karena berbedanya filter informasi. Namun umumnya, yang diributkan hanyalah hal-hal teknis non-esensial."),
        7: ("👁️ SUJANAN (Rawan Asumsi)", "Vibrasi energi ini rawan menarik miskomunikasi dan cemburu buta. Asumsi negatif sering memicu salah paham jika tidak dibedah lewat komunikasi."),
        8: ("🕊️ PESTHI (Damai & Rukun)", "Interaksi batin yang adem ayem dan minim drama. Kehadiran fisik satu sama lain bertindak menetralisir racun stres kehidupan.")
    }
    return hasil[sisa][0], hasil[sisa][1], random.choice(do_list[sisa]), random.choice(dont_list[sisa])

def proc_penjelasan_matriks(n1, n2, eso_val, nep_val):
    random.seed(generate_seed(f"pm_v2_{n1}_{n2}_{eso_val}_{nep_val}"))
    header = random.choice(["⚙️ ARSITEKTUR ANALISA", "📡 DEKODE SINYAL KOSMIK", "📜 LOGIKA MESIN NEURO"])
    f_eso = random.choice([f"Fusi nama <b>{n1}</b> & <b>{n2}</b> mengunci di <b>{eso_val}</b>. Ini adalah persona yang muncul saat kalian bersama.", f"Ekstraksi sandi menghasilkan <b>{eso_val}</b>. Menentukan bagaimana kalian dipandang sebagai entitas."])
    f_nep = random.choice([f"Kalkulasi sinkronisasi waktu (Total Neptu <b>{nep_val}</b>) memetakan dinamika ego bawah sadar.", f"Analisa siklus (Parameter <b>{nep_val}</b>) menjadi radar pengukur stabilitas emosi kalian."])
    return f'<div class="info-metric-box"><b style="color:#FFD700; font-size:14px;">{header}:</b><br>• <b style="color:white;">TOTAL ESOTERIK:</b> {f_eso}<br>• <b style="color:white;">TOTAL NEPTU:</b> {f_nep}</div>'

KAMUS_ABJAD = {
    'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 
    't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 
    's': 60, 'f': 80, 'q': 100, 'r': 200, 'c': 3, 'e': 5,
    'g': 1000, 'i': 10, 'o': 6, 'p': 80, 'u': 6, 'v': 6, 'x': 60
}

def hitung_nama_esoterik(nama):
    nama_clean = ''.join(filter(str.isalpha, str(nama).lower()))
    return sum(KAMUS_ABJAD.get(huruf, 0) for huruf in nama_clean) or 1

def get_rincian_esoterik(nama):
    r = [f"{h.upper()}({KAMUS_ABJAD.get(h,0)})" for h in ''.join(filter(str.isalpha, str(nama).lower())) if KAMUS_ABJAD.get(h,0)>0]
    return " + ".join(r) if r else "0"

def generate_dynamic_reading(total_jummal):
    mod = total_jummal % 4 if total_jummal % 4 != 0 else 4
    el = {1: ("🔥 API (Nar)", "Sistem saraf eksekusi cepat, Anda inisiator."), 2: ("🌍 TANAH (Turab)", "Fondasi logis dan membumi."), 3: ("💨 UDARA (Hawa)", "Konseptor ide tanpa henti."), 4: ("💧 AIR (Ma')", "Emosional peka, empati beradaptasi.")}
    p_red = " + ".join(list(str(total_jummal)))
    s_red = sum(int(d) for d in str(total_jummal))
    r_num = s_red
    while r_num > 9: r_num = sum(int(d) for d in str(r_num))
    r_dict = {1:"Pencipta jalan baru", 2:"Penyelaras harmoni", 3:"Penyampai pesan", 4:"Pembangun sistem", 5:"Agen transformasi", 6:"Pengayom sejati", 7:"Pencari esensi", 8:"Pemegang kendali", 9:"Kesadaran universal"}
    
    m_note = "<div style='background:rgba(212,175,55,0.1); padding:15px; border-radius:8px; border-left: 4px solid #FFD700; margin-top:15px; margin-bottom:15px; box-shadow: 0 4px 15px rgba(212,175,55,0.2);'><span style='color:#FFD700; font-size:16px; letter-spacing:1px; font-weight:900;'>⚡ KODE MASTER TERDETEKSI</span><br><span style='color:#e0e0e0; font-size:14px; line-height:1.6; display:inline-block; margin-top:5px;'>Sistem mendeteksi anomali vibrasi positif tingkat tinggi (Angka Master). Intuisi spiritual dan indra ke-6 Anda beroperasi pada gelombang Theta hari ini. Firasat, ide dadakan, atau 'suara hati' yang muncul bukanlah ilusi—itu adalah transmisi presisi dari <i>Higher Self</i> Anda. Gunakan kompas batin ini untuk mengambil keputusan krusial yang selama ini membingungkan logika analitis Anda.</span></div>" if any(m in str(total_jummal) for m in ["11","22","33"]) else ""
    
    return el[mod][0], el[mod][1], p_red, s_red, r_num, r_dict.get(r_num,""), m_note

def hitung_angka(tanggal):
    try:
        t = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
        while t > 9: t = sum(int(digit) for digit in str(t))
        return t
    except: return 1

def get_rincian_tanggal(tanggal):
    try:
        ts = tanggal.strftime("%d%m%Y")
        p = f"{' + '.join(list(ts))} = {sum(int(d) for d in ts)}"
        t = sum(int(d) for d in ts)
        while t > 9:
            p += f" ➡ {' + '.join(list(str(t)))} = {sum(int(d) for d in str(t))}"
            t = sum(int(d) for d in str(t))
        return p
    except: return "1 = 1"

def hitung_neptu_langsung(hari, pasaran):
    return {"Minggu":5,"Senin":4,"Selasa":3,"Rabu":7,"Kamis":8,"Jumat":6,"Sabtu":9}.get(hari,0) + {"Legi":5,"Pahing":9,"Pon":7,"Wage":4,"Kliwon":8}.get(pasaran,0)

# Menghitung angka pengguna secara dinamis
dynamic_users = get_dynamic_count()

# --- SIDEBAR PROMOSI & LOGIN ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        try: st.image("baru.jpg.png", use_container_width=True); st.markdown("<br>", unsafe_allow_html=True)
        except: pass
 
    st.markdown(f"### {get_greeting()}")
    
    # SYSTEM LOCK / MEMBERSHIP
    st.markdown("---")
    st.markdown("### 🔓 Akses Premium")
    if not st.session_state.premium:
        kode_input = st.text_input("Punya Kode Akses? Ketik di sini:", type="password")
        if kode_input:
            if kode_input.upper() == "NEUROVIP": # BISA DIGANTI KODE APA AJA BRO
                st.session_state.premium = True
                st.toast("Akses Terbuka! Selamat Datang di Mode VIP.", icon="👑")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Kode Salah atau Kadaluarsa.")
        st.markdown("<p style='font-size:13px; color:#888;'>Dapatkan Kode Akses via <a href='https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy.' target='_blank' style='color:#25D366; font-weight:bold; text-decoration:none;'>WhatsApp</a></p>", unsafe_allow_html=True)
    else:
        st.success("👑 Status: VIP MEMBER")
        if st.button("Logout"):
            st.session_state.premium = False
            st.rerun()
    
    # WA CTA (URGENT & AGGRESSIVE)
    st.markdown("---")
    st.markdown("""<div style='background: linear-gradient(135deg, #ff0000 0%, #8b0000 100%); padding: 18px; border-radius: 10px; text-align: center; border: 1px solid #ff4b4b; box-shadow: 0 5px 15px rgba(255,0,0,0.3);'>
<b style='color: white; font-size: 16px; letter-spacing: 1px;'>🔥 BUTUH ANALISA LEBIH DALAM?</b><br>
<span style='color: #ccc; font-size: 12px; display:block; margin-top:5px;'>Beberapa hasil (Blok Mental Spesifik) tidak bisa ditampilkan di sistem terbuka.</span>
<span style='color: #FFD700; font-size: 13px; display:inline-block; margin-top:5px; margin-bottom:12px;'>Konsultasi Private dengan Coach (Slot Terbatas)</span><br>
<a href='https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20butuh%20sesi%20kalibrasi%20private%20hari%20ini' target='_blank' style='background: #25D366; color: white; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 900; font-size: 14px; display: inline-block; box-shadow: 0 4px 10px rgba(37,211,102,0.4);'>💬 KLIK DI SINI SEKARANG</a>
</div>""", unsafe_allow_html=True)
    st.markdown("<br><center><small style='color:#666;'>© 2026 Neuro Nada Academy</small></center>", unsafe_allow_html=True)
 
# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

cur_planet, cur_instr, cur_color = get_planetary_hour()
st.markdown(f"""<div style='text-align: right;'><div class='live-badge' style='background: {cur_color};'>🕒 LIVE PLANET: {cur_planet.upper()}</div><div style='font-size: 11px; color: #888; margin-top: 5px;'>{cur_instr}</div></div>""", unsafe_allow_html=True)
 
st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900; color:#FFD700;'>🌌 BUKA KODE HIDUP ANDA HARI INI</h1>", unsafe_allow_html=True)
st.markdown("""<p style='text-align: center; font-size: 16px; color: #ccc;'>Ini bukanlah Ramalan konvensional. Ini adalah pemetaan presisi tinggi berdasarkan cetak biru nama (Hisab Jummal), garis waktu kelahiran (Meta-Program NLP), dan bioritme alam semesta Anda.<br><br><b style='color:#FFF;'>⚡ Dalam 10 detik, Anda akan meretas:</b><br><span style='color:#D4AF37;'>• Fluktuasi momentum rezeki hari ini<br>• Celah *Blind Spot* yang HARUS dieksekusi<br>• Sabotase mental bawah sadar yang WAJIB dihindari</span></p>""", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; margin-bottom:20px;'><span style='background:rgba(255,75,75,0.2); color:#ff4b4b; padding:8px 15px; border-radius:5px; font-size:13px; font-weight:bold; letter-spacing:1px;'>⚠️ PERINGATAN: Jangan teruskan jika Anda belum siap menghadapi cermin kebenaran diri Anda.</span></div>", unsafe_allow_html=True)
st.markdown("---")
 
tgl_today = datetime.date.today()
tab1, tab2, tab5, tab3, tab6, tab4 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Matrix 🔒", "⏱️ Quantum Engine 🔒", "🌌 Falak Ruhani 🔒", "📚 Neuro-Insights", "❓ FAQ & Disclaimer"])
 
# ==========================================
# TAB 1: IDENTITAS KOSMIK (HOOK & PAYWALL)
# ==========================================
with tab1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#fff;'>👇 Masukkan parameter Anda sekarang</h4>", unsafe_allow_html=True)
    nama_user = st.text_input("Nama Lengkap Sesuai Identitas Asli:", placeholder="Ketik nama lengkap...", key="t1_nama")
    
    col_tgl, col_wt = st.columns(2)
    with col_tgl:
        st.write("📅 **Data Masehi:**")
        tgl_input = st.date_input("Tanggal Lahir", value=datetime.date(1983, 9, 23), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")
    with col_wt:
        st.write("📜 **Data Weton:**")
        hari_input = st.selectbox("Hari Kelahiran", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="h_t1")
        pasaran_input = st.selectbox("Pasaran Kelahiran", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="p_t1")
    st.markdown("</div>", unsafe_allow_html=True)
 
    if st.button("🚀 Lihat Peluang & Sabotase Saya Hari Ini", key="btn_t1"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Filter Keamanan: Mohon ketik nama lengkap Anda (minimal 3 karakter).")
        else:
            try:
                with st.spinner('Menyelaraskan frekuensi kosmik dan algoritma NLP...'):
                    time.sleep(1.5)
                st.toast("Kalibrasi selesai! Membuka gerbang analisis...", icon="⚡")
                
                safe_name = get_safe_firstname(nama_user)
                angka_hasil = hitung_angka(tgl_input)
                rincian_tgl = get_rincian_tanggal(tgl_input)
                
                nilai_jummal = hitung_nama_esoterik(nama_user)
                rincian_jummal = get_rincian_esoterik(nama_user)
                el_nama, el_desc, p_reduk, s_reduk, r_num, r_desc, m_note = generate_dynamic_reading(nilai_jummal)
                
                nep = hitung_neptu_langsung(hari_input, pasaran_input)
                wet = f"{hari_input} {pasaran_input}"
                zod = get_zodiak(tgl_input)
                
                n_laku, d_laku, arah_naga = get_betaljemur_data(nep, hari_input)
                rezeki_data, usaha_data = get_rezeki_usaha(nep)
                
                punchy = arketipe_punchy.get(angka_hasil, arketipe_punchy[1])
                desk_ark_dinamis = proc_arketipe(safe_name, angka_hasil, zod, nep)
                shadow = proc_shadow_list(safe_name, angka_hasil)
                
                # Dynamic Action Generator based on Sun Phase for Hook
                aksi_list = [
                    f"Jebol kebuntuan Anda hari ini. Segera hubungi satu prospek atau koneksi kunci yang selama ini penanganannya Anda tunda akibat rasa ragu.",
                    f"Lakukan audit energi mental. Identifikasi dan hentikan SATU interaksi/tugas repetitif hari ini yang diam-diam menguras kewarasan Anda.",
                    f"Praktikkan delegasi radikal. Ada satu beban teknis yang menahan potensi besar Anda—lepaskan ego dan serahkan tugas itu ke orang yang tepat hari ini."
                ]
                aksi_teks = random.choice(aksi_list)
                
                # Mengambil Core Shadow untuk Red Flag
                core_shadow_raw = shadow[0]
                core_shadow_title = core_shadow_raw.split("**")[1].replace(":", "") if "**" in core_shadow_raw else core_shadow_raw.split(":")[0]
                
                # --- HASIL CEPAT 10 DETIK (HOOK - DYNAMIC & DEEP) ---
                st.markdown(f"""<div class="soft-fade" style="background: rgba(255,215,0,0.1); border-left: 5px solid #FFD700; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,215,0,0.3);">
<h3 style="margin-top:0; color:#FFD700; font-weight:900; letter-spacing:1px;">🎯 HASIL DECODING ANDA HARI INI</h3>
<ul style="font-size: 16px; line-height: 1.8; color: #fff; list-style-type: none; padding-left: 0;">
<li style="margin-bottom: 15px; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px;">
💰 <b>STATUS REZEKI (<span style='color:#FFD700;'>{rezeki_data[0].split('(')[0].strip()}</span>):</b><br>
<span style='color:#25D366; font-weight:bold; font-size:15px;'>MOMENTUM AKTIF.</span> <span style="color:#e0e0e0; font-size:14px; line-height:1.6;">{rezeki_data[1]}</span>
</li>
<li style="margin-bottom: 15px; background: rgba(37,211,102,0.1); border-left: 4px solid #25D366; padding: 15px; border-radius: 8px;">
⚡ <b>INSTRUKSI AKSI TAKTIS:</b><br>
<span style="color:#e0e0e0; font-size:14px; line-height:1.6;">{aksi_teks}</span>
</li>
<li style="margin-bottom: 10px; background: rgba(255,75,75,0.1); border-left: 4px solid #ff4b4b; padding: 15px; border-radius: 8px;">
🚫 <b>RED FLAG (LARANGAN MUTLAK):</b><br>
<span style="color:#ff4b4b; font-size:14px; font-weight:bold;">Waspadai letupan {core_shadow_title}!</span><br>
<span style="color:#e0e0e0; font-size:14px; line-height:1.6;">Sistem membaca adanya celah sabotase bawah sadar hari ini. Tahan dorongan impulsif atau ketakutan tak beralasan Anda sebelum menjatuhkan keputusan finansial atau komitmen besar.</span>
</li>
</ul>
<div style="background: rgba(255,75,75,0.2); padding: 8px 15px; border-radius: 5px; display: inline-block; margin-top: 10px;">
<b style="color:#ff4b4b; font-size:13px;">⏳ Fluktuasi energi ini hanya relevan hingga pergantian siklus (24 jam ke depan).</b>
</div>
</div>""", unsafe_allow_html=True)
                
                # --- PAYWALL: CEK STATUS PREMIUM ---
                if not st.session_state.premium:
                    st.markdown(f"""<div class="glass-container soft-fade" style="text-align:center; border: 2px solid #ff4b4b; padding: 30px 20px;">
<h3 style="color:#ff4b4b; margin-top:0;">🔓 Anda baru melihat 15% dari hasil *Decoding* Anda...</h3>
<div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: left; display: inline-block;">
<span style="color:#ccc; font-size: 15px;">Di dalam analisa Premium (Tanpa Batas):</span><br>
<b style="color:#fff;">• Blueprint kepribadian terdalam & Arsitektur Ego Anda</b><br>
<b style="color:#fff;">• 3 Titik Kebocoran Mental (Shadow) yang mensabotase cuan</b><br>
<b style="color:#fff;">• Strategi Arah Mata Angin (Geomansi) penarik keberuntungan</b><br>
<b style="color:#fff;">• Analisa Kompatibilitas Hubungan Bawah Sadar (Couple Matrix)</b>
</div>
<p style="color:#FFD700; font-size: 16px;"><b>🔥 Laporan ini tidak akan Anda temukan di Google.<br>Ini murni algoritma PERSONAL — hanya untuk Anda.</b></p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration:none;">
<div class="cta-button" style="font-size:18px; margin-top: 10px;">🚀 AKTIFKAN FULL REPORT SEKARANG</div>
</a>
<p style="font-size:14px; color:#ccc; margin-top:15px; margin-bottom: 5px;">Investasi: <b>Hanya Rp 19.000</b><br><i style="color:#888;">(Harga perkenalan platform. Bebas akses 1 bulan penuh.)</i></p>
<span style="background:rgba(255,75,75,0.2); color:#ff4b4b; padding:4px 10px; border-radius:3px; font-size:12px; font-weight:bold;">⚠️ Algoritma Harga dapat naik otomatis mengikuti *traffic* sistem.</span>
<div style="margin-top: 25px; border-top: 1px dashed #555; padding-top: 15px;">
<span style="font-size:14px; color:#25D366; font-weight:bold;">🔥 {dynamic_users} individu telah mengkalibrasi nasib mereka minggu ini.</span><br>
<span style="font-size:13px; color:#888;">Keluar dari kebingungan Anda sekarang juga.</span>
</div>
<br><br>
<div style='background: rgba(212,175,55,0.1); padding: 15px; border-radius: 10px; border: 1px solid #D4AF37;'>
<b style='color: #D4AF37; font-size: 16px; letter-spacing: 1px;'>🚀 EKSTRA BONUS (UNTUK ANDA HARI INI)</b><br>
<span style='color: white; font-size: 14px; display:inline-block; margin-top:5px; margin-bottom:12px;'><i>“Dapatkan akses langsung ke Modul Opini Eksklusif Hypno-NLP”</i></span>
</div>
</div>""", unsafe_allow_html=True)
                else:
                    # --- DEEP ANALYSIS (HANYA JIKA PREMIUM) ---
                    st.markdown(f"<h3 style='text-align:center;'>🌌 Laporan Decoding Lengkap: {safe_name}</h3>", unsafe_allow_html=True)
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Nilai Esoterik (Jummal)</div><div class="matrix-value matrix-value-special">{nilai_jummal}</div></div><div class="matrix-item"><div class="matrix-label">Core Element</div><div class="matrix-value">{el_nama.split(' ')[1] if len(el_nama.split(' '))>1 else el_nama}</div></div><div class="matrix-item"><div class="matrix-label">Meta-Program (NLP)</div><div class="matrix-value matrix-value-special">KODE {angka_hasil}</div></div><div class="matrix-item"><div class="matrix-label">Filter Astrologi</div><div class="matrix-value">{zod}</div></div><div class="matrix-item"><div class="matrix-label">Beban Weton</div><div class="matrix-value">{wet} ({nep})</div></div></div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="dynamic-reading-box soft-fade"><h4 style="color: #FFD700; margin-top:0;">🔍 Analisa Arsitektur Diri (DNA Numerologi)</h4><p><b>1. Sandi Esoterik Nama (Peta Vibrasi):</b><br><code style="color:#25D366; background:transparent; padding:0;">{rincian_jummal} = <b>{nilai_jummal}</b></code></p><ul style="margin-left: -15px; margin-bottom: 20px;"><li><b>Elemen Bawah Sadar:</b> {el_nama} - <i style="color:#aaa;">{el_desc}</i></li><li><b>Inti Jiwa (Root Frequency):</b> {p_reduk} = {s_reduk} ➡ <b>{r_num}</b> ({r_desc})</li></ul><p><b>2. Sandi Waktu Lahir (Meta-Program NLP):</b><br><code style="color:#FFD700; background:transparent; padding:0;">{rincian_tgl}</code><br><span style="font-size:14px; color:#ccc;">Ekstraksi di atas menghasilkan <b>KODE {angka_hasil}</b>. Angka final ini bukanlah tebakan, melainkan struktur *Blueprint* bagaimana otak <b>{safe_name}</b> memproses stres, memfilter informasi, dan mengeksekusi tindakan sedari Anda dilahirkan.</span></p>{m_note}</div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="primbon-box soft-fade"><div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;"><span style="color:#D4AF37; font-size:14px; font-weight:900; letter-spacing:2px;">📜 PETHIKAN ALGORITMA BETALJEMUR ADAMMAKNA</span></div>
<div style="font-size:15px; line-height:1.6; margin-bottom: 20px;"><b style="color:#FFF; font-size:18px; letter-spacing:1px;">{n_laku}</b><br><i style="color:#ccc; display:inline-block; margin-top:5px;">{d_laku}</i></div>
<div style="font-size:15px; line-height:1.6; margin-bottom: 20px; border-top: 1px dashed #555; border-bottom: 1px dashed #555; padding-top: 15px; padding-bottom: 15px;">
• <b style="color:#FFF;">Siklus Rezeki (<span style="color:#FFD700;">{rezeki_data[0]}</span>):</b><br><i style="color:#ccc; display:inline-block; margin-top:3px; margin-bottom:10px;">{rezeki_data[1]}</i><br>
• <b style="color:#FFF;">Resonansi Sektor Usaha (<span style="color:#25D366;">{usaha_data[0]}</span>):</b><br><i style="color:#ccc; display:inline-block; margin-top:3px;">{usaha_data[1]}</i>
</div>
<div style="font-size:15px; line-height:1.6; background: rgba(212,175,55,0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700;">
<span style="color:#FFD700;">🧭 <b>NAGA DINA (Arah Kejayaan Geomansi Hari {hari_input}):</b></span> <b style="font-size: 18px; color:#FFF;">{arah_naga}</b><br>
<i style="color:#e0e0e0; font-size:14px; display:inline-block; margin-top:8px;">*ACTIONABLE (Tindakan Fisik): Posisikan tubuh fisik Anda menghadap ke arah <b>{arah_naga}</b> saat melakukan negosiasi *closing*, mengirim *email* krusial, atau *brainstorming* pengambilan keputusan besar hari ini. Penyelarasan magnetik ini dipercaya kuat secara empiris untuk membuka 'Blind Spot' hambatan dan memuluskan niat (manifestasi) Anda.</i>
</div></div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"<h3 style='margin-bottom:5px;'>👁️ Decode Kepribadian Psikologis Dinamis: {safe_name}</h3>", unsafe_allow_html=True)
                    st.info(f"Sistem mengkalibrasi ulang pola perilaku Anda. Arsitektur mental (Arketipe) Anda dikunci secara absolut sebagai:\n\n### **{punchy['inti']}**")
                    st.markdown(f"<p style='font-size:15px; line-height:1.6; color:#ccc; margin-bottom:25px;'>{desk_ark_dinamis}</p>", unsafe_allow_html=True)
                    
                    c_kekuatan, c_shadow = st.columns(2)
                    with c_kekuatan:
                        st.markdown(f"🔥 <b style='color:#FFF; font-size:16px;'>KEKUATAN DOMINAN KARIER:</b>", unsafe_allow_html=True)
                        st.markdown(f"<ul class='list-punchy' style='color:#25D366; line-height:1.6;'><li>{punchy['kekuatan'][0]}</li><li style='margin-top:8px;'>{punchy['kekuatan'][1]}</li><li style='margin-top:8px;'>{punchy['kekuatan'][2]}</li></ul>", unsafe_allow_html=True)
                    with c_shadow:
                        st.markdown(f"⚠️ <b style='color:#FFF; font-size:16px;'>SHADOW (VIRUS BAWAH SADAR):</b>", unsafe_allow_html=True)
                        st.markdown(f"<ul class='list-punchy' style='color:#ff4b4b; line-height:1.6;'><li><span style='color:#e0e0e0'>{shadow[0]}</span></li><li style='margin-top:10px;'><span style='color:#e0e0e0'>{shadow[1]}</span></li><li style='margin-top:10px;'><span style='color:#e0e0e0'>{shadow[2]}</span></li></ul>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Sistem gagal melakukan komputasi tingkat tinggi: {e}")
 
# ==========================================
# TAB 2: COUPLE MATRIX (LOCKED)
# ==========================================
with tab2:
    if not st.session_state.premium:
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h3 style='color: #ff4b4b; font-weight: 900; margin-top:0;'>💞 KALIBRASI HUBUNGAN BAWAH SADAR</h3>
<p style='color: #ccc; font-size: 16px; margin-bottom: 20px;'>Bongkar algoritma ketidakcocokan Anda. Apakah hubungan ini:<br><b style='color:#ff4b4b;'>❤️ Pertemuan Jodoh Karmik?</b> | <b style='color:#FFD700;'>⚡ Fase Ujian Mental?</b> | <b style='color:#888;'>💔 Atau Bom Waktu Kehancuran?</b></p>
<p style='font-size: 14px; color: #aaa; margin-bottom: 30px;'>Masukkan 2 nama (pasangan/rekan bisnis) dan bedah letak letupan konflik kalian sekarang.<br><i style='color:#ff4b4b;'>⚠️ Peringatan: Hasil algoritma sangat frontal dan *to-the-point*.</i></p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN KODE VIA WHATSAPP (Rp 19.000)</div>
</a>
<p style='font-size:13px; color:#25D366; font-weight:bold; margin-top:15px;'>🔥 Akses ini sudah termasuk di dalam Paket Premium 1 Bulan.</p>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("💞 Penyatuan Esoterik & Betaljemur (Couple Matrix)")
        ca, cb = st.columns(2)
        with ca: 
            st.markdown("<h4 style='color:#FFD700;'>Pihak 1 (Aktor/Pria)</h4>", unsafe_allow_html=True)
            n1 = st.text_input("Nama Asli Pihak 1", key="n1_c")
            d1 = st.date_input("Lahir Masehi Pihak 1", value=datetime.date(1995, 1, 1), format="DD/MM/YYYY", key="d1_c")
            hc1 = st.selectbox("Hari Pihak 1", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="hc1")
            pc1 = st.selectbox("Pasaran Pihak 1", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="pc1")
        with cb: 
            st.markdown("<h4 style='color:#FF69B4;'>Pihak 2 (Reaktor/Wanita)</h4>", unsafe_allow_html=True)
            n2 = st.text_input("Nama Asli Pihak 2", key="n2_c")
            d2 = st.date_input("Lahir Masehi Pihak 2", value=datetime.date(1995, 1, 1), format="DD/MM/YYYY", key="d2_c")
            hc2 = st.selectbox("Hari Pihak 2", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=2, key="hc2")
            pc2 = st.selectbox("Pasaran Pihak 2", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=0, key="pc2")
        st.markdown("</div>", unsafe_allow_html=True)
            
        if st.button("🚀 Retas Kode Pasangan", key="btn_couple"):
            if str(n1).strip() and str(n2).strip():
                try:
                    with st.spinner('Menghitung benturan energi dan menumbuk ego...'):
                        time.sleep(1.5)
                    st.toast("Analisa sinkronisasi pasangan berhasil diekstrak!", icon="💞")
                    
                    safe_n1, safe_n2 = get_safe_firstname(n1, "Pria"), get_safe_firstname(n2, "Wanita")
                    zod1, zod2 = get_zodiak(d1), get_zodiak(d2)
                    nep_1, nep_2 = hitung_neptu_langsung(hc1, pc1), hitung_neptu_langsung(hc2, pc2)
                    sel = abs(hitung_angka(d1) - hitung_angka(d2))
                    
                    jummal_1, jummal_2 = hitung_nama_esoterik(n1), hitung_nama_esoterik(n2)
                    total_couple = jummal_1 + jummal_2
                    root_c = total_couple
                    while root_c > 9: root_c = sum(int(d) for d in str(root_c))
                    
                    c_title, c_desc = proc_couple_persona(root_c, safe_n1, safe_n2)
                    judul_jodoh, desk_jodoh, d_do, d_dont = proc_weton_kombo((nep_1+nep_2)%8 or 8, safe_n1, safe_n2, zod1, zod2)
                    
                    st.markdown(f"### 🔮 The Unified Resonance: {safe_n1} & {safe_n2}")
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Beban Neptu {safe_n1}</div><div class="matrix-value">{hc1} {pc1} ({nep_1})</div></div><div class="matrix-item"><div class="matrix-label">Beban Neptu {safe_n2}</div><div class="matrix-value">{hc2} {pc2} ({nep_2})</div></div><div class="matrix-item" style="background: rgba(212,175,55,0.2);"><div class="matrix-label" style="color:#FFD700;">TOTAL BENTURAN NEPTU</div><div class="matrix-value matrix-value-special">{nep_1 + nep_2}</div></div><div class="matrix-item"><div class="matrix-label">Total Frekuensi Esoterik</div><div class="matrix-value">{total_couple}</div></div></div>""", unsafe_allow_html=True)
                    st.markdown(proc_penjelasan_matriks(safe_n1, safe_n2, total_couple, (nep_1+nep_2)), unsafe_allow_html=True)
                    st.markdown(f'<div class="dynamic-reading-box soft-fade" style="border-left-color: #25D366;"><h4 style="color: #25D366; margin-top:0;">🧬 Persona Entitas Baru: {c_title}</h4><p style="color:#e0e0e0; line-height:1.6;">{c_desc}</p></div>', unsafe_allow_html=True)
                    st.info(f"**Titik Benturan Gesekan ({judul_jodoh}):**\n\n{desk_jodoh}")
                    
                    if sel in [0, 3, 6, 9]: st.success(f"💘 **SKOR META-PROGRAM (NLP): Sangat Sinkron.** Otak kalian memproses konflik dengan bahasa ego yang serupa.")
                    elif sel in [1, 2, 8]: st.warning(f"⚖️ **SKOR META-PROGRAM (NLP): Dinamis Labil.** Butuh banyak toleransi kalibrasi emosi agar tidak cepat bosan.")
                    else: st.error(f"🔥 **SKOR META-PROGRAM (NLP): Rawan Gesekan Tinggi.** Secara genetik psikologis, kalian memiliki filter penerimaan informasi yang bertolak belakang.")
         
                    c_do_c, c_dont_c = st.columns(2)
                    with c_do_c: st.markdown(f"<div class='soft-fade' style='background:rgba(37,211,102,0.1); padding:20px; border-radius:10px; border:1px solid #25D366; height:100%;'><b style='color:#25D366; font-size:16px;'>✅ PROTOKOL HUBUNGAN (DO):</b><br><br><span style='color:#e0e0e0; line-height:1.6;'>{d_do}</span></div>", unsafe_allow_html=True)
                    with c_dont_c: st.markdown(f"<div class='soft-fade' style='background:rgba(255,75,75,0.1); padding:20px; border-radius:10px; border:1px solid #ff4b4b; height:100%;'><b style='color:#ff4b4b; font-size:16px;'>❌ RED ZONE (DON'T):</b><br><br><span style='color:#e0e0e0; line-height:1.6;'>{d_dont}</span></div>", unsafe_allow_html=True)
                except Exception as e: st.error(f"Error komputasi: {e}")

# ==========================================
# TAB 5: QUANTUM ENGINE (LOCKED)
# ==========================================
with tab5:
    if not st.session_state.premium:
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 FITUR EKSKLUSIF DIKUNCI</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Anda sedang mengakses batas *Free Tier*. Buka akses <b>Tactical Action Plan (Pemetaan Aksi Taktis Harian Berbasis Menit)</b> yang dikalibrasi real-time dengan energi rotasi planet Anda.</p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN KODE VIA WHATSAPP (Rp 19.000)</div>
</a>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("⏱️ Live Cosmic Dashboard (Fate Hacking)")
        st.write("Sinkronkan langkah Anda dengan rotasi jam planet dan ritme sirkadian matahari untuk efisiensi eksekusi 10x lipat.")
        qe_nama = st.text_input("Nama Panggilan Target (Anda):", key="qe_n")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Tarik Data Taktis Saat Ini", key="btn_qe"):
            if qe_nama:
                with st.spinner('Membaca pergerakan astronomi *real-time*...'):
                    time.sleep(1.2)
                st.toast("Dashboard Taktis berhasil diperbarui!", icon="⏱️")
                
                safe_qe = get_safe_firstname(qe_nama)
                jummal_qe = hitung_nama_esoterik(qe_nama)
                mod_harian = (jummal_qe + sum(int(d) for d in tgl_today.strftime("%d%m%Y"))) % 7
                
                sun_fase, sun_desc = get_sun_phase()
                planet_live, planet_desc, planet_color = get_planetary_hour()
                
                siklus_nama, html_plan = proc_tactical_plan(safe_qe, mod_harian, planet_live, planet_desc, sun_fase, sun_desc)
                
                st.markdown(f"### 📡 Live Dashboard Komando: {safe_qe}")
                st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Fase Bioritme Harian</div><div class="matrix-value">{siklus_nama.split('(')[0].strip()}</div></div><div class="matrix-item"><div class="matrix-label">Fase Sirkadian Matahari</div><div class="matrix-value matrix-value-special">{sun_fase.split(' ')[0]}</div></div><div class="matrix-item" style="border-bottom: 2px solid {planet_color};"><div class="matrix-label">Intervensi Jam Planet</div><div class="matrix-value" style="color:{planet_color};">{planet_live}</div></div></div>""", unsafe_allow_html=True)
                
                st.markdown(html_plan, unsafe_allow_html=True)

# ==========================================
# TAB 3: FALAK RUHANI (LOCKED)
# ==========================================
with tab3:
    if not st.session_state.premium:
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 FITUR PENYEMBUHAN DIKUNCI</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Akses ditolak. Buka resep <b>Terapi Falak Ruhani, Dzikir Khusus Nama, Afirmasi NLP Terdalam, & Penawar Mental Block</b> dengan *Akses VIP*.</p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN KODE VIA WHATSAPP (Rp 19.000)</div>
</a>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("🌌 Terapi Falak Ruhani & Hypno-NLP Anchor")
        st.info("**Reset Ulang Mesin Saraf Anda**\n\nSistem mengonversi nama Anda menjadi angka getaran khusus, lalu memformulasikannya dengan frekuensi Asmaul Husna (Anchor Spiritual) dan Afirmasi Bawah Sadar (Sugesti NLP) yang spesifik didesain hanya untuk menghancurkan *Mental Block* utama Anda.")
        nama_ruhani = st.text_input("Masukkan Nama Lengkap Anda (Untuk Sinkronisasi Dzikir):", placeholder="Ketik nama asli...", key="input_ruhani")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Generate Resep Terapi Mental", key="btn_ruhani"):
            if nama_ruhani and len(nama_ruhani.strip()) >= 3:
                try:
                    with st.spinner('Mengekstrak sandi penyembuhan matriks Anda...'):
                        time.sleep(1.5)
                    st.toast("Protokol Terapi berhasil diturunkan dari sistem!", icon="✨")
                        
                    safe_nr = get_safe_firstname(nama_ruhani)
                    nilai_jummal_r = hitung_nama_esoterik(nama_ruhani)
                    
                    r_num_r = nilai_jummal_r
                    while r_num_r > 9: r_num_r = sum(int(d) for d in str(r_num_r))
                    
                    asma_terapi, vibrasi_asma, tujuan_ruhani, jumlah_dzikir = proc_falak_ruhani(nilai_jummal_r, r_num_r, safe_nr)
                    protokol_nlp = get_protokol_terapi(r_num_r, safe_nr)
                    
                    st.markdown(f"""<div class="soft-fade" style="background: linear-gradient(135deg, rgba(10, 20, 40, 0.9) 0%, rgba(20, 10, 40, 0.9) 100%); border-left: 5px solid #00FFFF; padding: 25px; border-radius: 12px; margin-top: 20px; box-shadow: 0 8px 25px rgba(0, 255, 255, 0.15);">
<div style="text-align:center; border-bottom:1px solid #00FFFF; padding-bottom:10px; margin-bottom:20px;">
<span style="color:#00FFFF; font-size:16px; font-weight:900; letter-spacing:2px;">🧠 PROTOKOL TERAPI KOMPREHENSIF: {safe_nr.upper()}</span>
</div>
<div style="margin-bottom: 20px;">
<b style="color:#ff4b4b; font-size:16px;">⚠️ MENTAL BLOCK (Virus Sabotase Bawah Sadar):</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.6; display:inline-block; margin-top:5px;">{protokol_nlp['block']}</span>
</div>
<div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
<b style="color:#FFF; font-size:16px;">✨ 1. ANCHOR SPIRITUAL KUNCI (Falak Ruhani)</b><br>
<span style="color:#aaa; font-size:14px; display:inline-block; margin-bottom:8px;">Gunakan Asma ini sebagai Dzikir penenang hati (pengunci fokus) saat pikiran sedang *chaos*:</span><br>
<b style="color:#00FFFF; font-size:22px;">{asma_terapi}</b> <span style="color:#FFD700; font-weight:bold; font-size:16px;">(BACA {jumlah_dzikir}x)</span><br>
<i style="color:#ccc; font-size:14px; display:inline-block; margin-top:5px; padding-top:8px; border-top:1px solid #333;">Tujuan Injeksi Batin: {tujuan_ruhani}</i>
</div>
<div style="background: rgba(255,215,0,0.05); border-left: 4px solid #FFD700; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
<b style="color:#FFD700; font-size:16px;">🗣️ 2. SUGESTI HYPNO-NLP (Afirmasi Pemutusan Rantai)</b><br>
<span style="color:#aaa; font-size:14px; display:inline-block; margin-bottom:8px;">Ucapkan kalimat sugesti ini berulang kali di dalam hati dengan penuh keyakinan dan rasakan emosinya sesaat menjelang tidur (Fase Gelombang Theta Terbuka):</span><br>
<div style="background: rgba(0,0,0,0.6); padding: 12px; border-radius:6px;"><i style="color:#fff; font-size:16px; line-height:1.6;">"{protokol_nlp['afirmasi']}"</i></div>
</div>
<div style="border-top: 1px dashed #555; padding-top: 15px; padding-bottom: 5px;">
<b style="color:#25D366; font-size:16px;">🏃‍♂️ 3. QUANTUM HABIT (Tindakan Fisik Pengunci Hari Ini)</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.6; display:inline-block; margin-top:5px;">Hanya berdiam diri tidak mengubah nasib karena Semesta hanya merespons *tindakan nyata*. Untuk menghancurkan struktur *Mental Block* Anda secara instan, paksa diri Anda untuk mengeksekusi satu tugas ini hari ini juga:<br><br>
<b style="color:#FFF; font-size:16px; background: rgba(37,211,102,0.2); padding: 8px; border-radius: 5px; display:inline-block;">{protokol_nlp['habit']}</b></span>
</div>
<p style="font-size:12px; color:#ff4b4b; margin-top:20px; font-weight:bold; text-align:center;">⏳ Sistem memonitor kebocoran energi. Lakukan protokol ini malam ini sebelum siklus tidur Anda me-reset semuanya!</p>
</div>""", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses sandi terapi *deep level*: {e}")
                
            else:
                st.warning("⚠️ Filter Keamanan: Ketik nama lengkap Anda (minimal 3 huruf) untuk otorisasi sinkronisasi.")

# ==========================================
# TAB 6: NEURO-INSIGHTS (KOLAM ARTIKEL)
# ==========================================
with tab6:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("📚 Neuro-Insights: Kalibrasi Mindset Otoritatif")
    st.write("Jelajahi pemikiran terdalam, modifikasi bawah sadar, dan telaah esoterik Nusantara langsung dari sudut pandang *Hypno-Copywriting*.")
    
    with st.expander("🧠 1. Kenapa Logika Sering Kalah Telak Oleh Perasaan?"):
        st.markdown("""
        **Oleh: Coach Ahmad Septian (NLP Trainer & Hypnotherapist)**
        ---
        Banyak eksekutif dan pengusaha mengira setiap keputusan bisnis atau hidup yang mereka buat sehari-hari adalah hasil kalkulasi rasional tingkat tinggi. Faktanya secara neuro-sains, **95% keputusan manusia dikendalikan mutlak oleh pikiran bawah sadar**—yang bahasa utamanya bukanlah angka, melainkan emosi. 
        
        Ketika logika berteriak "Jangan hubungi prospek itu karena berisiko ditolak", namun hati berkata "Tapi ada ketakutan aneh jika peluang ini hilang", siapakah yang memegang kendali eksekusi? Selalu perasaan (emosi ketakutan). Logika selalu datang belakangan hanya untuk merasionalisasi / mencari pembenaran atas emosi tersebut.
        
        **Strategi Modifikasi (NLP Reframing):** Jika Anda ingin membalikkan nasib, memecah *procrastination* (penundaan), atau menghancurkan kebiasaan buruk finansial, jangan berdebat dengan logika Anda sendiri. Anda tidak akan menang melawan diri sendiri. Ubahlah 'Rasa' (*Anchor* Emosional) yang menempel pada kebiasaan tersebut. Mulailah mengasosiasikan "bertindak berani" dengan "rasa lega yang luar biasa".
        """)
        
    with st.expander("💰 2. Rahasia Vibrasi Kebocoran Rezeki di Balik Sandi Nama"):
        st.markdown("""
        Pernahkah Anda merasa sudah banting tulang, mengorbankan waktu tidur dan keringat siang-malam, tapi rezeki selalu terasa 'lewat' begitu saja? Atau mungkin uang mudah masuk dalam jumlah besar, tapi anehnya selalu menguap habis untuk hal-hal darurat yang tidak terduga?
        
        Dalam ranah esoterik Nusantara (khususnya Metodologi Hisab Jummal), tidak ada yang namanya kebetulan. **Setiap huruf pada nama Anda (yang dipanggil setiap hari) membawa beban frekuensi psikologis tertentu.** Jika nama Anda memiliki vibrasi elemen "Api" (Nar) yang terlalu memonopoli ego tanpa penyeimbang elemen "Air" (Ma'), wajar jika secara impulsif bawah sadar, Anda sering mensabotase kesuksesan investasi Anda sendiri karena sifat terburu-buru, kesombongan instan, atau nafsu materialistik jangka pendek.
        
        **Tindakan Resolusi:** Lakukan kalibrasi identitas spiritual. Ini bukan berarti Anda harus repot ke catatan sipil mengganti nama KTP. Cukup temukan 'Asma' penyeimbang (*Falak Ruhani*) dan jadikan itu sebagai jangkar (*Anchor*) vibrasi baru di saat Anda sedang butuh mengambil keputusan fatal.
        """)
        
    with st.expander("⚡ 3. Lone Wolf Syndrome: Ilusi Mematikan dari Kata 'Mandiri'"):
        st.markdown("""
        Di era modern yang mengagungkan konsep *hustle-culture*, menjadi manusia serba bisa (Super-Soloist) sering dianggap keren. Anda memaksa belajar *copywriting* sendiri, membangun web sendiri, merancang produk sendiri, dan menjualnya sendiri. 
        
        Sayangnya, sikap yang terlihat seperti "Mandiri" ini seringkali hanyalah kedok yang digunakan ego untuk menutupi *Mental Block* yang jauh lebih dalam: **Insecurity dan Gengsi Meminta Tolong (Ego Supremacy).**
        
        Hukum tarik-menarik rezeki sangat jelas: Semesta mendistribusikan energi kelimpahannya melalui *tangan orang lain* (kolaborasi & delegasi). Jika Anda terus mengunci pintu dari bantuan orang lain karena merasa "lebih aman dan sempurna" jika dikerjakan sendiri, bersiaplah menghadapi mesin saraf yang cepat hancur akibat lelah mental (*Burnout*). Uang tidak masuk kepada mereka yang kelelahan, melainkan kepada mereka yang memiliki sistem yang efisien.
        """)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 4: FAQ & DISCLAIMER (LEGALITY)
# ==========================================
with tab4:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("❓ Parameter Sistem & Kebijakan Hak Cipta")
    
    with st.expander("🤔 1. Apa dasar algoritma dari Neuro Nada OS ini?"): 
        st.write("Sistem Neuro Nada OS adalah entitas *cyber-esoteric* independen. Platform ini memadukan kalkulasi numerologi purba (Gematria Arab/Hisab Jummal), siklus kalender pasaran Nusantara (Primbon Betaljemur Adammakna), yang dikalibrasi ulang dengan *profiling* psikologi modern berbasis *Neuro-Linguistic Programming* (NLP). Kami tidak meramal kejadian masa depan secara klenik, melainkan memetakan kecenderungan pola pikir (Meta-Program) di alam bawah sadar agar Anda bisa mengambil alih kemudi keputusan hidup Anda (Fate Hacking).")
        
    with st.expander("🤔 2. Kenapa terkadang hasilnya terkesan kasar atau menakutkan?"): 
        st.write("Algoritma ini didesain murni objektif. Sistem tidak dibuat untuk menyenangkan hati Anda (No Sugar-Coating). Fungsi utama mesin ini adalah membongkar *Blind Spot* (Titik Buta) dan kelemahan ego (Shadow) yang selama ini menghalangi Anda dari kelimpahan hidup. Pertumbuhan hanya terjadi saat kebenaran dihadapkan secara telanjang.")
        
    with st.expander("🤔 3. Apakah kalkulasi 'Naga Dina' dan 'Arah Hadap' itu mutlak?"): 
        st.write("Di dalam esoterik tradisional, hukum *Naga Dina* bertindak sebagai referensi geomansi (penyelarasan energi magnetik lokasi). Mengikuti rekomendasi arah dipercaya membantu memecah stagnasi energi ruang saat Anda mengambil keputusan bisnis/sosial. Namun, eksekusi dan tindakan logis Anda tetap memegang porsi 90% dari hasil keberhasilan.")
    
    st.markdown("<hr style='border-top: 1px dashed #555;'>", unsafe_allow_html=True)
    
    st.error("""**⚠️ DISCLAIMER LEGAL & ETIKA (HARAP DIBACA):**
Seluruh laporan hasil analisis (*Decoding*), prediksi rotasi planet, dan saran protokol terapi di platform **Neuro Nada Academy** disediakan semata-mata sebagai alat bantu pemicu kesadaran diri (*Self-Awareness Tool*), referensi kalibrasi mental, dan media eksperimental hiburan psikologis. 

Platform ini beserta *developer* (Coach Ahmad Septian) **BUKAN** merupakan penyedia layanan saran investasi finansial yang berlisensi, diagnosa medis, maupun jasa psikiatri/psikologi klinis absolut. 

Setiap langkah, eksekusi finansial, tindakan hubungan asmara, maupun perubahan rutinitas fisik yang Anda ambil berdasarkan keluaran aplikasi ini merupakan tanggung jawab rasional dan kehendak bebas (*Free Will*) Anda sepenuhnya. Pengembang tidak memikul tanggung jawab hukum atas kerugian materil maupun immaterial yang timbul dari interpretasi pengguna terhadap algoritma *software* ini.""")
    st.markdown("</div>", unsafe_allow_html=True)
 
# ==========================================
# SOCIAL PROOF
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Transformasi Kalibrasi Ego</h3>", unsafe_allow_html=True)
daftar_ulasan = ambil_ulasan()
if daftar_ulasan:
    marquee_content = " | ".join([f"<span style='color: #FFD700;'>{u.get('Rating', '⭐⭐⭐⭐⭐')}</span> <b>{u.get('Nama', 'User')}:</b> \"{u.get('Komentar', '')[:50]}...\"" for u in daftar_ulasan[:3]])
    st.markdown(f'<div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;"><marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">{marquee_content}</marquee></div>', unsafe_allow_html=True)
    for u in daftar_ulasan[:5]:
        if u.get("Komentar", ""): st.markdown(f'<div class="ulasan-box"><span style="color: #FFD700; font-size: 12px;">{u.get("Rating", "⭐⭐⭐⭐⭐")}</span><br><b>{u.get("Nama", "Entitas")}</b><br><i style="color: #ccc;">"{u.get("Komentar", "")}"</i></div>', unsafe_allow_html=True)

with st.expander("💬 Tinggalkan Testimoni Sinkronisasi Anda"):
    with st.form("form_review"):
        rn, rr, rk = st.text_input("Nama Penyamaran / Asli"), st.radio("Kalibrasi Energi", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"], horizontal=True), st.text_area("Deskripsi Dampak")
        if st.form_submit_button("Suntikkan Testimoni ke Sistem") and rn and rk:
            if kirim_ulasan(rn, rr, rk): 
                st.toast("Jejak energi ulasan Anda berhasil masuk ke *database* utama. Terima kasih!", icon="✨")
                time.sleep(1)
                st.rerun()
 
st.markdown("---")
st.markdown("<center><b style='color:#FFF; letter-spacing:1px;'>Ahmad Septian Dwi Cahyo</b><br><small style='color:#888;'>Certified NLP Trainer & Professional Hypnotherapist<br>Hak Cipta © 2026 Neuro Nada Academy (Ultimate Build)</small></center>", unsafe_allow_html=True)
