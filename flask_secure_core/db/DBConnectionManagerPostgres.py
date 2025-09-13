# DBConnectionManagerPostgres.py
# -*- coding: utf-8 -*-
"""This module manages the PostgreSQL database connection for flask_secure_core.
It includes methods to initialize the database, verify integrity, and manage the connection."""

from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
import time

import colorlogx.logger as colorlogx
logger = colorlogx.get_logger("DBConnectionManagerPostgres")

def read_sql_file(filepath):
    with open(filepath, "r") as file:
        return file.read()
    
class DBConnectionManager:
    _instance = None
    _pool = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DBConnectionManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, db_name, db_user, db_password, db_host='localhost', db_port=5432, minconn=3, maxconn=10, recreate_db=False):
        if self._pool is not None:
            return
        
        logger.info("Initializing PostgreSQL database connection pool...")
        try:
            self._pool = ThreadedConnectionPool(
                minconn=minconn,
                maxconn=maxconn,
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
        except Exception as e:
            logger.critical(f"Failed to connect to PostgreSQL database: {e}")
            raise
        logger.info("PostgreSQL database connection pool established")
        logger.info("Verifing database integrity...")
        self.__conn = self.__get_connection()
        if not self.__conn:
            logger.critical("Failed to create a database connection.")
            raise Exception("Database connection failed.")
        self.__cursor = self.__conn.cursor()
        self.__verify_db_integrity(recreate_db)
        self.__cursor.close()
        self.release_connection(self.__conn)
        
    def __verify_db_integrity(self, recreate_db):
        try:
            self.__cursor.execute("SELECT 1")
            if self.__cursor.fetchone() is None:
                logger.error("Database integrity check failed: No response from database.")
                raise Exception("Database integrity check failed.")
            if len(self.__get_all_tables()) == 0 or recreate_db:
                if not recreate_db: 
                    logger.error("Database integrity check failed: No tables found in the database. Initiating tables...") 
                else: 
                    logger.info("Recreating database tables as requested.")
                self.__init_db()
            logger.info("Database integrity verified successfully.")
        except Exception as e:
            logger.error(f"Error during database integrity verification: {e}")
            raise
    
    def __get_all_tables(self):
        """
        Retrieves all table names from the connected database.

        Parameters:
        None

        Returns:
        tables (list): A list of tuples, where each tuple contains one table name.
        """
        query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema');"
        try:
            logger.debug(f"executing SQL query: {query}")
            self.__cursor.execute(query)
            tables = self.__cursor.fetchall()
        except Exception as e:
            logger.error(f"Error retrieving table names: {e}")
        logger.debug(f"Table names retrieved: {tables}")
        return tables

    def __init_db(self):
        """
        WARNING: This function wipes the fsl scheme.

        This function drops the existing database schema and recreates 
        it by executing the SQL query from the initDB.sql file.
        It then commits the changes and prints a success message.

        Returns:
        bool: True if the tables are successfully initiated, False otherwise.

        Raises:
        Exception: If an error occurs while executing the SQL query or committing 
                   the changes.
        """
        logger.debug("create_tables is called")
        logger.debug("dropping existing tables in 5 seconds...\nPress strg+c to cancel")
        
        
        self.__drop_db()
        query = read_sql_file("./flask_secure_core/db/initDBv1.sql")
        logger.debug(f"executing SQL query: {query}")
        try:
            self.__cursor.execute(query)
            self.__conn.commit()
            from ..utils import hash_password
            self.__cursor.execute("INSERT INTO fsl.users (username, password, access_level) VALUES (%s, %s, %s)",
            ("admin", hash_password("admin"), 0))
            self.__conn.commit()

            logger.info("Tables initiated successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            self.__conn.rollback()
            return False
        return True
    
    def __drop_db(self):
        """
        WARNING: This function wipes the fsl scheme.
        Drops the fsl schema and recreates it. This is used to reset the database.

        Parameters:
        None

        Returns:
        None
        """
        logger.warning("\nDropping database in 5 Seconds!\n\n!!!! To cancel press CTRL+C !!!!\n")
        for i in range(5, 0, -1):
            print(f"Reset in {i}...")
            time.sleep(1)
        query = "DROP SCHEMA fsl CASCADE;"
        try:
            logger.debug(f"executing SQL query: {query}")
            self.__cursor.execute(query)
            logger.info("scheme fsl dropped")
            self.__conn.commit()
        except Exception as e:
            logger.error(f"Error dropping scheme fsl: {e}")
            self.__conn.rollback()


    def __get_connection(self):
        """
        Borrow a connection from the pool.
        """
        try:
            return self._pool.getconn()
        except Exception as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise
        
    def release_connection(self, conn):
        """
        Return a connection to the pool.
        """
        try:
            self._pool.putconn(conn)
        except Exception as e:
            logger.error(f"Error releasing connection to pool: {e}")
            raise

    
    def get_db_conn(self):
        """
        Get a new database connection from the pool.
        """
        conn = self.__get_connection()
        if not conn:
            logger.error("Failed to get a database connection.")
            raise Exception("Database connection failed.")
        return conn