import xlrd

data = xlrd.open_workbook('demo2.xls')

table = data.sheets()[0]

print(table.nrows)
print(table.ncols)

print(table.row_values(1)[1])

for nrow in range(1,table.nrows):
    print(table.row_values(nrow)[1]+"------"+str(table.row_values(nrow)[6]))
