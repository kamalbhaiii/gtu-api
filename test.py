import datetime

date = datetime.datetime.now()
todaysDate = [date.strftime(f'%d-%B-%Y').split('-')]
# print(todaysDate[0][1][0:3])
todaysDate = f"{todaysDate[0][0]}-{todaysDate[0][1][0:3]}-{todaysDate[0][2]}"
print(todaysDate)