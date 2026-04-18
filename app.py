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

# --- DATABASE EMAIL PREMIUM (POIN 1: PENGGANTI KODE "NEUROVIP") ---
# Lu bisa masukin email klien yang udah bayar ke dalam list ini secara manual, 
# atau nantinya di-connect ke Google Sheets.
VIP_EMAILS = [
    "neurovip@gmail.com", 
    "ahmad@neuronada.com",
    "klien1@gmail.com"
]

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
    .ulasan-box { background: rgba(30, 30, 30, 0.6); backdrop-filter: blur(10px); padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700; margin-bottom: 12px; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .glass-container { background: rgba(25, 25, 25, 0.5); backdrop-filter: blur(12px); padding: 20px; border-radius: 12px; border: 1px solid rgba(212,175,55,0.2); box-shadow: 0 8px 32px 0 rgba(0,0,0,0.4); margin-bottom: 15px; }
    .primbon-box { background: linear-gradient(135deg, rgba(43,27,5,0.8) 0%, rgba(74,48,0,0.8) 100%); backdrop-filter: blur(10px); padding: 25px; border-radius: 12px; border: 1px solid #D4AF37; box-shadow: 0 8px 25px rgba(212,175,55,0.3); margin-top: 20px; margin-bottom: 20px; }
    .dynamic-reading-box { background: rgba(20, 20, 20, 0.7); backdrop-filter: blur(5px); padding: 20px; border-radius: 12px; border-left: 5px solid #FFD700; margin-top: 15px; margin-bottom: 15px; font-size: 15px; line-height: 1.6; }
    .matrix-container { display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; padding: 15px; background: rgba(10,10,10,0.8); border-radius: 10px; border: 1px solid #333; margin-bottom: 5px; box-shadow: inset 0 2px 15px rgba(0,0,0,0.6); }
    .matrix-item { flex: 1; min-width: 80px; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 18px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }
    .list-punchy { padding-left: 20px; margin-bottom: 15px; font-size: 15px; }
    .list-punchy li { margin-bottom: 8px; }
    .live-badge { background: linear-gradient(90deg, #D4AF37, #FFD700); color: #000; padding: 8px 20px; border-radius: 30px; font-weight: 900; font-size: 14px; letter-spacing: 1px; display: inline-block; box-shadow: 0 4px 15px rgba(255,215,0,0.4); }
    .info-metric-box { background: rgba(255,215,0,0.05); border: 1px solid rgba(255,215,0,0.2); padding: 15px; border-radius: 8px; font-size: 14px; color: #ccc; margin-bottom: 20px; line-height: 1.6; }
    </style>""", unsafe_allow_html=True
)

def get_dynamic_count():
    start_date = datetime.date(2026, 4, 15) 
    today = datetime.date.today()
    delta = (today - start_date).days
    return f"{1287 + (max(0, delta) * 5):,}".replace(",", ".")

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

URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            return [row for row in csv.DictReader(io.StringIO(response.read().decode('utf-8')))][::-1]
    except: return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        urllib.request.urlopen(urllib.request.Request(URL_POST, data=data))
        return True
    except: return False

def generate_seed(base_str): return int(hashlib.md5(base_str.encode('utf-8')).hexdigest(), 16) % (10**8)
def get_safe_firstname(name_str, default="User"): return str(name_str).strip().split()[0].upper() if str(name_str).strip() else default

# --- TAB 5: QUANTUM ENGINE (AWAM-FRIENDLY & DEEP) ---
def proc_tactical_plan(nama, mod_harian, planet_live, planet_desc, sun_fase, sun_desc):
    random.seed(generate_seed(f"tac_{nama}_{mod_harian}_{planet_live}"))
    fase_detail = {
        0: {"nama": "🔴 FASE NADIR (Titik Terendah Baterai Mental)", "analisa": f"Sistem saraf dan gelombang otak {nama} sedang berada di titik paling lemah hari ini. Ibarat baterai gawai, mental Anda sedang di posisi 5%. Tubuh batin Anda menuntut pemulihan sistem. Memaksakan ambisi besar atau berpikir keras di jam ini rawan membuat Anda kelelahan secara berlebihan. Emosi Anda sedang sensitif.", "do": ["Pilih pekerjaan repetitif yang minim analisa (membalas email, merapikan dokumen, menghapus file tak terpakai).", "Lakukan *Deep Rest*. Tutup mata sejenak, atau lakukan peregangan badan. Biarkan otak Anda memulihkan diri."], "dont": "SANGAT DISARANKAN untuk tidak mengambil keputusan finansial besar, memulai proyek baru, atau memicu konflik hari ini. Filter logika Anda sedang tidak optimal."},
        1: {"nama": "🟢 FASE INISIASI (Percikan Api Pertama)", "analisa": f"Ini adalah momentum emas Anda, {nama}! Ada dorongan energi segar di alam bawah sadar Anda. Apapun—sekecil apapun—tindakan yang Anda mulai di jam ini memiliki daya dorong (*momentum*) 3x lipat lebih mulus dibanding hari biasa. Semesta sedang berpihak pada keberanian Anda untuk melangkah.", "do": ["Jangan berpikir terlalu panjang, segera eksekusi. Luncurkan ide yang tertunda, hubungi prospek penting, atau kirim proposal.", "Lakukan langkah pertama. Hari ini adalah tentang kemauan untuk memulai, bukan mencari kesempurnaan mutlak."], "dont": "HINDARI sifat *over-analysis* (terlalu banyak pertimbangan). Berdiam diri atau menunda pekerjaan hari ini adalah pemborosan peluang rezeki Anda."},
        2: {"nama": "🔵 FASE SINKRONISASI (Magnet Bantuan Orang Lain)", "analisa": f"Mode 'Berjuang Sendirian' {nama} sedang diturunkan frekuensinya. Energi hari ini mendesak Anda untuk sadar bahwa rezeki dan solusi masalah tidak selalu di tangan Anda sendiri, melainkan dititipkan lewat orang lain. Aura Anda sedang sangat magnetis dan mudah diterima oleh lawan bicara.", "do": ["Hubungi pihak yang biasanya sulit ditembus. Aura persuasif Anda hari ini sedang berada di titik optimal.", "Delegasikan tugas! Serahkan pekerjaan yang menghambat Anda kepada rekan kerja atau ahlinya."], "dont": "JANGAN memaksakan diri memikul segalanya sendirian (*Lone Wolf Syndrome*). Anda hanya akan kelelahan dan hasil akhirnya kurang maksimal."},
        3: {"nama": "🟡 FASE RESONANSI (Daya Tembus Kata-Kata)", "analisa": f"Sirkuit komunikasi {nama} sedang menyala terang benderang. Kata-kata yang Anda ucapkan atau tulis hari ini memiliki daya tembus yang lebih mudah diterima oleh alam bawah sadar orang yang mendengarnya.", "do": ["Ini adalah waktu terbaik untuk mempromosikan sesuatu! Buat naskah penawaran, *copywriting*, presentasi, atau tayangan langsung (*Live*).", "*Speak up*. Jika ada hal yang perlu didiskusikan secara serius dengan pasangan atau rekan, sampaikan sekarang. Mereka lebih mudah menerima sudut pandang Anda."], "dont": "SANGAT DISAYANGKAN kalau Anda memilih menutup diri hari ini. Energi persuasi positif Anda akan terbuang percuma."},
        4: {"nama": "🟤 FASE MATERIALISASI (Kunci Gembok Keuangan)", "analisa": f"Gelombang otak {nama} sedang berubah wujud menjadi sangat realistis dan penuh perhitungan. Energi hari ini murni tentang 'Pengamanan'. Semesta mendorong Anda untuk memperkuat fondasi, mengecek arus kas, dan menyelesaikan hal-hal manajerial yang penting namun sering diabaikan.", "do": ["Audit pembukuan Anda. Cek pengeluaran yang tidak perlu minggu ini. Rapikan catatan keuangan bisnis.", "Fokus selesaikan hal-hal teknis/operasional (SOP) yang mungkin terasa monoton namun krusial bagi fondasi kerja Anda."], "dont": "HINDARI spekulasi! Jangan mengambil risiko investasi tanpa data valid, dan berhati-hatilah jika meminjamkan dana hari ini. Kunci keamanan finansial Anda!"},
        5: {"nama": "🟠 FASE EKSPANSI (Dobrak Tembok Ketakutan)", "analisa": f"Adrenalin kosmik {nama} sedang memuncak! Batas ketakutan dan rasa kurang percaya diri (*Mental Block*) Anda sedang rapuh. Ini adalah jam yang tepat untuk melangkah keluar zona nyaman. Tubuh dan mental Anda sangat siap untuk menembus tantangan berat.", "do": ["Pilih 1 tindakan yang paling membuat Anda ragu minggu ini (misal: menghubungi pimpinan atau *cold calling* klien) dan kerjakan sekarang.", "Lakukan pendekatan yang unik dan berbeda dari kebiasaan Anda untuk mendobrak kebosanan pasar."], "dont": "JANGAN biarkan diri Anda diam tanpa aktivitas. Energi ekspansi ini jika tidak disalurkan bisa berbalik menjadi kecemasan atau kegelisahan yang tidak beralasan."},
        6: {"nama": "🟣 FASE ELEVASI (Tabungan Karma Baik)", "analisa": f"Radar spiritual {nama} menembus urusan materi hari ini. Anda memancarkan vibrasi penyembuh dan pengayom. Semesta meminta Anda sejenak menyeimbangkan ambisi materi dengan kembali ke 'Akar': keluarga, kepedulian sosial, dan keikhlasan batin.", "do": ["Hubungi keluarga atau pasangan, tanyakan kabarnya dari hati ke hati. Turunkan ego jika ada kesalahpahaman.", "Tarik kelimpahan melalui rasa syukur dan berbagi. Bantu sesama yang membutuhkan tanpa pamrih."], "dont": "HINDARI perdebatan keras kepala, memaksakan kehendak, atau memanipulasi situasi demi sekadar keuntungan finansial. Hukum timbal balik energi berlaku kuat hari ini."}
    }
    fd = fase_detail[mod_harian]
    buka = random.choice([
        f"Melalui pembacaan algoritma waktu lahir Anda dan posisi langit detik ini, sistem mendeteksi adanya transisi energi yang sangat signifikan pada diri Anda, **{nama}**. Panduan eksekusi Anda bergeser pada mode di bawah.", 
        f"Peringatan Taktis untuk **{nama}**! Gelombang kosmik sedang berpusat membedah sektor eksekusi Anda. Ini adalah momen krusial. Mengabaikan ritme ini dapat membuat Anda kehilangan efisiensi kerja hari ini."
    ])
    planet_murni = planet_live.split(' ')[0]
    matahari_murni = sun_fase.split(' ')[0]
    koneksi = random.choice([
        f"Diperkuat oleh tarikan energi Jam {planet_murni} yang menyelaraskan Fase {matahari_murni} di tubuh Anda, situasi ini memicu urgensi untuk mengambil tindakan terarah.", 
        f"Resonansi dari {planet_murni} yang bertemu dengan ritme sirkadian {matahari_murni} Anda, menempatkan otak bawah sadar Anda pada tingkat penyerapan yang tinggi."
    ])
    
    do_html = "".join([f"<li style='margin-bottom: 10px;'>{item}</li>" for item in random.sample(fd["do"], 2)])
    html_output = f"""<div class="live-engine-box soft-fade" style="background: rgba(20,20,25,0.9); border-left: 4px solid #00FFFF; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,255,255,0.1);">
<h4 style="color: #00FFFF; margin-top:0; letter-spacing: 1px; font-weight:900;">⚡ TACTICAL ACTION PLAN <span style="font-size:12px; color:#ff4b4b; font-weight:normal;">(⏳ Valid 24 Jam)</span></h4>
<p style="color: #ccc; font-size: 15px; line-height: 1.7; margin-bottom:20px;">
{buka}<br><br>
<b style="color:#FFF; font-size:16px;">STATUS MESIN MENTAL ANDA: <span style="color:#FFD700;">{fd['nama']}</span></b><br>
<span style="color:#e0e0e0;">{fd['analisa']}</span><br><br>
<i style="color:#888;">Sinkronisasi Kosmik:</i> {koneksi} ({planet_desc})
</p>
<div style="background: rgba(37,211,102,0.1); border: 1px solid rgba(37,211,102,0.4); padding: 18px; border-radius: 8px; margin-bottom: 15px;">
<b style="color: #25D366; font-size:15px; letter-spacing:1px;">🎯 PROTOKOL EKSEKUSI (SANGAT DISARANKAN HARI INI):</b>
<ul style="color: #e0e0e0; font-size: 15px; margin-top: 10px; margin-bottom: 0; padding-left: 20px; line-height:1.6;">
{do_html}
</ul>
</div>
<div style="background: rgba(255,75,75,0.1); border: 1px solid rgba(255,75,75,0.4); padding: 18px; border-radius: 8px;">
<b style="color: #ff4b4b; font-size:15px; letter-spacing:1px;">🛑 ZONA RAWAN (PANTANGAN UTAMA):</b><br>
<span style="color: #e0e0e0; font-size: 15px; display:inline-block; margin-top:8px; line-height:1.6;">{fd['dont']}</span>
</div>
<p style="font-size:13px; color:#ff4b4b; margin-top:15px; font-weight:bold; text-align:center;">⏳ Sistem mendeteksi fluktuasi energi konstan. Manfaatkan peluang tindakan ini sebelum pergantian fase!</p>
</div>"""
    return fd['nama'].split('(')[0].strip(), html_output

# --- TAB 3: FALAK RUHANI (AWAM-FRIENDLY) ---
def proc_falak_ruhani(total_jummal, root_num, nama):
    ruhani_data = {
        1: {"asma": "Ya Fattah (Maha Pembuka)", "vibrasi": "Mendobrak Jalan Buntu & Ego Berlebihan", "tujuan": "Asma ini beresonansi untuk membuka jalan yang dirasa buntu. Fungsinya membantu melepaskan hambatan kesombongan, sifat keras kepala, atau gengsi yang menahan Anda dari menerima kemudahan rezeki."},
        2: {"asma": "Ya Salam (Maha Sejahtera)", "vibrasi": "Membangun Perisai Ketenangan Batin", "tujuan": "Asma ini bertindak sebagai perisai mental. Membantu menetralisir frekuensi negatif dari lingkungan yang tidak sehat, serta meredakan beban hati akibat terlalu sering memendam perasaan demi menjaga harmoni."},
        3: {"asma": "Ya Mushawwir (Maha Pembentuk)", "vibrasi": "Menarik Ide Menjadi Wujud Nyata", "tujuan": "Khusus bagi yang sering mengalami *overthinking*. Energi Asma ini mengarahkan gagasan Anda ke tindakan nyata, mengurangi kecenderungan menunda, sehingga rencana Anda dapat terealisasi menjadi hasil fisik."},
        4: {"asma": "Ya Muqit (Maha Pemberi Kecukupan)", "vibrasi": "Membongkar 'Mental Kekurangan'", "tujuan": "Resep untuk merilis rasa takut akan kekurangan (*Scarcity Mindset*). Asma ini membantu menanamkan rasa aman yang utuh, dan memancing stabilitas finansial melalui keyakinan bahwa kelimpahan selalu tersedia."},
        5: {"asma": "Ya Basith (Maha Melapangkan)", "vibrasi": "Memperluas Kapasitas Penerimaan Diri", "tujuan": "Membuka sekat-sekat batasan dalam diri. Asma ini bekerja melapangkan perasaan terkekang, mengurangi rasa jenuh terhadap rutinitas, dan menyiapkan kesiapan mental Anda untuk menerima tanggung jawab kesuksesan yang lebih besar."},
        6: {"asma": "Ya Wadud (Maha Mengasihi)", "vibrasi": "Membangkitkan Daya Tarik & Kasih Sayang", "tujuan": "Berfokus pada penyembuhan luka batin. Saat hati Anda pulih, Asma ini membantu memancarkan energi kehangatan dan rasa hormat, yang secara otomatis menarik kepercayaan dan kasih sayang dari relasi di sekitar Anda."},
        7: {"asma": "Ya Batin (Maha Tersembunyi)", "vibrasi": "Menajamkan Mata Batin & Intuisi", "tujuan": "Asma ini berfungsi menjernihkan radar intuisi Anda. Sangat membantu dalam mempertajam kepekaan membaca bahasa tubuh dan niat sesungguhnya dari orang lain, menjauhkan Anda dari potensi penipuan dalam hubungan atau bisnis."},
        8: {"asma": "Ya Ghaniy (Maha Kaya)", "vibrasi": "Menyelaraskan Integritas & Otoritas", "tujuan": "Bagi mereka yang ditakdirkan mengejar pencapaian tinggi. Asma ini menyelaraskan mental Anda dengan frekuensi kelimpahan murni, sekaligus menjaga hati agar tetap berpijak pada kebijaksanaan dan jauh dari keserakahan."},
        9: {"asma": "Ya Hakim (Maha Bijaksana)", "vibrasi": "Pencerahan & Pelepasan Beban Masa Lalu", "tujuan": "Berfungsi sebagai sarana pembersih residu batin. Membantu melepaskan rasa bersalah yang diam-diam menahan laju diri Anda, mengurangi ekspektasi berlebih pada orang lain, dan menyelaraskan langkah Anda dengan tujuan yang lebih mulia."}
    }
    data = ruhani_data.get(root_num, ruhani_data[1])
    return data["asma"], data["vibrasi"], data["tujuan"], total_jummal

def get_protokol_terapi(root_num, nama):
    random.seed(generate_seed(f"pt_deep_{nama}_{root_num}"))
    b1 = random.choice([
        f"**Sikap Mandiri Berlebihan (Ego Penolakan):** Otak bawah sadar Anda ({nama}) terprogram untuk merasa 'semua harus dikerjakan sendiri agar sempurna'. Namun, kebiasaan memikul beban ini rawan membuat Anda kelelahan parah dan menutup peluang kolaborasi yang membawa rezeki.", 
        f"**Kebutuhan Mengontrol (Control Freak):** Anda ({nama}) memiliki ketakutan terpendam untuk menyerahkan kendali kepada orang lain. Akibatnya, Anda menanggung porsi kerja yang melampaui kapasitas wajar. Kesuksesan terhambat karena energi fisik Anda memiliki batasan."
    ])
    a1 = random.choice([
        f"Saya, {nama}, dengan ikhlas menurunkan perisai ego saya malam ini. Saya menyadari bahwa mendelegasikan tugas adalah langkah cerdas, bukan tanda kelemahan. Saya mengizinkan kemudahan masuk ke dalam hidup saya.", 
        f"Mulai saat ini, saya ({nama}) berhenti memforsir diri melebihi batas. Saya layak mendapat dukungan. Saya layak beristirahat. Semesta memiliki banyak cara untuk mempermudah langkah saya."
    ])
    h1 = random.choice(["Temukan 1 tugas hari ini yang BISA Anda kerjakan sendiri, namun dengan sengaja **mintalah bantuan** rekan/pasangan untuk menyelesaikannya. Latih diri Anda untuk menerima kebaikan orang lain.", "Hubungi seorang mentor atau pihak yang kompeten hari ini. Sampaikan kendala teknis Anda dan dengarkan masukannya dengan hati terbuka tanpa sikap defensif."])

    b2 = random.choice([
        f"**Sindrom Mengalah (People Pleaser):** Ini adalah titik rawan Anda, {nama}. Anda cenderung menyerap beban orang lain dan mengorbankan batas toleransi diri Anda sendiri hanya untuk menjaga perasaan pihak yang terkadang kurang menghargai Anda.", 
        f"**Kekhawatiran Tidak Diterima:** Langkah {nama} sering tertahan karena Anda mendahulukan kepentingan orang lain karena takut dijauhi. Anda lupa, melindungi kewarasan diri sendiri adalah prioritas yang tidak boleh dikompromikan."
    ])
    a2 = random.choice([
        f"Saya, {nama}, memegang kendali penuh atas energi kedamaian saya. Kesejahteraan batin saya adalah prioritas utama. Mulai saat ini, saya berhak menolak hal yang menguras energi tanpa merasa bersalah.", 
        f"Saya ({nama}) dengan sadar melepaskan keharusan membahagiakan semua orang. Saya menolak menjadi penampung keluh kesah negatif. Menyatakan 'TIDAK' adalah hak saya."
    ])
    h2 = random.choice(["Latih Ketegasan Diri: Berlatihlah menyampaikan penolakan yang sopan namun tegas ('Maaf, saya sedang tidak bisa') pada satu permintaan yang memberatkan hari ini.", "Detoksifikasi Energi: Senyapkan notifikasi dari grup atau individu yang kerap mengeluh dan membawa energi negatif selama 24 jam ke depan."])

    b3 = random.choice([f"**Fokus yang Terpecah:** Otak Anda ({nama}) sangat brilian dalam memproduksi ide, namun eksekusinya kerap terhenti di tengah jalan. Anda cepat bosan dan mudah terdistraksi proyek baru sebelum yang lama memberikan hasil nyata.", f"**Antusiasme Sesaat:** Anda ({nama}) sangat bersemangat di tahap awal sebuah ide. Namun ketika memasuki fase teknis yang menuntut konsistensi, dorongan Anda meredup dan mencari pelarian ke inspirasi lain. Ini adalah bentuk sabotase diri."])
    a3 = random.choice([f"Saya, {nama}, mengarahkan pikiran saya untuk lebih fokus dan membumi. Saya menyadari, satu karya yang diselesaikan dengan tuntas jauh lebih bernilai daripada ribuan ide yang hanya sebatas wacana.", f"Fokus saya tajam dan terarah. Saya ({nama}) berkomitmen untuk menahan rasa jenuh dan menyelesaikan tanggung jawab yang telah saya mulai hingga tuntas 100%."])
    h3 = random.choice(["Gunakan Teknik Blok Waktu. Pilih 1 pekerjaan utama, atur pengingat selama 20 menit, dan paksa diri Anda fokus bekerja tanpa membuka media sosial hingga waktu habis.", "Tertibkan Lingkungan: Pikiran yang kusut sering bermula dari meja kerja yang berantakan. Rapikan area kerja atau bersihkan file tidak terpakai di perangkat Anda hari ini."])

    b4 = random.choice([f"**Mentalitas Kekurangan (Scarcity Mindset):** Di alam bawah sadar {nama}, terdapat rasa cemas berlebih terhadap kondisi finansial di masa depan. Kecemasan ini membuat Anda terlalu menahan diri dan melewatkan banyak peluang berharga untuk bertumbuh.", f"**Terperangkap di Zona Aman:** Anda ({nama}) cenderung menghindari risiko dengan dalih 'berjaga-jaga atas kemungkinan buruk'. Secara hukum ketertarikan, fokus berlebih pada skenario buruk justru menghambat datangnya energi kelimpahan."])
    a4 = random.choice([f"Saya, {nama}, hari ini melepaskan rasa cemas akan kekurangan. Saya percaya bahwa rezeki dan jalan keluar selalu tersedia di alam semesta. Kondisi saya aman, dan kelimpahan sedang mengalir menuju saya.", f"Saya ({nama}) mengizinkan diri saya menikmati hasil kerja keras dengan wajar. Kelimpahan adalah energi positif, dan saya menyambut kehadirannya dengan penuh syukur."])
    h4 = random.choice(["Praktik Melepaskan Keterikatan: Belikan satu hal yang berkualitas untuk menghargai diri Anda sendiri hari ini. Saat membayar, lepaskan rasa berat hati dan sadari bahwa Anda pantas mendapatkannya.", "Pecah Kebekuan Finansial: Lakukan tindakan berbagi/donasi secara spontan hari ini tanpa banyak perhitungan. Niatkan untuk melonggarkan ikatan kecemasan dalam batin Anda."])

    b5 = random.choice([f"**Kecenderungan Menghindari (Escapism):** Saat dihadapkan pada komitmen atau rutinitas panjang yang menuntut pertanggungjawaban, sistem saraf {nama} bereaksi defensif. Anda memiliki dorongan terpendam untuk menghindar dan mencari 'kebebasan' sesaat.", f"**Penolakan pada Rutinitas Stabil:** Kunci kemajuan Anda tertunda karena Anda ({nama}) rentan terhadap rasa jenuh. Ketika sebuah proyek atau hubungan memasuki fase stabil, Anda justru cenderung mencari distraksi baru yang merusak fokus."])
    a5 = random.choice([f"Saya, {nama}, menyadari bahwa pencapaian besar lahir dari ketahanan menghadapi rutinitas. Kedisiplinan bukanlah sesuatu yang mengekang, melainkan fondasi kokoh untuk mencapai visi besar saya.", f"Saya ({nama}) memegang kendali atas rasa bosan yang muncul di benak saya. Saya berdamai dengan proses yang repetitif demi hasil yang luar biasa."])
    h5 = random.choice(["Pilih SATU tugas penting yang terasa monoton dan sering Anda tunda. Paksa diri Anda duduk fokus dan tuntaskan pekerjaan tersebut hari ini juga tanpa alasan.", "Praktik Repetisi Terstruktur: Buatlah satu kebiasaan kecil di pagi hari. Lakukan secara konsisten dan identik selama 3 hari berturut-turut untuk melatih otot komitmen Anda."])

    b6 = random.choice([f"**Sindrom Penyelamat (Savior Complex):** Anda ({nama}) kerap merasa bersalah jika menikmati kenyamanan hidup sementara ada kenalan yang sedang kesulitan. Anda cenderung mengorbankan kesejahteraan pribadi untuk menanggung beban pihak lain.", f"**Pengorbanan yang Menguras Hati:** Anda ({nama}) memberikan terlalu banyak waktu dan empati kepada pihak luar, namun sering merasa hampa karena perhatian tersebut kurang mendapat timbal balik yang setimpal saat Anda sedang membutuhkan dukungan."])
    a6 = random.choice([f"Saya, {nama}, dengan penuh kesadaran mengutamakan kesejahteraan diri saya terlebih dahulu. Saya harus memastikan tangki energi saya penuh sebelum berusaha membantu orang lain. Merawat diri adalah prioritas suci.", f"Saya ({nama}) melepaskan peran sebagai penyelamat bagi semua orang. Saya berhak menikmati pencapaian dan kebahagiaan dari hasil jerih payah saya tanpa rasa bersalah sedikit pun."])
    h6 = random.choice(["Batas Waktu Pribadi: Sisihkan waktu minimal 45 menit hari ini khusus untuk diri sendiri ('Me-Time'). Jauhkan perangkat komunikasi dan lakukan hal yang membuat Anda rileks tanpa memikirkan masalah orang lain.", "Hargai Diri Sendiri: Pesan atau masak makanan istimewa khusus untuk Anda nikmati hari ini. Luangkan waktu untuk bersantai dan sadari bahwa Anda sangat berharga."])

    b7 = random.choice([f"**Kelumpuhan Analisa (Paralysis by Analysis):** Ketajaman logika {nama} kerap berbalik membebani diri sendiri. Anda terlalu dalam menganalisa setiap skenario risiko hingga akhirnya Anda kehilangan momentum untuk mengambil tindakan nyata.", f"**Hambatan Kepercayaan:** Pengalaman kurang menyenangkan di masa lalu membuat {nama} memasang filter kecurigaan yang tebal. Anda rentan menolak niat baik atau peluang kolaborasi positif karena prasangka yang belum tentu benar."])
    a7 = random.choice([f"Saya, {nama}, melepaskan keharusan untuk memastikan segala sesuatu secara absolut sebelum melangkah. Saya membiarkan diri saya berproses, yakin bahwa saya memiliki kemampuan untuk mengatasi tantangan yang muncul di depan.", f"Saya ({nama}) berdamai dengan masa lalu. Saya membuka diri pada peluang baru dan meyakini bahwa tidak semua pengalaman akan mengulang kekecewaan yang sama."])
    h7 = random.choice(["Jeda Keheningan: Ambil waktu duduk tenang tanpa interupsi gawai selama 15 menit. Biarkan pikiran Anda mengalir tanpa berusaha menganalisa atau menilainya.", "Latih Keterbukaan Hati: Hari ini, terimalah satu apresiasi atau bentuk kerja sama dari seseorang dengan lapang dada tanpa perlu mencari-cari motif tersembunyi."])

    b8 = random.choice([f"**Dorongan Kendali Berlebih:** Di balik kewibawaan {nama}, terdapat tekanan internal untuk selalu tampil sempurna dan memegang kontrol. Anda memforsir diri dan lingkungan sekitar secara ketat demi memenuhi standar target pencapaian Anda.", f"**Keletihan Mengejar Ambisi:** Naluri kemajuan {nama} sangat luar biasa. Namun, orientasi pada target yang tanpa henti ini secara perlahan mulai mengorbankan kualitas kedamaian pikiran dan keseimbangan hidup Anda."])
    a8 = random.choice([f"Saya, {nama}, menyadari bahwa kekuatan sejati juga terletak pada kemampuan untuk berserah. Saya mengizinkan diri saya melepaskan kendali atas hal-hal yang di luar batasan kewenangan saya.", f"Saya ({nama}) mengendurkan intensitas ambisi yang terlalu mengikat. Saya yakin bahwa rezeki dan kemajuan akan mengalir dengan lebih lancar saat batin saya berada dalam kondisi tenang."])
    h8 = random.choice(["Praktik Mendelegasikan Wewenang: Hari ini, berikan ruang bagi tim, rekan, atau keluarga untuk mengambil suatu keputusan operasional. Apapun hasilnya, tahan diri Anda untuk tidak mengintervensi berlebihan.", "Batas Tuntas Aktivitas: Tentukan jam berhenti bekerja yang tegas hari ini (misal pukul 17:00). Setelahnya, alihkan fokus sepenuhnya dari urusan pekerjaan demi pemulihan mental Anda."])

    b9 = random.choice([f"**Empati Tanpa Batas:** Toleransi {nama} seringkali terlalu tinggi. Anda cenderung memberikan pemakluman dan kesempatan berulang kali kepada individu yang jelas-jelas memberikan dampak negatif pada hidup Anda.", f"**Kekecewaan pada Realita:** Anda ({nama}) memandang kehidupan dengan idealisme moral yang tinggi. Saat realitas sosial tidak sejalan dengan ekspektasi luhur Anda, Anda rentan mengalami kelelahan empati dan kekecewaan mendalam."])
    a9 = random.choice([f"Saya, {nama}, menyadari bahwa tanggung jawab saya bukan untuk memikul ekspektasi dan kesalahan semua orang. Saya melepaskan pihak-pihak tersebut untuk belajar dari proses mereka sendiri.", f"Energi kepedulian saya ({nama}) sangat berharga. Saya akan menyalurkannya dengan lebih bijak. Saya tegas menjaga jarak dari hal-hal yang merugikan ketenangan jiwa saya."])
    h9 = random.choice(["Puasa Informasi Negatif: Kurangi secara drastis konsumsi berita yang memicu amarah atau keluhan di media sosial selama 24 jam ke depan. Lindungi ruang pikiran Anda.", "Sikap Menahan Diri: Sepanjang hari ini, latih diri Anda untuk lebih banyak mendengar. Tahan keinginan untuk memberikan solusi atau nasihat kecuali jika pihak tersebut benar-benar memintanya secara langsung."])

    protokol = {1: {"block": b1, "afirmasi": a1, "habit": h1}, 2: {"block": b2, "afirmasi": a2, "habit": h2}, 3: {"block": b3, "afirmasi": a3, "habit": h3}, 4: {"block": b4, "afirmasi": a4, "habit": h4}, 5: {"block": b5, "afirmasi": a5, "habit": h5}, 6: {"block": b6, "afirmasi": a6, "habit": h6}, 7: {"block": b7, "afirmasi": a7, "habit": h7}, 8: {"block": b8, "afirmasi": a8, "habit": h8}, 9: {"block": b9, "afirmasi": a9, "habit": h9}}
    return protokol.get(root_num, protokol[1])

def proc_shadow_list(nama, angka):
    random.seed(generate_seed(f"shd_deep_{nama}_{angka}"))
    semua_shadow = {
        1: ["**Ego Kemandirian Ekstrem:** Anda lebih memilih menanggung kesulitan sendirian daripada harus meminta bantuan. Beban yang ditahan terus-menerus ini sangat rawan menyebabkan kelelahan fisik dan mental (*burnout*).", "**Sikap Terlalu Perfeksionis:** Anda kerap menunda peluncuran karya atau keputusan karena terlalu fokus mencari detail yang kurang sempurna, sehingga sering kehilangan momentum emas.", "**Mengabaikan Sinyal Tubuh:** Ambisi yang kuat kerap mematikan sinyal lelah dari sistem saraf Anda. Anda memaksakan diri bekerja hingga melebihi ambang batas kewajaran kesehatan."],
        2: ["**Mengorbankan Diri (People Pleaser):** Anda secara rutin menekan keinginan dan kebahagiaan pribadi demi menjaga perasaan orang lain, yang belum tentu menghargai pengorbanan tersebut.", "**Menyerap Energi Negatif:** Tingkat empati Anda membuat Anda rentan menyerap keluh kesah dan aura negatif dari lingkungan, yang pada akhirnya merusak kestabilan *mood* Anda sendiri.", "**Menyimpan Kecewa Rapat-rapat:** Terlalu banyak memendam rasa kecewa demi menghindari konflik. Saat batas kesabaran habis, hal sepele bisa memicu luapan emosi yang merusak hubungan."],
        3: ["**Menyembunyikan Keresahan:** Anda terampil menutupi kegelisahan dan rasa kurang percaya diri dengan menampilkan persona yang ceria, santai, dan banyak bicara di depan publik.", "**Fokus yang Mudah Beralih:** Daya cipta ide Anda sangat tinggi, namun mudah dilanda kebosanan. Seringkali proyek belum tuntas, Anda sudah beralih pada hal baru yang tampak lebih menarik.", "**Reaksi Verbal yang Tajam:** Saat ego Anda merasa terancam, Anda refleks melontarkan kritik atau komentar sarkas yang sangat tajam dan membekas di hati lawan bicara."],
        4: ["**Terjebak di Zona Nyaman:** Ketakutan bawah sadar terhadap kegagalan membuat Anda enggan mengambil risiko. Anda lebih memilih rutinitas aman meskipun hal itu menutup pintu peluang yang lebih besar.", "**Kecenderungan Mengatur Detail (Micro-managing):** Rasa cemas terhadap ketidaksempurnaan membuat Anda sering mencampuri cara kerja orang lain, menciptakan suasana yang kaku dan tegang.", "**Meredam Emosi Secara Ekstrem:** Saat menghadapi situasi krisis, Anda sering menutup akses emosi dan tampil sangat rasional atau terkesan dingin demi mempertahankan kendali logika."],
        5: ["**Kecenderungan Menghindar (Escapism):** Terdapat rasa enggan terhadap komitmen jangka panjang. Anda sering merasa dorongan kuat untuk menghindar saat sebuah proyek atau hubungan menuntut stabilitas tinggi.", "**Kehilangan Minat pada Rutinitas:** Otak Anda membutuhkan stimulasi hal baru. Menghadapi proses repetitif membuat saraf Anda cepat jenuh dan berpotensi mensabotase konsistensi kerja Anda.", "**Antusiasme yang Cepat Pudar:** Semangat Anda sangat membara di fase awal, namun ketika rutinitas menuntut kebosanan, Anda cenderung melepaskan proyek tersebut di tengah jalan."],
        6: ["**Sindrom Penyelamat (Savior Complex):** Anda menguras terlalu banyak tenaga, uang, dan waktu untuk menyelesaikan masalah orang lain, hingga Anda melupakan pentingnya memprioritaskan kesejahteraan diri sendiri.", "**Terbelenggu Rasa Bersalah:** Anda sulit menikmati hasil jerih payah atau waktu istirahat yang berkualitas, karena pikiran Anda selalu terbebani oleh kondisi orang lain yang kurang beruntung.", "**Ekspektasi Timbal Balik Batin:** Meskipun Anda tulus berkorban, jauh di lubuk hati terdapat kekecewaan yang mendalam jika upaya besar Anda diabaikan atau tidak mendapat apresiasi yang layak."],
        7: ["**Hambatan Berpikir Terlalu Jauh (Over-analyzing):** Ketajaman analisa Anda seringkali berujung pada keraguan. Anda terlalu lama memperhitungkan risiko sehingga terlambat mengambil tindakan nyata.", "**Krisis Kepercayaan (Trust Issue):** Kekhawatiran akan kekecewaan membuat Anda memasang filter keraguan yang tebal. Anda rentan menolak peluang kerja sama yang bagus karena prasangka yang belum tentu terbukti.", "**Standar Intelektual Terlalu Kaku:** Karena standar kualitas yang Anda pegang sangat tinggi, Anda kerap merasa kurang sefrekuensi dengan lingkungan sekitar, sehingga terkesan menjaga jarak."],
        8: ["**Dominasi dan Kendali Ketat:** Di balik karakter kuat Anda, terdapat keengganan untuk memperlihatkan kelemahan. Anda membangun citra tangguh yang membuat Anda kesulitan untuk rileks dan berserah diri.", "**Kesulitan Mendelegasikan Tugas:** Anda merasa ragu untuk melepaskan kendali pekerjaan kepada orang lain. Anda menuntut segala sesuatu berjalan sesuai metode spesifik Anda, yang berisiko menciptakan ketegangan.", "**Menekan Empati Demi Target:** Dalam tekanan mengejar ambisi materi, kepekaan emosional Anda sering dinonaktifkan. Penilaian Anda terhadap relasi rawan didasarkan murni pada asas keuntungan profesional semata."],
        9: ["**Pemakluman yang Merugikan Diri (Toxic Empathy):** Kesabaran Anda terlampau luas. Anda terlalu mudah memberikan kesempatan kepada individu yang sudah jelas memberikan pengaruh buruk secara berulang pada hidup Anda.", "**Kekecewaan Terhadap Realitas:** Anda memiliki standar moral yang sangat idealis. Saat menghadapi realita perilaku manusia yang oportunis, Anda mudah merasa letih secara mental dan kecewa mendalam.", "**Mengabaikan Pemenuhan Pribadi:** Terlalu fokus pada visi yang lebih besar atau pemulihan kondisi orang di sekitar Anda, membuat Anda sering kehilangan kontak dengan apa yang sebenarnya Anda butuhkan untuk bahagia hari ini."]
    }
    return random.sample(semua_shadow[angka], 3)


# --- TAB 1: IDENTITAS KOSMIK (AWAM-FRIENDLY) ---
arketipe_punchy = {
    1: {"inti": "Sang Perintis (Inisiator & Pendobrak Batasan)", "kekuatan": ["Keberanian tinggi mengambil langkah yang dihindari banyak orang", "Kemandirian mutlak (sangat efisien tanpa perlu banyak instruksi)", "Fokus pada eksekusi cepat, meminimalkan rapat atau teori yang bertele-tele"]},
    2: {"inti": "Sang Penyelaras (Negosiator & Pembaca Emosi)", "kekuatan": ["Kepekaan empati tinggi, mampu membaca dinamika situasi dengan cepat", "Piawai dalam diplomasi dan melunakkan negosiasi yang alot", "Mampu menjadi penengah konflik tanpa menimbulkan ketegangan baru"]},
    3: {"inti": "Sang Visioner (Konseptor & Komunikator Persuasif)", "kekuatan": ["Daya tarik komunikasi yang memikat (unggul dalam presentasi/pemasaran)", "Pikiran yang selalu kaya akan ide-ide segar dan solusi kreatif", "Kemampuan meyakinkan audiens dengan tata bahasa yang berkarisma"]},
    4: {"inti": "Sang Transformator (Arsitek Sistem & Pilar Fondasi)", "kekuatan": ["Pola pikir sangat terstruktur, logis, dan menyukai keteraturan operasional", "Integritas tinggi, sosok tepercaya untuk mengamankan aset atau data penting", "Ketekunan luar biasa dalam menangani detail yang sering dihindari orang lain"]},
    5: {"inti": "Sang Penggerak (Eksplorator Cepat Tanggap)", "kekuatan": ["Kelincahan berpikir sangat tajam di bawah situasi tak terduga atau krisis", "Inovator berani, kerap menemukan pendekatan baru yang belum terpikirkan pasar", "Kecepatan adaptasi yang sangat tinggi terhadap perubahan tren atau teknologi"]},
    6: {"inti": "Sang Harmonizer (Pengayom & Pilar Perlindungan)", "kekuatan": ["Insting yang sangat kuat untuk membina dan mengayomi lingkungan sekitarnya", "Memancarkan aura aman yang membuat rekan/klien mudah menaruh kepercayaan", "Rasa tanggung jawab moral yang sangat teguh dalam menuntaskan komitmen"]},
    7: {"inti": "Sang Legacy Builder (Analis Presisi & Pencari Esensi)", "kekuatan": ["Ketajaman intuisi yang peka mendeteksi ketidaksesuaian atau informasi palsu", "Kemampuan analisa mendalam, selalu memikirkan mitigasi risiko sebelum melangkah", "Menjunjung standar kualitas yang tinggi, memastikan hasil kerja selalu eksklusif"]},
    8: {"inti": "Sang Sovereign (Eksekutor Otoritatif & Magnet Kelimpahan)", "kekuatan": ["Daya tahan mental yang sangat kokoh dalam menghadapi tekanan target besar", "Insting tajam dalam memetakan peluang investasi dan pertumbuhan aset", "Kewibawaan alami yang membuat arahan Anda mudah diikuti oleh tim"]},
    9: {"inti": "Sang Kesadaran Tinggi (Pemikir Bijaksana & Berwawasan Luas)", "kekuatan": ["Kemampuan memandang situasi secara komprehensif tanpa mudah tersulut emosi", "Pemahaman mendalam pada kebutuhan sejati klien, meningkatkan kualitas relasi", "Kebijaksanaan bawaan yang sering menjadikan Anda tempat meminta pandangan strategis"]}
}

def proc_arketipe(nama, angka, zodiak, neptu):
    random.seed(generate_seed(f"hyper_ark_deep_{nama}_{angka}_{zodiak}_{neptu}"))
    buka = random.choice([
        f"Ibarat setiap sistem memiliki bahasa pemrograman dasar, pola pikir bawah sadar **{nama}** secara alami terbentuk pada **KODE {angka}** sejak awal.",
        f"Kombinasi antara garis waktu kelahiran dan karakteristik elemen {zodiak} memetakan keunggulan psikologis **{nama}** secara presisi di **KODE {angka}**."
    ])
    
    inti = {
        1: "Ini menandakan Anda memiliki motor penggerak bertipe Sang Perintis. Anda memiliki resistensi alami terhadap birokrasi yang terlalu kaku. Anda sangat menghargai otonomi, dan potensi Anda akan paling bersinar saat diberikan kebebasan penuh untuk memulai proyek atau merintis jalan baru.",
        2: "Ini berarti Anda dikaruniai karakteristik Sang Penyelaras sejati. Anda dibekali kepekaan emosional yang tinggi, mampu menyerap dinamika lingkungan dengan cepat. Kemampuan 'membaca' karakter dari bahasa non-verbal ini menjadikan Anda seorang negosiator yang sangat ulung.",
        3: "Ini menunjukkan kekuatan utama Anda terletak sebagai Komunikator yang Magnetis. Aset terbesar Anda adalah kemampuan mengartikulasikan ide. Pikiran Anda kaya akan gagasan inovatif, dan ketika disampaikan dengan tepat, pesan Anda memiliki daya tembus persuasif yang luar biasa.",
        4: "Ini berarti Anda adalah Arsitek Sistem (Sang Pembangun Fondasi). Anda menyukai kejelasan, keamanan, dan struktur. Cara berpikir Anda sangat teratur dan matematis. Fondasi perusahaan atau keluarga sangat membutuhkan stabilitas dan ketelitian tingkat tinggi seperti yang Anda miliki.",
        5: "Ini berarti Anda beroperasi dengan mode Eksplorator. Rutinitas yang monoton akan dengan cepat memadamkan semangat Anda. Ketajaman analisa dan kreativitas Anda justru akan menyala paling terang ketika Anda dihadapkan pada situasi krisis atau saat mengeksplorasi wilayah baru.",
        6: "Ini menandakan Anda membawa energi Sang Harmonizer (Pengayom). Dedikasi dan rasa tanggung jawab moral Anda sangat tinggi. Secara insting, Anda akan selalu berusaha memastikan keamanan dan kesejahteraan orang-orang yang berada di dalam lingkaran kepercayaan Anda.",
        7: "Ini berarti Anda memiliki kerangka berpikir Analitik Forensik. Anda tidak akan mudah puas dengan jawaban yang dangkal. Filter rasionalitas Anda sangat rapat, memastikan setiap keputusan yang diambil selalu berbasiskan data, observasi tajam, dan pembuktian logis.",
        8: "Ini menunjukkan Anda memancarkan aura Sang Sovereign (Pemegang Kendali). Fokus alam bawah sadar Anda sangat terarah pada pencapaian, stabilitas material, dan kepemimpinan. Anda memiliki wibawa dominan yang menempatkan Anda pada posisi pengambil keputusan strategis.",
        9: "Ini berarti Anda memiliki pendekatan layaknya Pemikir Bijaksana (*Old Soul*). Anda memandang realitas kehidupan dengan sudut pandang yang lebih luas dan matang. Empati universal yang Anda miliki memudahkan Anda untuk melihat benang merah dari setiap persoalan yang kompleks."
    }
    
    shadow = {
        1: "Tantangan utamanya adalah sisi ego kemandirian Anda. Keengganan untuk meminta bantuan seringkali membuat Anda memikul beban berlebih, yang sangat rentan menyebabkan kelelahan ekstrem (*burnout*).",
        2: "Sisi yang harus diwaspadai adalah kecenderungan menomorduakan diri sendiri (People Pleasing). Menekan perasaan demi menyenangkan pihak lain lambat laun akan memicu beban stres batin yang menumpuk.",
        3: "Hal yang perlu dikelola adalah kecenderungan fokus yang terpecah. Terlalu banyak melompat dari satu ide ke ide lain berisiko membuat proyek Anda terhenti di tengah jalan tanpa hasil nyata.",
        4: "Kelemahan yang harus dihindari adalah kecenderungan *Micro-managing* (mengatur detail secara berlebih). Ketakutan akan risiko bisa membuat Anda terlalu kaku dan lambat dalam mengambil peluang penting.",
        5: "Tantangan terbesar Anda adalah menjaga komitmen jangka panjang. Seringkali ketika sebuah proses menuntut konsistensi yang stabil, dorongan impulsif untuk 'mencari hal baru' dapat mensabotase kelangsungan proyek Anda.",
        6: "Kecenderungan yang perlu dievaluasi adalah sifat pengorbanan Anda yang kadang tidak mengenal batas. Memaksakan diri membantu pihak yang tidak kooperatif hanya akan menguras energi vital Anda secara sia-sia.",
        7: "Waspadai jebakan 'Kelumpuhan Analisa' (*Paralysis by Analysis*). Terlalu banyak menimbang risiko seringkali membuat Anda kehilangan momentum bertindak, ditambah skeptisisme berlebih yang rawan menghambat kolaborasi.",
        8: "Sisi yang butuh pelembutan adalah ketakutan Anda akan hilangnya kontrol. Kesulitan untuk berserah atau mendelegasikan wewenang dapat memicu tekanan stres kronis dan sikap kaku terhadap diri sendiri maupun orang lain.",
        9: "Karena standar idealisme yang tinggi, titik rapuh Anda adalah mudah merasa letih secara emosional saat menghadapi realita. Energi kepedulian Anda harus dilindungi agar tidak terkuras oleh lingkungan yang kurang tepat."
    }
    
    return f"{buka} {inti[angka]}<br><br><span style='color:#ccc;'>{shadow[angka]}</span>"

def get_betaljemur_data(neptu):
    lk = {
        7: ("Lebu Katiup Angin (Rentan Terpecah)", "Fokus pikiran Anda cenderung mudah terdistraksi oleh faktor eksternal. Anda membutuhkan jadwal rutinitas yang terstruktur. Jika tidak, ada potensi waktu atau sumber daya Anda terbuang untuk hal yang kurang prioritas."),
        8: ("Lakuning Geni (Karakteristik Elemen Api)", "Sistem emosi Anda ibarat percikan yang mudah membesar. Di satu sisi, ambisi dan semangat kerja Anda menyala terang. Namun Anda wajib memegang kendali atas emosi dan tutur kata agar tidak merusak relasi profesional yang sudah terjalin baik."),
        9: ("Lakuning Angin (Akselerasi & Fluktuatif)", "Daya adaptasi Anda sangat gesit, namun *mood* Anda dapat berubah dengan cepat. Energi ini sangat efektif untuk penyelesaian kesepakatan (*closing*) kilat, namun kurang ideal untuk merumuskan kontrak kerja sama jangka panjang."),
        10: ("Pandito Mbangun Teki (Aura Kedalaman Analisa)", "Ketenangan berpikir mendominasi Anda. Ini adalah indikasi emas untuk selalu melakukan introspeksi, menyusun strategi secara matang, dan mempertajam analisa logika. Otak Anda mampu mengurai kerumitan masalah dengan sangat jernih."),
        11: ("Aras Tuding (Fase Terpilih)", "Aura kepemimpinan dan inisiatif aktif di dalam diri Anda. Anda akan sering berada dalam posisi di mana Anda ditunjuk—baik untuk memimpin penyelesaian masalah mendadak, maupun untuk menyambut peluang rezeki baru. Hadapi dengan rasa percaya diri!"),
        12: ("Aras Kembang (Daya Tarik Persuasif)", "Tingkat pesona dan komunikasi simpatik Anda sangat mekar. Pendapat Anda akan lebih mudah diterima dan dihormati oleh lingkungan. Ini adalah modal terbaik untuk melobi pihak penting atau membangun koneksi bernilai tinggi."),
        13: ("Lakuning Lintang (Kharisma yang Tenang)", "Anda memancarkan ketenangan yang seringkali menarik perhatian tanpa disadari, namun batin Anda cenderung menginginkan ruang privasi. Pesannya adalah: Sesekali melangkahlah keluar dari zona nyaman, karena ada peluang kolaborasi menanti Anda."),
        14: ("Lakuning Rembulan (Pembawa Harmoni)", "Kehadiran Anda bertindak sebagai penyeimbang suasana bagi lingkungan sekitar. Rekan kerja akan merasa nyaman di dekat Anda. Manfaatkan kejernihan batin ini untuk mengambil keputusan bisnis yang berlandaskan asas saling menguntungkan (*win-win*)."),
        15: ("Lakuning Srengenge (Pancaran Ketegasan)", "Aura wibawa Anda sangat kuat, logis, dan tegas. Arahan Anda sulit untuk dibantah. Manfaatkan gelombang ketegasan ini untuk mengeksekusi proyek yang tertunda atau mendisiplinkan operasional yang kurang efektif."),
        16: ("Lakuning Banyu (Kedalaman Strategi)", "Ketenangan Anda menutupi arus analisa yang sangat kuat di dalam pikiran. Anda terlihat fleksibel menghadapi orang, namun memiliki perhitungan presisi. Sangat tepat untuk melakukan observasi diam-diam sebelum mengajukan penawaran krusial di menit akhir."),
        17: ("Lakuning Bumi (Fondasi Baja Terstruktur)", "Pikiran Anda sangat realistis, gigih, dan terstruktur. Anda kurang dapat menolerir rencana tanpa dasar yang kuat. Gunakan energi ini untuk 'merapikan barisan': memverifikasi laporan keuangan, mengecek aset, dan menyempurnakan alur kerja bisnis."),
        18: ("Lakuning Paripurna (Otoritas Kematangan)", "Ini adalah fase kematangan penuh! Otoritas Anda diakui dengan rasa hormat. Peringatan etika: Karena ucapan Anda memiliki bobot yang besar, hindari melontarkan keluhan atau kalimat pesimis, dan fokuslah mengucapkan afirmasi keberhasilan.")
    }
    return lk.get(neptu,("Anomali Sistem","Pola energi tidak standar. Gunakan intuisi logis Anda dengan kehati-hatian ekstra."))[0], lk.get(neptu,("Anomali",""))[1]

def get_naga_dina(hari_eksekusi):
    nd = {"Minggu":"Timur", "Senin":"Selatan", "Selasa":"Barat", "Rabu":"Utara", "Kamis":"Timur", "Jumat":"Selatan", "Sabtu":"Selatan"}
    return nd.get(hari_eksekusi,"Netral")

def get_rezeki_usaha(neptu, tgl_hari_ini):
    angka_hari_ini = sum(int(d) for d in tgl_hari_ini.strftime("%d%m%Y"))
    dinamis_7 = (neptu + angka_hari_ini) % 7 or 7
    dinamis_5 = (neptu + angka_hari_ini) % 5 or 5
    
    r = {
        1: ("Wasesa Segara (Arus Kelimpahan Luas)", "Saluran rezeki Anda sedang dalam fase ekspansi yang sangat luas hari ini. Kejutan peluang finansial kerap muncul dari arah yang tidak diperhitungkan sebelumnya. Kunci optimalisasinya: Singkirkan keraguan, dan beranikan diri untuk mengambil langkah maju!"),
        2: ("Tunggak Semi (Regenerasi Berkelanjutan)", "Memiliki karakter pertumbuhan yang persisten. Apabila hari ini Anda menemui hambatan teknis atau penundaan kesepakatan, pertahankan ketenangan Anda. Algoritma ini menandakan bahwa setiap kerugian berpotensi memantul kembali menjadi keuntungan yang lebih mapan ke depannya."),
        3: ("Satria Wibawa (Modal Kepercayaan Tinggi)", "Fokus utama rezeki Anda hari ini bukan sekadar pada transaksi tunai instan, melainkan pada peningkatan 'Kredibilitas' (Trust) dan perluasan relasi berkualitas. Wibawa profesional adalah aset utama Anda hari ini; pertahankan standar etika dan tata bahasa Anda."),
        4: ("Sumur Sinaba (Sumber Solusi Inspiratif)", "Kapasitas energi Anda bertindak sebagai pusat rujukan hari ini. Klien atau relasi akan proaktif mencari Anda untuk meminta solusi dan perspektif. Berikan nilai tambah (*value*) terbaik Anda secara tulus, karena dari sinilah konversi kesepakatan komersial Anda akan bermula."),
        5: ("Bumi Kapetak (Panen Dedikasi Kerja)", "Fase ini menuntut dedikasi praktis tanpa kompromi. Kesuksesan finansial hari ini membutuhkan implementasi strategi jitu dan kesediaan menangani detail teknis. Kesediaan Anda untuk berkonsentrasi pada hal operasional akan memberikan imbal hasil yang sangat sepadan."),
        6: ("Satria Wirang (Fase Kalibrasi Mental)", "Peringatan stabilitas! Anda sedang memasuki zona evaluasi hari ini. Mungkin akan ada hambatan kecil atau perbedaan pandangan yang menguji kesabaran. Ini adalah proses pembentukan ketahanan mental sebelum Anda menaiki level finansial berikutnya. Tetaplah merespons dengan kepala dingin."),
        7: ("Lebu Katiup Angin (Waspada Kebocoran Kas)", "Arus keuangan Anda sedang dalam status peringatan dini hari ini. Potensi pemasukan memang ada, namun dorongan untuk melakukan pengeluaran impulsif atau konsumtif juga meningkat drastis. Segera amankan likuiditas Anda ke dalam instrumen investasi jangka panjang yang lebih aman.")
    }[dinamis_7]
    u = {
        1: ("Sandang (Sektor Kebutuhan Penunjang)", "Potensi perputaran modal paling optimal hari ini berada pada sektor komoditas pendukung, gaya hidup, mode, atau jasa yang berfokus pada perbaikan citra dan representasi pihak lain."),
        2: ("Pangan (Sektor Pemenuhan Esensial)", "Aktivitas komersial Anda hari ini memiliki resonansi kuat pada bidang kuliner, kebutuhan ritel harian, atau layanan yang bersifat memberikan 'nutrisi' seperti edukasi dan pengembangan kapasitas diri."),
        3: ("Beja (Akselerasi Keberuntungan Murni)", "Gelombang momentum Anda sangat mendukung aktivitas tingkat tinggi hari ini. Waktu yang ideal untuk melakukan kesepakatan kontrak bernilai strategis, manajemen instrumen aset, atau peluncuran layanan inovatif."),
        4: ("Lara (Zona Evaluasi Keputusan)", "Status waspada pada pengambilan keputusan tunggal. Sangat disarankan untuk tidak mengeksekusi ekspansi modal atau investasi mandiri hari ini. Anda perlu meminta pandangan tambahan (*second opinion*) dari penasihat atau pihak ketiga yang kredibel."),
        5: ("Pati (Status Penahanan Strategis)", "Disarankan untuk membekukan sementara aktivitas transaksi berisiko tinggi. Hindari spekulasi finansial murni hari ini. Salurkan energi hari ini untuk melakukan audit internal, mengevaluasi sistem kerja, atau melakukan perbaikan struktur manajemen.")
    }[dinamis_5]
    
    if dinamis_7 in [1, 3, 4]: status_warna = "#25D366"  
    elif dinamis_7 in [2, 5]: status_warna = "#FFD700" 
    else: status_warna = "#ff4b4b" 
    
    return r, u, status_warna
 
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

# --- TAB 2: COUPLE MATRIX (AWAM-FRIENDLY & DEEP) ---
def proc_penjelasan_matriks(n1, n2, eso_val, nep_val):
    random.seed(generate_seed(f"pm_v4_{n1}_{n2}_{eso_val}_{nep_val}"))
    header = random.choice(["⚙️ BEDAH MESIN NEURO-RELATIONSHIP", "📡 DEKODE SINYAL KOSMIK PASANGAN", "📜 LOGIKA ALGORITMA PENYATUAN EGO"])
    
    f_eso = random.choice([
        f"Penyatuan frekuensi dari nama <b>{n1}</b> dan <b>{n2}</b> memiliki pijakan yang jelas. Hasil perhitungannya mengunci pada Frekuensi <b>{eso_val}</b>. Angka ini mencerminkan 'Identitas Ketiga'—yakni bagaimana lingkungan luar dan relasi profesional menilai aura keselarasan saat kalian tampil berdua.", 
        f"Kombinasi energi dari sebutan nama <b>{n1}</b> dan <b>{n2}</b> bermuara pada resonansi angka <b>{eso_val}</b>. Hal ini memberikan gambaran tentang tujuan kolaborasi mendasar mengapa kalian dapat terhubung dalam dinamika yang sama."
    ])
    
    f_nep = random.choice([
        f"Perhitungan dari gravitasi kelahiran (Total Neptu <b>{nep_val}</b>) memetakan titik lemah komunikasi (*Blind Spot*) dari karakter mendasar masing-masing. Ini merupakan peta sensitivitas di mana perbedaan pandangan rawan memanas jika tidak ditangani dengan kepala dingin.", 
        f"Analisis siklus parameter waktu (Benturan Neptu <b>{nep_val}</b>) berfungsi sebagai indikator stabilitas mental hubungan. Angka ini membongkar pola tersembunyi: Bagaimana mekanisme pertahanan diri masing-masing aktif saat menghadapi tekanan atau krisis bersama."
    ])
    
    return f'<div class="info-metric-box"><b style="color:#FFD700; font-size:15px; letter-spacing:1px;">{header}:</b><br><br>• <b style="color:white;">TOTAL FREKUENSI ESOTERIK:</b><br><span style="color:#ccc; display:inline-block; margin-top:4px; margin-bottom:12px; font-size:14px;">{f_eso}</span><br>• <b style="color:white;">TOTAL BENTURAN NEPTU:</b><br><span style="color:#ccc; display:inline-block; margin-top:4px; font-size:14px;">{f_nep}</span></div>'

def proc_couple_persona(root_c, n1, n2):
    random.seed(generate_seed(f"cp_deep_{n1}_{n2}_{root_c}"))
    buka = random.choice([
        f"Pemetaan resonansi mencatat bahwa penggabungan profil psikologis **{n1}** dan **{n2}** menghasilkan gelombang **Root {root_c}**.",
        f"Ketika karakter **{n1}** disandingkan dengan pendekatan **{n2}**, sistem mendeteksi terbentuknya dinamika hubungan yang terkunci di **Root {root_c}**."
    ])
    
    # PENJELASAN FILOSOFI DASAR ROOT 1-9
    filosofi = {
        1: "Dalam numerologi esoterik, Angka 1 melambangkan Genesis (penciptaan) dan kemandirian mutlak. Ketika dua orang bersatu dan menghasilkan Root 1, entitas hubungan ini berfokus pada dorongan penaklukan dan pencapaian luar. Ini adalah energi pemimpin. Hubungan ini tidak dirancang untuk sekadar bermesraan pasif, melainkan untuk membangun 'kerajaan' bersama dan memenangkan persaingan hidup secara dominan.",
        2: "Angka 2 adalah simbol dualitas tertinggi, mewakili keseimbangan, intuisi, dan penerimaan emosional murni. Hubungan dengan Root 2 berfungsi sebagai wadah penyembuhan. Visi fundamental dari frekuensi ini adalah menciptakan kedamaian batin dan keharmonisan. Mereka berkomunikasi lebih banyak lewat perasaan non-verbal dibandingkan logika keras, menjadikannya hubungan yang sangat peka dan suportif.",
        3: "Angka 3 mewakili ekspresi daya cipta, pesona, dan magnetisme sosial. Root 3 memancarkan frekuensi yang sangat terang dan butuh panggung. Hubungan ini memiliki tujuan untuk berekspansi melalui koneksi sosial, ide-ide kreatif, dan keceriaan. Mereka adalah pasangan yang menghidupkan suasana di lingkungan mana pun mereka berada, namun harus waspada agar komitmen tidak terabaikan oleh interaksi luar yang terlalu luas.",
        4: "Angka 4 adalah arsitektur keteraturan (seperti 4 pilar kokoh penyangga gedung). Root 4 tidak menyukai angan-angan tanpa bukti. Hubungan ini menuntut struktur yang membumi, logis, dan sangat realistis. Esensi dari penyatuan ini adalah mengunci rasa aman (khususnya secara materi dan loyalitas). Ini adalah frekuensi anti-badai yang mengutamakan ketahanan jangka panjang di atas romansa sesaat.",
        5: "Angka 5 melambangkan energi kinetik, eksplorasi, dan perubahan. Root 5 menghasilkan hubungan yang tidak bisa dikekang oleh rutinitas statis. Tujuan penyatuan mereka adalah untuk memecahkan kebosanan melalui petualangan, pembelajaran hal baru, dan mengambil risiko yang terukur bersama-sama. Kebebasan ruang gerak personal adalah oksigen mutlak bagi keberhasilan hubungan ini.",
        6: "Angka 6 adalah frekuensi pengayoman, pengorbanan moral, dan kekeluargaan. Entitas Root 6 sering kali bertindak sebagai pelindung (*Sanctuary*) tidak hanya bagi mereka berdua, tapi juga bagi lingkungan sekitar. Visi utama hubungan ini adalah menciptakan 'Rumah' yang sesungguhnya—tempat di mana nilai-nilai tradisi, kesetiaan absolut, dan perlindungan emosional dijunjung tinggi.",
        7: "Angka 7 bermakna kedalaman misteri, analisis intelektual, dan pencarian esensi. Root 7 menciptakan hubungan yang sangat eksklusif dan privat. Mereka jarang mencari validasi publik atau pamer di media sosial. Koneksi mereka divalidasi lewat percakapan filosofis tingkat tinggi dan pemahaman spiritual yang tak kasat mata. Terkesan dingin dari luar, namun memiliki ikatan batin yang sangat rasional.",
        8: "Angka 8 adalah simbol *infinity*, gravitasi material, dan otoritas karmik. Root 8 adalah penyatuan beban berat sekaligus kelimpahan besar. Hubungan ini ditakdirkan untuk mengelola sumber daya, bisnis, atau manusia dalam skala yang luas. Jika ego berhasil diselaraskan menjadi satu visi integritas, kombinasi ini akan menarik perputaran finansial dan wibawa sosial secara besar-besaran.",
        9: "Angka 9 adalah puncak kematangan spiritual, penyelesaian, dan toleransi universal. Root 9 mempertemukan dua individu dengan tingkat kedewasaan batin yang tinggi. Seringkali, frekuensi ini hadir untuk saling menyembuhkan trauma masa lalu (*Healing*). Fokus utama mereka tidak lagi egois, melainkan bagaimana kolaborasi mereka bisa memberikan nilai atau dampak positif yang lebih luas bagi orang lain."
    }

    desc = {
        1: ("THE EMPIRE BUILDERS (Kekuatan Pendorong Target Besar)", f"Sinergi kalian memancarkan ketegasan yang berorientasi pada pencapaian. Saat {n1} dan {n2} berkolaborasi, fokus utamanya bukan hanya pada romantisme semata, melainkan pada eksekusi terukur untuk mengumpulkan aset, mencapai target profesional, dan meningkatkan kualitas hidup secara signifikan. Peringatan: Hindari adu dominasi; pembagian wewenang dalam hubungan harus dikelola dengan bijak."),
        2: ("THE EMPATHIC RESONANCE (Harmoni Keterikatan Batin)", f"Kalian dianugerahi tingkat empati dua arah yang sangat responsif. Cukup mudah bagi {n1} maupun {n2} untuk memahami perubahan nuansa hati pasangan hanya dari isyarat non-verbal tanpa harus banyak bertanya. Keunggulan kolaborasi ini adalah kemampuannya saling menenangkan dan meredam kecemasan mental (*anxiety*) di tengah kerasnya tantangan eksternal."),
        3: ("THE MAGNETIC CHARM (Daya Tarik Sosial Dinamis)", f"Frekuensi gabungan kalian memiliki pesona komunikasi yang kuat di ranah sosial. {n1} dan {n2} adalah tipe pasangan yang mampu menghidupkan suasana dan membawa energi positif ke dalam lingkungan pergaulan. Keluwesan komunikasi ini sangat memudahkan kalian dalam memperluas koneksi, membangun relasi bisnis, dan mendapatkan simpati dari figur penting."),
        4: ("THE ARCHITECTS OF REALITY (Struktur Fondasi Anti-Badai)", f"Hubungan ini tidak dibangun sekadar di atas janji manis sesaat, melainkan ditopang oleh perhitungan realitas jangka panjang yang matang! Pemikiran {n1} dan {n2} secara konsisten berorientasi pada keamanan masa depan, kestabilan finansial, dan kesetiaan prinsip. Krisis atau rintangan berat akan kesulitan merobohkan fondasi yang telah kalian verifikasi bersama."),
        5: ("THE QUANTUM NOMADS (Penjelajah Inovasi & Tantangan)", f"Karakteristik hubungan kalian menuntut kecepatan dan pembaruan konstan. Rutinitas statis yang berulang dapat membuat dinamika ini terasa hambar. Daya tarik antara {n1} dan {n2} akan menyala paling optimal ketika kalian bersama-sama menghadapi tantangan baru, merintis pengalaman tak terduga, dan menghindari pola konvensional yang membosankan."),
        6: ("THE SANCTUARY (Pusat Perlindungan Emosional)", f"Sinergi kalian mewakili tingkat kepedulian yang sangat mendalam. Hubungan {n1} dan {n2} bertindak layaknya pusat pemulihan (*Sanctuary*). Keterikatan ini tidak hanya menenangkan satu sama lain, namun kerabat atau kolega terdekat juga kerap datang kepada kalian untuk mencari pencerahan dan dukungan moral saat mereka menghadapi kesulitan hidup."),
        7: ("THE MYSTIC SYNERGY (Koneksi Analitis Eksklusif)", f"Dinamika hubungan kalian cenderung menjaga privasi, mendalam, dan memiliki standar percakapan filosofis yang jarang dipahami oleh lingkungan luar. {n1} dan {n2} jauh lebih menikmati waktu berdua untuk membedah konsep pemikiran atau strategi hidup dibandingkan mencari pengakuan publik atau terlalu mengumbar aktivitas di media sosial."),
        8: ("THE MATERIAL GRAVITY (Kapasitas Magnet Finansial)", f"Ini adalah sinergi dengan potensi luar biasa: Apabila manajemen ego kalian berdua berhasil diselaraskan pada visi yang sama, penyatuan {n1} dan {n2} memiliki daya dobrak finansial yang signifikan! Kemitraan ini dapat membuka peluang bisnis dan mendatangkan kepercayaan dari klien level atas. Catatan penting: Pastikan nilai materi tidak mengesampingkan rasa saling menghargai."),
        9: ("THE CONSCIOUS UNION (Pemulihan Kedewasaan Batin)", f"Tingkat penerimaan emosional kalian berada pada tahap yang sangat dewasa. {n1} dan {n2} saling terhubung dengan potensi kuat untuk saling memperbaiki trauma masa lalu atau pola pikir negatif sebelumnya. Interaksi kalian diwarnai oleh tingkat toleransi yang sangat baik. Kalian merupakan katalis pertumbuhan positif bagi satu sama lain.")
    }
    
    data = desc.get(root_c, ("UNCHARTED ANOMALY", "Entitas frekuensi tak tertebak."))
    filosofi_dasar = filosofi.get(root_c, "Anomali frekuensi terdeteksi. Silakan periksa kembali parameter yang dimasukkan.")
    return data[0], filosofi_dasar, f"{buka} {data[1]}"

def proc_weton_kombo(sisa, n1, n2, z1, z2):
    random.seed(generate_seed(f"wt_deep_{n1}_{n2}_{sisa}_{z1}_{z2}"))
    do_list = {
        1: [f"Terapkan taktik psikologi *Pacing-Leading*. Saat argumen memanas, hindari perdebatan langsung! Validasi terlebih dahulu perasaannya (misal: 'Saya mengerti perspektif kamu...'), lalu perlahan masukkan rasionalisasi dari Anda.", f"Gunakan aturan jeda (*Time-Out*). Saat intonasi suara mulai meninggi, segera ambil jeda 15 menit di ruangan berbeda. Biarkan amigdala (pusat emosi) dari {z1} dan {z2} kembali tenang agar komunikasi tetap konstruktif."],
        2: [f"Posisikan {n2} sebagai rekan pengambil keputusan (*Mastermind Partner*). Hindari mengambil langkah strategis atau finansial besar secara sepihak. Keterlibatan bersama akan mengalirkan rasa dihargai yang menguatkan kerja sama.", f"Bangun keakraban (*Rapport*) dengan apresiasi terhadap hal-hal kecil. Jangan menunggu momen besar untuk memberikan validasi. Pujian atas kontribusi kecil yang dilakukan {n1} setiap hari akan menumbuhkan wibawa hubungan."],
        3: [f"Hadirkan jeda kejutan (*Pattern Interrupt*) secara berkala. Ubah rute perjalanan, buat agenda akhir pekan tanpa rencana ketat, atau ciptakan inovasi kecil agar reseptor kebahagiaan kalian tidak kebas oleh rutinitas harian.", f"Tetapkan sesi diskusi mendalam (*Deep-Talk*) tanpa gangguan gawai secara rutin. Sinkronisasikan ulang target dan selesaikan kekhawatiran masa depan bersama untuk menjaga keselarasan frekuensi kolaborasi kalian."],
        4: [f"Terapkan teknik pembingkaian ulang (*Reframing*) saat diterpa kendala berat. Ubah pola komunikasi dari saling menyalahkan menjadi 'Kita Berdua Bersama Melawan Tantangan Ini'. Pertahankan kesolidan tim internal Anda!", f"Sadari konsep tempaan: Ketidakcocokan opini di fase awal ini hanyalah proses adaptasi (*stress test*) untuk menguji ketangguhan visi kalian. Kurangi sedikit keegoisan, ini adalah fase transisi menuju kestabilan panjang."],
        5: [f"Rencanakan transparansi finansial secara terbuka dan dewasa. Diskusikan kewajiban, target, dan rencana investasi dengan kepala dingin. Penyelarasan rasa syukur dan kepastian operasional adalah kunci kekuatan kalian.", f"Tampillah sebagai penopang emosi (*Emotional Anchor*). Jika salah satu sedang pesimis terhadap situasi masa depan, tugas mutlak pihak lainnya adalah membawa sudut pandang optimis berbasis data untuk mereset fokus otak."],
        6: [f"Berikan jarak spasial (*Space*) sesaat ketika ketegangan meningkat. Kerangka penerimaan informasi kalian memiliki perbedaan mendasar. Saat indikasi miskomunikasi muncul, mundur selangkah sebelum situasi menjadi eskalasi konflik.", f"Jadikan selera humor cerdas sebagai peredam (*Antidote*). Saat perdebatan mulai terasa terlalu kaku dan melelahkan, kemampuan untuk menertawakan ketegangan akan secara efektif mereset saraf komunikasi yang buntu."],
        7: [f"Kunci komunikasi yang sehat: Wajib berbasis fakta terukur, bukan berasumsi. Jika terdapat keraguan, selalu biasakan untuk bertanya: 'Apakah maksud dari tindakan kamu tadi A atau B?'. Klarifikasi dini mencegah salah paham yang membesar.", f"Berikan apresiasi sesuai dengan bahasa penerimaan pasangannya (*Love Language*). Tingkatkan komunikasi afirmatif dan waktu berkualitas untuk menekan munculnya ketidakpastian batin dan pikiran negatif tanpa dasar."],
        8: [f"Cegah penurunan minat (*Boredom*) dengan merancang pencapaian baru bersama. Hubungan yang terlalu stabil kadang rawan kehilangan percikan. Eksplorasi proyek bisnis atau pelajari hal baru berdua untuk meningkatkan ikatan kolaborasi.", f"Jangan biarkan rasa aman membuat Anda menurunkan kualitas diri. Pertahankan standar penampilan, wawasan, dan kualitas kepemimpinan (*grooming*) agar pasangan tetap menemukan nilai lebih yang selalu dapat dikagumi."]
    }
    dont_list = {
        1: [f"SANGAT DISARANKAN untuk tidak melakukan *Mind-Reading* negatif (menebak-nebak pikiran buruk)! Hindari mengambil kesimpulan bahwa '{n2} sengaja bertindak demikian untuk merugikan' tanpa menanyakan konfirmasi secara faktual.", f"Hindari memulai konfrontasi beda pendapat saat salah satu pihak berada dalam kondisi kelelahan, lapar, atau tekanan tinggi (*H.A.L.T*). Logika rasional sedang tidak optimal, dan diskusi hanya akan berpusat pada reaksi emosional."],
        2: [f"Waspadai ilusi 'Pencitraan Sempurna' di media sosial. Menampilkan keharmonisan berlebihan ke pihak luar padahal terdapat ketegangan komunikasi internal yang tidak diselesaikan, lambat laun akan menggerus kepercayaan diri hubungan kalian.", f"Jangan biarkan celah sedikit pun bagi intervensi pihak luar (keluarga besar atau rekan) untuk mendikte keputusan rumah tangga/hubungan kalian. Keputusan taktis harus disepakati murni secara internal oleh kalian berdua."],
        3: [f"Hindari perangkap *Comfort Zone* (Zona Nyaman). Jangan sampai kenyamanan rutinitas asmara ini justru menumpulkan ketajaman visi karier atau semangat pertumbuhan ekonomi masing-masing pihak karena merasa 'sudah cukup aman'.", f"Dilarang mengabaikan standar perawatan diri dan etika hanya karena merasa telah mendapatkan komitmen dari {n1}. Kehilangan ketertarikan visual dan intelektual secara bertahap dapat mengurangi antusiasme dalam hubungan jangka panjang."],
        4: [f"Sangat tidak dianjurkan menggunakan keunggulan status masa lalu atau gengsi personal untuk mendominasi argumentasi di depan {n2}. Fase adaptasi ini menuntut kesediaan melepaskan pola pertahanan diri yang kurang produktif.", f"Hindari melontarkan ancaman pengakhiran hubungan saat emosi sedang tidak stabil di masa transisi. Mengucapkan ultimatum perpisahan di momen kritis adalah tindakan yang secara permanen akan merusak struktur kepercayaan (*Trust*)."],
        5: [f"Jangan jadikan nominal pendapatan sebagai satu-satunya indikator keberhasilan hubungan antara {n1} dan {n2}. Jika ikatan komunikasi dan apresiasi diabaikan, kelimpahan materi justru tidak dapat memberikan pemenuhan batin.", f"Waspadai bibit keangkuhan! Sangat dihindari bersikap meremehkan orang lain atau kompetitor ketika pintu kesuksesan kalian mulai terbuka lebar. Mempertahankan sikap profesional yang rendah hati akan menjaga kontinuitas relasi bisnis."],
        6: [f"Ingatlah prinsip ini: Saat terjadi perdebatan panas, HINDARI sepenuhnya kritik terhadap atribut fisik, mengungkit kegagalan masa lalu yang sensitif, atau melukai harga diri personal {n2}. Kritiklah permasalahannya, bukan menyerang martabatnya.", f"Jangan menggunakan metode hukuman diam (*Silent Treatment*) secara berlebihan tanpa kejelasan waktu batas. Memutuskan komunikasi sepihak tanpa memberi tahu alasan akan menciptakan kebingungan yang memicu trauma dan ketidakpercayaan."],
        7: [f"HINDARI penggunaan kata-kata mutlak (*Universal Quantifiers*) saat sedang tidak sependapat, seperti: 'Kamu SELALU mementingkan diri sendiri!' atau 'Kamu TIDAK PERNAH mendengarkan!'. Generalisasi ini akan memicu respons sangat defensif.", f"Sangat tidak dianjurkan untuk menurunkan standar etika dengan menginspeksi privasi data gawai atau komunikasi pasangan tanpa izin tertulis. Indikasi kurangnya rasa percaya kronis ini dapat mematikan kehangatan alami dalam hubungan."],
        8: [f"Waspadai pola *Take it for granted* (Menganggap remeh komitmen). Sangat tidak disarankan untuk berhenti memberikan inisiatif dan dedikasi terhadap kesejahteraan {n2} seperti halnya saat proses perkenalan awal sedang berlangsung.", f"Jangan membiarkan alur rutinitas operasional keseharian mengabaikan kebutuhan inovasi dan interaksi hangat. Hubungan yang terlalu mekanis membutuhkan dorongan kejutan kreatif agar energi interaksi tidak menjadi membosankan."]
    }
    hasil = {
        1: ("💔 SINDROM PEGAT (Potensi Gesekan Argumen Tajam)", "Pemetaan mendeteksi adanya perbedaan arsitektur pemrosesan respons ketika kalian menghadapi masalah. Layaknya dua entitas dengan sifat komando, perdebatan konseptual bisa meningkat menjadi adu ego yang alot jika rasa saling menghormati intelektual tidak dipertahankan secara sadar."),
        2: ("👑 RESONANSI RATU (Proyeksi Wibawa Kelas Atas)", "Sinergi karakter kalian menampilkan profil kemitraan yang sangat prestisius. Terdapat dorongan otoritas yang kuat yang membuat kolega, bawahan, atau lingkaran profesional di sekeliling otomatis memberikan apresiasi dan menaruh hormat ketika kalian tampil secara representatif."),
        3: ("💞 FREKUENSI JODOH (Keselarasan Pemahaman Naluri)", "Ikatan komunikasi kalian dapat terjalin dengan cukup mengalir. Terdapat frekuensi psikologis mendasar yang sangat cocok, sehingga perbedaan pandangan operasional akan dengan mudah ditemukan titik temu solusinya tanpa menguras energi batin yang terlalu berlebihan."),
        4: ("🌱 FASE TOPO (Ujian Transformasi Karakter)", "Fase awal penyatuan ini merupakan kawah evaluasi. Interaksi pada bulan-bulan pertama menuntut penyesuaian (*adjustment*) emosional yang tinggi dan melelahkan. Namun, jika pemahaman ego masing-masing berhasil melampaui masa ujian ini, ikatan loyalitas kalian di masa depan akan sangat kokoh terhadap intervensi luar."),
        5: ("💰 ALGORITMA TINARI (Penguatan Magnet Kelimpahan)", "Ini merupakan indikator kemitraan yang positif! Kolaborasi entitas ini merepresentasikan kemudahan dalam meraih target finansial. Hambatan dan stagnasi pekerjaan yang sebelumnya membebani dapat berangsur terurai sejak kalian merumuskan visi komitmen bersama yang lebih tertata."),
        6: ("⚡ FRIKSI PADU (Pusaran Miskomunikasi Sistem)", "Sistem memetakan probabilitas terjadinya pengulangan miskomunikasi (*noise*). Perselisihan ini umumnya bukan disebabkan oleh ketiadaan visi bersama, melainkan murni perbedaan *filter* persepsi: satu pihak mengolah data dengan objektivitas keras, pihak lain merespons dengan pendekatan rasa. Membutuhkan titik kompromi yang disiplin."),
        7: ("👁️ JEBAKAN SUJANAN (Kerentanan Asumsi Negatif)", "Indikator waspada pada transparansi! Interaksi penyatuan ini sangat rentan memicu kesalahpahaman berbasis *asumsi*. Banyak interpretasi keliru yang bermunculan di benak tanpa ada bukti faktual, yang berisiko menciptakan perdebatan fiktif. Selalu pastikan komunikasi berjalan secara eksplisit."),
        8: ("🕊️ ANCHOR PESTHI (Zona Keseimbangan Ketahanan Stres)", "Kondisi penyatuan yang sangat sehat. Keterikatan ini mampu bertindak sebagai penyeimbang biologis untuk meredam pelepasan hormon stres. Hubungan interaktif kalian cenderung konsisten, tenang, dan secara signifikan melindungi kapasitas rasionalitas masing-masing pihak dari tekanan pihak luar.")
    }
    return hasil[sisa][0], hasil[sisa][1], random.choice(do_list[sisa]), random.choice(dont_list[sisa])

KAMUS_ABJAD = {'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 's': 60, 'f': 80, 'q': 100, 'r': 200, 'c': 3, 'e': 5, 'g': 1000, 'i': 10, 'o': 6, 'p': 80, 'u': 6, 'v': 6, 'x': 60}
def hitung_nama_esoterik(nama): return sum(KAMUS_ABJAD.get(h, 0) for h in ''.join(filter(str.isalpha, str(nama).lower()))) or 1
def get_rincian_esoterik(nama):
    r = [f"{h.upper()}({KAMUS_ABJAD.get(h,0)})" for h in ''.join(filter(str.isalpha, str(nama).lower())) if KAMUS_ABJAD.get(h,0)>0]
    return " + ".join(r) if r else "0"

def generate_dynamic_reading(total_jummal):
    mod = total_jummal % 4 if total_jummal % 4 != 0 else 4
    el = {1: ("🔥 API (Nar)", "Kecepatan eksekusi yang tinggi, tegas, dan berjiwa pelopor yang berani mengambil inisiatif di awal."), 2: ("🌍 TANAH (Turab)", "Pendekatan berbasis logika realitas, kokoh mempertahankan prinsip, serta fokus utama pada stabilitas aset material."), 3: ("💨 UDARA (Hawa)", "Proses berpikir lincah yang kaya gagasan, adaptif di berbagai kondisi, serta kemampuan komunikasi persuasif yang kuat."), 4: ("💧 AIR (Ma')", "Tingkat sensitivitas empati yang dalam, fleksibel menghadapi perubahan, namun tegas ketika prinsip dasarnya dilanggar.")}
    p_red = " + ".join(list(str(total_jummal)))
    s_red = sum(int(d) for d in str(total_jummal))
    r_num = s_red
    while r_num > 9: r_num = sum(int(d) for d in str(r_num))
    r_dict = {1:"Penginisiasi jalan & Eksekutor dominan", 2:"Katalis harmoni batin & Negosiator bijak", 3:"Perancang konsep & Ahli persuasi publik", 4:"Pembuat struktur logika & Penjaga integritas SOP", 5:"Fasilitator transformasi & Pengambil risiko terukur", 6:"Pilar perlindungan moral & Penjaga keamanan kolektif", 7:"Pencari kedalaman analitis & Auditor independen", 8:"Pemegang otoritas strategis & Perencana pertumbuhan material", 9:"Pemikir berwawasan universal & Penyelesai hambatan emosional"}
    
    m_note = "<div style='background:rgba(212,175,55,0.1); padding:15px; border-radius:8px; border-left: 4px solid #FFD700; margin-top:15px; margin-bottom:15px; box-shadow: 0 4px 15px rgba(212,175,55,0.2);'><span style='color:#FFD700; font-size:16px; letter-spacing:1px; font-weight:900;'>⚡ ANOMALI KODE MASTER TERDETEKSI!</span><br><span style='color:#e0e0e0; font-size:14px; line-height:1.6; display:inline-block; margin-top:5px;'>Sistem mendeteksi adanya resonansi yang tidak biasa (Angka Master) pada inti identitas Anda. Radar pemahaman intuitif Anda sedang bekerja sangat maksimal di gelombang otak yang tenang. Gagasan strategis atau solusi tak terduga yang melintas di pikiran Anda saat ini sangat mungkin merupakan wawasan presisi yang melampaui analisa rasional biasa. Berikan ruang bagi intuisi tersebut untuk memandu langkah operasional Anda ke depan.</span></div>" if any(m in str(total_jummal) for m in ["11","22","33"]) else ""
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

def hitung_neptu_langsung(hari, pasaran): return {"Minggu":5,"Senin":4,"Selasa":3,"Rabu":7,"Kamis":8,"Jumat":6,"Sabtu":9}.get(hari,0) + {"Legi":5,"Pahing":9,"Pon":7,"Wage":4,"Kliwon":8}.get(pasaran,0)

dynamic_users = get_dynamic_count()

# --- SIDEBAR PROMOSI & LOGIN ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        try: st.image("baru.jpg.png", use_container_width=True); st.markdown("<br>", unsafe_allow_html=True)
        except: pass
 
    st.markdown(f"### {get_greeting()}")
    st.markdown("---")
    
    # PERUBAHAN POIN 1: LOGIN BERBASIS EMAIL BUKAN KODE "NEUROVIP" LAGI
    st.markdown("### 🔓 Akses Premium")
    if not st.session_state.premium:
        email_input = st.text_input("Masukan Email Akses VIP:", placeholder="Ketik email terdaftar Anda...")
        if email_input:
            if email_input.lower() in VIP_EMAILS: 
                st.session_state.premium = True
                st.toast("Akses Terbuka! Selamat Datang di Mode VIP.", icon="👑")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Email Anda belum terdaftar aktif.")
        
        # PERUBAHAN POIN 2: CTA DI SIDEBAR MENGARAH KE PAYMENT GATEWAY OTOMATIS
        st.markdown("<p style='font-size:13px; color:#888;'>Belum punya akses VIP? <br><a href='[LINK_PAYMENT_GATEWAY_LU_DISINI]' target='_blank' style='color:#25D366; font-weight:bold; text-decoration:none;'>🚀 Daftar & Bayar Otomatis Di Sini</a></p>", unsafe_allow_html=True)
    else:
        st.success("👑 Status: VIP MEMBER")
        if st.button("Logout"):
            st.session_state.premium = False
            st.rerun()
    
    st.markdown("---")
    st.markdown("""<div style='background: linear-gradient(135deg, #ff0000 0%, #8b0000 100%); padding: 18px; border-radius: 10px; text-align: center; border: 1px solid #ff4b4b; box-shadow: 0 5px 15px rgba(255,0,0,0.3);'>
<b style='color: white; font-size: 16px; letter-spacing: 1px;'>🔥 BUTUH ANALISA LEBIH MENDALAM?</b><br>
<span style='color: #ccc; font-size: 12px; display:block; margin-top:5px;'>Beberapa pemetaan (Hambatan Spesifik) tidak dapat ditampilkan secara publik.</span>
<span style='color: #FFD700; font-size: 13px; display:inline-block; margin-top:5px; margin-bottom:12px;'>Konsultasi Privat dengan Coach (Slot Terbatas)</span><br>
<a href='https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20butuh%20sesi%20kalibrasi%20privat%20hari%20ini' target='_blank' style='background: #25D366; color: white; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 900; font-size: 14px; display: inline-block; box-shadow: 0 4px 10px rgba(37,211,102,0.4);'>💬 KLIK DI SINI SEKARANG</a>
</div>""", unsafe_allow_html=True)
    st.markdown("<br><center><small style='color:#666;'>© 2026 Neuro Nada Academy</small></center>", unsafe_allow_html=True)

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

cur_planet, cur_instr, cur_color = get_planetary_hour()
st.markdown(f"""<div style='text-align: right;'><div class='live-badge' style='background: {cur_color};'>🕒 LIVE PLANET: {cur_planet.upper()}</div><div style='font-size: 11px; color: #888; margin-top: 5px;'>{cur_instr}</div></div>""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900; color:#FFD700;'>🌌 BUKA KODE HIDUP ANDA HARI INI</h1>", unsafe_allow_html=True)
st.markdown("""<p style='text-align: center; font-size: 16px; color: #ccc;'>Sistem ini adalah instrumen pemetaan presisi tinggi berdasarkan kerangka profil nama (Sandi Frekuensi), garis waktu kelahiran (Sintaksis Meta-Program Otak), dan bioritme pergerakan makrokosmos saat ini.<br><br><b style='color:#FFF;'>⚡ Kurang dari 10 detik, Anda akan memperoleh wawasan:</b><br><span style='color:#D4AF37;'>• Prediksi dorongan momentum produktivitas hari ini<br>• Celah *Blind Spot* kritis yang perlu penanganan segera<br>• Potensi kebiasaan yang menyabotase fokus dan target Anda</span></p>""", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; margin-bottom:20px;'><span style='background:rgba(255,75,75,0.2); color:#ff4b4b; padding:8px 15px; border-radius:5px; font-size:13px; font-weight:bold; letter-spacing:1px;'>⚠️ PERINGATAN: Laporan ini dirancang dengan objektivitas tinggi untuk mengidentifikasi area yang membutuhkan perbaikan fundamental karakter.</span></div>", unsafe_allow_html=True)
st.markdown("---")
 
tgl_today = datetime.date.today()
tab1, tab2, tab5, tab3, tab6, tab4 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Matrix 🔒", "⏱️ Quantum Engine 🔒", "🌌 Falak Ruhani 🔒", "📚 Neuro-Insights", "❓ FAQ & Disclaimer"])
 
# ==========================================
# TAB 1: IDENTITAS KOSMIK
# ==========================================
with tab1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#fff;'>👇 Masukkan parameter Anda sekarang untuk di-decode</h4>", unsafe_allow_html=True)
    nama_user = st.text_input("Nama Lengkap Sesuai Identitas Asli:", placeholder="Ketik nama lengkap Anda di sini...", key="t1_nama")
    
    col_tgl, col_wt = st.columns(2)
    with col_tgl:
        st.write("📅 **Data Masehi:**")
        tgl_input = st.date_input("Tanggal Lahir", value=datetime.date(1995, 1, 1), min_value=datetime.date(1930, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")
    with col_wt:
        st.write("📜 **Data Weton:**")
        hari_input = st.selectbox("Hari Kelahiran", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="h_t1")
        pasaran_input = st.selectbox("Pasaran Kelahiran", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="p_t1")
    st.markdown("</div>", unsafe_allow_html=True)
 
    if st.button("🚀 Petakan Potensi Tindakan Saya", key="btn_t1"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Filter Keamanan: Mohon ketik nama lengkap Anda (minimal 3 karakter).")
        else:
            try:
                with st.spinner('Menyelaraskan *mapping* frekuensi makrokosmik dengan arsitektur otak Anda...'): time.sleep(1.5)
                st.toast("Kalibrasi sukses! Struktur pola pikir Anda berhasil diurai sistem.", icon="⚡")
                
                safe_name = get_safe_firstname(nama_user)
                angka_hasil = hitung_angka(tgl_input)
                rincian_tgl = get_rincian_tanggal(tgl_input)
                nilai_jummal = hitung_nama_esoterik(nama_user)
                rincian_jummal = get_rincian_esoterik(nama_user)
                el_nama, el_desc, p_reduk, s_reduk, r_num, r_desc, m_note = generate_dynamic_reading(nilai_jummal)
                
                nep = hitung_neptu_langsung(hari_input, pasaran_input)
                wet = f"{hari_input} {pasaran_input}"
                zod = get_zodiak(tgl_input)
                
                hari_ini_str = {"Monday":"Senin", "Tuesday":"Selasa", "Wednesday":"Rabu", "Thursday":"Kamis", "Friday":"Jumat", "Saturday":"Sabtu", "Sunday":"Minggu"}[tgl_today.strftime("%A")]
                n_laku, d_laku = get_betaljemur_data(nep)
                arah_naga = get_naga_dina(hari_ini_str)
                rezeki_data, usaha_data, r_color = get_rezeki_usaha(nep, tgl_today)
                
                punchy = arketipe_punchy.get(angka_hasil, arketipe_punchy[1])
                desk_ark_dinamis = proc_arketipe(safe_name, angka_hasil, zod, nep)
                shadow = proc_shadow_list(safe_name, angka_hasil)
                
                aksi_list = [
                    f"Atasi penundaan Anda hari ini. Segera ambil sarana komunikasi dan hubungi satu prospek, klien, atau koneksi kunci yang selama ini Anda hindari hanya karena kekhawatiran yang tidak logis.",
                    f"Lakukan evaluasi penggunaan energi mental Anda. Identifikasi dengan jujur lalu minimalisir SATU interaksi atau tugas repetitif hari ini yang menyedot konsentrasi Anda tanpa memberikan imbal balik yang jelas.",
                    f"Terapkan distribusi tanggung jawab (*delegation*) yang tegas! Terdapat beban manajerial yang menahan kapasitas omset Anda. Serahkan penyelesaian tugas operasional tersebut kepada orang yang lebih tepat hari ini."
                ]
                aksi_teks = random.choice(aksi_list)
                core_shadow_raw = shadow[0]
                core_shadow_title = core_shadow_raw.split("**")[1].replace(":", "") if "**" in core_shadow_raw else core_shadow_raw.split(":")[0]
                
                st.markdown(f"""<div class="soft-fade" style="background: rgba(255,215,0,0.1); border-left: 5px solid #FFD700; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,215,0,0.3);">
<h3 style="margin-top:0; color:#FFD700; font-weight:900; letter-spacing:1px;">🎯 HASIL PENILAIAN ALGORITMA HARI INI</h3>
<ul style="font-size: 16px; line-height: 1.8; color: #fff; list-style-type: none; padding-left: 0;">
<li style="margin-bottom: 15px; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px;">
💰 <b>STATUS REZEKI (<span style='color:{r_color};'>{rezeki_data[0].split('(')[0].strip()}</span>):</b><br>
<span style='color:{r_color}; font-weight:bold; font-size:15px;'>MOMENTUM AKTIF HARI INI.</span> <span style="color:#e0e0e0; font-size:14px; line-height:1.7;">{rezeki_data[1]}</span>
</li>
<li style="margin-bottom: 15px; background: rgba(37,211,102,0.1); border-left: 4px solid #25D366; padding: 15px; border-radius: 8px;">
⚡ <b>INSTRUKSI TINDAKAN OPERASIONAL:</b><br>
<span style="color:#e0e0e0; font-size:14px; line-height:1.7;">{aksi_teks}</span>
</li>
<li style="margin-bottom: 10px; background: rgba(255,75,75,0.1); border-left: 4px solid #ff4b4b; padding: 15px; border-radius: 8px;">
🚫 <b>INDIKATOR RISIKO (TITIK WASPADA):</b><br>
<span style="color:#ff4b4b; font-size:14px; font-weight:bold;">Perhatikan munculnya {core_shadow_title}!</span><br>
<span style="color:#e0e0e0; font-size:14px; line-height:1.7;">Sistem membaca adanya celah kerentanan pengambilan keputusan hari ini. Tahan kuat-kuat dorongan reaktif atau rasa kurang percaya diri Anda sebelum menyetujui komitmen jangka panjang atau transaksi yang signifikan.</span>
</li>
</ul>
<div style="background: rgba(255,75,75,0.2); padding: 8px 15px; border-radius: 5px; display: inline-block; margin-top: 10px;">
<b style="color:#ff4b4b; font-size:13px;">⏳ Fluktuasi algoritma ini dioptimalkan relevansinya untuk 24 jam ke depan. Ambil tindakan taktis sekarang.</b>
</div>
</div>""", unsafe_allow_html=True)
                
                if not st.session_state.premium:
                    # PERUBAHAN POIN 2: CTA DI TAB 1 MENGARAH KE PAYMENT GATEWAY
                    st.markdown(f"""<div class="glass-container soft-fade" style="text-align:center; border: 2px solid #ff4b4b; padding: 30px 20px;">
<h3 style="color:#ff4b4b; margin-top:0;">🔓 Anda baru mengakses sebagian dari hasil pemetaan *Decoding* Anda...</h3>
<div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: left; display: inline-block;">
<span style="color:#ccc; font-size: 15px;">Di dalam zona Akses Penuh (Premium):</span><br>
<b style="color:#fff;">• Pemetaan kepribadian terdalam & Arsitektur Karakter yang memengaruhi keputusan Anda</b><br>
<b style="color:#fff;">• 3 Titik Kerentanan Psikologis (*Shadow*) yang berpotensi memperlambat progres kinerja Anda</b><br>
<b style="color:#fff;">• Indikator Penyelarasan Fokus Berdasarkan Kompas Waktu (*Naga Dina*) HARI INI</b><br>
<b style="color:#fff;">• Tab Matriks Kolaborasi: Bedah intensitas keselarasan komunikasi dengan rekan atau pasangan</b>
</div>
<p style="color:#FFD700; font-size: 16px;"><b>🔥 Catatan: Laporan komprehensif ini dikalibrasi secara eksklusif berdasar data unik klien.<br>Merupakan panduan spesifik untuk perbaikan manajemen diri.</b></p>
<a href="[LINK_PAYMENT_GATEWAY_LU_DISINI]" target="_blank" style="text-decoration:none;">
<div class="cta-button" style="font-size:18px; margin-top: 10px;">🚀 AKTIFKAN LAPORAN PENUH SEKARANG</div>
</a>
<p style="font-size:14px; color:#ccc; margin-top:15px; margin-bottom: 5px;">Investasi Sistem: <b>Hanya Rp 19.000</b><br><i style="color:#888;">(Pembayaran otomatis. Akses instan 24 jam dengan Email Anda.)</i></p>
<div style="margin-top: 25px; border-top: 1px dashed #555; padding-top: 15px;">
<span style="font-size:14px; color:#25D366; font-weight:bold;">🔥 {dynamic_users} individu telah memanfaatkan wawasan sistem ini untuk kemajuan mereka.</span><br>
<span style="font-size:13px; color:#888;">Ambil kendali atas arah langkah Anda hari ini.</span>
</div>
</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h3 style='text-align:center;'>🌌 Laporan Intelijen Personal: {safe_name}</h3>", unsafe_allow_html=True)
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Nilai Esoterik Nama</div><div class="matrix-value matrix-value-special">{nilai_jummal}</div></div><div class="matrix-item"><div class="matrix-label">Karakteristik Elemen</div><div class="matrix-value">{el_nama.split(' ')[1] if len(el_nama.split(' '))>1 else el_nama}</div></div><div class="matrix-item"><div class="matrix-label">OS Otak (Meta-Program)</div><div class="matrix-value matrix-value-special">KODE {angka_hasil}</div></div><div class="matrix-item"><div class="matrix-label">Indikator Zodiak</div><div class="matrix-value">{zod}</div></div><div class="matrix-item"><div class="matrix-label">Gravitasi Weton Klien</div><div class="matrix-value">{wet} ({nep})</div></div></div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="dynamic-reading-box soft-fade"><h4 style="color: #FFD700; margin-top:0;">🔍 Dekoding Arsitektur Mesin Diri (DNA Numerologi)</h4><p><b>1. Sandi Esoterik Nama (Aura Tarikan Potensi):</b><br><code style="color:#25D366; background:transparent; padding:0; font-size:15px;">{rincian_jummal} = <b>{nilai_jummal}</b></code></p><ul style="margin-left: -15px; margin-bottom: 20px; color:#ccc; line-height:1.7;"><li><b>Kerangka Bawah Sadar:</b> {el_nama} - <i>{el_desc}</i></li><li><b>Orientasi Dasar:</b> {p_reduk} = {s_reduk} ➡ <b>{r_num}</b> ({r_desc})</li></ul><p><b>2. Sandi Garis Waktu Lahir (Meta-Program NLP):</b><br><code style="color:#FFD700; background:transparent; padding:0; font-size:15px;">{rincian_tgl}</code><br><span style="font-size:14px; color:#ccc; display:inline-block; margin-top:8px; line-height:1.7;">Ekstraksi di atas mengkategorikan kerangka analisa Anda pada <b>KODE {angka_hasil}</b>. Pengkategorian ini membedah wujud *Blueprint* genetik yang menjelaskan secara rasional bagaimana mekanisme pemrosesan informasi dari <b>{safe_name}</b> bekerja saat berada di bawah tekanan target, menerima instruksi dari pihak luar, hingga pembentukan gaya kepemimpinan dasar.</span></p>{m_note}</div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="primbon-box soft-fade"><div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;"><span style="color:#D4AF37; font-size:14px; font-weight:900; letter-spacing:2px;">📜 REFERENSI LOGIKA ALGORITMA: BETALJEMUR ADAMMAKNA</span></div>
<div style="font-size:15px; line-height:1.7; margin-bottom: 20px;"><b style="color:#FFF; font-size:18px; letter-spacing:1px;">{n_laku}</b><br><i style="color:#ccc; display:inline-block; margin-top:5px;">{d_laku}</i></div>
<div style="font-size:15px; line-height:1.7; margin-bottom: 20px; border-top: 1px dashed #555; border-bottom: 1px dashed #555; padding-top: 15px; padding-bottom: 15px;">
• <b style="color:#FFF;">Siklus Potensi Material Hari Ini (<span style="color:{r_color};">{rezeki_data[0]}</span>):</b><br><span style="color:#ccc; display:inline-block; margin-top:5px; margin-bottom:12px;">{rezeki_data[1]}</span><br>
• <b style="color:#FFF;">Afinitas Sektor Pengembangan (<span style="color:#25D366;">{usaha_data[0]}</span>):</b><br><span style="color:#ccc; display:inline-block; margin-top:5px;">{usaha_data[1]}</span>
</div>
<div style="font-size:15px; line-height:1.7; background: rgba(212,175,55,0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700;">
<span style="color:#FFD700;">🧭 <b>NAGA DINA (Orientasi Geografis Resolusi Hari {hari_ini_str}):</b></span> <b style="font-size: 18px; color:#FFF;">{arah_naga}</b><br>
<i style="color:#e0e0e0; font-size:14px; display:inline-block; margin-top:8px;">*APLIKASI LAPANGAN: Saat memimpin negosiasi penting, mengirim proposal tingkat tinggi, atau melakukan pertimbangan manajerial HARI INI, pertimbangkan untuk menempatkan fokus arah fisik ke <b>{arah_naga}</b>. Ini merupakan metode penyelarasan fokus yang dipercaya dapat mengurangi hambatan eksternal di ruang kerja Anda.</i>
</div></div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"<h3 style='margin-bottom:5px;'>👁️ Bedah Tuntas Kepribadian Psikologis: {safe_name}</h3>", unsafe_allow_html=True)
                    st.info(f"Sistem telah menganalisis kerangka karakter autentik Anda secara mendalam. Arsitektur mental pendorong tindakan Anda berpusat pada peranan:\n\n### **{punchy['inti']}**")
                    st.markdown(f"<p style='font-size:15px; line-height:1.7; color:#ccc; margin-bottom:25px;'>{desk_ark_dinamis}</p>", unsafe_allow_html=True)
                    
                    c_kekuatan, c_shadow = st.columns(2)
                    with c_kekuatan:
                        st.markdown(f"🔥 <b style='color:#FFF; font-size:16px;'>KEUNGGULAN UTAMA (PRODUKTIVITAS):</b>", unsafe_allow_html=True)
                        st.markdown(f"<ul class='list-punchy' style='color:#25D366; line-height:1.7;'><li>{punchy['kekuatan'][0]}</li><li style='margin-top:8px;'>{punchy['kekuatan'][1]}</li><li style='margin-top:8px;'>{punchy['kekuatan'][2]}</li></ul>", unsafe_allow_html=True)
                    with c_shadow:
                        st.markdown(f"⚠️ <b style='color:#FFF; font-size:16px;'>SHADOW (POTENSI HAMBATAN MENTAL):</b>", unsafe_allow_html=True)
                        st.markdown(f"<ul class='list-punchy' style='color:#ff4b4b; line-height:1.7;'><li><span style='color:#e0e0e0'>{shadow[0]}</span></li><li style='margin-top:10px;'><span style='color:#e0e0e0'>{shadow[1]}</span></li><li style='margin-top:10px;'><span style='color:#e0e0e0'>{shadow[2]}</span></li></ul>", unsafe_allow_html=True)
                
            except Exception as e: st.error(f"Sistem mengalami kendala saat melakukan komputasi parameter: {e}")
 
# ==========================================
# TAB 2: COUPLE MATRIX
# ==========================================
with tab2:
    if not st.session_state.premium:
        # PERUBAHAN POIN 2: CTA DI TAB 2 MENGARAH KE PAYMENT GATEWAY
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h3 style='color: #ff4b4b; font-weight: 900; margin-top:0;'>💞 KALIBRASI DINAMIKA RELASI & KOMUNIKASI</h3>
<p style='color: #ccc; font-size: 16px; margin-bottom: 20px;'>Petakan struktur perbedaan pendapat dan keselarasan Anda dengan rekan yang dituju. Temukan arah perkembangan hubungan ini secara profesional/personal:<br><b style='color:#ff4b4b;'>❤️ Sinergi yang Saling Melengkapi?</b> | <b style='color:#FFD700;'>⚡ Fase Penyesuaian Karakter Ekstra?</b> | <b style='color:#888;'>💔 Atau Konflik Berulang Akibat Miskomunikasi?</b></p>
<p style='font-size: 14px; color: #aaa; margin-bottom: 30px;'>Ketik 2 nama pihak terkait dan bedah di titik mana perdebatan seringkali menemui jalan buntu.<br><i style='color:#ff4b4b;'>⚠️ Catatan Objektivitas: Hasil keluaran algoritma ini disusun untuk memberikan transparansi tajam tanpa mengurangi fakta ketidakcocokan. Digunakan untuk keperluan evaluasi relasi.</i></p>
<a href="[LINK_PAYMENT_GATEWAY_LU_DISINI]" target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 AKSES FITUR PEMETAAN HUBUNGAN DI SINI</div>
</a>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("💞 Penyatuan Esoterik & Dinamika Betaljemur (Couple Matrix)")
        ca, cb = st.columns(2)
        with ca: 
            st.markdown("<h4 style='color:#FFD700;'>Pihak 1 (Aktor Utama / Pria)</h4>", unsafe_allow_html=True)
            n1 = st.text_input("Ketik Nama Panggilan Pihak 1", key="n1_c")
            d1 = st.date_input("Lahir Masehi Pihak 1", value=datetime.date(1995, 1, 1), min_value=datetime.date(1930, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="d1_c")
            hc1 = st.selectbox("Hari Pihak 1", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="hc1")
            pc1 = st.selectbox("Pasaran Pihak 1", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="pc1")
        with cb: 
            st.markdown("<h4 style='color:#FF69B4;'>Pihak 2 (Aktor Penyeimbang / Wanita)</h4>", unsafe_allow_html=True)
            n2 = st.text_input("Ketik Nama Panggilan Pihak 2", key="n2_c")
            d2 = st.date_input("Lahir Masehi Pihak 2", value=datetime.date(1998, 5, 10), min_value=datetime.date(1930, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="d2_c")
            hc2 = st.selectbox("Hari Pihak 2", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=2, key="hc2")
            pc2 = st.selectbox("Pasaran Pihak 2", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=0, key="pc2")
        st.markdown("</div>", unsafe_allow_html=True)
            
        if st.button("🚀 Retas Dinamika Komunikasi Pasangan", key="btn_couple"):
            if str(n1).strip() and str(n2).strip():
                try:
                    with st.spinner('Melakukan komputasi untuk membongkar pola interaksi komunikasi kedua belah pihak...'): time.sleep(1.5)
                    st.toast("Analisa sinkronisasi relasi sukses dipetakan!", icon="💞")
                    
                    safe_n1, safe_n2 = get_safe_firstname(n1, "Pria"), get_safe_firstname(n2, "Wanita")
                    zod1, zod2 = get_zodiak(d1), get_zodiak(d2)
                    nep_1, nep_2 = hitung_neptu_langsung(hc1, pc1), hitung_neptu_langsung(hc2, pc2)
                    sel = abs(hitung_angka(d1) - hitung_angka(d2))
                    jummal_1, jummal_2 = hitung_nama_esoterik(n1), hitung_nama_esoterik(n2)
                    total_couple = jummal_1 + jummal_2
                    root_c = total_couple
                    while root_c > 9: root_c = sum(int(d) for d in str(root_c))
                    
                    c_title, c_filosofi, c_desc = proc_couple_persona(root_c, safe_n1, safe_n2)
                    judul_jodoh, desk_jodoh, d_do, d_dont = proc_weton_kombo((nep_1+nep_2)%8 or 8, safe_n1, safe_n2, zod1, zod2)
                    
                    st.markdown(f"### 🔮 Rekapitulasi Resonansi: {safe_n1} 💥 {safe_n2}")
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Beban Karakter {safe_n1}</div><div class="matrix-value">{hc1} {pc1} ({nep_1})</div></div><div class="matrix-item"><div class="matrix-label">Beban Karakter {safe_n2}</div><div class="matrix-value">{hc2} {pc2} ({nep_2})</div></div><div class="matrix-item" style="background: rgba(212,175,55,0.2); border-left: 1px solid #D4AF37; border-right: 1px solid #D4AF37;"><div class="matrix-label" style="color:#FFD700;">SKOR AKUMULASI BENTURAN</div><div class="matrix-value matrix-value-special">{nep_1 + nep_2}</div></div><div class="matrix-item"><div class="matrix-label">Kalkulasi Frekuensi Bersama</div><div class="matrix-value">{total_couple}</div></div></div>""", unsafe_allow_html=True)
                    
                    st.markdown(proc_penjelasan_matriks(safe_n1, safe_n2, total_couple, (nep_1+nep_2)), unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="dynamic-reading-box soft-fade" style="border-left-color: #25D366; background: rgba(10,30,15,0.8);">
<h4 style="color: #25D366; margin-top:0; letter-spacing:1px;">🧬 Karakteristik Hubungan Keseluruhan: {c_title}</h4>
<div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 3px solid #FFD700;">
<b style="color: #FFD700; font-size: 14px; letter-spacing: 1px;">🧠 APA ITU ROOT {root_c}? (DEKODE FILOSOFI DASAR)</b><br>
<span style="color:#ccc; line-height:1.7; font-size:14px; display:inline-block; margin-top:5px;">{c_filosofi}</span>
</div>
<p style="color:#e0e0e0; line-height:1.7; font-size:15px;"><b style="color:#FFF;">⚡ ANALISIS SINERGI SPESIFIK ({safe_n1} & {safe_n2}):</b><br>{c_desc}</p>
</div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="soft-fade" style="background: rgba(30,20,20,0.8); border: 1px solid #ff4b4b; border-left: 5px solid #ff4b4b; padding: 20px; border-radius: 8px; margin-bottom:20px;">
                    <b style="color:#ff4b4b; font-size:16px;">Titik Kerentanan Komunikasi Bawah Sadar ({judul_jodoh}):</b><br>
                    <span style="color:#ccc; display:inline-block; margin-top:8px; line-height:1.7; font-size:15px;">{desk_jodoh}</span>
                    </div>""", unsafe_allow_html=True)
                    
                    if sel in [0, 3, 6, 9]: 
                        st.markdown(f"<div class='info-metric-box soft-fade' style='border-color:#25D366; background:rgba(37,211,102,0.05);'><span style='font-size:24px;'>💘</span> <b style='color:#25D366; font-size:15px;'>TINGKAT KESELARASAN NLP: Sangat Konstruktif.</b><br><span style='color:#ccc; margin-top:5px; display:inline-block; line-height:1.6;'>Pola kognitif Anda dan pasangan dalam memproses penyelesaian masalah memiliki dasar yang serupa. Hal ini memungkinkan transfer informasi berjalan efisien dan minim kesalahpahaman.</span></div>", unsafe_allow_html=True)
                    elif sel in [1, 2, 8]: 
                        st.markdown(f"<div class='info-metric-box soft-fade' style='border-color:#FFD700; background:rgba(255,215,0,0.05);'><span style='font-size:24px;'>⚖️</span> <b style='color:#FFD700; font-size:15px;'>TINGKAT KESELARASAN NLP: Membutuhkan Kalibrasi Intensif.</b><br><span style='color:#ccc; margin-top:5px; display:inline-block; line-height:1.6;'>Hubungan ini menuntut upaya penyelarasan empati yang konsisten. Terkadang gelombang komunikasi bersinergi dengan baik, namun di waktu lain berpotensi mengalami pembiasan makna yang memicu keheningan.</span></div>", unsafe_allow_html=True)
                    else: 
                        st.markdown(f"<div class='info-metric-box soft-fade' style='border-color:#ff4b4b; background:rgba(255,75,75,0.05);'><span style='font-size:24px;'>🔥</span> <b style='color:#ff4b4b; font-size:15px;'>TINGKAT KESELARASAN NLP: Risiko Miskomunikasi Signifikan.</b><br><span style='color:#ccc; margin-top:5px; display:inline-block; line-height:1.6;'>Perhatian khusus! Pendekatan kalian dalam menerima realita (*Map of the World*) bekerja dari sudut pandang yang bertolak belakang. Penjelasan dari satu pihak dapat dimaknai sangat berbeda oleh pihak lain, sehingga menuntut tingkat toleransi ekstra demi menemukan resolusi.</span></div>", unsafe_allow_html=True)
         
                    c_do_c, c_dont_c = st.columns(2)
                    with c_do_c: st.markdown(f"<div class='soft-fade' style='background:rgba(37,211,102,0.05); padding:20px; border-radius:10px; border:1px solid #25D366; height:100%; box-shadow: inset 0 0 20px rgba(37,211,102,0.05);'><b style='color:#25D366; font-size:16px; letter-spacing:1px;'>✅ PROTOKOL PENYELESAIAN KONFLIK (DISARANKAN):</b><hr style='border-color:rgba(37,211,102,0.2); margin-top:10px; margin-bottom:15px;'><span style='color:#e0e0e0; line-height:1.7; font-size:14px;'>{d_do}</span></div>", unsafe_allow_html=True)
                    with c_dont_c: st.markdown(f"<div class='soft-fade' style='background:rgba(255,75,75,0.05); padding:20px; border-radius:10px; border:1px solid #ff4b4b; height:100%; box-shadow: inset 0 0 20px rgba(255,75,75,0.05);'><b style='color:#ff4b4b; font-size:16px; letter-spacing:1px;'>❌ ZONA RAWAN (SANGAT DIHINDARI):</b><hr style='border-color:rgba(255,75,75,0.2); margin-top:10px; margin-bottom:15px;'><span style='color:#e0e0e0; line-height:1.7; font-size:14px;'>{d_dont}</span></div>", unsafe_allow_html=True)
                except Exception as e: st.error(f"Sistem gagal mengekstraksi data evaluasi relasi: {e}")

# ==========================================
# TAB 5: QUANTUM ENGINE
# ==========================================
with tab5:
    if not st.session_state.premium:
        # PERUBAHAN POIN 2: CTA DI TAB 5 MENGARAH KE PAYMENT GATEWAY
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 FITUR EKSKLUSIF MANAJEMEN WAKTU</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Anda telah mencapai batas ulasan pada layanan reguler. Dapatkan akses menuju <b>Tactical Action Plan (Peta Arahan Eksekusi Berbasis Pemantauan Real-time)</b> yang membantu menyelaraskan alur produktivitas Anda mengikuti dinamika fase harian.</p>
<a href="[LINK_PAYMENT_GATEWAY_LU_DISINI]" target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN AKSES FITUR LENGKAP DI SINI</div>
</a>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("⏱️ Live Cosmic Dashboard (Pemetaan Kinerja Taktis)")
        st.write("Sinkronkan inisiatif pekerjaan Anda dengan fase energi yang optimal. Sistem ini memandu Anda menetapkan waktu terbaik untuk mengambil kebijakan strategis dengan meminimalisasi hambatan prosedural yang tidak perlu.")
        qe_nama = st.text_input("Ketik Nama Panggilan Fokus Analisa:", key="qe_n")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Unduh Data Taktis Terkini", key="btn_qe"):
            if qe_nama:
                with st.spinner('Menganalisis kondisi fase optimal Anda saat ini secara *real-time*...'): time.sleep(1.2)
                st.toast("Dashboard Manajerial sukses diperbarui dengan parameter baru!", icon="⏱️")
                
                safe_qe = get_safe_firstname(qe_nama)
                jummal_qe = hitung_nama_esoterik(qe_nama)
                mod_harian = (jummal_qe + sum(int(d) for d in tgl_today.strftime("%d%m%Y"))) % 7
                sun_fase, sun_desc = get_sun_phase()
                planet_live, planet_desc, planet_color = get_planetary_hour()
                
                siklus_nama, html_plan = proc_tactical_plan(safe_qe, mod_harian, planet_live, planet_desc, sun_fase, sun_desc)
                
                st.markdown(f"### 📡 Panel Arahan Taktis: {safe_qe}")
                st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Fase Cadangan Bioritme Harian</div><div class="matrix-value">{siklus_nama}</div></div><div class="matrix-item"><div class="matrix-label">Siklus Jam Biologis Matahari</div><div class="matrix-value matrix-value-special">{sun_fase.split(' ')[0]}</div></div><div class="matrix-item" style="border-bottom: 2px solid {planet_color};"><div class="matrix-label">Intervensi Pengaruh Kosmik Eksternal</div><div class="matrix-value" style="color:{planet_color};">{planet_live}</div></div></div>""", unsafe_allow_html=True)
                st.markdown(html_plan, unsafe_allow_html=True)

# ==========================================
# TAB 3: FALAK RUHANI
# ==========================================
with tab3:
    if not st.session_state.premium:
        # PERUBAHAN POIN 2: CTA DI TAB 3 MENGARAH KE PAYMENT GATEWAY
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 FITUR MANAJEMEN EMOSIONAL TERKUNCI</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Hak akses ditangguhkan. Silakan peroleh izin tingkat lanjut untuk mengakses <b>Modul Terapi Falak Ruhani, Penyelarasan Dzikir Sesuai Afinitas, Afirmasi NLP, dan Arahan Tindakan Pengurai *Mental Block* Kepemimpinan</b>.</p>
<a href="[LINK_PAYMENT_GATEWAY_LU_DISINI]" target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 BUKA AKSES PENUH DI SINI</div>
</a>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("🌌 Ruang Modifikasi Perilaku & Intervensi NLP")
        st.info("**Reset Ulang Pola Respons Negatif Anda**\n\nSistem mengolah struktur nama Anda untuk mengidentifikasi kecenderungan hambatannya. Nilai konversi tersebut disandingkan dengan parameter Asmaul Husna (sebagai mekanisme penenang/*Anchoring* spiritual) dan afirmasi terstruktur (Sugesti NLP). Rumusan metode ini dirancang untuk menetralisir sumber dominan *Mental Block* yang menahan kemajuan profesional Anda.")
        nama_ruhani = st.text_input("Konfirmasi Nama Lengkap Anda (Untuk Sinkronisasi Dzikir Dasar):", placeholder="Ketik nama identitas asli...", key="input_ruhani")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Generate Modul Panduan Terapi Diri", key="btn_ruhani"):
            if nama_ruhani and len(nama_ruhani.strip()) >= 3:
                try:
                    with st.spinner('Memproses ekstraksi pedoman penanganan *Mental Block* Anda...'): time.sleep(1.5)
                    st.toast("Protokol terapi sukses dijabarkan!", icon="✨")
                        
                    safe_nr = get_safe_firstname(nama_ruhani)
                    nilai_jummal_r = hitung_nama_esoterik(nama_ruhani)
                    r_num_r = nilai_jummal_r
                    while r_num_r > 9: r_num_r = sum(int(d) for d in str(r_num_r))
                    
                    asma_terapi, vibrasi_asma, tujuan_ruhani, jumlah_dzikir = proc_falak_ruhani(nilai_jummal_r, r_num_r, safe_nr)
                    protokol_nlp = get_protokol_terapi(r_num_r, safe_nr)
                    
                    st.markdown(f"""<div class="soft-fade" style="background: linear-gradient(135deg, rgba(10, 20, 40, 0.9) 0%, rgba(20, 10, 40, 0.9) 100%); border-left: 5px solid #00FFFF; padding: 25px; border-radius: 12px; margin-top: 20px; box-shadow: 0 8px 25px rgba(0, 255, 255, 0.15);">
<div style="text-align:center; border-bottom:1px solid #00FFFF; padding-bottom:10px; margin-bottom:20px;">
<span style="color:#00FFFF; font-size:16px; font-weight:900; letter-spacing:2px;">🧠 RESEP PROTOKOL INTERVENSI DIRI: BAPAK/IBU {safe_nr.upper()}</span>
</div>
<div style="margin-bottom: 20px;">
<b style="color:#ff4b4b; font-size:16px; letter-spacing:1px;">⚠️ EVALUASI HAMBATAN (Potensi Sabotase Pola Pikir):</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.7; display:inline-block; margin-top:8px;">{protokol_nlp['block']}</span>
</div>
<div style="background: rgba(0,0,0,0.5); padding: 18px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #00FFFF;">
<b style="color:#FFF; font-size:16px; letter-spacing:1px;">✨ 1. MEKANISME KETENANGAN SPIRITUAL (*ANCHORING* RUHANI)</b><br>
<span style="color:#aaa; font-size:14px; display:inline-block; margin-bottom:12px; line-height:1.6;">Panduan Penerapan: Gunakan lafaz Asma ini sebagai pengatur ritme pernapasan saat Anda dihadapkan pada tekanan pekerjaan atau kebuntuan pengambilan keputusan. Tarik napas secara perlahan, dan ucapkan di dalam batin secara berulang:</span><br>
<b style="color:#00FFFF; font-size:24px;">{asma_terapi}</b> <span style="color:#FFD700; font-weight:bold; font-size:16px; margin-left:10px; background:rgba(255,215,0,0.2); padding:4px 8px; border-radius:5px;">(BACA {jumlah_dzikir}x DALAM HATI)</span><br>
<i style="color:#ccc; font-size:14px; display:inline-block; margin-top:12px; padding-top:12px; border-top:1px dashed #444; line-height:1.6;"><b>Fungsi Utama Pengendalian Fokus:</b> {tujuan_ruhani}</i>
</div>
<div style="background: rgba(255,215,0,0.05); border-left: 4px solid #FFD700; padding: 18px; border-radius: 8px; margin-bottom: 20px;">
<b style="color:#FFD700; font-size:16px; letter-spacing:1px;">🗣️ 2. SUGESTI HYPNO-NLP (Afirmasi Penyelarasan Pola Pikir Ulang)</b><br>
<span style="color:#aaa; font-size:14px; display:inline-block; margin-bottom:12px; line-height:1.6;">Panduan Penerapan: Ulangi penegasan ini di dalam pikiran disertai dengan imajinasi visual dari kelegaan yang Anda harapkan. Sangat direkomendasikan dilakukan sekitar 5 menit sebelum Anda memasuki fase tidur (kondisi gelombang otak Theta yang mempermudah penerimaan sugesti mental):</span><br>
<div style="background: rgba(0,0,0,0.6); padding: 15px; border-radius:6px; border:1px solid rgba(255,215,0,0.2);"><i style="color:#fff; font-size:16px; line-height:1.7;">"{protokol_nlp['afirmasi']}"</i></div>
</div>
<div style="border-top: 1px dashed #555; padding-top: 20px; padding-bottom: 5px;">
<b style="color:#25D366; font-size:16px; letter-spacing:1px;">🏃‍♂️ 3. INTI INISIATIF (Tindakan Fundamental Hari Ini)</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.7; display:inline-block; margin-top:8px;">Hanya memahami secara rasional tidak akan menghasilkan perbaikan jika tanpa diiringi bukti tindakan konkrit. Sebagai pembuktian penolakan Anda terhadap sikap defensif masa lalu, paksakan diri Anda secara sadar untuk merealisasikan tugas spesifik ini hari ini:<br><br>
<div style="background: rgba(37,211,102,0.1); border: 1px solid #25D366; padding: 15px; border-radius: 8px;"><b style="color:#FFF; font-size:16px; line-height:1.6;">{protokol_nlp['habit']}</b></div></span>
</div>
<p style="font-size:13px; color:#ff4b4b; margin-top:25px; font-weight:bold; text-align:center;">⏳ Sistem menempatkan prioritas tinggi pada penguraian hambatan ini. Segera realisasikan 3 tindakan di atas SEKARANG JUGA sebelum pergantian fokus keseharian menenggelamkan komitmen tersebut!</p>
</div>""", unsafe_allow_html=True)
                except Exception as e: st.error(f"Terdapat kendala mesin dalam menurunkan protokol mendalam: {e}")
            else: st.warning("⚠️ Peringatan Input: Masukkan nama lengkap yang valid untuk keakuratan kalibrasi matriks.")

# ==========================================
# TAB 6 & 4
# ==========================================
with tab6:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("📚 Neuro-Insights: Peningkatan Kualitas Perspektif Manajerial")
    st.write("Jelajahi kerangka kerja mendalam dalam mengelola pemikiran, memodifikasi kebiasaan alam bawah sadar, dan mengintegrasikan wawasan esoterik Nusantara dengan kacamata analitik *Hypno-Copywriting* modern.")
    with st.expander("🧠 1. Mengapa Pertimbangan Rasional Seringkali Dimentahkan oleh Tarikan Emosional?"):
        st.markdown("""**Oleh: Coach Ahmad Septian (NLP Trainer & Hypnotherapist)**\n\nSebagian besar profesional menyalahartikan bahwa keputusan manajerial yang mereka buat didasarkan murni pada rasionalitas data. Faktanya, studi dalam keilmuan neuro-sains menemukan bahwa **95% dari tindakan manusia diinisiasi oleh perintah alam bawah sadar**—yang mana instruksi operasionalnya tidak berbentuk angka logika, melainkan berupa memori emosional atau sensasi 'Rasa'.\n\nSebagai contoh: Apabila rasionalitas Anda memberikan instruksi "Kirim penawaran sekarang untuk mendatangkan omset", namun di kedalaman pikiran bawah sadar tersimpan resistensi "Namun ada kekhawatiran besar ditolak yang menurunkan rasa aman", keputusan mana yang akhirnya tereksekusi? Emosi ketakutan seringkali mendominasi jalannya tindakan. Pikiran logis pada akhirnya difungsikan sekadar untuk mencari argumen pembenaran atas penundaan tersebut.\n\n**Metode Resolusi (NLP Reframing):** Perdebatan melawan pikiran sendiri seringkali berujung pada keletihan tanpa arah. Upaya yang lebih terarah adalah dengan mengubah asosiasi atau tarikan rasa (*Anchor*) pada suatu tindakan. Modifikasi pola pemikiran di dalam otak Anda dengan merangkaikan tindakan positif ("Pengambilan Risiko Berani") kepada hadiah emosional berupa "Sensasi Kelegaan yang Sangat Nyaman".""")
    with st.expander("💰 2. Dinamika Pengelolaan Finansial dan Relevansi Komposisi Nama (Hisab Jummal)"):
        st.markdown("""Apakah Anda merasa memiliki beban pekerjaan berlebih namun tingkat keuntungan finansial sering kali terasa sekadar singgah lalu menghilang dengan cepat? Atau, di saat keuntungan skala besar hadir, segera muncul situasi darurat yang memaksakan pengeluaran dadakan?\n\nDalam sudut pandang kalkulasi esoterik klasik Nusantara (termasuk kajian Hisab Jummal), interaksi kejadian bukan dilihat dari asas kebetulan. **Setiap sebutan identitas yang diucapkan berulang kali diyakini mentransmisikan daya stimulasi psikologis.** Jika sebuah nama mengandung dominasi unsur pendorong seperti "Api" tanpa diimbangi komponen peredam stabilitas seperti "Air", maka profil psikologis tersebut cenderung menciptakan respons yang reaktif dan gegabah dalam aspek investasi maupun manajemen material.\n\n**Metode Resolusi Taktis:** Anda tidak diwajibkan untuk merevisi identitas secara legal/administratif. Langkah adaptasi difokuskan pada pengadopsian frekuensi resonansi penyeimbang. Temukan metode penetralisir emosi (misalnya lafaz *Falak Ruhani*) untuk dijadikan sebuah jangkar mental (*Anchor*) di saat Anda dihadapkan pada persimpangan pengambilan keputusan material.""")
    with st.expander("⚡ 3. Sindrom Kepemimpinan Tunggal (Lone Wolf): Evaluasi Kritis terhadap Label 'Kemandirian'"):
        st.markdown("""Dalam budaya profesional saat ini, memegang banyak jabatan ganda (multitasking tanpa henti) terkadang terlihat heroik di permukaan. Anda memaksakan kapabilitas mengatur urusan produksi, penjualan, desain, sekaligus distribusi secara independen.\n\nNamun realitas evaluatifnya adalah: Apa yang dibingkai sebagai "Kemandirian Manajerial" ini seringkali hanyalah tameng pelindung atas kelemahan fundamental berupa **Rasa Kurang Aman (*Insecurity*) dan Kesulitan untuk Mendelegasikan Kekuasaan!** Anda terjebak dalam pemikiran bahwa tingkat kompetensi standar kerja orang lain seringkali lebih rendah dan berpotensi merugikan kinerja Anda.\n\nPadahal, prinsip manajemen sumber daya mengajarkan bahwa ekspansi kelimpahan terjadi melalui distribusi kerja kolektif (*Delegation & Collaboration*). Dengan mempertahankan sifat monopolistik di hampir seluruh ranah teknis, Anda memposisikan sistem saraf dan kemampuan fisik pada ambang keletihan fatal (*Burnout*). Efisiensi keuntungan tertinggi masuk melalui sistem operasional yang terdistribusi rapi, bukan pada kapasitas memikul kerja tanpa kenal waktu secara sendirian.""")
    st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("❓ Penjelasan Fungsional Sistem & Batasan Etika")
    with st.expander("🤔 1. Apakah sistem pemetaan Neuro Nada OS ini melibatkan unsur mistik tertentu?"): 
        st.write("Sistem ini tidak memuat afiliasi dengan pendekatan irasional, syirik, atau pun takhayul klinis. Neuro Nada OS merupakan instrumen observasi *cyber-esoteric* yang terstruktur. Platform ini memadukan pengolahan algoritma klasik atas aksara nama (pendekatan Gematria Arab / Hisab Jummal) dan kalibrasi kalender alam secara temporal (sistem Primbon Betaljemur Jawa). Keseluruhan nilai keluaran kemudian diinterpretasikan ulang dengan basis keilmuan NLP (*Neuro-Linguistic Programming*). Tidak ada janji mutlak tentang wawasan kejadian di masa depan. Platform ini dirancang sebagai sarana pengungkapan profil kesadaran, titik potensi *Blind Spot*, serta strategi mereset kecenderungan pola pikir agar Anda memiliki kesadaran penuh saat mengelola operasional (Fate Hacking).")
    with st.expander("🤔 2. Mengapa laporan analisis yang diberikan terkesan sangat terbuka, langsung, dan keras?"): 
        st.write("Layanan analisis ini murni dibangun atas asas penyampaian fakta objektivitas secara maksimal. Algoritma laporan **TIDAK** didesain untuk menjadi platform penyenang ego (*Sugar-Coating*). Tujuannya adalah untuk secara tegas membongkar habis kelemahan pola manajerial dan tabir penolakan (*Blind Spot* / *Shadow*) yang sering kali mati-matian ditutupi dalam keseharian. Kami meyakini bahwa langkah kematangan psikologis yang solid hanya bisa terbentuk ketika Anda siap menerima konfrontasi tulus mengenai ruang lingkup perbaikan diri tanpa pembiasan.")
    with st.expander("🤔 3. Seberapa esensial peran kepatuhan terhadap indikator kompas arah kerja ('Naga Dina')?"): 
        st.write("Di dalam teori penyelarasan frekuensi klasik, parameter arah gerak *Naga Dina* bertindak selayaknya teori fisika terhadap magnet bumi (*Geomansi*). Implementasi penyelarasan postur ke arah tersebut ditujukan untuk mengoptimalisasi sinkronisasi psikologis dan mengurangi pembiasan pikiran bawah sadar saat tengah fokus. Namun di atas semua aspek metafisika, logika dan kecakapan nyata dalam mengeksekusi rencana bisnis adalah faktor penentu utamanya (dengan rasio pembagian pengaruh di estimasi sekitar 90% determinasi pribadi dan 10% efek dorongan energi lingkungan).")
    st.markdown("<hr style='border-top: 1px dashed #555;'>", unsafe_allow_html=True)
    st.error("""**⚠️ BATASAN PERTANGGUNGJAWABAN HUKUM (DISCLAIMER PENGGUNAAN):**\nSetiap laporan hasil penelusuran identitas psikologis (*Decoding*), perkiraan waktu kosmik ideal, dan langkah rekomendasi terapeutik di atas diberikan murni sebagai fasilitator kesadaran diri (*Self-Awareness Tool*) yang bersifat eksperimental dan menumbuhkan literasi psikologis alternatif.\n\nPlatform analitik ini beserta seluruh tim *developer* (Coach Ahmad Septian) **SAMA SEKALI BUKAN** perwakilan entitas layanan pialang keuangan/investasi, penyedia tenaga medis yang tersertifikasi, konsultan psikologi klinis, maupun bentuk layanan hukum/kepastian medis.\n\nKewenangan penuh atas eksekusi finansial (perdagangan / investasi saham), komitmen status asmara, hingga pengambilan langkah hidup signifikan yang diputuskan pasca interaksi dengan materi konten aplikasi ini merupakan 100% konsekuensi sadar dari kebijakan mandiri pihak pengguna (*Free Will*). Hak penuh atas pengembang ditangguhkan dari potensi klaim mengenai kemungkinan kesalahan tafsir maupun kerugian terkait.""")
    st.markdown("</div>", unsafe_allow_html=True)
 
# ==========================================
# SOCIAL PROOF & FOOTER
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Riwayat Transformasi Diri dari Para Praktisi Evaluasi Karakter</h3>", unsafe_allow_html=True)
daftar_ulasan = ambil_ulasan()
if daftar_ulasan:
    marquee_content = " | ".join([f"<span style='color: #FFD700;'>{u.get('Rating', '⭐⭐⭐⭐⭐')}</span> <b>{u.get('Nama', 'User')}:</b> \"{u.get('Komentar', '')[:50]}...\"" for u in daftar_ulasan[:3]])
    st.markdown(f'<div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;"><marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">{marquee_content}</marquee></div>', unsafe_allow_html=True)
    for u in daftar_ulasan[:5]:
        if u.get("Komentar", ""): st.markdown(f'<div class="ulasan-box"><span style="color: #FFD700; font-size: 12px;">{u.get("Rating", "⭐⭐⭐⭐⭐")}</span><br><b style="font-size:15px;">{u.get("Nama", "Entitas")}</b><br><i style="color: #ccc; line-height:1.6; display:inline-block; margin-top:5px;">"{u.get("Komentar", "")}"</i></div>', unsafe_allow_html=True)

with st.expander("💬 Sampaikan Ulasan atau Kesan atas Temuan Resolusi Karakter Anda"):
    with st.form("form_review"):
        rn, rr, rk = st.text_input("Identitas Representatif Anda"), st.radio("Seberapa Akurat Pemetaan Kami terhadap Anda?", ["⭐⭐⭐⭐⭐ (Sangat Sesuai Realita)", "⭐⭐⭐⭐ (Mewakili Karakter Sehari-hari)", "⭐⭐⭐ (Cukup Tepat Sebagai Acuan)", "⭐⭐ (Perlu Penggalian Lanjut)", "⭐ (Tidak Berkaitan Penuh)"], horizontal=True), st.text_area("Silakan Jabarkan Temuan Menarik atau Kendala Ego Anda di Kolom Ini")
        if st.form_submit_button("Rekam Fakta Evaluasi Anda ke Sistem") and rn and rk:
            if kirim_ulasan(rn, rr.split(' ')[0], rk): 
                st.toast("Jejak refleksi berharga Anda sukses masuk ke pencatatan basis data pusat. Apresiasi tertinggi!", icon="🔥")
                time.sleep(1)
                st.rerun()
 
st.markdown("---")
st.markdown("<center><b style='color:#FFF; letter-spacing:1px; font-size:16px;'>Ahmad Septian Dwi Cahyo</b><br><span style='color:#888; font-size:13px; display:inline-block; margin-top:5px;'>Certified NLP Trainer & Professional Hypnotherapist<br>Hak Cipta © 2026 Neuro Nada Academy (Build-V4.4 Email Auth)</span></center>", unsafe_allow_html=True)
