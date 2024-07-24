import pandas as pd
df = pd.read_csv('data_for_dash_01.csv',encoding='utf-8-sig')
lines = df['comments']
with open('comment.txt', 'w',encoding='utf-8-sig') as file:
    i = 1
    for line in lines:
        file.write(f'{i}.'+ line + '\n')
        i += 1
##---------------------------ให้บอททำการสรุป ------------------------------##

##---------------------------อ่านเพื่อนำไปสู่ HTML ------------------------------##
with open('comment.txt', 'r',encoding='utf-8-sig') as file:
    look = file.read()
    print(look)