import aiosqlite
DB_NAME="users.sql"
DB_SUB="subscriptions.sql"
async def init_first_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS users (
                         user_id INTEGER PRIMARY KEY,
                         first_name TEXT,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )
        """)
async def init_second_db():
    async with aiosqlite.connect(DB_SUB) as db:
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS subscriptions (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER ,
                         car_brand TEXT NOT NULL,
                         car_model TEXT NOT NULL,
                         max_price INTEGER,
                         FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE )
         """)

async def add_users(user_id,firstname):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO users (user_id,first_name) VALUES(?,?)",(user_id,firstname))