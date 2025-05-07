
import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image

def text_to_bits(text):
    """Metni binary formata çevirir"""
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits):
    """Binary formatı metne çevirir"""
    try:
        n = int(''.join(bits), 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    except UnicodeDecodeError:
        return "Kod çözme hatası: Geçersiz mesaj biçimi"

def encode_dct(image_path, message, output_path):
    """DCT kullanarak mesajı görüntüye gömer"""
    # Görüntüyü yükle
    img = Image.open(image_path).convert('L')  # Görüntüyü gri tonlamalıya çevir
    img_array = np.array(img, dtype=np.float32)

    # Mesajı binary'e çevir ve uzunluğunu ekle
    message_bits = text_to_bits(message)
    message_length = bin(len(message_bits))[2:].zfill(32)  # 32 bit uzunluk
    data_to_hide = message_length + message_bits

    # Görüntüyü bloklara ayır
    block_size = 8
    rows, cols = img_array.shape
    # Kapasite kontrolü: Her blokta sadece 1 bit gömüyoruz
    max_bits = (rows // block_size) * (cols // block_size)
    if len(data_to_hide) > max_bits:
        raise ValueError(f"Mesaj çok uzun ({len(data_to_hide)} bit), görüntü kapasitesi {max_bits} bit!")

    # Mesaj bitlerini yerleştirecek indeks
    bit_index = 0

    # Görüntüdeki her blok için DCT uygula
    for i in range(0, rows, block_size):
        for j in range(0, cols, block_size):
            # 8x8'lik blok al
            block = img_array[i:i + block_size, j:j + block_size]
            if block.shape != (block_size, block_size):
                continue  # Eksik blokları atla

            # DCT uygulama
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')

            # Sadece [1,1] katsayısına bit göm (düşük frekans)
            if bit_index < len(data_to_hide):
                coeff = dct_block[1, 1]
                if data_to_hide[bit_index] == '1':
                    dct_block[1, 1] = abs(coeff) + 50 if coeff >= 0 else -(abs(coeff) + 50)
                else:
                    dct_block[1, 1] = abs(coeff) if coeff >= 0 else -abs(coeff)
                bit_index += 1

            # IDCT ile blokları geri dönüştür
            reconstructed_block = idct(idct(dct_block.T, norm='ortho').T, norm='ortho')
            # Piksel değerlerini [0, 255] aralığında tut
            img_array[i:i + block_size, j:j + block_size] = np.clip(reconstructed_block, 0, 255)

    # Yeni görüntüyü kaydet
    Image.fromarray(np.uint8(img_array)).save(output_path)
    return True

def decode_dct(image_path):
    """DCT ile gömülü mesajı çıkarır"""
    # Görüntüyü yükle
    img = Image.open(image_path).convert('L')  # Görüntüyü gri tonlamalıya çevir
    img_array = np.array(img, dtype=np.float32)

    # Mesaj bitlerini çıkarmak için liste
    message_bits = []
    block_size = 8
    rows, cols = img_array.shape

    # İlk 32 biti oku (mesaj uzunluğu)
    length_bits = []
    bit_index = 0
    for i in range(0, rows, block_size):
        for j in range(0, cols, block_size):
            block = img_array[i:i + block_size, j:j + block_size]
            if block.shape != (block_size, block_size):
                continue
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
            if bit_index < 32:
                coeff = dct_block[1, 1]
                length_bits.append('1' if abs(coeff) > 25 else '0')
                bit_index += 1
            if bit_index >= 32:
                break
        if bit_index >= 32:
            break

    # Mesaj uzunluğunu kontrol et
    print("Çıkarılan uzunluk bitleri:", ''.join(length_bits))  # Debugging
    try:
        message_length = int(''.join(length_bits), 2)
        print("Kodlanmış mesaj uzunluğu:", message_length)  # Debugging
    except ValueError:
        return "Hata: Geçersiz mesaj uzunluğu"

    # Mesaj bitlerini oku
    bit_index = 0
    for i in range(0, rows, block_size):
        for j in range(0, cols, block_size):
            block = img_array[i:i + block_size, j:j + block_size]
            if block.shape != (block_size, block_size):
                continue
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
            if bit_index >= 32 and len(message_bits) < message_length:
                coeff = dct_block[1, 1]
                message_bits.append('1' if abs(coeff) > 25 else '0')
            bit_index += 1
            if len(message_bits) >= message_length:
                break
        if len(message_bits) >= message_length:
            break

    # İlk birkaç biti yazdır (debugging)
    print("İlk 50 mesaj biti:", ''.join(message_bits[:50]))  # Debugging
    # Bitleri metne çevir
    return bits_to_text(message_bits)

# Örnek kullanım
if __name__ == "__main__":
    input_image = "kriptoloji.jpg"  # Gömme işlemi yapacağımız görüntü
    output_image = "kriptoloji_gizli.jpg"  # Mesajın gömüldüğü görüntü
    secret_message = "Bu bir gizli mesajdir gazihan!"  # Gömülecek mesaj

    try:
        # Mesajı DCT ile gömme
        encode_dct(input_image, secret_message, output_image)
        print("Mesaj başarıyla gömüldü!")

        # Gömülü mesajı çıkarma
        decoded_message = decode_dct(output_image)
        print("Çıkarılan mesaj:", decoded_message)
    except Exception as e:
        print("Hata:", str(e))