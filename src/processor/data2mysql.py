import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))

load_dotenv()
DATA_FILE = os.path.join(project_root, os.getenv("DATA"))
MySQL_USER = os.getenv("MySQL_USER")
MySQL_PASSWORD = os.getenv("MySQL_PASSWORD")

database_config = {
    'user': MySQL_USER,
    'password': MySQL_PASSWORD,
    'host': 'localhost',
    'port': 3306
}


def ensure_database(engine, db_name):
    with engine.connect() as conn:
        conn.execute(
            text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4;")
        )
        conn.commit()


def ensure_table(engine, db_name, table_name, df_sample):
    with engine.connect() as conn:
        result = conn.execute(
        text(f"SELECT COUNT(*) FROM information_schema.tables "
             f"WHERE table_schema = '{db_name}' AND table_name = '{table_name}';")
    )
    table_exists = result.scalar() > 0
    conn.commit()

    if not table_exists: # 表不存在，建空表
        df_sample.head(0).to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )
        print(f"已建立空表 [{table_name}]")
    else:
        print(f"表 [{table_name}] 已存在")

    return table_exists


def get_existing_data(engine, table_name): # 读取表中数据
    try:
        df_existing = pd.read_sql_table(table_name, con=engine)
        return df_existing
    except Exception:
        return pd.DataFrame()


def filter_new_data(df_new, df_existing, subset_columns=None): #表中数据与写入数据去重
    if df_existing.empty:
        return df_new

    if subset_columns is None: # 按所有列完全匹配去重
        df_existing_hash = set(df_existing.apply(tuple, axis=1))
        mask = df_new.apply(tuple, axis=1).map(lambda x: x not in df_existing_hash)
    else:
        # 按指定列去重
        existing_keys = set(df_existing[subset_columns].apply(tuple, axis=1))
        mask = df_new[subset_columns].apply(tuple, axis=1).map(lambda x: x not in existing_keys)

    df_unique = df_new[mask]
    return df_unique


def main():
    db_name = "RB"
    table_name = "samples"

    base_engine = create_engine(  # 连接
        f"mysql+pymysql://{database_config['user']}:{database_config['password']}"
        f"@{database_config['host']}:{database_config['port']}"
        f"?charset=utf8mb4"
    )
    ensure_database(base_engine, db_name) # 库不存在则新建
    target_engine = create_engine(
        f"mysql+pymysql://{database_config['user']}:{database_config['password']}"
        f"@{database_config['host']}:{database_config['port']}/{db_name}"
        f"?charset=utf8mb4"
    )

    try:
        df = pd.read_csv(DATA_FILE, encoding='utf-8')
        print(f"待写入数据共 {len(df)} 条")        
        ensure_table(target_engine, db_name, table_name, df) # 表不存在则新建
        df_existing = get_existing_data(target_engine, table_name)
        print(f"表 [{table_name}] 中已有 {len(df_existing)} 条数据")

        df_unique = filter_new_data(df, df_existing, subset_columns=None) # 写入数据去重

        if df_unique.empty:
            print("没有新数据需要写入")
        else:
            df_unique.to_sql( # 追加写入
                name=table_name,
                con=target_engine,
                if_exists='append',
                index=False,
                chunksize=1000
            )
            print(f"追加写入 {len(df_unique)} 条数据")

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()