import pandas as pd
import os
from sklearn.model_selection import train_test_split

# --- PRE-PROSES DATA ---

# Path ke file CSV yang berisi anotasi gambar
annotations_path = 'styles.csv'
# Direktori tempat semua gambar disimpan
images_dir = 'images'

# Membaca file CSV yang berisi metadata gambar
annotations = pd.read_csv(annotations_path)

# Menambahkan kolom baru untuk memetakan ID gambar ke path file gambar
annotations['image_path'] = annotations['id'].apply(lambda x: os.path.join(images_dir, f"{x}.jpg"))

# Menfilter barisan data agar hanya gambar yang ada di direktori yang dipakai
annotations = annotations[annotations['image_path'].apply(os.path.exists)]

# Mengambil tipe pakaian yang unik dan membuat pemetaan ke label numerik
article_types = annotations['articleType'].unique()
article_type_to_index = {art: idx for idx, art in enumerate(article_types)}  # Memetakan tipe pakaian ke indeks numerik
index_to_article_type = {idx: art for art, idx in article_type_to_index.items()}  # Memetakan indeks kembali ke tipe pakaian

# Menambahkan kolom label numerik ke dataset
annotations['articleType_index'] = annotations['articleType'].map(article_type_to_index)

# Membagi dataset menjadi train, test, dan validation
train, test = train_test_split(annotations, test_size=0.2, random_state=42)  # Membagi 20% data untuk testing
train, val = train_test_split(train, test_size=0.2, random_state=42)  # Membagi train menjadi 80% train dan 20% validation

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --- GENERATOR GAMBAR ---

# Mengatur preprocessing gambar untuk training dan validation (menormalisasi piksel ke 0-1)
train_datagen = ImageDataGenerator(rescale=1.0/255.0)
val_datagen = ImageDataGenerator(rescale=1.0/255.0)

# Membuat generator untuk data training
train_generator = train_datagen.flow_from_dataframe(
    train,
    x_col='image_path',            # Kolom yang berisi path gambar
    y_col='articleType_index',     # Kolom target dengan label numerik
    target_size=(224, 224),        # Mengubah ukuran gambar ke 224x224 (sesuai dengan MobileNetV2)
    batch_size=32,                 # Jumlah gambar dalam satu batch
    class_mode='raw'               # Mengembalikan label numerik mentah
)

# Membuat generator untuk data validation
val_generator = val_datagen.flow_from_dataframe(
    val,
    x_col='image_path',
    y_col='articleType_index',
    target_size=(224, 224),
    batch_size=32,
    class_mode='raw'
)

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam

# --- PEMBANGUNAN MODEL ---

# Memuat model MobileNetV2 yang sudah dilatih sebelumnya tanpa lapisan atas (include_top=False)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Menambahkan lapisan khusus untuk klasifikasi
x = base_model.output
x = GlobalAveragePooling2D()(x)          # Menambahkan lapisan pooling global
x = Dense(128, activation='relu')(x)     # Lapisan Dense dengan 128 unit dan aktivasi ReLU
predictions = Dense(len(article_types), activation='softmax')(x)  # Lapisan output dengan softmax untuk klasifikasi multi-kategori

# Menggabungkan model dasar dengan lapisan tambahan ke dalam satu model
model = Model(inputs=base_model.input, outputs=predictions)

# Membekukan lapisan dasar agar tidak diperbarui saat pelatihan awal
for layer in base_model.layers:
    layer.trainable = False

# Mengkompilasi model dengan optimizer Adam dan loss sparse categorical cross-entropy
model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# --- MELATIH MODEL ---

# Melatih model menggunakan generator training dan validation
history = model.fit(
    train_generator,            # Generator untuk data training
    validation_data=val_generator,  # Generator untuk data validation
    epochs=10                   # Melatih selama 10 epoch
)

# Menyimpan model yang sudah dilatih ke file
model.save('article_type_model.h5')

import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# --- PREDIKSI REAL-TIME MENGGUNAKAN WEBCAM ---

# Memuat model yang sudah dilatih sebelumnya
model = load_model('article_type_model.h5')

# Membuka koneksi ke webcam (0 adalah webcam default)
cap = cv2.VideoCapture(0)

while True:
    # Membaca frame dari webcam
    ret, frame = cap.read()
    if not ret:  # Menghentikan loop jika frame tidak dapat ditangkap
        break

    # Memproses frame agar sesuai dengan input model
    resized_frame = cv2.resize(frame, (224, 224))      # Mengubah ukuran gambar menjadi 224x224
    image_array = img_to_array(resized_frame) / 255.0  # Menormalisasi piksel gambar ke rentang 0-1
    image_array = np.expand_dims(image_array, axis=0)  # Menambahkan dimensi batch

    # Membuat prediksi menggunakan model
    prediction = model.predict(image_array)
    predicted_index = np.argmax(prediction)              # Mengambil indeks dari probabilitas tertinggi
    predicted_article = index_to_article_type[predicted_index]  # Mengembalikan indeks ke tipe pakaian

    # Menampilkan prediksi pada frame webcam
    cv2.putText(frame, predicted_article, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Clothing Detector', frame)

    # Menghentikan loop ketika menekan tombol 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan sumber daya webcam dan menutup semua jendela OpenCV
cap.release()
cv2.destroyAllWindows()
