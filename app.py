import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
import math
import plotly.graph_objects as go
import random
import csv
import io

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada Deep Analysis", 
    page_icon="🌌", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- CUSTOM CSS ---
st.markdown(
    """<style>
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        font-weight: 800 !important; border: none !important;
        padding: 12px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
        box-shadow: 0 4px 10px rgba(255,215,0,0.3);
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #FFC107 !important; }
    
    .cta-button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff0000 100%);
        color: white !important; padding: 15px; text-align: center; 
        border-radius: 8px; font-weight: 900; font-size: 16px; 
        box-shadow: 0 6px 15px rgba(255, 75, 75, 0.4);
        text-transform: uppercase; letter-spacing: 1px;
        transition: 0.3s;
    }
    .cta-button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255, 75, 75, 0.6); }

    .ulasan-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 12px; font-size: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .cosmic-box {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #4a4a8a;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 15px;
    }
    
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px;
        padding: 12px; background-color: #101010; border-radius: 10px;
        border: 1px solid #333; margin-bottom: 20px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    .matrix-item { flex: 1; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 16px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }
    
    .list-punchy { padding-left: 20px; margin-bottom: 15px; font-size: 15px; }
    .list-punchy li { margin-bottom: 8px; }
    </style>""", unsafe_allow_html=True
)

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa Kosmik"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

# ==========================================
# DATABASE CLOUD: GOOGLE SHEETS
# ==========================================
URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            decoded = response.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            # Balik urutan biar yang paling baru (terbawah di sheet) muncul duluan
            return [row for row in reader][::-1]
    except: return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        req = urllib.request.Request(URL_POST, data=data)
        urllib.request.urlopen(req)
        return True
    except: return False

# --- SIDEBAR PROMOSI & VIDEO ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        try: st.image("baru.jpg.png", use_container_width=True); st.markdown("<br>", unsafe_allow_html=True)
        except: pass
    elif os.path.exists("baru.jpg"): st.image("baru.jpg", use_container_width=True)

    st.markdown(f"### {get_greeting()}")
    st.markdown("### 🎬 Hypno-Video Vault")
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
    st.markdown("---")
    st.info("**Reset Pola Pikir Anda**\n\nMari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    st.markdown(f"[👉 **Amankan Jadwal Anda**](https://wa.me/628999771486?text={urllib.parse.quote('Halo Coach Ahmad, saya siap kalibrasi.')})")
    st.caption("© 2026 Neuro Nada Academy")

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900;'>🌌 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #D4AF37; margin-bottom:0;'>Meretas Realita Anda Melalui Kode Waktu Kelahiran</p>", unsafe_allow_html=True)
st.markdown("---")

tgl_today = datetime.date.today()

# --- DATABASE ARKETIPE ---
arketipe_punchy = {
    1: {"inti": "Sang Perintis yang lahir untuk memimpin, benci didikte, dan selalu fokus pada tujuan masa depan.", "kekuatan": ["Daya dobrak tinggi & berani ambil risiko", "Mandiri secara absolut", "Fokus eksekusi (Outcome-oriented)"]},
    2: {"inti": "Sang Penyelaras yang menjadi lem perekat hubungan, sangat peka membaca emosi lingkungan sekitar.", "kekuatan": ["Kapasitas empati level tinggi", "Negosiator & pencipta harmoni ulung", "Kemampuan adaptasi emosional (Rapport)"]},
    3: {"inti": "Sang Visioner dengan pikiran bak kembang api; kaya ide, ekspresif, dan magnetis dalam pergaulan.", "kekuatan": ["Komunikasi memikat (Persuasif)", "Kreativitas & imajinasi tanpa batas", "Ahli mencairkan suasana beku"]},
    4: {"inti": "Sang Transformator yang bertumpu pada struktur, detail, dan keteraturan hidup yang logis.", "kekuatan": ["Pola pikir sangat terstruktur & rapi", "Pekerja keras yang bisa diandalkan 100%", "Ketelitian tingkat dewa (Prosedural)"]},
    5: {"inti": "Sang Penggerak yang memuja kebebasan, haus petualangan, dan tercepat beradaptasi dengan perubahan.", "kekuatan": ["Kelincahan berpikir (Agility)", "Inovator & pemecah kebuntuan", "Keberanian mengeksplorasi hal baru"]},
    6: {"inti": "Sang Harmonizer yang menjadi pelindung natural, rela berkorban demi merawat lingkaran terdekatnya.", "kekuatan": ["Insting pengayom yang luar biasa", "Tanggung jawab moral level tinggi", "Loyalitas & dedikasi tanpa pamrih"]},
    7: {"inti": "Sang Legacy Builder yang haus kebenaran, pemikir mendalam, dan memiliki intuisi spiritual tajam.", "kekuatan": ["Kemampuan analisa (Deep Structure)", "Intuisi & firasat yang sering akurat", "Sangat selektif menilai kualitas"]},
    8: {"inti": "Sang Sovereign dengan visi kerajaan. Eksekutor ulung yang memancarkan otoritas dan kelimpahan materi.", "kekuatan": ["Tahan banting terhadap tekanan mental", "Insting bisnis & strategi tajam", "Kemampuan memegang kendali (Leader)"]},
    9: {"inti": "Sang Kesadaran Tinggi (Old Soul) yang memandang dunia secara holistik dengan idealisme luhur.", "kekuatan": ["Kebijaksanaan & pemikiran luas", "Kepedulian universal (Humanisme)", "Mampu melihat 'Big Picture' kehidupan"]}
}

arketipe_deskripsi = {
    1: "Anda lahir untuk memimpin dan membuka jalan. Arketipe ini memiliki dorongan internal yang kuat untuk mandiri dan benci jika harus didikte. Anda adalah pengambil risiko yang berani, namun seringkali merasa kesepian karena merasa harus memikul tanggung jawab sendirian.",
    2: "Anda adalah lem perekat dalam setiap hubungan. Bakat Anda adalah mendengarkan dan menciptakan harmoni. Arketipe ini sangat peka terhadap perasaan orang lain, namun seringkali kehilangan identitas diri karena terlalu sibuk menyenangkan orang lain (*People Pleaser*).",
    3: "Anda adalah pembawa pesan dan inspirasi. Pikiran Anda bekerja seperti kembang api; penuh warna dan ide kreatif. Anda pandai menarik perhatian, namun tantangan terbesar Anda adalah menyelesaikan apa yang sudah Anda mulai karena mudah teralihkan oleh hal baru.",
    4: "Anda adalah pembangun sistem. Keamanan, keteraturan, dan detail adalah nafas Anda. Anda sangat bisa diandalkan dan praktis. Namun, Arketipe ini sering terjebak dalam kekakuan dan stres luar biasa jika rencana hidup tidak berjalan sesuai jadwal.",
    5: "Anda adalah simbol kebebasan dan adaptasi. Arketipe ini haus akan pengalaman baru dan petualangan. Anda sangat cepat belajar hal baru, namun seringkali merasa hampa karena sulit menemukan 'rumah' atau tujuan tetap dalam jangka panjang.",
    6: "Anda adalah pengayom sejati. Fokus hidup Anda adalah melayani dan merawat orang-orang yang Anda cintai. Anda memiliki standar moral yang tinggi. Sisi gelapnya: Anda sering merasa dieksploitasi karena Anda memberi terlalu banyak tanpa batasan.",
    7: "Anda adalah pencari kebenaran dan makna terdalam. Pikiran Anda sangat tajam dan intuitif. Anda tidak puas dengan hal permukaan. Namun, Arketipe ini sering mengisolasi diri dan terjebak dalam labirin pikirannya sendiri (*Overthinking*).",
    8: "Anda adalah figur otoritas dan kelimpahan. Arketipe ini memiliki visi besar untuk membangun kerajaan finansial atau pengaruh sosial. Anda sangat tangguh, namun tantangan terbesar Anda adalah berdamai dengan sisi rapuh dan emosional dalam diri Anda.",
    9: "Anda adalah jiwa tua yang bijaksana. Anda peduli pada kemanusiaan dan cinta universal. Anda memandang dunia dengan kacamata holistik. Tantangannya: Anda sering merasa patah hati melihat realitas dunia yang tidak seindah idealisme Anda."
}

closing_brutal_dinamis = {
    1: ["Overthinking karena merasa hasil belum sempurna", "Gengsi minta tolong saat memikul beban sendirian", "Membangun tembok ego untuk menutupi rasa sepi"],
    2: ["Mengorbankan kebahagiaan diri demi ekspektasi orang lain", "Sulit berkata TIDAK yang berujung kelelahan mental", "Memendam amarah dalam hati demi menghindari konflik"],
    3: ["Menyembunyikan gelisah batin di balik topeng senyuman", "Cepat kehilangan motivasi jika rutinitas membosankan", "Insomnia karena pikiran terlalu berisik dan over-analisa"],
    4: ["Stres parah jika rencana mendadak berubah di luar kendali", "Terjebak di zona nyaman karena takut ambil resiko baru", "Sering dinilai terlalu dingin atau kaku oleh pasangan"],
    5: ["Sindrom Cepat Bosan yang mensabotase karya dan hubungan", "Kelelahan saraf karena otak tak pernah diizinkan istirahat", "Merasa hampa karena kehilangan pijakan komitmen"],
    6: ["Burnout ekstrim karena sibuk mengurus hidup orang lain", "Sikap Over-Protective yang diam-diam mengekang", "Rasa bersalah luar biasa jika memakai waktu untuk diri sendiri"],
    7: ["Menganalisa terus tanpa aksi nyata (Paralysis by Analysis)", "Merasa terasing karena merasa tak ada yang sepemikiran", "Mencurigai niat baik orang akibat luka masa lalu"],
    8: ["Merasa hampa dan kosong di saat mencapai puncak sukses", "Sangat sulit melepaskan kontrol dan memaafkan", "Memaksa tubuh bekerja dan mengabaikan alarm lelah"],
    9: ["Sering memaklumi orang toxic atas nama kasihan", "Patah hati hebat akibat ekspektasi berlebihan pada manusia", "Kelelahan batin memikirkan beban dunia yang bukan tanggung jawabnya"]
}

tips_zodiak_nlp = {
    "Aries": "Pacing dulu emosinya, baru perlahan Lead ke logika Anda.", "Taurus": "Berikan data logis, biarkan mereka merasa itu keputusannya.",
    "Gemini": "Ikuti ritme cepatnya; gunakan bahasa visual.", "Cancer": "Hati-hati nada suara; cara Anda bicara adalah segalanya.",
    "Leo": "Sentuh egonya dengan apresiasi tulus sebelum memberi kritik.", "Virgo": "Tarik perhatiannya dari detail ke Gambaran Besar.",
    "Libra": "Bantu mereka mengambil keputusan dari keinginan internal mereka.", "Scorpio": "Bangun trust terdalam; pantang berbohong sekecil apapun.",
    "Sagittarius": "Hubungkan masalah saat ini dengan visi masa depan.", "Capricorn": "Mulai dari logika fungsional, lalu turun ke emosional.",
    "Aquarius": "Sajikan ide anti-mainstream untuk memancing intelektualnya.", "Pisces": "Tarik perlahan ke fakta realita saat imajinasinya mulai negatif."
}

link_produk = {
    1: "http://lynk.id/neuronada/kj98l4zgzwdw/checkout", 2: "http://lynk.id/neuronada/6z23q03121lg/checkout",
    3: "http://lynk.id/neuronada/0rd6gr7nlzxp/checkout", 4: "http://lynk.id/neuronada/elp83loeyggg/checkout",
    5: "http://lynk.id/neuronada/wne9p4q1l3d9/checkout", 6: "http://lynk.id/neuronada/nm840y6nlo21/checkout",
    7: "http://lynk.id/neuronada/vv0797ll7g7o/checkout", 8: "http://lynk.id/neuronada/ropl1lm6rz8g/checkout",
    9: "http://lynk.id/neuronada/704ke23nzmgx/checkout"
}

# --- FUNGSI LOGIKA NUMERIK & FALAK ---
def get_arketipe(angka):
    arketipe_dict = {
        1: "The Leader (Sang Perintis)", 2: "The Mediator (Sang Penyelaras)", 
        3: "The Communicator (Sang Visioner)", 4: "The Architect (Sang Transformator)", 
        5: "The Explorer (Sang Penggerak)", 6: "The Nurturer (Sang Harmonizer)", 
        7: "The Analyst (Sang Legacy Builder)", 8: "The Strategist (Sang Sovereign)", 
        9: "The Humanist (Sang Kesadaran Tinggi)"
    }
    return arketipe_dict.get(angka, "Pribadi Unik")

def hitung_angka(tanggal):
    total = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def hitung_angka_nama(nama):
    huruf_angka = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':1, 'K':2, 'L':3, 'M':4, 'N':5, 'O':6, 'P':7, 'Q':8, 'R':9, 'S':1, 'T':2, 'U':3, 'V':4, 'W':5, 'X':6, 'Y':7, 'Z':8}
    total = sum(huruf_angka.get(h, 0) for h in nama.upper())
    if total == 0: return 1
    while total > 9: total = sum(int(d) for d in str(total))
    return total

def get_neptu_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari_n = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_n = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    hari = hari_n[tanggal.weekday()]
    pasaran = pasaran_n[selisih_hari % 5]
    n_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    n_pas = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    return (n_hari[hari] + n_pas[pasaran]), f"{hari} {pasaran}"

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

def get_birth_moon(date):
    epoch = datetime.date(2000, 1, 6)
    days = (date - epoch).days
    lunations = days / 29.53058867
    p = lunations % 1
    if p < 0.03 or p > 0.97: return "🌑 New Moon (Bulan Baru)", "Kekuatan internal sangat tajam. Anda menyerap banyak energi dari alam bawah sadar.", "Menyusun target besar secara diam-diam dan rahasia.", "Terlalu cepat mencari validasi dan persetujuan dari orang luar."
    elif p < 0.22: return "🌒 Waxing Crescent (Bulan Sabit Awal)", "Dorongan batin tinggi untuk bertumbuh dan sangat mudah menarik peluang baru.", "Berani mengambil eksekusi konkrit pada ide pertama Anda.", "Menunda pekerjaan karena keraguan dan rasa pesimis bawaan."
    elif p < 0.28: return "🌓 First Quarter (Paruh Awal)", "Karakter petarung yang aktif. Otak Anda bereaksi sangat cepat saat menghadapi krisis.", "Mengambil risiko terukur dan memecahkan masalah mendadak.", "Menyerah pada rintangan teknis atau bertindak ceroboh tanpa data."
    elif p < 0.47: return "🌔 Waxing Gibbous (Bulan Cembung Awal)", "Perfeksionis dan teliti. Anda terus mengevaluasi segala hal menuju titik sempurna.", "Memperhatikan detail pekerjaan dan mengasah skill spesifik.", "Mengabaikan kritik membangun karena merasa diri paling benar."
    elif p < 0.53: return "🌕 Full Moon (Bulan Purnama)", "Gelombang otak dalam frekuensi puncak. Anda sangat karismatik namun rentan meledak.", "Tampil memimpin di depan publik dan menginspirasi massa.", "Membuat keputusan emosional atau berdebat keras dengan pasangan."
    elif p < 0.72: return "🌖 Waning Gibbous (Bulan Cembung Akhir)", "Bakat alami sebagai Mentor. Anda merasa damai ketika bisa mendistribusikan ilmu.", "Berbagi pengalaman dan menjadi penengah yang bijak bagi sahabat.", "Menyombongkan kesuksesan masa lalu dan enggan beradaptasi."
    elif p < 0.78: return "🌗 Last Quarter (Paruh Akhir)", "Berani mengambil keputusan ekstrem untuk membuang hal yang tidak lagi berguna.", "Membersihkan lingkaran pertemanan toxic dan merapikan hidup.", "Menyimpan dendam, terikat masa lalu, dan bernostalgia pada luka."
    else: return "🌘 Waning Crescent (Bulan Sabit Akhir)", "Memancarkan energi 'Healer' intuitif. Sangat peka pada akhir dari sebuah siklus kehidupan.", "Merawat diri sendiri dan melepaskan ekspektasi berlebihan pada manusia.", "Memaksakan tubuh untuk bekerja ekstra keras mengejar ambisi materi semata."

def get_daily_dynamic_sync():
    today = datetime.date.today()
    epoch = datetime.date(2000, 1, 6)
    days = (today - epoch).days
    lunations = days / 29.53058867
    p = lunations % 1
    energy_score = int(math.sin(p * math.pi) * 100)
    
    fase_info = {
        "New Moon": ("🌑 New Moon (Bulan Baru)", "Energi semesta sedang kosong (Fase Awal). Waktu terbaik untuk merenung dan mereset niat."),
        "Waxing Crescent": ("🌒 Waxing Crescent (Bulan Sabit Awal)", "Energi mulai bertumbuh (Fase Pembenihan). Bagus untuk eksekusi langkah awal."),
        "First Quarter": ("🌓 First Quarter (Paruh Awal)", "Fase krisis dan aksi. Gesekan energi tinggi, butuh keberanian mengambil keputusan cepat."),
        "Waxing Gibbous": ("🌔 Waxing Gibbous (Bulan Cembung Awal)", "Fase penyempurnaan dan evaluasi detail sebelum mencapai puncak target."),
        "Full Moon": ("🌕 Full Moon (Bulan Purnama)", "Puncak energi emosional dan magnetis. Tarikan gravitasi semesta sedang berada di titik terkuat."),
        "Waning Gibbous": ("🌖 Waning Gibbous (Bulan Cembung Akhir)", "Fase membagikan hasil (Distribusi). Waktu terbaik untuk berbagi dan mentoring orang lain."),
        "Last Quarter": ("🌗 Last Quarter (Paruh Akhir)", "Fase pelepasan. Waktu yang sangat tepat untuk membuang beban batin dan kebiasaan buruk."),
        "Waning Crescent": ("🌘 Waning Crescent (Bulan Sabit Akhir)", "Fase istirahat dan pemulihan sistem saraf secara total sebelum siklus bulan yang baru dimulai.")
    }
    
    daily_do = {
        "New Moon": ["Reset niat dan susun blueprint jangka panjang hari ini.", "Waktu emas untuk merenung dan merencanakan target baru.", "Fokus ke dalam diri, matangkan strategi sebelum eksekusi."],
        "Waxing Crescent": ["Baterai mulai terisi. Eksekusi ide konkrit pertama Anda sekarang!", "Lakukan langkah kecil namun pasti menuju target Anda.", "Buka relasi baru, momentum sedang berpihak pada Anda."],
        "First Quarter": ["Pecahkan rintangan keras hari ini. Otak Anda sangat reaktif!", "Ambil keputusan berani, ini saatnya unjuk gigi.", "Hadapi masalah yang selama ini Anda hindari."],
        "Waxing Gibbous": ["Fokus tinggi! Sempurnakan detail dan asah skill teknis Anda.", "Cek ulang semua pekerjaan, pastikan kualitasnya sempurna.", "Fase penyempurnaan, lakukan evaluasi mikro hari ini."],
        "Full Moon": ["Puncak daya tarik magnetis! Launching karya atau perluas networking.", "Ekspresikan diri Anda, aura Anda sedang memancar maksimal.", "Waktu yang tepat untuk tampil di depan publik."],
        "Waning Gibbous": ["Fase syukur. Bagikan pengalaman dan mentoring ke orang lain.", "Traktir teman, sedekah, atau apresiasi tim Anda.", "Sebarkan energi positif dan ilmu yang Anda punya."],
        "Last Quarter": ["Pembersihan total! Putuskan hubungan toxic dan kebiasaan buruk.", "Detoks digital, rapikan area kerja Anda.", "Evaluasi dan buang strategi yang terbukti gagal."],
        "Waning Crescent": ["Fase penyembuhan batin. Istirahatkan sistem saraf Anda.", "Lakukan me-time, meditasi, atau nikmati hobi ringan.", "Maafkan diri Anda untuk kesalahan kemarin."]
    }
    
    daily_dont = {
        "New Moon": ["Terburu-buru mencari validasi publik atau pamer progres.", "Memulai konflik yang tidak perlu demi ego sesaat.", "Grasa-grusu mengambil keputusan tanpa data valid."],
        "Waxing Crescent": ["Prokrastinasi dan meragukan kemampuan diri sendiri.", "Terlalu banyak mikir sampai lupa bertindak (Overthinking).", "Mendengarkan kritik dari orang yang tidak selevel."],
        "First Quarter": ["Menyerah pada halangan teknis pertama yang muncul.", "Menghindari tanggung jawab karena takut gagal.", "Mencari jalan pintas yang merugikan etika kerja."],
        "Waxing Gibbous": ["Cepat puas dan mengabaikan kritik membangun.", "Terjebak ilusi kesempurnaan (Perfeksionis berlebihan).", "Meremehkan detail kecil yang sebenarnya krusial."],
        "Full Moon": ["Berdebat emosional dan membuat keputusan reaktif.", "Terpancing provokasi atau drama di sosial media.", "Membiarkan ego mendominasi percakapan penting."],
        "Waning Gibbous": ["Egois, pelit ilmu, dan menolak perubahan.", "Menyombongkan diri atas pencapaian masa lalu.", "Menahan hak atau rezeki orang lain."],
        "Last Quarter": ["Menyimpan dendam dan bernostalgia pada masa lalu kelam.", "Ragu-ragu membuang barang atau emosi rongsokan.", "Kembali ke kebiasaan buruk yang sudah ditinggalkan."],
        "Waning Crescent": ["Memaksakan diri bekerja ekstra keras (Hustle culture).", "Memulai proyek raksasa dari nol saat energi habis.", "Begadang dan menguras tenaga untuk hal tidak penting."]
    }
    
    if p < 0.03 or p > 0.97: k = "New Moon"
    elif p < 0.22: k = "Waxing Crescent"
    elif p < 0.28: k = "First Quarter"
    elif p < 0.47: k = "Waxing Gibbous"
    elif p < 0.53: k = "Full Moon"
    elif p < 0.72: k = "Waning Gibbous"
    elif p < 0.78: k = "Last Quarter"
    else: k = "Waning Crescent"
    
    phase_emoji, phase_desc = fase_info[k]
    return phase_emoji, phase_desc, energy_score, random.choice(daily_do[k]), random.choice(daily_dont[k])

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Sistem Saraf"])

# ==========================================
# TAB 1: IDENTITAS KOSMIK 
# ==========================================
with tab1:
    st.subheader("Akses Blueprint Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama asli Anda...", key="t1_nama")
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1995, 1, 1), min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")

    if st.button("Kalkulasi Blueprint (Mulai)"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Mohon ketik nama lengkap untuk sinkronisasi vibrasi.")
        elif tgl_input == tgl_today: 
            st.error("🚨 Tanggal lahir tidak valid.")
        else:
            status_text = st.empty()
            status_text.markdown("⏳ *Menghubungkan ke gelombang kosmik...*")
            time.sleep(0.7)
            status_text.markdown("⏳ *Mengekstraksi sandi tanggal lahir & Weton...*")
            time.sleep(0.7)
            status_text.markdown("⏳ *Mendeteksi konflik batin dan pola sabotase diri...*")
            time.sleep(0.9)
            status_text.empty()
            
            angka_hasil = hitung_angka(tgl_input)
            angka_nama = hitung_angka_nama(nama_user)
            nep, wet = get_neptu_weton(tgl_input)
            zod = get_zodiak(tgl_input)
            ark_n = get_arketipe(angka_hasil)
            
            m_phase, m_sifat, m_do, m_dont = get_birth_moon(tgl_input)
            today_phase, today_desc, today_energy, today_do, today_dont = get_daily_dynamic_sync()
            
            punchy = arketipe_punchy.get(angka_hasil)
            desk_ark = arketipe_deskripsi.get(angka_hasil)
            shadow = closing_brutal_dinamis.get(angka_hasil)
            
            hook_text = random.choice([
                "Sistem mendeteksi adanya anomali unik pada arketipe Anda.",
                "Ada pola tersembunyi yang jarang Anda sadari selama ini.",
                "Gelombang bawah sadar Anda menunjukkan sinkronisasi yang menarik."
            ])
            
            st.snow()
            st.markdown(f"<h3 style='text-align:center;'>🌌 Blueprint Kosmik: {nama_user.upper()}</h3>", unsafe_allow_html=True)
            
            # --- DAILY GUIDANCE KOSMIK (WARNA DINAMIS + KETERANGAN FASE) ---
            if today_energy > 70: warna_baterai, glow = "#25D366", "rgba(37, 211, 102, 0.5)"
            elif today_energy > 40: warna_baterai, glow = "#FFD700", "rgba(255, 215, 0, 0.5)"
            else: warna_baterai, glow = "#ff4b4b", "rgba(255, 75, 75, 0.5)"
            
            st.markdown(f"""
            <div class="cosmic-box" style="box-shadow: 0 4px 15px {glow};">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #333; padding-bottom:10px; margin-bottom:10px;">
                    <span style="color:#888; font-size:12px; font-weight:bold; letter-spacing:1px;">DAILY SYNC (HARI INI)</span>
                    <span style="color:{warna_baterai}; font-weight:900; font-size:14px; text-shadow: 0 0 8px {warna_baterai};">BATERAI EMOSI: {today_energy}%</span>
                </div>
                <div style="font-size:14px; line-height:1.6; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px dashed #444;">
                    <span style="color:#aaa;">Fase Semesta Hari Ini:</span> <b style="color:white; font-size:15px;">{today_phase}</b><br>
                    <i style="color:#ccc; font-size:13px;">"{today_desc}"</i>
                </div>
                <div style="font-size:14px; line-height:1.6;">
                    <span style="color:#FFD700;">✅ <b>FOKUS HARI INI:</b></span> {today_do}<br>
                    <span style="color:#ff4b4b;">❌ <b>HINDARI:</b></span> {today_dont}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="matrix-container">
                <div class="matrix-item"><div class="matrix-label">Kode Nama</div><div class="matrix-value matrix-value-special">{angka_nama}</div></div>
                <div class="matrix-item"><div class="matrix-label">Kode Program</div><div class="matrix-value matrix-value-special">{angka_hasil}</div></div>
                <div class="matrix-item"><div class="matrix-label">Energi Weton</div><div class="matrix-value">{wet}</div></div>
                <div class="matrix-item"><div class="matrix-label">Pola Zodiak</div><div class="matrix-value">{zod}</div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- THE DEEP READING ---
            st.markdown("### 👁️ Decode Kepribadian Bawah Sadar")
            st.info(f"*{hook_text}* Perpaduan frekuensi weton **{wet}** dan zodiak **{zod}** melahirkan arketipe unik dalam diri Anda:\n\n**IDENTITAS INTI:** {punchy['inti']}")
            
            st.subheader(f"🧬 Penjelasan Mendalam: {ark_n}")
            st.write(desk_ark)
            
            st.markdown("🔥 **3 KEKUATAN DOMINAN:**")
            st.markdown(f"""
            <ul class="list-punchy" style="color:#25D366;">
                <li>{punchy['kekuatan'][0]}</li>
                <li>{punchy['kekuatan'][1]}</li>
                <li>{punchy['kekuatan'][2]}</li>
            </ul>
            """, unsafe_allow_html=True)
            
            st.markdown("⚠️ **SISI GELAP (SHADOW SELF):**")
            st.markdown(f"""
            <ul class="list-punchy" style="color:#ff4b4b;">
                <li>{shadow[0]}</li>
                <li>{shadow[1]}</li>
                <li>{shadow[2]}</li>
            </ul>
            """, unsafe_allow_html=True)
            
            # --- PENJELASAN FALAK KELAHIRAN ---
            st.markdown("---")
            st.subheader("🌑 Energi Bawah Sadar (Fase Bulan Lahir)")
            st.write(f"Sistem kosmik mencatat Anda lahir pada fase **{m_phase}**. {m_sifat}")
            c_f_do, c_f_dont = st.columns(2)
            c_f_do.success(f"✅ **POTENSI ALAMI:**\n{m_do}")
            c_f_dont.error(f"❌ **RESIKO BAWAAN:**\n{m_dont}")
            
            # --- PSYCHOLOGICAL CTA ---
            st.markdown("<br>", unsafe_allow_html=True)
            url_t = link_produk.get(angka_hasil, "https://lynk.id/neuronada")
            st.markdown(f"""
            <a href="{url_t}" target="_blank" style="text-decoration: none;">
                <div class="cta-button">
                    ⚠️ BONGKAR MENTAL BLOCK KODE {angka_hasil} & REBUT KENDALI HIDUP ANDA
                </div>
            </a>
            """, unsafe_allow_html=True)
            st.caption("<center>Modul PDF ini memuat skrip re-programming alam bawah sadar khusus untuk mematikan pola sabotase diri Anda.</center>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("<h4 style='text-align:center;'>🚀 Tindakan Ekstra</h4>", unsafe_allow_html=True)
            wa_text = f"Coach Ahmad, saya merinding baca hasil mapping Kode {angka_hasil}. Saya capek jadi korban 'Shadow Self'. Saya siap kalibrasi di Private Session."
            c_share, c_wa = st.columns(2)
            
            with c_share:
                wa_share = f"Gila, akurat banget! Blueprint bawah sadar gue kebongkar semua. Cobain cek identitas kosmik lu di sini: https://lynk.id/neuronada"
                st.markdown(f"<a href='https://api.whatsapp.com/send?text={urllib.parse.quote(wa_share)}' target='_blank'><div style='background-color:#333; color:white; padding:10px; text-align:center; border-radius:8px; font-weight:bold;'>📤 Bagikan ke Status / Teman</div></a>", unsafe_allow_html=True)
            with c_wa:
                st.markdown(f"<a href='https://wa.me/628999771486?text={urllib.parse.quote(wa_text)}' target='_blank'><div style='background-color:#25D366; color:white; padding:10px; text-align:center; border-radius:8px; font-weight:bold;'>📲 Tanya Jadwal Private</div></a>", unsafe_allow_html=True)

# ==========================================
# TAB 2: COUPLE SYNC 
# ==========================================
with tab2:
    st.subheader("Sinkronisasi Asmara")
    st.write("Analisis benturan ego dan resonansi kosmik antara Anda dan pasangan.")
    ca, cb = st.columns(2)
    with ca: 
        n1 = st.text_input("Nama Anda", key="n1")
        d1 = st.date_input("Lahir Anda", value=datetime.date(1995, 1, 1), min_value=datetime.date(1940, 1, 1), max_value=tgl_today, key="d1")
    with cb: 
        n2 = st.text_input("Nama Pasangan", key="n2")
        d2 = st.date_input("Lahir Pasangan", value=datetime.date(1995, 1, 1), min_value=datetime.date(1940, 1, 1), max_value=tgl_today, key="d2")
        
    if st.button("Cek Kompatibilitas Bawah Sadar"):
        if n1 and n2:
            st.snow()
            
            zod1 = get_zodiak(d1); ne_1, we_1 = get_neptu_weton(d1)
            m_phase1, _, _, _ = get_birth_moon(d1)
            fase1_nama = m_phase1.split(" ", 1)[1] 
            
            zod2 = get_zodiak(d2); ne_2, we_2 = get_neptu_weton(d2)
            m_phase2, _, _, _ = get_birth_moon(d2)
            fase2_nama = m_phase2.split(" ", 1)[1]
            
            sel = abs(hitung_angka(d1) - hitung_angka(d2))
            sisa_weton = (ne_1 + ne_2) % 8
            
            hasil_weton_kombo = {
                1: ("💔 PEGAT (Ujian Ego)", "Terdapat perbedaan mendasar dalam cara memproses emosi dan dominasi ego.", "Turunkan ego. Gunakan teknik Pacing (menyelaraskan) sebelum berargumen dengan pasangan.", "Mind-Reading (berharap pasangan peka tanpa diberi tahu) dan mengungkit masa lalu."),
                2: ("👑 RATU (Kharisma & Harmoni)", "Penyatuan vibrasi ini memancarkan wibawa. Orang sekitar segan melihat kalian.", "Fokus pada apresiasi harian. Jadikan pasangan sebagai partner diskusi strategis.", "Terjebak pencitraan eksternal (terlihat sempurna di luar tapi rapuh saat berdua)."),
                3: ("💞 JODOH (Sinkronisasi Alami)", "Penerimaan bawah sadar luar biasa tinggi. Kalian seperti sudah saling mengenal lama.", "Ciptakan kejutan-kejutan spontan agar romansa tidak monoton.", "Terjebak di zona nyaman yang membosankan dan berhenti meng-upgrade diri."),
                4: ("🌱 TOPO (Ujian Bertumbuh)", "Awal hubungan butuh banyak kalibrasi, namun akan sangat solid jika melewati badai.", "Kuasai teknik Reframing (ubah sudut pandang) saat krisis melanda.", "Memaksakan standar nilai pribadi ke pasangan dan bersikap kaku."),
                5: ("💰 TINARI (Magnet Rezeki)", "Vibrasi kalian jika disatukan akan menarik kelancaran finansial dan hoki.", "Bangun nilai spiritual bersama, kolaborasi dalam ide atau bisnis.", "Menjadikan materi atau uang sebagai satu-satunya perekat hubungan."),
                6: ("⚡ PADU (Beda Frekuensi)", "Sering terjadi letupan perdebatan karena beda cara filter informasi di otak.", "Validasi emosinya lebih dulu sebelum membantah logikanya (Teknik Yes-Set).", "Konfrontasi langsung saat emosi sedang tinggi (Baterai Emosi sedang merah)."),
                7: ("👁️ SUJANAN (Rawan Asumsi)", "Ada kecenderungan muncul rasa insecure, cemburu, atau salah paham mendadak.", "Buka komunikasi transparan, bicarakan sesuatu murni berdasarkan fakta.", "Menggunakan bahasa generalisasi ('Kamu selalu begini', 'Kamu gapernah gitu')."),
                0: ("🕊️ PESTHI (Damai & Rukun)", "Hubungan yang stabil, adem ayem, dan jauh dari drama penguras energi mental.", "Rutin mencari aktivitas, liburan, atau hobi baru bersama.", "Saking damainya bisa terasa hambar, jangan biarkan api asmara padam begitu saja.")
            }
            
            judul_weton, desk_weton, saran_do, saran_dont = hasil_weton_kombo.get(sisa_weton, ("Analisa Unik", "Butuh kalibrasi", "Perbaiki komunikasi", "Jangan egois"))
            
            st.markdown("---")
            st.markdown(f"### 🔮 Analisis Resonansi: {n1.split()[0].capitalize()} & {n2.split()[0].capitalize()}")
            st.info(f"Menyatukan filter pikiran **{zod1}** dengan **{zod2}** ibarat menggabungkan dua elemen alam. Secara Falak, frekuensi kosmik **{fase1_nama}** milikmu berbenturan dan beresonansi dengan energi **{fase2_nama}** pasangan. Ditambah akar budaya **{we_1}** dan **{we_2}**, kombinasi ini membentuk ikatan yang sangat spesifik:")
            
            st.markdown(f"#### {judul_weton}")
            st.write(desk_weton)
            
            if sel in [0, 3, 6, 9]: st.success("💘 **SKOR META-PROGRAM (NLP): 90% (Sangat Sinkron)**\nSangat mudah memahami *Love Language* satu sama lain tanpa banyak bicara.")
            elif sel in [1, 2, 8]: st.warning("⚖️ **SKOR META-PROGRAM (NLP): 70% (Dinamis)**\nBanyak beda sudut pandang, butuh kedewasaan untuk saling melengkapi.")
            else: st.error("🔥 **SKOR META-PROGRAM (NLP): 50% (Rawan Gesekan)**\nEgo tinggi sering berbenturan keras. Butuh teknik komunikasi bawah sadar khusus.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Berdasarkan Kalkulasi Di Atas, Ini Panduan Hubungan Anda:**")
            c_do_c, c_dont_c = st.columns(2)
            with c_do_c:
                st.success(f"✅ **LAKUKAN INI:**\n\n{saran_do}")
            with c_dont_c:
                st.error(f"❌ **HINDARI INI:**\n\n{saran_dont}")

# ==========================================
# TAB 3: AUDIT SISTEM SARAF
# ==========================================
with tab3:
    st.subheader("🕸️ Audit Sistem Saraf (Wheel of Life)")
    
    st.info("**Apa itu Audit Sistem Saraf?**\n\nDalam dunia psikologi dan NLP, energi manusia mengalir layaknya jaring roda. Jika satu area mendapat skor sangat rendah, roda hidup Anda akan 'oleng' dan menciptakan kebocoran energi *(Burnout)* yang menghambat kesuksesan di area lain. Geser *slider* di bawah ini sejujur-jujurnya untuk melihat di mana letak kebocoran energi Anda saat ini.")

    kategori_label = ['Kesehatan Mental', 'Karir & Finansial', 'Asmara', 'Spiritual', 'Fisik']
    sk = [st.slider(k, 1, 10, 5) for k in kategori_label]
    
    if st.button("Mulai Audit Radar"):
        fig = go.Figure(data=go.Scatterpolar(
            r=sk+[sk[0]], 
            theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], 
            fill='toself', 
            fillcolor='rgba(212, 175, 55, 0.4)', 
            line=dict(color='#D4AF37')
        ))
        st.plotly_chart(fig)
        
        avg = sum(sk)/5
        
        pesan_rendah = [
            "🚨 **KONDISI KRITIS (ALARM BAWAH SADAR BERBUNYI)**\n\nSistem saraf Anda sedang kelelahan parah. Jangan paksa mesin tetap berjalan jika olinya habis. Anda butuh 'Detoks Mental' secepatnya sebelum berujung pada psikosomatis (sakit fisik karena pikiran).",
            "⚠️ **KEBOCORAN ENERGI FATAL**\n\nGrafik Anda melesak ke dalam. Roda kehidupan Anda sedang sangat oleng. Berhenti sejenak, ini bukan waktunya mengejar dunia, tapi waktunya menyelamatkan kewarasan batin Anda."
        ]
        
        pesan_sedang = [
            "⚖️ **FASE STAGNAN (ADA REM TANGAN YANG MENAHAN)**\n\nKondisi Anda cukup aman, namun tidak maksimal. Anda merasa 'oke' tapi sebenarnya jalan di tempat. Tutup celah pada area dengan skor terendah agar Anda bisa melesat tanpa beban.",
            "🟡 **ZONA NYAMAN YANG MENIPU**\n\nSistem mendeteksi Anda memendam potensi besar yang tertahan oleh satu atau dua masalah yang belum tuntas. Selesaikan area terlemah Anda, dan lihat keajaiban mulai terjadi hari ini."
        ]
        
        pesan_tinggi = [
            "🔥 **PEAK STATE (GELOMBANG EMAS)**\n\nLuar biasa! Sinkronisasi otak dan tindakan Anda sedang sangat sempurna. Roda berputar mulus. Ini adalah momentum terbaik untuk mengambil keputusan besar dan mengeksekusi visi Anda!",
            "🌟 **HIGH PERFORMANCE MODE**\n\nJaring energi Anda sangat kuat dan seimbang. Anda memancarkan aura magnetis yang akan menarik peluang, rezeki, dan keberuntungan dengan sangat mudah."
        ]

        st.markdown("---")
        if avg < 5: 
            st.error(random.choice(pesan_rendah))
        elif avg < 8: 
            st.warning(random.choice(pesan_sedang))
        else: 
            st.success(random.choice(pesan_tinggi))

# ==========================================
# SOCIAL PROOF (ULASAN DINAMIS)
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Transformasi</h3>", unsafe_allow_html=True)

# Ambil data real dari Google Sheets
daftar_ulasan = ambil_ulasan()

if daftar_ulasan:
    # Marquee (Running Text) menggunakan data dinamis (3 data terbaru)
    pilihan_marquee = daftar_ulasan[:3]
    marquee_content = " | ".join([f"<span style='color: #FFD700;'>{u.get('Rating', '⭐⭐⭐⭐⭐')}</span> <b>{u.get('Nama', 'User')}:</b> \"{u.get('Komentar', '')[:50]}...\"" for u in pilihan_marquee])
    
    marquee_html = f"""
    <div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;">
        <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">
            {marquee_content}
        </marquee>
    </div>
    """
    st.markdown(marquee_html, unsafe_allow_html=True)

    # List Testimoni (5 Real Rating Terkini)
    for u in daftar_ulasan[:5]:
        nama_klien = u.get("Nama", "Jiwa Kosmik")
        rating_klien = u.get("Rating", "⭐⭐⭐⭐⭐")
        komentar_klien = u.get("Komentar", "")
        
        if komentar_klien: # Hanya tampilkan jika ada komentar
            st.markdown(f"""
            <div class="ulasan-box">
                <span style="color: #FFD700; font-size: 12px;">{rating_klien}</span><br>
                <b>{nama_klien}</b><br>
                <i style="color: #ccc;">"{komentar_klien}"</i>
            </div>
            """, unsafe_allow_html=True)
else:
    st.caption("<center>Belum ada ulasan terbaru.</center>", unsafe_allow_html=True)

with st.expander("💬 Bagikan Pengalaman Anda"):
    with st.form("form_review"):
        rn = st.text_input("Nama")
        rr = st.radio("Rating Bintang", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐"], horizontal=True)
        rk = st.text_area("Ulasan (Gimana akurasinya?)")
        if st.form_submit_button("Kirim Ulasan") and rn and rk:
            if kirim_ulasan(rn, rr, rk): 
                st.success("Terkirim! Testimoni Anda akan muncul setelah refresh.")
                time.sleep(1)
                st.rerun()

st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Certified NLP Trainer & Professional Hypnotherapist © 2026</small></center>", unsafe_allow_html=True)
