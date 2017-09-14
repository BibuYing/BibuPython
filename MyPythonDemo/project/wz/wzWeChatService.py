import itchat
import pymysql
import time
import logging
import threading
import os
import datetime


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
            cursor.execute("SELECT id,answer,date FROM tb_answer ORDER BY id DESC")
            values = cursor.fetchall()

            # 如果没有数据
            if (len(values) <= 0):
                return None

            data = values[0]
            # 如果数据不是今天的
            if not self.isToday(data[2]):
                logger.debug("数据不是今天")
                return None

            logger.debug("数据是今天")
            return data[1]
        except Exception as e:
            logger.debug(e)
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
        return dateStr == time.strftime("%Y-%m-%d")

    def getSendUser(self):
        try:
            conn = pymysql.connect(user=self.mysql_user, password=self.mysql_password, database=self.mysql_database,
                                   charset="utf8")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_name FROM tb_user WHERE DATE_FORMAT(last_push_time,'%Y-%m-%d')!=DATE_FORMAT(now(),'%Y-%m-%d') OR ISNULL(last_push_time)")
            values = cursor.fetchall()
            return values
        except Exception as e:
            logger.error(e)
            return None
        finally:
            cursor.close()
            conn.commit()
            conn.close()

    def updataSendUserTime(self, userName):
        logger.debug("更新" + userName + "的推送记录")
        try:
            conn = pymysql.connect(user=self.mysql_user, password=self.mysql_password, database=self.mysql_database,
                                   charset="utf8")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tb_user SET push_num = push_num+1,last_push_time = now() WHERE user_name=%s", userName)
            values = cursor.fetchall()
            logger.debug("更新成功")
            return values
        except Exception as e:
            logger.error(e)
            logger.debug("更新失败")
            return None
        finally:
            cursor.close()
            conn.commit()
            conn.close()


class WeChat():
    def __init__(self):
        login = itchat.auto_login(hotReload=True)
        # itchat.run()

    @itchat.msg_register(itchat.content.TEXT)
    def text_reply(msg):

        remarkName = msg['User']['RemarkName']
        text = msg['Text']
        logger.info("收到 " + remarkName + " 的信息：" + text)

        # return "自动回复: " + msg['Text']
        answer = localData.getAnswer()
        if answer:
            answer = "wz" + answer
            localData.updataSendUserTime(remarkName);
        else:
            answer = "今天还没答案"

        logger.debug("返回:" + answer)
        return answer

    def send(self, user, text):
        friends = itchat.search_friends(name=user)
        if friends:
            itchat.send(text, toUserName=friends[0]['UserName'])
        else:
            logger.debug("找不到该好友:" + user)
        pass


def pushAnswer():
    users = localData.getSendUser()
    if not users:
        logger.debug("推送列表为空，今天无需再推送")
        return

    logger.debug("今天需要推送的用户:" + str(users))

    answer = localData.getAnswer()

    if not answer:
        logger.error("当天需要推送的数据为空")
    else:
        answer = "wz" + answer
        for user in users:
            weChat.send(user[0], answer)
            localData.updataSendUserTime(user[0])
            logger.debug("已推送:" + user[0])
            time.sleep(5)


if __name__ == '__main__':

    fileName = "./wechat_log/"
    if not os.path.exists(fileName):
        os.makedirs(fileName)

    # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(fileName + str(time.strftime("%Y_%m_%d")) + '.log')
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

    localData = LocalDate()
    weChat = WeChat()

    wechat_run = threading.Thread(target=itchat.run)
    wechat_run.start()

    while True:
        nowTime = int(time.time())
        today = datetime.datetime.now()

        # 获取0点时间戳
        zt = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        zeroTime = int(time.mktime(zt.timetuple()))

        if nowTime > zeroTime and nowTime < zeroTime + 62:
            logger.debug("\n======" + str(time.strftime("%Y-%m-%d")) + "======")

        dt = datetime.datetime(today.year, today.month, today.day, 19, 30, 0)
        pushTime = int(time.mktime(dt.timetuple()))

        if int(nowTime) in range(pushTime - 31, pushTime + 31):
            pushAnswer()

        time.sleep(1 * 60)
