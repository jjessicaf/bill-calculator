import sqlite3 as sl
from io import BytesIO
from PIL import Image


db = "app.db"

def create():
    """
    creates the database
    :return: none
    """
    conn = sl.connect(db)
    curs = conn.cursor()

    curs.execute('''
        CREATE TABLE IF NOT EXISTS images (
            filename TEXT PRIMARY KEY,
            data BLOB
        )
    ''')

    conn.commit()  # commit changes before continuing
    conn.close()

def remove_table(tb_name):
    """
    clears entries in database
    :return: none
    """
    conn = sl.connect(db)
    curs = conn.cursor()

    # remove table
    curs.execute("DROP TABLE IF EXISTS images;")

    conn.commit()
    conn.close()

def get_taxrates():
    """
    gets tax rates from api, stores in file
    :return: none
    """
    # find api with tax rates for each state


    # scrape using beautifulsoup

    # store in file
    return 1

def upload_image(image_file):
    """
    stores data from file into specified table in database
    :param fn: name of file storing data
    :param data: data of file
    :return: none
    """

    remove_table('images')
    create()
    img = Image.open(image_file)

    # Convert the image to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    data = img_bytes.getvalue()

    fn = image_file.filename

    if fn is None or data is None:
        return False

    conn = sl.connect(db)
    curs = conn.cursor()

    curs.execute('''
            INSERT OR REPLACE INTO images (filename, data) VALUES (?, ?)
        ''', (fn, sl.Binary(data)))

    conn.commit()
    conn.close()
    return fn

def get_image(fn):
    if fn is None:
        return False

    conn = sl.connect(db)
    curs = conn.cursor()

    # retrieve the image path
    curs.execute('''
            SELECT data FROM images WHERE filename = ?
        ''', (fn,))

    result = curs.fetchone()

    curs.close()
    conn.close()
    return result

    if result is None:
        return None, 404

    # Get the image data from the result
    image_data = result[0]
    img_bytes = BytesIO()
    image_data.save(img_bytes, format='JPEG')
    image_data = img_bytes.getvalue()

    curs.close()
    conn.close()

    return image_data

