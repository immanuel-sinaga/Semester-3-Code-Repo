import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import pandas as pd

# Memuat model yang sudah dilatih
model = load_model('article_type_model.h5')

# Memuat dataset hanya untuk memetakan artikel ke indeks
annotations_path = 'styles.csv'
annotations = pd.read_csv(annotations_path)

# Membuat pemetaan indeks ke tipe pakaian
article_types = annotations['articleType'].unique()
index_to_article_type = {idx: art for idx, art in enumerate(article_types)}

# Mengakses webcam untuk deteksi real-time
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Mengubah ukuran frame agar sesuai dengan input model (224x224)
    resized_frame = cv2.resize(frame, (224, 224))
    # Normalisasi gambar ke rentang 0-1
    image_array = img_to_array(resized_frame) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # Melakukan prediksi menggunakan model
    prediction = model.predict(image_array)
    predicted_index = np.argmax(prediction)
    predicted_article = index_to_article_type[predicted_index]

    # Menampilkan prediksi di layar webcam
    cv2.putText(frame, predicted_article, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Menampilkan frame dari webcam
    cv2.imshow('PAC', frame)

    # Keluar dari loop saat menekan tombol 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Membebaskan sumber daya webcam dan menutup window OpenCV
cap.release()
cv2.destroyAllWindows()
