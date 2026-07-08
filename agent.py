import flet as ft
import requests
import google.generativeai as genai
import threading
import time

# --- 1. API ANAHTARLARI ---
GEMINI_API_KEY = "AIzaSyB3aFqXp-4oDoKO0MrH6etYfPpbUBkzObM"
SERPAPI_KEY = "b9c8b6231435deb405beac751443afe37cce25933370c1155745b159f168d3a9"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. VERİ MOTORU (SERPAPI ORGANİK ARAMA) ---
def ilanlari_getir_ve_temizle(meslek, lokasyon):
    url = "https://serpapi.com/search.json"
    
    # Strateji değişikliği: Özel iş ilanları modülü yerine, 
    # normal Google aramasını (engine: "google") kullanıyoruz.
    parametreler = {
        "engine": "google", 
        "q": f"{meslek} iş ilanları {lokasyon}", # Arama sorgumuzu özelleştirdik
        "hl": "tr",
        "gl": "tr",
        "api_key": SERPAPI_KEY
    }
    
    try:
        response = requests.get(url, params=parametreler)
        if response.status_code == 200:
            veri = response.json()
            
            # Artık 'jobs_results' yerine 'organic_results' (gerçek siteler) içinden çekiyoruz
            ilanlar = veri.get('organic_results', [])
            
            if not ilanlar:
                return None, f"'{meslek} {lokasyon}' için organik arama sonucu bulunamadı."
                
            birlesik_metin = ""
            
            # İlk 8 gerçek arama sonucunu alıyoruz
            for ilan in ilanlar[:8]: 
                baslik = ilan.get('title', 'Belirtilmemiş')
                # Arama sonuçlarındaki o kısa açıklama metni (snippet) bizim işimizi harika görecek
                aciklama = ilan.get('snippet', '') 
                
                # Sadece iş ilanı olduğundan emin olduğumuz anlamlı verileri alalım
                if aciklama:
                    birlesik_metin += f"İlan: {baslik}\nÖzet Açıklama: {aciklama}\n\n"
                
            return birlesik_metin, None
        else:
            return None, f"API Hatası: {response.status_code}"
    except Exception as e:
        return None, f"Bağlantı Hatası: {str(e)}"

# --- 3. ARAYÜZ VE SİSTEM ENTEGRASYONU ---
def main(page: ft.Page):
    page.theme_mode = 'Dark'
    page.window_width = 500
    page.window_height = 800
    page.title = "Job Agent MVP"

    msglv = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)

    # İş ilanı araması için iki ayrı kutu
    meslek_input = ft.TextField(hint_text="Meslek (Örn: Python Developer)", expand=True, border_radius=15, filled=True)
    lokasyon_input = ft.TextField(hint_text="Lokasyon (Örn: Türkiye veya Remote)", expand=True, border_radius=15, filled=True)

    def ai_msg(text):
        return ft.Container(
            content=ft.Markdown(value=text, selectable=True, code_theme="atom-one-dark"),
            alignment=ft.Alignment.CENTER_LEFT,
            padding=15,
            bgcolor=ft.Colors.BLUE_GREY_800,
            border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15, bottom_left=0),
            margin=ft.margin.only(right=50),
        )

    def user_msg(text):
        return ft.Container(
            content=ft.Text(text, color='white'),
            alignment=ft.Alignment.CENTER_RIGHT,
            padding=12,
            bgcolor=ft.Colors.BLUE_700,
            border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=0, bottom_left=15),
            margin=ft.margin.only(left=50),
        )

    def analiz_et(e):
        meslek = meslek_input.value.strip()
        lokasyon = lokasyon_input.value.strip()
        
        if not meslek:
            return 
        
        welcome_text.visible = False
        
        # Kullanıcının ne arattığını ekrana bas
        msglv.controls.append(user_msg(f"Arama: {meslek} - {lokasyon}"))
        loading_msg = ft.Text("İlanlar çekiliyor ve analiz ediliyor, lütfen bekleyin...", italic=True, color=ft.Colors.GREY_400)
        msglv.controls.append(loading_msg)
        # API'ler arası bağlantı süreceği için kullanıcıya bilgi ver
        meslek_input.value = ""
        lokasyon_input.value = ""
        page.update()
        
        time.sleep(0.1)
       

        # 2. Ağır işlemleri arka planda (thread) çalıştırarak ekranın donmasını engelle
        def arka_plan_isleme():
            # Aşama 1: İlanları Çek
            ilan_metinleri, hata = ilanlari_getir_ve_temizle(meslek, lokasyon)
            msglv.controls.remove(loading_msg)

            if hata:
                msglv.controls.append(ai_msg(f"**Sistem Hatası:** {hata}"))
            else:
                # Aşama 2: Yapay Zekaya (Gemini) Rapor Yazdır
                prompt = f"""
                Sen profesyonel bir İnsan Kaynakları ve Kariyer analistisin.
                Lütfen bu ilanları analiz et ve Türkçe bir rapor sun:
                
                **1. En Çok İstenen Teknik Yetenekler ve Diller**
                **2. Beklenen Sosyal Beceriler (Soft Skills)**
                **3. Genel Deneyim ve Ortak Beklentiler**
                
                İlan Metinleri:
                {ilan_metinleri}
                """
                try:
                    response = model.generate_content(prompt)
                    msglv.controls.append(ai_msg(response.text))
                except Exception as err:
                    msglv.controls.append(ai_msg(f"**Yapay Zeka Hatası:** {str(err)}"))

            page.update() # Sonuçlar geldiğinde ekranı tekrar güncelle

        # Arka plan işlemini başlat
        threading.Thread(target=arka_plan_isleme, daemon=True).start()

    welcome_text = ft.Container(
        content=ft.Text("Job Agent'a Hoşgeldiniz...", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE), text_align="center"),
        alignment=ft.Alignment.CENTER,
        expand=True,
    )

    # Arama kutuları ve buton tasarımı
    input_area = ft.Container(
        content=ft.Column([
            ft.Row([meslek_input, lokasyon_input]),
            ft.ElevatedButton(content=ft.Text("İlanları Bul ve Analiz Et"), icon=ft.Icons.SEARCH, on_click=analiz_et, width=600, height=50)
        ]),
        padding=ft.padding.all(20),
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
    )

    page.add(
        ft.Stack(
            controls=[
                welcome_text,
                ft.Column(controls=[msglv, input_area], expand=True)
            ],
            expand=True
        )
    )

ft.app(target=main)