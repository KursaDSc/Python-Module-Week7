Project: Python Module - CRM v2 Interface Development
Team Size: 5 Members (1 Team Leader, 4 Developers/UI Designers)
Methodology: Agile-Scrum
Version: 1.0
Date: 2025-05-24

🎯 Project Overview
Bu proje kapsamında, CRM v2 sistemi için kullanıcı ve admin rollerine uygun oturum açma ekranı, tercihler menüsü ve uygulama içi sayfalar içeren bir arayüz geliştirilecektir. Arayüzler PyQt6 ile geliştirilecek ve arka plan verileriyle entegrasyon sağlanacaktır.

🧩 Component Breakdown
1. Login Window
Purpose: Kullanıcı veya admin girişi yapılacak ekran.

Elements:

Kullanıcı adı ve şifre giriş kutuları

“Giriş” butonu (başarılı/başarısız uyarı metni ile)

“Kapat” butonu

Style:

Soft dark/light theme

Yuvarlatılmış köşeler, hover efektli butonlar

GridLayout ile responsive yapı

Functional Rule: Giriş yapılan kullanıcı admin ise Admin Menüye, değilse Kullanıcı Menüye yönlendirilir.

2. Preference Menu (User)
Buttons:

Applications

Mentor Meeting

Interviews

Exit

Style:

Tema: Açık renkli arayüz

Kendi içinde farklı bir tema (Login ekranından farklı)

3. Preference Menu (Admin)
Ekstra Button:

Admin Menu

Style:

Tema: Açık mavi - beyaz kontrast, admin arayüzünü belirginleştirir

4. Applications Page
Elements:

Arama kutusu + Search butonu

3 Filtreleme butonu: All Applications, Mentor Meeting Defined, Mentor Interview Undefined

7 Kolonlu tablo

“Return to Preferences” butonu (Admin/User rolleri farkı dikkate alınmalı)

Style:

Şeffaf tablo arkaplanı

Buton kenarlıkları belirgin

Hafif mavi tonlamalar

5. Mentor Interview Page
Elements:

Arama kutusu + Search butonu

“All Conversations” butonu

ComboBox (Sayfa 2 verilerine göre dropdown menü)

“Return to Preferences” butonu

Style:

Gri-gümüş renk paleti

Sekmeler arasında geçişleri sade hale getiren tasarım

6. Interviews Page
Elements:

Arama kutusu + Search butonu

2 buton: Project Submitted, Project Not Submitted

“Return to Preferences” butonu

Style:

Yeşil ve gri tonlar

Flat button design

7. Admin Menu Page
Elements:

Event Records (Google Calendar üzerinden çekilecek)

Mail gönderim butonu (Etkinlik katılımcılarına)

“Return to Admin Menu”

Exit

Style:

Kurumsal mavi-gri tema

E-posta gönderim durumu mesaj paneli

📐 UI/UX Standards
Font: Poppins veya Arial, min. 12px

Renk Temaları:

Kullanıcı: #f2f2f2, #cde7ff

Admin: #d1d1e0, #b3cde0

Butonlar: hover = #e6f2ff, clicked = #b3d1ff

Frame Margin: 10px

Border Radius: 10px

Transition Time: 0.2s hover

🧠 Navigation Flow
text
Kodu kopyala
Login Window
│
├──> User Login → Preference Menu
│               ├──> Applications Page
│               ├──> Mentor Meeting Page
│               └──> Interviews Page
│
└──> Admin Login → Admin Menu
                ├──> Applications Page
                ├──> Mentor Meeting Page
                ├──> Interviews Page
                ├──> Event Records Page
                └──> Mail Sending
🛠 Technology Stack
Component	Tool
UI Framework	PyQt6
Backend	SQLite (placeholder)
Email Sending	smtplib
Calendar API	Google Calendar API
Project Tracking	GitHub Projects
Task Management	Scrum Board (GitHub)
Version Control	Git + GitHub

👥 Team Roles & Responsibilities
Role	Name	Responsibilities
Team Leader	[Your Name]	Sprint yönetimi, GitHub koordinasyonu, code review
UI Designer	Member 1	PyQt6 UI tasarımı ve stil yönetimi
Backend Dev	Member 2	Giriş kontrolü, veri yükleme, filtreleme
API Integrator	Member 3	Google Calendar ve SMTP Mail API bağlantıları
QA Tester	Member 4	Sayfa geçişleri, butonlar, search & filtre testleri

🧪 Test Plan
 Giriş başarısız/success case testleri

 Her sayfanın Return buton testi

 Tüm butonların hover & press state testleri

 ComboBox seçimlerine göre doğru veri çağrımı

 Mail gönderim fonksiyonunun dummy test ile doğrulanması

 Google Calendar veri çekme API testi

📁 Folder Structure Proposal
bash
Kodu kopyala
crm_v2/
├── assets/               # icon, image, style files
├── ui/
│   ├── login.py
│   ├── preferences_user.py
│   ├── preferences_admin.py
│   ├── applications.py
│   ├── mentor.py
│   └── interviews.py
├── services/
│   ├── auth.py
│   ├── calendar_service.py
│   └── mail_service.py
├── data/
│   └── sample_data.xlsx
├── tests/
│   ├── test_login.py
│   └── test_navigation.py
├── main.py
└── README.md
📅 Milestones (Sprint Plan - 2 Hafta)
Sprint	Task	Owner	Status
Week 1	Login ekranı ve sayfa yönlendirme	UI + Backend	🔄 In Progress
Week 1	Preferences ekranlarının tasarımı	UI Designer	✅ Done
Week 2	Uygulama ve mentor sayfalarının veri bağlantısı	Backend Dev	⏳ To Do
Week 2	Google Calendar entegrasyonu ve e-posta gönderimi	API Integrator	⏳ To Do
Week 2	Test senaryoları ve hata raporlarının oluşturulması	QA Tester	⏳ To Do

