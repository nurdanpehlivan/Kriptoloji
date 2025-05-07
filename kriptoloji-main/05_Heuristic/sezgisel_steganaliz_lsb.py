import wave
import struct

def embed_message(input_wav, output_wav, message):
    # Mesajı bitlere çevir (sonuna NULL byte ekle)
    message_bytes = message.encode('utf-8')
    message_bits = ''.join(f'{byte:08b}' for byte in message_bytes) + '00000000'

    # WAV dosyasını oku
    with wave.open(input_wav, 'rb') as wav_in:
        params = wav_in.getparams()
        frames = wav_in.readframes(params.nframes)
        samples = list(struct.unpack('<' + 'h' * params.nframes, frames))

    # Mesajı göm
    modified_samples = samples[:]
    for i, bit in enumerate(message_bits):
        modified_samples[i] &= ~1  # Son biti sıfırla
        modified_samples[i] |= int(bit)  # Yeni biti yerleştir

    # Yeni dosyaya yaz
    with wave.open(output_wav, 'wb') as wav_out:
        wav_out.setparams(params)
        modified_frames = struct.pack('<' + 'h' * len(modified_samples), *modified_samples)
        wav_out.writeframes(modified_frames)

    print(f"Mesaj başarıyla gömüldü → {output_wav}")


def extract_message(stego_wav):
    with wave.open(stego_wav, 'rb') as wav_file:
        frames = wav_file.readframes(wav_file.getnframes())
        samples = list(struct.unpack('<' + 'h' * wav_file.getnframes(), frames))

    # Bitleri oku
    bits = ''
    for sample in samples:
        bits += str(sample & 1)

    # 8-bitlik bloklara ayır ve karaktere dönüştür
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if byte == '00000000':  # NULL karaktere ulaşıldı
            break
        chars.append(chr(int(byte, 2)))

    return ''.join(chars)


# === ÖRNEK KULLANIM ===

input_path = "../8s_audio.wav"  # Orijinal WAV dosyanın adı
output_path = "../8s_audio_with_message.wav"  # Mesaj gömülecek yeni dosya
secret_message = "Bu bir gizli mesajdır!"

# Mesajı göm
embed_message(input_path, output_path, secret_message)

# Mesajı çöz
recovered = extract_message(output_path)
print("Çözülen mesaj:", recovered)
