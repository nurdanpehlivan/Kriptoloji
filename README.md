# Kriptoloji
🔍 Steganaliz Nedir?
Steganaliz, bir dosyada (görüntü, ses, video) gizlenmiş bir mesaj olup olmadığını tespit etme veya bu mesajı açığa çıkarma sürecidir. Kriptolojideki "şifre kırma" ne ise, steganografideki karşılığı steganalizdir.

📌 1. LSB (Least Significant Bit Insertion) Algoritması
Gizleme Tekniği:
LSB yöntemi, dijital medyanın her piksel/ses örneğinin en az anlam taşıyan (LSB) bitlerini gizli verilerle değiştirir. Örneğin bir pikselin RGB değeri (10101100) ise, son bitini (0) gizli veriyle değiştirerek 10101101 yapar.

Steganaliz:

İstatistiksel analizler (örneğin Chi-Square testi) ile bit düzeyinde düzensizlikler tespit edilir.

Görsel veya ses kalitesinde gözle fark edilmeyen ama analizle tespit edilebilen sapmalar oluşur.

📌 2. JPEG Algoritması (DCT – Discrete Cosine Transform)
Gizleme Tekniği:
JPEG görüntülerde sıkıştırma DCT (Ayrık Kosinüs Dönüşümü) ile yapılır. Gizli bilgiler, yüksek frekanslı DCT katsayılarının LSB bitlerine gömülür. Bu yöntem daha az fark edilir çünkü insanlar yüksek frekanslı detaylara daha az duyarlıdır.

Steganaliz:

DCT katsayılarındaki anormallikler tespit edilir.

Histogram ya da JPEG quantization tablosu analiziyle fark edilir.

📌 3. BPCS (Bit Plane Complexity Segmentation)
Gizleme Tekniği:
BPCS, görüntüleri bit düzeyinde karmaşıklıklarına göre bölümlere ayırır. İnsan gözü tarafından fark edilmeyecek kadar karmaşık (kaotik) bölgelerde veri saklanır.

Avantajı: Çok daha fazla veri saklanabilir.

Steganaliz:

Görsel bölgelerin karmaşıklığına ters düşen bilgi yoğunlukları tespit edilir.

Görüntünün kaotik bölgeleriyle veri oranı karşılaştırılır.

📌 4. Maskeleme ve Filtreleme Yöntemleri
Gizleme Tekniği:
Özellikle ses ve resim gibi ortamlarda, insanlar tarafından fark edilemeyecek gürültü veya sinyal bölgelerine veri gömülür. Görselde örneğin parlaklık farklarıyla veri saklama yapılabilir.

Steganaliz:

İnsan algısının sınırlarını aşan küçük değişiklikler analizle tespit edilir.

Orijinal dosyayla karşılaştırmalı analiz (differential analysis) yapılabilir.

📌 5. Sezgisel Steganaliz Yöntemleri (Heuristic Methods)
Teknik:
Makine öğrenmesi, istatistiksel modelleme veya sinyal işleme ile gizli veri olup olmadığını tahmin etmeye çalışan yaklaşımlardır. Belirli bir algoritmaya bağlı değildirler.

Kullanılan yöntemler:

Yapay sinir ağları

Karar ağaçları

Anomali tespiti

SVM (Support Vector Machines)

Avantajı: Yeni veya bilinmeyen steganografi tekniklerine karşı etkilidir.
