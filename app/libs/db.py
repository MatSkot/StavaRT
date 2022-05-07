from databases import Database

from app.settings import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE

stats_db = Database(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_DATABASE}")


async def create_table():
    await stats_db.execute(query='''CREATE TABLE IF NOT EXISTS public.stats (
        record_id varchar NOT NULL,
        start_time timestamptz(0) NULL,
        finish_time timestamptz(0) NULL,
        CONSTRAINT stats_pk PRIMARY KEY (record_id)
    );''')


async def save_stats(record_id, start_time, finish_time):
    query = '''INSERT INTO stats (record_id, start_time, finish_time)
        VALUES (:record_id, :start_time, :finish_time)
        ON CONFLICT (record_id) DO UPDATE
        SET start_time = :start_time, finish_time = :finish_time'''

    await stats_db.execute(query, {
        'record_id': record_id,
        'start_time': start_time,
        'finish_time': finish_time
    })
