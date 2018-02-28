# 将淘宝客的excel表数据导入到数据库中
import xlrd
import pymysql
import time

print(time.strftime('%H:%M:%S',time.localtime(time.time()))+"打开excel中...")
data = xlrd.open_workbook('demo2.xls')
table = data.sheet_by_index(0)
print(time.strftime('%H:%M:%S',time.localtime(time.time()))+"打开成功")


def insert(sql):
    try:
        print(time.strftime('%H:%M:%S', time.localtime(time.time())) + "开始插入数据库")
        print(sql)
        conn = pymysql.connect(user='root', password='0122',
                               database='db_bibuweb', charset="utf8")

        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        # 发生错误时回滚
        conn.rollback()
        print("执行Mysql: % s时出错： % s" % (sql, e))
    finally:
        cursor.close()
        conn.close()
        print(time.strftime('%H:%M:%S', time.localtime(time.time())) + "插入完成")


def input(start,end):
    sql = "INSERT INTO api_discounts(commodity_id,commodity,commodity_image,commodity_detail,commodity_type,tbk_url,commodity_price,volume,income_rate,tbk_brokerage,seller_wangwang,seller_id,store_name,store_type,coupon_id,coupon_total,coupon_surplus,coupon_price,coupon_start_time,coupon_end_time,coupon_url,coupon_generalize_url)VALUES"
    print(time.strftime('%H:%M:%S', time.localtime(time.time())) + "开始遍历数据表")
    for nrows in range(start, end):
        commodity_id = pymysql.escape_string(table.cell_value(nrows, 0))
        commodity = pymysql.escape_string(table.cell_value(nrows, 1))
        commodity_image = pymysql.escape_string(table.cell_value(nrows, 2))
        commodity_detail = pymysql.escape_string(table.cell_value(nrows, 3))
        commodity_type = str(table.cell_value(nrows, 4))

        tbk_url = pymysql.escape_string(table.cell_value(nrows, 5))
        commodity_price = float(table.cell_value(nrows, 6))
        volume = int(table.cell_value(nrows, 7))
        income_rate = float(table.cell_value(nrows, 8))
        tbk_brokerage = float(table.cell_value(nrows, 9))

        seller_wangwang = pymysql.escape_string(table.cell_value(nrows, 10))
        seller_id = pymysql.escape_string(table.cell_value(nrows, 11))
        store_name = pymysql.escape_string(table.cell_value(nrows, 12))
        store_type = pymysql.escape_string(table.cell_value(nrows, 13))
        coupon_id = pymysql.escape_string(table.cell_value(nrows, 14))

        coupon_total = int(table.cell_value(nrows, 15))
        coupon_surplus = int(table.cell_value(nrows, 16))
        coupon_price = pymysql.escape_string(table.cell_value(nrows, 17))
        coupon_start_time = pymysql.escape_string(table.cell_value(nrows, 18))
        coupon_end_time = pymysql.escape_string(table.cell_value(nrows, 19))

        coupon_url = pymysql.escape_string(table.cell_value(nrows, 20))
        coupon_generalize_url = pymysql.escape_string(table.cell_value(nrows, 21))

        value = "('%s','%s','%s','%s','%s','%s',%f,%d,%f,%f,'%s','%s','%s','%s','%s',%d,%d,'%s','%s','%s','%s','%s')" % (
            commodity_id, commodity, commodity_image, commodity_detail, commodity_type, tbk_url, commodity_price,
            volume,
            income_rate, tbk_brokerage, seller_wangwang, seller_id, store_name, store_type, coupon_id, coupon_total,
            coupon_surplus, coupon_price, coupon_start_time, coupon_end_time, coupon_url, coupon_generalize_url)
        sql = sql + value + ",";
    print(time.strftime('%H:%M:%S', time.localtime(time.time())) + "遍历完成")
    insert(sql[0:-1])


input(1,3000)
input(3000,6000)
input(6000,8000)
input(8000,table.nrows)
