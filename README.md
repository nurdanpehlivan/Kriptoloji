# 🛡️ Kriptoloji: Steganaliz Teknikleri

## 🔍 Steganaliz Nedir?

**Steganaliz**, bir dosyada (görüntü, ses, video) gizlenmiş bir mesaj olup olmadığını tespit etme veya bu mesajı açığa çıkarma sürecidir.  
Kriptolojideki "şifre kırma" ne ise, steganografideki karşılığı **steganalizdir**.

---

## 📌 1. LSB (Least Significant Bit Insertion) Algoritması

### 🔧 Gizleme Tekniği:
LSB yöntemi, dijital medyanın her piksel/ses örneğinin **en az anlam taşıyan (LSB)** bitlerini gizli verilerle değiştirir.  
Örneğin: `10101100` → `10101101` (son bit değiştirildi).

### 🕵️‍♂️ Steganaliz:
- İstatistiksel analizler (ör. Chi-Square testi) ile bit düzeyinde düzensizlikler tespit edilir.
- Görsel/ses kalitesinde fark edilmeyen ancak analizle bulunabilen sapmalar oluşur.

---

## 📌 2. JPEG Algoritması (DCT – Discrete Cosine Transform)

### 🔧 Gizleme Tekniği:
JPEG görüntülerde **Ayrık Kosinüs Dönüşümü (DCT)** kullanılarak sıkıştırma yapılır.  
Gizli bilgiler, **yüksek frekanslı DCT katsayılarının LSB bitlerine** gömülür.

### 🕵️‍♂️ Steganaliz:
- DCT katsayılarındaki anormallikler tespit edilir.
- Histogram ve JPEG quantization tabloları analiz edilerek fark edilir.

---

## 📌 3. BPCS (Bit Plane Complexity Segmentation) Algoritması

### 🔧 Gizleme Tekniği:
Görüntüler, **bit düzeyindeki karmaşıklıklarına göre** bölümlere ayrılır.  
**Kaotik (karmaşık) bölgeler**, insan gözü tarafından fark edilemeyecek kadar uygundur ve veri bu bölgelere gizlenir.

### ✅ Avantajı:
- Daha fazla veri saklama kapasitesi.

### 🕵️‍♂️ Steganaliz:
- Karmaşık bölgelerdeki bilgi yoğunlukları karşılaştırılır.
- Görüntünün karmaşıklık düzenine ters düşen veri tespit edilir.

---

## 📌 4. Maskeleme ve Filtreleme Yöntemleri

### 🔧 Gizleme Tekniği:
Özellikle **ses ve görüntü** dosyalarında, insanların fark edemeyeceği **gürültü/sinyal bölgeleri** kullanılarak veri gömülür.  
Görsellerde örneğin parlaklık farklarıyla bu yapılabilir.

### 🕵️‍♂️ Steganaliz:
- İnsan algısının fark edemeyeceği küçük değişiklikler analizle tespit edilir.
- Orijinal dosya ile karşılaştırmalı analiz (**differential analysis**) yapılabilir.

---

## 📌 5. Sezgisel Steganaliz Yöntemleri (Heuristic Methods)

### 🔧 Teknik:
Makine öğrenmesi, istatistiksel modelleme veya sinyal işleme ile **gizli veri olup olmadığını tahmin eder**.  
Belirli bir algoritmaya bağlı değildir.

### 🛠️ Kullanılan Yöntemler:
- Yapay sinir ağları (ANN)
- Karar ağaçları
- Anomali tespiti
- Destek vektör makineleri (SVM)

### ✅ Avantajı:
- Yeni veya bilinmeyen steganografi tekniklerine karşı bile etkilidir.

---

> Bu doküman, steganografi içeren medya dosyalarındaki gizli verileri tespit etmek için kullanılan başlıca steganaliz tekniklerini özetlemektedir.
