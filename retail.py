import pandas as pd
import math

# [1] Baca dataset
print("[1] BACA DATASET")
retail = pd.read_csv("E:/DQLab/Dataset/retail_raw_test.csv")
print("DataFrame :\n", retail.head())
print("Info dataframe :\n", retail.info())

# [2] Ubah tipe data
print("\n[2] UBAH TIPE DATA")
retail["customer_id"] = retail["customer_id"].apply(lambda x: x.split("'")[1]).astype("int64")
retail["quantity"] = retail["quantity"].apply(lambda x: x.split("'")[1]).astype("int64")
retail["item_price"] = retail["item_price"].apply(lambda x: x.split("'")[1]).astype("int64")
# Cetak type data
print(retail.dtypes)

# 3. Transform "product_value" supaya bentuknya seragam dengan format "PXXXX",
# assign ke kolom baru "product_id", dan drop kolom "product_value", jika terdapat nan gantilah dengan "unknown"
print("\n[3] TRANSFORM product_value MENJADI product_id")


# Buat fungsi


def impute_product_value(val):
    if math.isnan(val):
        return "unknown"
    else:
        return 'P' + '{:0>4}'.format(str(val).split('.')[0])


# Buat kolom product_is
retail["product_id"] = retail["product_value"].apply(lambda x: impute_product_value(x))

# Hapus kolom product_value
retail.drop(["product_value"], axis=1, inplace=True)
# Cetak data teratas
print(retail.head())

# [4] Transform order_date menjadi value dengan format "YYYY-mm-dd"
print("\n[4] TRANSFORM order_date MENJADI format YYYY-mm-dd")
months_dict = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}
retail["order_date"] = pd.to_datetime(
    retail["order_date"].apply(lambda x: str(x)[-4] + "-" + months_dict[str(x)[:3]] + "-" + str(x)[4:7]))
print("Type date :\n", retail.dtypes)

# [5] Mengatasi data hilang di beberapa kolom
print("\n[5] HANDLING MISSING VALUE")
# Kolom "city" dan "province" masih memiliki missing value,
# nilai yang hilang di kedua kolom ini diisi saja dengan "unknown"

# Cek jumlah missing value tiap kolom
print(retail.isna().sum())

# isi missing value kolom city, province dan brand
retail["city"] = retail["city"].fillna("unknown")
retail["province"] = retail["province"].fillna("unknown")
retail["brand"] = retail["brand"].fillna("no_brand")

# Cek informasi tiap kolom
print("\n", retail.info())

# [6] Buat kolom "city/province" gabungan dari kolom city dan province lalu delete kolom asalnya
print("\n[6] MEMBUAT KOLOM BARU city/province")
retail["city/province"] = retail["city"] + "/" + retail["province"]

# Hapus kolom city dan province
retail.drop(["city", "province"], axis=1, inplace=True)
# Cek kolom city dan province
print(retail.columns)

# [7] Membuat hierarchical index dari kolom city/province, order_date, customer_id, order_id, dan product_id
print("\n[7] MEMBUAT HIERACHICAL INDEX")
retail = retail.set_index(["city/province", "order_date", "customer_id", "order_id", "product_id"])

# urutkanlah berdasarkan index yang baru
retail = retail.sort_index()
print(retail.head())

# [8] Membuat kolom "total_price" dari perkalian quantity dan item_price
print("\n[8] MEMBUAT KOLOM total_price")

retail["total_price"] = retail["quantity"] * retail["item_price"]
print(retail.head())

# [9] Slice dataset agar hanya terdapat data bulan Januari 2019
print("\n[9] SLICE DATASET UNTUK BULAN JANUARI 2019 SAJA")
idx = pd.IndexSlice
retail_jan2019 = retail.loc[idx[:, "2019-01-01":"2019-01-31"], :]
print("Dataset akhir:\n", retail_jan2019)
