import os
import shutil
import random
from collections import defaultdict

def count_images(directory):
    class_counts = defaultdict(int)  # Untuk menyimpan jumlah gambar per kelas
    for cls in os.listdir(directory):
        class_dir = os.path.join(directory, cls)
        if os.path.isdir(class_dir):
            class_counts[cls] = len(os.listdir(class_dir))  # Hitung jumlah gambar per kelas
    return class_counts

# Path ke folder dataset asli
dataset_dir = 'C:\\Users\\ASUS\\OneDrive\\Documents\\tomat'

# Path untuk menyimpan data yang telah di-split
train_dir = 'C:\\Users\\ASUS\\OneDrive\\Documents\\split_dataset\\train'
val_dir = 'C:\\Users\\ASUS\\OneDrive\\Documents\\split_dataset\\val'
test_dir = 'C:\\Users\\ASUS\\OneDrive\\Documents\\split_dataset\\test'

# Membuat folder train, val, dan test jika belum ada
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Mendapatkan list semua kelas dalam dataset (setiap kelas adalah subfolder)
classes = os.listdir(dataset_dir)
print("Kelas yang ditemukan:", classes)  # Cek apakah semua kelas muncul

# Membuat dictionary untuk menyimpan path gambar dari setiap kelas
class_images = {cls: [] for cls in classes}

# Mengisi dictionary dengan path gambar dari setiap kelas
for cls in classes:
    class_dir = os.path.join(dataset_dir, cls)  # Path ke folder setiap kelas
    images = os.listdir(class_dir)  # Mendapatkan list semua gambar dalam kelas
    class_images[cls] = [os.path.join(class_dir, img) for img in images]  # Menyimpan path gambar dalam list
    print(f"Jumlah gambar di kelas {cls}: {len(images)}")  # Pastikan setiap kelas ada gambarnya

# Menyamakan jumlah gambar di setiap kelas dengan random sampling jika perlu (misalnya menjadi 800 gambar per kelas)
target_size = 800

# Dictionary untuk menyimpan gambar yang sudah disesuaikan per kelas
balanced_images = {}

for cls, images in class_images.items():
    if len(images) > target_size:
        balanced_images[cls] = random.sample(images, target_size)  # Random sampling jika gambar lebih banyak
    else:
        balanced_images[cls] = images  # Biarkan jika gambar sudah cukup atau kurang

# Tentukan jumlah data untuk train, val, dan test
train_size = 560
val_size = 120
test_size = 120

# Membagi gambar dari setiap kelas ke dalam train, val, dan test set secara manual
for cls, images in balanced_images.items():
    random.shuffle(images)  # Acak gambar
    train_images = images[:train_size]  # Ambil 560 gambar untuk train
    val_images = images[train_size:train_size + val_size]  # Ambil 120 gambar untuk validasi
    test_images = images[train_size + val_size:train_size + val_size + test_size]  # Ambil 120 gambar untuk test
    
    # Pastikan setiap kelas diproses
    print(f"Memproses kelas {cls}:")
    print(f"Train images: {len(train_images)}, Val images: {len(val_images)}, Test images: {len(test_images)}")
    
    # Membuat folder untuk kelas saat ini dalam folder train, val, dan test
    os.makedirs(os.path.join(train_dir, cls), exist_ok=True)
    os.makedirs(os.path.join(val_dir, cls), exist_ok=True)
    os.makedirs(os.path.join(test_dir, cls), exist_ok=True)

    # Menyalin gambar train ke folder train/kelas
    for img in train_images:
        shutil.copy(img, os.path.join(train_dir, cls))

    # Menyalin gambar val ke folder val/kelas
    for img in val_images:
        shutil.copy(img, os.path.join(val_dir, cls))

    # Menyalin gambar test ke folder test/kelas
    for img in test_images:
        shutil.copy(img, os.path.join(test_dir, cls))

# Mengecek distribusi data train, validasi, dan test
train_counts = count_images(train_dir)  # Hitung jumlah gambar di folder train
val_counts = count_images(val_dir)      # Hitung jumlah gambar di folder validasi
test_counts = count_images(test_dir)    # Hitung jumlah gambar di folder test

# Menampilkan hasil distribusi data untuk setiap kelas
print("Distribusi data train:", train_counts)
print("Distribusi data validasi:", val_counts)
print("Distribusi data test:", test_counts)

