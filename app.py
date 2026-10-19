
import streamlit as st
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# ==========================
# Pengaturan Halaman
# ==========================
st.set_page_config(page_title="AI Rekomendasi Produk")

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("")

# Simpan salinan asli untuk ringkasan & tampilan
df_asli = df.copy()

# ==========================
# Encoding Kolom Kategorikal
# ==========================
encoder_produk = LabelEncoder()
df["nama_produk"] = encoder_produk.fit_transform(df["nama_produk"])

encoder_momen = LabelEncoder()
df["momen_hari_besar"] = encoder_momen.fit_transform(df["momen_hari_besar"])

encoder_status = LabelEncoder()
df["status_penjualan"] = encoder_status.fit_transform(df["status_penjualan"])

kolom_kategori = ["kategori", "ada_promo"]

for kolom in kolom_kategori:
    df[kolom] = LabelEncoder().fit_transform(df[kolom])

# ==========================
# Feature & Target
# Karena pengguna hanya memasukkan bulan, fitur dibatasi pada
# produk, bulan, dan momen hari besar (momen ditentukan dari bulan).
# jumlah_terjual dan stok_awal_bulan tidak dipakai (data leakage).
# ==========================
fitur = ["nama_produk",
        "kategori",
        "bulan",
        "harga_satuan",
        "diskon_persen",
        "ada_promo",
        "biaya_iklan",
        "rating_produk",
        "momen_hari_besar"]

X = df[fitur]
y = df["status_penjualan"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.10,
    random_state=42,
    stratify=y
)

# ==========================
# Training Model
# ==========================
@st.cache_resource
def latih_model():
    model = ''
    model.fit()
    return model

model = latih_model()

nama_bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

kategori_produk = df_asli.groupby("nama_produk")["kategori"].first()

# ==========================
# Tampilan
# ==========================
st.title("🛒 AI Rekomendasi Produk untuk Dijual")

st.write("Pilih bulan, lalu AI akan merekomendasikan produk yang berpeluang laris.")

bulan_nama = st.selectbox("Bulan Penjualan", nama_bulan)

bulan = nama_bulan.index(bulan_nama) + 1

# ==========================
# Prediksi
# ==========================
if st.button("Rekomendasikan"):

    # Momen hari besar yang paling umum pada bulan tersebut
    momen = df_asli[df_asli["bulan"] == bulan]["momen_hari_besar"].mode()[0]

    produk_bulan = (
        df[df["bulan"] == bulan]
        .groupby("nama_produk", as_index=False)
        .agg(
            kategori=("kategori", "first"),
            bulan=("bulan", "first"),
            harga_satuan=("harga_satuan", "mean"),
            diskon_persen=("diskon_persen", "mean"),
            ada_promo=("ada_promo", lambda s: s.mode().iloc[0]),
            biaya_iklan=("biaya_iklan", "mean"),
            rating_produk=("rating_produk", "mean"),
            momen_hari_besar=("momen_hari_besar", lambda s: s.mode().iloc[0]),
        )
    )

    daftar_produk = encoder_produk.inverse_transform(produk_bulan["nama_produk"])

    data_input = produk_bulan[fitur]
    idx_laris = list(model.classes_).index(encoder_status.transform(["Laris"])[0])
    peluang = model.predict_proba(data_input)[:, idx_laris]

    # Rata-rata penjualan historis tiap produk pada bulan tersebut
    rata_jual = (df_asli[df_asli["bulan"] == bulan]
                 .groupby("nama_produk")["jumlah_terjual"].mean().round(0))

    hasil = pd.DataFrame({
        "Produk": daftar_produk,
        "Kategori": [kategori_produk[p] for p in daftar_produk],
        "peluang": peluang,
        "Rata-rata Terjual (unit)": [int(rata_jual[p]) for p in daftar_produk],
    })

    rekomendasi = hasil[hasil["peluang"] >= 0.5].sort_values("peluang", ascending=False)

    if rekomendasi.empty:
        rekomendasi = hasil.sort_values("Rata-rata Terjual (unit)", ascending=False).head(3)
        st.info(f"Bulan {bulan_nama} tidak ada produk dengan lonjakan penjualan khusus. "
                "Berikut 3 produk dengan rata-rata penjualan tertinggi.")
    else:
        st.success(f"Produk yang direkomendasikan untuk bulan {bulan_nama} "
                   f"(momen: {momen}) 🎉")

    rekomendasi["Peluang Laris"] = (rekomendasi["peluang"] * 100).round(0).astype(int).astype(str) + "%"

    st.dataframe(
        rekomendasi[["Produk", "Kategori", "Peluang Laris", "Rata-rata Terjual (unit)"]],
        hide_index=True,
        use_container_width=True
    )
