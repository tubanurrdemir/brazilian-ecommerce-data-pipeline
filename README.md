
# 🛒 Brazilian E-Commerce Analytics Pipeline

*[Türkçe versiyonu aşağıdadır / Turkish version is below]*

## 📊 Live Dashboard
[Click here to view the Interactive Tableau Dashboard](https://public.tableau.com/app/profile/tuba.nur.demi.r/viz/BrezilyaE-TicaretSatAnalizi/Dashboard1?publish=yes)
---

## 📝 Project Overview (English)
This end-to-end data engineering and analytics project processes real-world e-commerce data from Brazil. The goal of this project is to build an automated ETL pipeline, model the data in a relational database, and create an interactive dashboard for actionable business insights.

## 🛠️ Tech Stack
* **Python (Pandas, SQLAlchemy):** Data extraction, cleaning (handling time-traveling records and missing values), and loading.
* **PostgreSQL:** Relational database management and data modeling.
* **Tableau:** Interactive data visualization and business intelligence.

## ⚙️ Pipeline Architecture
1. **Extract:** Raw CSV data is ingested using Python.
2. **Transform:** Data quality issues (e.g., illogical delivery dates, undefined payment types) are cleaned using Pandas.
3. **Load:** Cleaned datasets are loaded directly into a PostgreSQL database.
4. **Model:** A SQL View (`master_satis_tablosu`) is created to join multiple tables for seamless BI integration.
5. **Visualize:** The optimized data is connected to Tableau to analyze sales performance, regional distribution, and payment methods.

---

## 📝 Proje Özeti (Türkçe)
Bu uçtan uca veri mühendisliği ve analitiği projesi, Brezilya'ya ait gerçek dünya e-ticaret verilerini işlemektedir. Bu projenin amacı; otomatik bir ETL boru hattı kurmak, veriyi ilişkisel bir veritabanında modellemek ve iş kararlarına yön verecek interaktif bir gösterge paneli (dashboard) oluşturmaktır.

## 🛠️ Kullanılan Teknolojiler
* **Python (Pandas, SQLAlchemy):** Veri çekme, temizleme (zaman yolculuğu yapan hatalı kayıtların ve eksik verilerin ayıklanması) ve yükleme.
* **PostgreSQL:** İlişkisel veritabanı yönetimi ve veri modelleme.
* **Tableau:** İnteraktif veri görselleştirme ve iş zekası.

## ⚙️ Boru Hattı Mimarisi (Pipeline Architecture)
1. **Extract (Çıkar):** Ham CSV verileri Python kullanılarak sisteme alınır.
2. **Transform (Dönüştür):** Veri kalitesi sorunları (ör. mantıksız teslimat tarihleri, tanımsız ödeme türleri) Pandas kullanılarak temizlenir.
3. **Load (Yükle):** Temizlenmiş veri setleri doğrudan PostgreSQL veritabanına yüklenir.
4. **Model (Modelle):** Kesintisiz BI (İş Zekası) entegrasyonu için birden fazla tabloyu birleştiren bir SQL Görünümü (`master_satis_tablosu`) oluşturulur.
5. **Visualize (Görselleştir):** Optimize edilmiş veri, satış performansını, bölgesel dağılımı ve ödeme yöntemlerini analiz etmek için Tableau'ya bağlanır.
