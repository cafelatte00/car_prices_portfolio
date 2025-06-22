import pandas as pd
from sqlalchemy import create_engine, text

# # 接続確認
# engine = create_engine('postgresql+psycopg2://car_db_user:mypassword@localhost:5432/car_data_db')

# with engine.connect() as conn:
#    result = conn.execute(text("SELECT version();"))
#    for row in result:
#        print(row[0])

# DB接続情報
db_config = {
    'user': 'car_db_user',
    'password': 'mypassword',  # ここを書き換え
    'host': 'localhost',
    'port': '5432',
    'database': 'car_data_db'
}

# 接続URL構築
db_url = f"postgresql://{db_config['user']}:{db_config['password']}@" \
         f"{db_config['host']}:{db_config['port']}/{db_config['database']}"

engine = create_engine(db_url)

# CSV読み込み
df = pd.read_csv('../data/processed/cleaned_data.csv')

# PostgreSQLテーブル作成（id SERIAL付き）
create_table_sql = """
DROP TABLE IF EXISTS car_prices;
CREATE TABLE car_prices (
    id SERIAL PRIMARY KEY,
    kaggle_id INTEGER,
    price INTEGER,
    levy INTEGER,
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    prod_year INTEGER,
    category VARCHAR(50),
    leather_interior BOOLEAN,
    fuel_type VARCHAR(50),
    engine_volume NUMERIC(4,1),
    is_turbo BOOLEAN,
    mileage INTEGER,
    cylinders INTEGER,
    gear_box_type VARCHAR(50),
    drive_wheels VARCHAR(50),
    doors VARCHAR(10),
    wheel VARCHAR(30),
    color VARCHAR(30),
    airbags INTEGER
);
"""

# テーブル作成 & データ保存
with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.commit()

df.to_sql("car_prices", con=engine, if_exists="append", index=False)
print("データを PostgreSQL に保存しました！")








