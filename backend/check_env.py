import asyncio
import asyncpg

async def test():
    try:
        # Подключение без пароля
        conn = await asyncpg.connect(
            host='db',
            port=5432,
            user='sil_user_POSTGRES',
            password='hjevsHEe84we',  # Пустой пароль
            database='sil_POSTGRES'
        )
        print("✅ Подключено БЕЗ пароля!")
        await conn.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

asyncio.run(test())