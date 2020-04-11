from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64encode
import mysql.connector
from mysql.connector import Error

block_size = AES.block_size


def pad(plain_text):
    number_of_bytes_to_pad = block_size - len(plain_text) % block_size
    ascii_string = chr(number_of_bytes_to_pad)
    padding_str = number_of_bytes_to_pad * ascii_string
    padded_plain_text = plain_text + padding_str
    return padded_plain_text


key = b'weJiSEvR5yAC5ftB'
iv = b'ssdkF$HUy2A#D%kd'


def encrypt(text):
    text = pad(text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_text = cipher.encrypt(text.encode('utf-8'))
    return b64encode(encrypted_text).decode("utf-8")


def insertToDB(mail):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='eventosjobo',
                                             user='root',
                                             password='1234')

        cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO correos (correos) VALUE (%s)"""

        encryptedMail = encrypt(mail)

        print(encryptedMail)
        cursor.execute(sql_insert_query, (encryptedMail,))
        connection.commit()

        print("Data inserted successfully into employee table using the prepared statement")

    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


insertToDB('anunciosjobo@gmail.com')