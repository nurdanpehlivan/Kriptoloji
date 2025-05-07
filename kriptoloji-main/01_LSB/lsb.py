import wave
import numpy as np

def text_to_bits(text):
    """Metni UTF-8 ile ikili formata çevirir."""
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

def bits_to_text(bits):
    """İkili formattan UTF-8 metne çevirir."""
    bytes_list = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]
    return bytes(bytes_list).decode('utf-8', errors='replace')

def hide_message(input_wav, output_wav, message):
    """Mesajı ses dosyasına gizler."""
    # WAV dosyasını oku
    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(wav.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)

        # Stereo mu kontrol et
        if params.nchannels == 2:
            samples = samples[::2]  # sadece sol kanal

        # Mesajı bitlere çevir
        message_bits = text_to_bits(message)
        length_bits = format(len(message_bits), '032b')
        bits_to_hide = length_bits + message_bits

        if len(bits_to_hide) > len(samples):
            raise ValueError("Ses dosyası mesajı gizlemek için çok kısa!")

        modified_samples = samples.copy()
        for i, bit in enumerate(bits_to_hide):
            modified_samples[i] = (modified_samples[i] & ~1) | int(bit)

        # Eğer stereo ise tüm kanalları yeniden inşa et
        if params.nchannels == 2:
            full_samples = np.frombuffer(frames, dtype=np.int16)
            full_samples[::2] = modified_samples  # sadece sol kanal değiştirildi
            modified_bytes = full_samples.tobytes()
        else:
            modified_bytes = modified_samples.tobytes()

        # Yeni WAV dosyasını yaz
        with wave.open(output_wav, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(modified_bytes)

def extract_message(input_wav):
    """Gizlenmiş mesajı çıkarır."""
    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(wav.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)

        if params.nchannels == 2:
            samples = samples[::2]  # sadece sol kanal

        length_bits = ''.join(str(samples[i] & 1) for i in range(32))
        message_length = int(length_bits, 2)

        message_bits = ''.join(str(samples[i] & 1) for i in range(32, 32 + message_length))
        return bits_to_text(message_bits)

def main():
    input_wav = "input.wav"
    output_wav = "output.wav"
    message = "Bu, Türkçe karakterler içeren bir test mesajıdır: ç, ğ, ü, ö, İ, Ş, Ğ. Steganografi testi başarılı mı bakalım!"

    print(f"Gizlenen mesaj: {message}")
    hide_message(input_wav, output_wav, message)
    print("Mesaj ses dosyasına gizlendi!")

    extracted_message = extract_message(output_wav)
    print(f"Çıkarılan mesaj: {extracted_message}")

if __name__ == "__main__":
    main()
