import cv2
import os
import datetime

# === Pastikan folder "photos" ada ===
if not os.path.exists("photos"):
    os.makedirs("photos")

# === Fungsi filter ===
def apply_filter(frame, mode):
    if mode == 0:
        return frame
    elif mode == 1:
        # Grayscale
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    
    elif mode == 3:
        # Cartoon effect
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, 
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon
    elif mode == 4:
        # Mirror (flip horizontal)
        return cv2.flip(frame, 1)
    elif mode == 5:
        # Blur
        return cv2.GaussianBlur(frame, (21, 21), 0)
    else:
        return frame

# === Inisialisasi kamera ===
cap = cv2.VideoCapture(0)

filter_mode = 0
filter_names = ["Normal", "Grayscale", "Sepia", "Cartoon", "Mirror", "Blur"]

print("=== Photobox Aktif ===")
print("Tekan angka (0–5) untuk ganti filter")
print("Tekan [SPASI] untuk ambil foto")
print("Tekan [Q] untuk keluar")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    filtered = apply_filter(frame, filter_mode)

    # Jika filter grayscale, ubah jadi 3 channel biar bisa tampil warna teks
    if len(filtered.shape) == 2:
        filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)

    cv2.putText(filtered, f"Filter: {filter_names[filter_mode]}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    cv2.imshow("📸 Photobox", filtered)

    key = cv2.waitKey(1) & 0xFF

    # Ganti filter
    if key in [ord(str(i)) for i in range(6)]:
        filter_mode = int(chr(key))
    
    # Ambil foto
    elif key == 32:  # Tombol spasi
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photos/photo_{filter_names[filter_mode]}_{timestamp}.jpg"
        cv2.imwrite(filename, filtered)
        print(f"[✔] Foto disimpan: {filename}")
    
    # Keluar
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
