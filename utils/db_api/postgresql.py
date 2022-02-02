# from typing import Union

# import asyncpg
# from asyncpg import Connection
# from asyncpg.pool import Pool

# from data import config

# class Database:

#     def __init__(self):
#         self.pool: Union[Pool, None] = None

#     async def create(self):
#         self.pool = await asyncpg.create_pool(
#             user=config.DB_USER,
#             password=config.DB_PASS,
#             host=config.DB_HOST,
#             database=config.DB_NAME
#         )

#     async def execute(self, command, *args,
#                       fetch: bool = False,
#                       fetchval: bool = False,
#                       fetchrow: bool = False,
#                       execute: bool = False
#                       ):
#         async with self.pool.acquire() as connection:
#             connection: Connection
#             async with connection.transaction():
#                 if fetch:
#                     result = await connection.fetch(command, *args)
#                 elif fetchval:
#                     result = await connection.fetchval(command, *args)
#                 elif fetchrow:
#                     result = await connection.fetchrow(command, *args)
#                 elif execute:
#                     result = await connection.execute(command, *args)
#             return result

#     async def create_table_users(self):
#         sql = """
#         CREATE TABLE IF NOT EXISTS Users (
#         id SERIAL PRIMARY KEY,
#         full_name VARCHAR(255) NOT NULL,
#         username varchar(255) NULL,
#         telegram_id BIGINT NOT NULL UNIQUE,
#         lavel VARCHAR(5) NOT NULL,
#         til VARCHAR(50) NULL,
#         kategory_id_list INTEGER[] UNIQUE
#         );
#         """
#         await self.execute(sql, execute=True)

#     async def create_table_words(self):
#         sql = """
#             CREATE TABLE IF NOT EXISTS Words (
#                 id SERIAL PRIMARY KEY,
#                 eng VARCHAR(50) NOT NULL,
#                 uz VARCHAR(50) NOT NULL,
#                 turi VARCHAR(20) NOT NULL,
#                 tgmp3id VARCHAR NULL
#             );
#         """
#         await self.execute(sql,execute=True)


#     async def create_table_kategories(self):
#         sql = """
#             CREATE TABLE IF NOT EXISTS Kategories (
#                 id SERIAL PRIMARY KEY,
#                 creator_tg_id VARCHAR(20) NOT NULL,
#                 name VARCHAR NOT NULL,
#                 word_id_list INTEGER[]
#             )
#         """
#         await self.execute(sql,execute=True)



#     @staticmethod
#     def format_args(sql, parameters: dict):
#         sql += " AND ".join([
#             f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
#                                                           start=1)
#         ])
#         return sql, tuple(parameters.values())

#     #For users table
#     async def add_user(self, full_name, username, telegram_id,lavel):
#         sql = "INSERT INTO users (full_name, username, telegram_id, lavel ) VALUES($1, $2, $3, $4) returning *"
#         return await self.execute(sql, full_name, username, telegram_id, lavel, fetchrow=True)

#     async def insert_user_kategory(self,telegram_id,kategory_id):
#         sql = """UPDATE Users SET kategory_id_list=array_append(kategory_id_list,$1) WHERE telegram_id=$2"""
#         return await self.execute(sql, kategory_id, telegram_id, execute=True)

#     async def select_all_users(self):
#         sql = "SELECT * FROM Users"
#         return await self.execute(sql, fetch=True)

#     async def select_user(self, **kwargs):
#         sql = "SELECT * FROM Users WHERE "
#         sql, parameters = self.format_args(sql, parameters=kwargs)
#         return await self.execute(sql, *parameters, fetchrow=True)

#     async def count_users(self):
#         sql = "SELECT COUNT(*) FROM Users"
#         return await self.execute(sql, fetchval=True)

#     async def update_user_username(self, username, telegram_id):
#         sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
#         return await self.execute(sql, username, telegram_id, execute=True)

#     async def update_user_language(self,telegram_id,lang):
#         sql = "UPDATE Users SET til=$1 WHERE telegram_id=$2"
#         return await self.execute(sql,lang,telegram_id,execute=True)

#     async def delete_users(self):
#         await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

#     async def drop_users(self):
#         await self.execute("DROP TABLE Users", execute=True)

#     #For words table
#     async def add_word(self,uz,eng,turi):
#         sql = "INSERT INTO Words (eng,uz,turi) VALUES ($1, $2, $3 ) returning *"
#         return await self.execute(sql, eng, uz, turi, fetchrow=True)
        
#     async def select_word(self,**kwargs):
#         sql = "SELECT * FROM Words WHERE "
#         sql, parameters = self.format_args(sql, parameters=kwargs)
#         return await self.execute(sql, *parameters, fetchrow=True)
#     async def get_tables_list(self):
#         return await self.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'",fetch=True)

#     async def drop_words(self):
#         return await self.execute("DROP TABLE Words;",execute=True)

#     #For kategories table
#     async def insert_new_kategory(self,name,creator_tg_id):
#         sql = """INSERT INTO Kategories (name, creator_tg_id ) VALUES($1, $2) returning *"""
#         return await self.execute(sql, name, str(creator_tg_id), fetchrow=True,execute=True)
    
#     async def insert_kategory_word(self,kategory_id:int,word_id:int):
#         kategory = await self.select_kategory(kategory_id)
#         try:
#             if word_id in kategory.get("word_id_list"):
#                 return 0
#         except TypeError:
#             pass
#         sql = """UPDATE Kategories SET word_id_list=array_append(word_id_list,$2) WHERE id=$1"""
#         return await self.execute(sql, kategory_id, word_id, execute=True)

#     async def select_kategory(self,kategory_id):
#         sql = "SELECT * FROM Kategories WHERE id=$1"
#         return await self.execute(sql,kategory_id,fetchrow=True, execute=True)
#     async def delete_kategory(self,kategory_id:int,telegram_id:int):
#         sql = "update users set kategory_id_list=array_remove(kategory_id_list,$1) where telegram_id=$2;"
#         sql2 = "DELETE FROM Kategories WHERE id=$1"
#         await self.execute(sql2,kategory_id,execute=True)
#         return await self.execute(sql,kategory_id,telegram_id,execute=True)
#     async def drop_kategories(self):
#         sql = "DROP TABLE Kategories;"
#         await self.execute(sql,execute=True)

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
            database=config.DB_NAME
        )


    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
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



#--------------------------------------------------------------------------

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS USERS (
        id SERIAL PRIMARY KEY,
        telegramID BIGINT NOT NULL UNIQUE,
        fullName VARCHAR(255) NULL,
        userName varchar(255) NULL,
        categoryListID INTEGER[] UNIQUE
        );
        """
        await self.execute(sql, execute=True)


    async def addNew_user(self, telegramID, fullName, userName):
        sql = "INSERT INTO USERS (telegramID, fullName, userName ) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, telegramID, fullName, userName, fetchrow=True)

    async def insert_user_category(self, telegramID, categoryID):
        sql = """UPDATE USERS SET categoryListID=array_append(categoryListID,$1) WHERE telegramID=$2"""
        return await self.execute(sql, categoryID, telegramID, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_user_language(self, telegram_id, lang):
        sql = "UPDATE Users SET til=$1 WHERE telegram_id=$2"
        return await self.execute(sql, lang, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE USERS", execute=True)


#---------------------------------------------------------------------- 

    async def create_table_categories(self):
        sql = """
            CREATE TABLE IF NOT EXISTS CATEGORIES (
                id SERIAL PRIMARY KEY,
                userID VARCHAR(255) NOT NULL,
                title VARCHAR NOT NULL,
                wordListID INTEGER[] UNIQUE
            );
        """
        await self.execute(sql,execute=True)

    async def insert_new_kategory(self, title, userID):
        sql = """INSERT INTO CATEGORIES (title, userid) VALUES($1, $2) returning *"""
        return await self.execute(sql, title, str(userID), fetchrow=True, execute=True)

    async def insert_kategory_word(self, kategoryID: int, word_id: int):
        kategory = await self.select_kategory(kategoryID)
        try:
            if word_id in kategory.get("word_id_list"):
                return 0
        except TypeError:
            pass
        sql = """UPDATE CATEGORIES SET word_id_list=array_append(word_id_list,$2) WHERE id=$1"""
        return await self.execute(sql, kategoryID, word_id, execute=True)

    async def select_category(self, categoryID):
        sql = "SELECT * FROM CATEGORIES WHERE id=$1"
        return await self.execute(sql, categoryID, fetchrow=True, execute=True)

    async def delete_kategory(self, categoryID: int, telegram_id: int):
        sql = "UPDATE USERS SET categoryListID=array_remove(categoryListID,$1) where telegram_id=$2;"
        sql2 = "DELETE FROM CATEGORIES WHERE id=$1"
        await self.execute(sql2, categoryID, execute=True)
        return await self.execute(sql, categoryID, telegram_id, execute=True)

    async def drop_categories(self):
        sql = "DROP TABLE CATEGORIES;"
        await self.execute(sql, execute=True)


#-----------------------------------------------------------------

    async def create_table_words(self):
        sql = """
            CREATE TABLE IF NOT EXISTS WORDS (
                id SERIAL PRIMARY KEY,
                userID VARCHAR(255) NOT NULL,
                categoryID VARCHAR(255) NOT NULL,
                english VARCHAR(255) NOT NULL,
                synEng VARCHAR(255),
                definiton1 VARCHAR(255),
                antEng VARCHAR(255),
                definiton2 VARCHAR(255),
                uzbek VARCHAR(255)
            );
        """
        await self.execute(sql,execute=True)


    async def add_word(self,uz,eng,turi):
        sql = "INSERT INTO Words (eng,uz,turi) VALUES ($1, $2, $3 ) returning *"
        return await self.execute(sql, eng, uz, turi, fetchrow=True)


    async def select_word(self,**kwargs):
        sql = "SELECT * FROM Words WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    async def get_tables_list(self):
        return await self.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'",fetch=True)


    async def drop_words(self):
        return await self.execute("DROP TABLE Words;",execute=True)

#--------------------------------------------------------------------

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())