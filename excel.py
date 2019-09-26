import os
import pandas as pd
import xlrd


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


path = 'E:/excel/'

outfile = path + '/result.csv'
if os.path.exists(outfile):
    os.remove(outfile)

files = file_name(path)
result = pd.DataFrame(columns=['姓名', '住房公积金', '累计子女教育', '累计住房贷款利息', '累计住房租金', '累计赡养老人', '累计继续教育'])

for i in range(0, len(files)):
    data = xlrd.open_workbook(path+'/'+files[i])
    print(files[i])
    table = data.sheet_by_index(0)
    name = table.cell(int(3), int(1)).value
    gjj = table.cell(int(0), int(0)).value
    znjy = table.cell(int(13), int(6)).value
    dklx = table.cell(int(23), int(6)).value
    zfzj = table.cell(int(34), int(2)).value
    sylr = table.cell(int(37), int(6)).value
    jxjy = table.cell(int(16), int(2)).value
    result.loc[i] = [name, gjj, znjy, dklx, zfzj, sylr, jxjy]

result.to_csv(outfile, encoding="utf_8_sig")
