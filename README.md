# Job Agent MVP

Job Agent, belirli bir meslek ve lokasyona ait güncel iş ilanlarını gerçek zamanlı olarak tarayan, toplanan verileri yapay zeka entegrasyonu ile analiz ederek kullanıcıya kapsamlı bir kariyer ve yetenek raporu sunan Python tabanlı bir asenkron masaüstü/mobil arayüz uygulamasıdır.

Bu proje, iş arayanların veya sektör analizi yapmak isteyen geliştiricilerin, pazarın mevcut beklentilerini (teknik beceriler, sosyal yetkinlikler, deneyim seviyeleri) saniyeler içinde tek bir raporda görmesini sağlar.

---

## Öne Çıkan Özellikler

*   **Gerçek Zamanlı Veri Motoru:** SerpApi (Google Organic Search Engine) entegrasyonu sayesinde hedef lokasyondaki en güncel iş fırsatlarını anlık olarak yakalar.
*   **Gelişmiş Yapay Zeka Analizi:** Çekilen ilan metinlerinin snippet'lerini gemini-2.5-flash(Uyumsuzluklardan dolayı geçici bir süre eski gemini sürümü kullandık) modeline besleyerek derinlemesine İK analizi yapar.
*   **Modern ve Dinamik Arayüz:** Flet framework'ü kullanılarak geliştirilmiş, karanlık mod (Dark Mode) destekli, duyarlı (responsive) ve modern bir kullanıcı deneyimi sunar.
*   **Donmayan Asenkron Yapı:** Arka planda çalışan çoklu iş parçacığı (threading) mimarisi sayesinde, API istekleri ve yapay zeka analizleri gerçekleştirilirken kullanıcı arayüzü asla donmaz veya kilitlenmez.

---

## Kullanılan Teknolojiler

*   **Python 3.x**
*   **Flet:** Flutter tabanlı Python UI Framework'ü
*   **Google Generative AI:** gemini-2.5-flash LLM modeli
*   **SerpApi:** Google Arama Motoru veri çekme servisi
*   **Requests:** HTTP istek yönetimi

---

## Proje Yapısı

```text
Job.Agent/
│
├── agent.py          # Uygulamanın tüm arayüz, veri ve yapay zeka mantığı
├── api.env           # API Anahtarlarının güvenli bir şekilde saklandığı yer (Yerel)
└── .gitignore        # Hassas verilerin GitHub'a yüklenmesini engelleyen kurallar
````
---------------------------
## Projeden birkaç ekran görüntüsü :


<img width="531" height="887" alt="image" src="https://github.com/user-attachments/assets/8d52d419-ccd8-49f0-a174-f2c12f6aa85c" />
<img width="542" height="895" alt="image" src="https://github.com/user-attachments/assets/88c664f9-0070-4586-9a77-62c30d97ae80" />
<img width="578" height="894" alt="image" src="https://github.com/user-attachments/assets/eff133f5-e424-41d2-9a6d-74acd382fc52" />
<img width="1020" height="676" alt="image" src="https://github.com/user-attachments/assets/fffe4ea9-7251-4de1-b623-cab1ccc0bfa7" />


