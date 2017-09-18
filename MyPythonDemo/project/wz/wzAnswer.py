import requests, pymysql
import time as t
from bs4 import BeautifulSoup
from datetime import *
import logging
import os


class LocalDate():
    def __init__(self):
        self.mysql_user = 'root'
        self.mysql_password = '0122'
        self.mysql_database = 'db_wz_answer'
        pass

    def getAnswer(self):

        try:
            conn = pymysql.connect(user=self.mysql_user, password=self.mysql_password, database=self.mysql_database,
                                   charset="utf8")
            cursor = conn.cursor()
            cursor.execute("SELECT id,answer,date,question FROM tb_answer ORDER BY id DESC")
            values = cursor.fetchall()

            # 如果没有数据
            if (len(values) <= 0):
                return None

            data = values[0]
            # 如果数据不是今天的
            if not self.isToday(data[2]):
                logger.debug("数据库尚未收入今天答案")
                return None

            logger.debug("今天已经收录答案")
            return data[1], data[2], data[3]
        except Exception as e:
            logger.error(e)
            return None
        finally:
            cursor.close()
            conn.commit()
            conn.close()

    def isToday(self, dateStr):
        """
        答案是否为当天的
        :param dateStr:
        :return:
        """
        return dateStr == t.strftime("%Y-%m-%d")

    def insertAnswer(self, data):
        if data == None or len(data) != 4:
            return False

        try:
            conn = pymysql.connect(user=self.mysql_user, password=self.mysql_password,
                                   database=self.mysql_database, charset="utf8")
            cursor = conn.cursor()
            sql = "INSERT INTO tb_answer(question,answer,date,data_from,add_time)VALUES(%s,%s,%s,%s,NOW())"
            cursor.execute(sql, data)
            return True
        except Exception as e:
            logger.error(e)
            return False
        finally:
            cursor.close()
            conn.commit()
            conn.close()


class GetAnswer():
    def __init__(self):
        self.headers = {'User_Agent': 'Mozill/4.0(compatible; MSIE 6.0; Windows NT)'}

    def getHtml(self, url):
        re = requests.get(url, self.headers)
        if re.status_code != 200:
            logger.error("请求失败:" + str(re.status_code))
            return None

        html = re.content.decode("utf8", "ignore")
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def get_3987_answer(self, url):
        logger.debug("开始获取数据" + url)
        soup = self.getHtml(url)

        if not soup:
            return None

        table_all = soup.find_all("table")

        if not table_all or len(table_all) <= 0:
            logger.error("解析数据异常")
            return None

        table = table_all[0]
        tr_all = table.find_all('tr')

        if not tr_all or len(tr_all) <= 0:
            logger.error("解析数据异常")
            return None

        td_all = tr_all[1].find_all('td')

        if not td_all or len(td_all) <= 2:
            logger.error("解析数据异常")
            return None

        date = str(td_all[0].string)
        question = str(td_all[1].string)
        answer = str(td_all[2].string[2:])

        # date = td[0].find();
        # logger(date)

        date = t.strftime(str(datetime.now().year) + "-%m-%d", t.strptime(date, "%m月%d日"))

        if (localData.isToday(date)):
            logger.debug("活得最新数据:" + question + "--" + answer + "--" + str(date))
            return question, answer, date, url
        else:
            logger.debug("题目数据不是今天的：" + date)
            return None


if __name__ == '__main__':
    fileName = "./answer_log/"
    if not os.path.exists(fileName):
        os.makedirs(fileName)

    # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(fileName + str(t.strftime("%Y_%m_%d")) + '.log')
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    # formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]:%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    localData = LocalDate()
    getAnswer = GetAnswer();
    logger.debug("=====脚 本 开 始 运 行=====")

    local_answer = localData.getAnswer()

    if not local_answer or not localData.isToday(local_answer[1]):
        logger.debug("当天数据不存在，开始获取数据")

        num = 0
        while True:
            num += 1

            logger.debug("第" + str(num) + "次获取数据")

            answers = getAnswer.get_3987_answer("http://app.3987.com/gonglue/16917.html")

            if answers:
                logger.debug("获取数据正常，开始插入数据库")
                statu = localData.insertAnswer(answers)
                if statu:
                    logger.debug("插入数据成功")
                    break
                else:
                    logger.error("插入数据失败")

            else:
                logger.debug("返回数据不符合要求")

            t.sleep(60 * 30)

    else:
        logger.debug("当天数据已存在，开始检查更新")

        answers = getAnswer.get_3987_answer("http://app.3987.com/gonglue/16917.html")

        isUpdata = False

        if not local_answer[2] == answers[0]:
            logger.debug("题目不一致")
            isUpdata = True

        if not local_answer[0] == answers[1]:
            logger.debug("答案不一致")
            isUpdata = True

        if isUpdata:
            logger.debug("需要更新题库")
            if answers:
                logger.debug("开始插入数据库")
                statu = localData.insertAnswer(answers)
                if statu:
                    logger.debug("插入数据成功")
                else:
                    logger.error("插入数据失败")
            else:
                logger.debug("返回数据不符合要求")

        else:
            logger.debug("题库不需要更新")

    logger.debug("运行结束，关闭脚本")
    logger.debug("=========================\n")
