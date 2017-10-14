from flask import Flask
from flask import request
import pymysql

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return "wz好的"+getAnswer()


def getAnswer():
    try:
        conn = pymysql.connect(user="root", password="0122", database="db_wz_answer",
                               charset="utf8")
        cursor = conn.cursor()
        cursor.execute("SELECT id,answer,date FROM tb_answer ORDER BY id DESC")
        values = cursor.fetchall()

        # 如果没有数据
        if (len(values) <= 0):
            return None

        data = values[0]
        return data[1]
    except Exception as e:
        return None
    finally:
        cursor.close()
        conn.commit()
        conn.close()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)