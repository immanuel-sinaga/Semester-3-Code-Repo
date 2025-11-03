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

# Memuat gambar statis (ubah path sesuai gambar yang ingin digunakan)
image_path = 'Dress.jpg'  # Ganti dengan path gambar yang ingin digunakan
image = cv2.imread(image_path)

# Memeriksa apakah gambar berhasil dimuat
if image is None:
    print("Error")
else:
    # Mengubah ukuran gambar agar sesuai dengan input model (224x224)
    resized_image = cv2.resize(image, (224, 224))
    # Normalisasi gambar ke rentang [0, 1]
    image_array = img_to_array(resized_image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # Melakukan prediksi menggunakan model
    prediction = model.predict(image_array)
    predicted_index = np.argmax(prediction)
    predicted_article = index_to_article_type[predicted_index]

    # Menampilkan prediksi di gambar
    cv2.putText(image, predicted_article, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Menampilkan gambar dengan label prediksi
    cv2.imshow('PAC', image)

    # Menunggu penekanan tombol sebelum menutup window gambar
    cv2.waitKey(0)
    cv2.destroyAllWindows()
