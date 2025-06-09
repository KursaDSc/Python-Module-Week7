# Mentor Meeting Platformu (Python Module - Week 7 Project)

Bu proje, mentorluk sürecinde yapılan görüşmeleri organize etmek, aramak, filtrelemek ve analiz etmek için tasarlanmış bir masaüstü uygulamasıdır. PyQt6 kullanılarak geliştirilmiş bu uygulama, Google Sheets üzerinde tutulan verilerle etkileşimli çalışır.

## 🚀 Proje Amacı

Katılımcılar ile mentorlar arasında yapılan görüşmelerin kaydını tutmak, değerlendirme notlarını listelemek ve bu görüşmeleri daha verimli bir şekilde yönetmek amacıyla geliştirilmiştir.

---

## 🛠️ Kullanılan Teknolojiler

- **Python 3.10+**
- **PyQt6**
- **Google Sheets API**
- **gspread / oauth2client** (Google Sheets servisi için)
- **Object-oriented Design (OOP)**

---

## 📂 Proje Yapısı

Python-Module-Week7/
│
├── main.py # Uygulamanın başlangıç noktası
├── ui/
│ ├── login.ui # Giriş ekranı arayüzü
│ ├── mentor.ui # Mentor arayüzü
│ ├── participant.ui # Katılımcı arayüzü
│
├── pages/
│ ├── login_page.py # Giriş ekranı işlemleri
│ ├── mentor_page.py # Mentor ekranı işlemleri
│ └── participant_page.py # Katılımcı ekranı işlemleri
│
├── services/
│ ├── google_sheets_service.py # Google Sheets verisi okuma/yazma
│
├── config.py # Sayfa/sheet ayarları
└── README.md # Proje açıklamaları


---

## 🧭 Sayfa ve Dosya Açıklamaları

### 1. `main.py`

> Uygulamanın ana dosyasıdır. Kullanıcı arayüzünü başlatır ve giriş ekranını çağırır.

---

### 2. `login_page.py` & `login.ui`

> Kullanıcının rolüne göre (mentor veya katılımcı) uygun sayfaya yönlendirilmesini sağlar. Giriş ekranıdır.

- Giriş yapan kişinin adı ve rolüne göre yönlendirme yapar.
- Kullanıcı arayüzü `login.ui` dosyasında tanımlanmıştır.

---

### 3. `mentor_page.py` & `mentor.ui`

> Mentorların geçmiş görüşmeleri filtreleyerek görebileceği, değerlendirme yapabileceği ekrandır.

#### Temel Özellikler:
- Arama ve filtreleme (isim veya karar bazlı)
- Google Sheets üzerinden verileri çeker
- Başlıkları İngilizce'ye çevirir
- ToolTip ile içerik açıklamaları gösterir

---

### 4. `participant_page.py` & `participant.ui`

> Katılımcıların görüşme talep formunu doldurduğu arayüzdür.

#### Temel Özellikler:
- Katılımcı adı, müsaitlik durumu ve ilgilendiği alan gibi bilgiler girilir
- Form verileri doğrudan Google Sheets’e kaydedilir

---

### 5. `google_sheets_service.py`

> Google Sheets API üzerinden veri okuma ve yazma işlemlerini yapan servis katmanıdır.

---

### 6. `config.py`

> Google Sheets ID'leri, çalışma sayfası adları ve diğer yapılandırmaları içerir. Sayfalar arası ortak olarak kullanılır.

---

## 📸 Ekran Görüntüleri

- ![Login Screen](https://github.com/user-attachments/assets/dbe76fcf-f408-408e-b74f-57a006403d74)
- ![Mentor_Screen](https://github.com/user-attachments/assets/0bdacc67-7ffc-4d81-85f2-6fa679a20b4d)
---

## 🤝 Katkı Sağlayanlar

- **VIT-7 Team 1**

---

## 📄 Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Detaylı bilgi için `LICENSE` dosyasına bakabilirsiniz.
