from databases import Database

stats_db = Database("postgresql://postgres:postgres@127.0.0.1:5432/stava")


async def save_stats(record_id, start_time, finish_time):
    query = '''INSERT INTO stats (record_id, start_time, finish_time)
        VALUES (:record_id, :start_time, :finish_time)
        ON CONFLICT (record_id) DO UPDATE
        SET start_time = :start_time, finish_time = :finish_time'''

    await stats_db.execute_many(query=query, values={
        'record_id': record_id,
        'start_time': start_time,
        'finish_time': finish_time
    })
