from eCommerce_DataGenerator import Utils
import sqlite3

conn = sqlite3.connect('eCommerce_Simulation.db')
Utils.create_tables(conn)
conn.close()
