import aiosqlite
DB_NAME="users.sql"
DB_SUB="subscriptions.sql"
async def init_first_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS users (
                         user_id INTEGER PRIMARY KEY,
                         first_name TEXT,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );
        """)
        await db.commit()
async def init_second_db():
    async with aiosqlite.connect(DB_SUB) as db:
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS subscriptions (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER ,
                         car_brand TEXT NOT NULL,
                         car_model TEXT NOT NULL,
                         max_price INTEGER,
                         FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE );
         """)
        await db.commit()
async def add_users(user_id,firstname):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id,first_name) VALUES(?,?);",(user_id,firstname))
        await db.commit()
async def add_ann(user_id,car_brand,car_model,max_price):
    async with aiosqlite.connect(DB_SUB) as db:
        await db.execute("INSERT OR IGNORE INTO subscriptions (user_id,car_brand,car_model,max_price) VALUES (?,?,?,?);",(user_id,car_brand,car_model,max_price))
        await db.commit()
async def select_sub(user_id):
    async with aiosqlite.connect(DB_SUB) as db:
        cousor =await db.execute("SELECT car_brand,car_model,max_price FROM subscriptions WHERE user_id =?;",(user_id,))
        rows = await cousor.fetchall()
        return rows
async def del_sub(user_id,brand,model,price):
    async with aiosqlite.connect(DB_SUB) as db:
        await db.execute("DELETE FROM subscriptions WHERE user_id=? AND car_brand=? AND car_model=? AND max_price=?",(user_id,brand,model,price))
        await db.commit()