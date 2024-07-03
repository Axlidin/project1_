from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS project_first_users (
        id SERIAL PRIMARY KEY,
        referal_id BIGINT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    # async def add_user(self, full_name, username, telegram_id):
    #     sql = "INSERT INTO project_first_users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
    #     return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    ###referal id
    async def add_referal_id(self, telegram_id, referal_id=None):
        sql = "INSERT INTO project_first_users (telegram_id, referal_id) VALUES($1, $2) returning *"
        return await self.execute(sql, telegram_id, referal_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM project_first_users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM project_first_users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM project_first_users"
        return await self.execute(sql, fetchval=True)

    ###referal id count
    async def count_referal_id(self, tg_id):
        sql = "SELECT COUNT(*) FROM project_first_users WHERE referal_id = $1"
        return await self.execute(sql, tg_id, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM project_first_users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE project_first_users", execute=True)

    async def see_users(self, tg_id):
        sql = "SELECT * FROM project_first_users WHERE telegram_id=$1"
        return await self.execute(sql, tg_id, fetch=True)

        ###########hamyonlar

    async def create_table_hamyonlar(self):
        sql = """
        CREATE TABLE IF NOT EXISTS project_first_hamyonlar (
            id SERIAL PRIMARY KEY,
            hamyon_nomi VARCHAR(20) NOT NULL,
            card_number BIGINT,
            telegram_id BIGINT NOT NULL,
            UNIQUE (telegram_id, hamyon_nomi)
        );
        """
        await self.execute(sql, execute=True)

    async def see_hamyonlar(self, tg_id):
        sql = "SELECT hamyon_nomi, card_number FROM project_first_hamyonlar WHERE telegram_id = $1"
        result = await self.execute(sql, tg_id, fetch=True)
        if result:
            hamyonim = {row['hamyon_nomi']: row['card_number'] for row in result}
            return hamyonim
        return {}

    async def see_hamyonlar_humouz(self, tg_id):
        sql = "SELECT hamyon_nomi, card_number FROM project_first_hamyonlar WHERE telegram_id = $1 AND hamyon_nomi = 'humouzcard'"
        return await self.execute(sql, tg_id, fetchrow=True)

    async def see_hamyon_humouz(self, tg_id):
        sql = "SELECT hamyon_nomi, card_number FROM project_first_hamyonlar WHERE telegram_id = $1 AND hamyon_nomi = 'humouzcard'"
        return await self.execute(sql, tg_id, fetchrow=True)

    async def see_my_hamyonlar(self, tg_id, hamyon_nomi):
        sql = "SELECT * FROM project_first_hamyonlar WHERE telegram_id = $1 AND hamyon_nomi = $2"
        return await self.execute(sql, tg_id, hamyon_nomi, fetchrow=True)

    async def add_hamyon(self, telegram_id, card_type, card_number):
        sql = """
        INSERT INTO project_first_hamyonlar (telegram_id, hamyon_nomi, card_number)
        VALUES ($1, $2, $3)
        ON CONFLICT (telegram_id, hamyon_nomi)
        DO UPDATE SET card_number = EXCLUDED.card_number
        RETURNING *
        """
        return await self.execute(sql, telegram_id, card_type, card_number, fetchrow=True)

    async def select_all_users_hamyonlar(self):
        sql = "SELECT * FROM project_first_hamyonlar"
        return await self.execute(sql, fetch=True)

    async def select_user_hamyon(self, **kwargs):
        sql = "SELECT * FROM project_first_hamyonlar WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users_hamyonlar(self):
        sql = "SELECT COUNT(*) FROM project_first_hamyonlar"
        return await self.execute(sql, fetchval=True)

    async def count_hamyonlar(self, tg_id):
        sql = "SELECT COUNT(*) FROM project_first_hamyonlar WHERE telegram_id = $1"
        return await self.execute(sql, tg_id, fetchval=True)

    async def delete_hamyonlar(self):
        await self.execute("DELETE FROM project_first_hamyonlar WHERE TRUE", execute=True)

    async def drop_hamyonlar(self):
        await self.execute("DROP TABLE project_first_hamyonlar", execute=True)

        #####superadmin
    async def create_table_SuperAdmin(self):
        sql = """
        CREATE TABLE IF NOT EXISTS SuperAdmin_ (
        id SERIAL PRIMARY KEY,
        Superadmin_fio varchar(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def add_SuperAdmin(self, Superadmin_fio, telegram_id):
        sql = ("INSERT INTO SuperAdmin_ (Superadmin_fio, telegram_id)"
               " VALUES($1, $2) returning *")
        return await self.execute(sql, Superadmin_fio, telegram_id,
                                  fetchrow=True)

    async def select_all_SuperAdmin(self):
        sql = "SELECT * FROM SuperAdmin_"
        return await self.execute(sql, fetch=True)

    async def select_SuperAdmin(self, **kwargs):
        sql = "SELECT * FROM SuperAdmin_ WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_SuperAdmin(self):
        sql = "SELECT COUNT(*) FROM SuperAdmin_"
        return await self.execute(sql, fetchval=True)

    async def delete_SuperAdmin(self):
        await self.execute("DELETE FROM SuperAdmin_ WHERE TRUE", execute=True)

    async def drop_SuperAdmin(self):
        await self.execute("DROP TABLE SuperAdmin_", execute=True)

    async def see_SuperAdmin(self, tg_id):
        sql = "SELECT telegram_id FROM SuperAdmin_ WHERE telegram_id=$1"
        return await self.execute(sql, tg_id, fetchval=True)

    # lang tekshirish
    async def check_lang_SuperAdmin(self, telegram_id):
        sql = "SELECT SuperAdmin__lang FROM SuperAdmin_ WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchval=True)

    ###allowed message
    async def create_table_SuperAdmin_allowe_msg(self):
        sql = """
        CREATE TABLE IF NOT EXISTS SuperAdmin_allowe_msg (
        id SERIAL PRIMARY KEY,
        username varchar(255) NOT NULL,
        telegram_id BIGINT NOT NULL, 
        karta1 varchar(255) NULL,
        karta1_num varchar(255) NULL,
        karta2 varchar(255) NULL,
        karta2_num varchar(255) NULL,
        send_time varchar(100) NOT NULL,
        allowed_time varchar(100) NOT NULL,
        amoun_money varchar(50) NULL,
        amaliyot_type varchar(50) NOT NULL,
        status varchar(50) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_SuperAdmin_allowe_msg(self, username, telegram_id, karta1, karta1_num, send_time, allowed_time,
                                        amoun_money,
                                        amaliyot_type, status, karta2=None, karta2_num=None):
        sql = (
            "INSERT INTO SuperAdmin_allowe_msg (username, telegram_id, karta1, karta1_num, karta2, karta2_num, send_time, allowed_time, amoun_money, amaliyot_type, status)"
            " VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) returning *"
        )
        if karta2 is None:
            karta2 = ''
        if karta2_num is None:
            karta2_num = ''

        return await self.execute(sql, username, telegram_id, karta1, karta1_num, karta2, karta2_num, send_time,
                                  allowed_time,
                                  amoun_money, amaliyot_type, status, fetchrow=True)
    async def select_all_SuperAdmin_allowe_msg(self):
        sql = "SELECT * FROM SuperAdmin_allowe_msg"
        return await self.execute(sql, fetch=True)

    async def select_SuperAdmin_allowe_msg(self, **kwargs):
        sql = "SELECT * FROM SuperAdmin_allowe_msg WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_SuperAdmin_allowe_msg(self):
        sql = "SELECT COUNT(*) FROM SuperAdmin_allowe_msg"
        return await self.execute(sql, fetchval=True)

    async def delete_SuperAdmin_allowe_msg(self, telegram_id):
        await self.execute("DELETE FROM SuperAdmin_allowe_msg WHERE telegram_id=$1", telegram_id, execute=True)

    async def drop_SuperAdmin_allowe_msg(self):
        await self.execute("DROP TABLE SuperAdmin_allowe_msg", execute=True)

    async def see_SuperAdmin_allowe_msg(self, tg_id):
        sql = "SELECT * FROM SuperAdmin_allowe_msg WHERE telegram_id=$1"
        return await self.execute(sql, tg_id, fetch=True)