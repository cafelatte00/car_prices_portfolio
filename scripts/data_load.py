import pandas as pd

print("=== プログラムを開始します ===")

# csvファイルのパス
file_path = '../data/raw/train.csv'

# データ読み込み
df = pd.read_csv(file_path)

# 最初の5行を表示
print(df.head())

# 最後の5行を表示
# print(df.tail())

print("データの読み込みが完了しました。")

