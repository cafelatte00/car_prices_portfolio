import os
import numpy as np
import pandas as pd

print("=== データ整形処理を開始します ===")

# ファイルパスの指定
input_path = '../data/raw/train.csv'
output_path = '../data/processed/cleaned_data.csv'

# 保存先のディレクトリが存在愛ない場合は作成。ある場合はスルー
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# CSVの読み込み
df = pd.read_csv(input_path)


# ▼データ確認▼

# データフレーム全体を表示（行数が多いと省略される）
# print(df)
# カラムごとの型・欠損値・行数をまとめて確認
# print(df.info())
# 全てのカラム名を取得（※属性なのでカッコが不要）
# print(df.columns)
# 各カラムに欠損値が含まれているかをTrue/Falseで確認
# print(df.isnull().any())
# 各カラムごとの欠損値（NaN）の数を表示
# print(df.isnull().sum())
# データフレームの先頭を表示
# print(df.head())
# データフレームの先頭を表示
# print(df.head(10))
# 最初の5行を表示
# print(df.tail())
# 数値データの統計要約を表示
# count:データ件数（欠損を除く）mean:平均値 std:標準偏差（ばらつきの度合い） min:最小値 25%:第1四分位数 50%:中央値 75%:第3四分位数 max:最大値
# print(df.describe())
# print(df.dtypes)
# print(df['Levy'].dtype)
# type(df['Levy'][0])


# ▼データ変換▼

# 1. Levy列の「-」をNaNに置き換え、object型からfloat型に変換
df['Levy'] = df['Levy'].replace('-', np.nan)
df['Levy'] = pd.to_numeric(df['Levy'], errors='coerce')

# 2. Leather interior列をtrue/Falseに変換。
# df['Leather interior'] = df['Leather interior'].replace({'Yes': True, 'No': False}).infer_objects(copy=False).astype(bool)
df['Leather interior'] = df['Leather interior'].map({'Yes': True, 'No': False})

# 3. Engine volume列をEngine_volume_num列とis_turbo列に分割
# Engine volume列に'Turbo'という文字が含まれているかを判定し、True/Falseの新しい列を作成
df['is_turbo'] = df['Engine volume'].str.contains('Turbo', na=False)
# 'Engine volume'列の位置（インデックス）を取得
position = df.columns.get_loc('Engine volume')
# 'is_turbo'列を取り出して削除（Seriesとして一時変数columnに保存）
column = df.pop('is_turbo')
# 'Engine volume'の次の列に'is_turbo'列を挿入（カラム順の調整）
df.insert(position + 1, 'is_turbo', column)
# 'Engine volume'列から ' Turbo' の文字列を除去（正規表現ではなく文字列一致で削除）
df['Engine volume'] = df['Engine volume'].str.replace(' Turbo', '', regex=False)
# 'Engine volume'列を文字列から数値（float）に変換。変換できない値はNaNにする
df['Engine volume'] = pd.to_numeric(df['Engine volume'], errors='coerce')

# 4. Mileage列の" km"を除去し、int型に変換
# 「.str」はPandasのSeries 内の文字列に適用できる メソッド集 を提供する "アクセサ" であり、その正体は StringMethods クラス。
df['Mileage'] = df['Mileage'].str.replace(' km', '', regex=False)
# object型からfloat型に変換,欠損値がもしあればNaNに変換
df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce')
# NaNを0に置き換え、int型に変換（小数点以下は切り捨て）
df['Mileage'] = df['Mileage'].fillna(0).astype(int)

# 5. Doors列の中で日付に誤変換されているものを修正（2-3:2〜3枚, 4-5:4〜5枚, >5:5枚より多い）
# 先頭の0を削除
df['Doors'] = df['Doors'].str.replace(r'^0', '', regex=True)
df['Doors'] = df['Doors'].str.replace('Mar', '3', regex=True)
df['Doors'] = df['Doors'].str.replace('May', '5', regex=True)

# 6. BD用にカラム名をsnake_caseに変換
df.columns = [
    "kaggle_id", "price", "levy", "manufacturer", "model", "prod_year", "category",
    "leather_interior", "fuel_type", "engine_volume", "is_turbo", "mileage",
    "cylinders", "gear_box_type", "drive_wheels", "doors", "wheel", "color", "airbags"
]

# 7. 明示的な数値型変換（保存前の仕上げ)
df["kaggle_id"] = df["kaggle_id"].astype(int)
df["price"] = df["price"].astype(int)
df["leather_interior"] = df["leather_interior"].astype(bool)
df["is_turbo"] = df["is_turbo"].astype(bool)
df["cylinders"] = df["cylinders"].astype(int)
df["airbags"] = df["airbags"].astype(int)
# print(df.info())

# ▼ 保存処理 ▼
# データフレームをCSVファイルとして保存。index=Falseで自動的に保存される行番号を保存しない設定に変更。
df.to_csv(output_path, index=False)

print(f"加工済みデータを保存しました: {output_path}")
print("=== データ整形処理が完了しました ===")
