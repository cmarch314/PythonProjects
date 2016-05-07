import re

# Use day_dict and is_leap_year in your tomorrow function

day_dict ={ 1 : 31,
            2 : 28,
            3 : 31,
            4 : 30,
            5 : 31,
            6 : 30,
            7 : 31,
            8 : 31,
            9 : 30,
           10 : 31, 
           11 : 30,
           12 : 31} 

def is_leap_year(month:int)->bool:
    return (month%4 == 0 and month%100 != 0) or month%400==0

def days_in(month:int,year:int)->int:
    return (29 if month==2 and is_leap_year(year) else day_dict[month])


def tomorrow(date:str)->str:
    valid = re.match("^([1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01])/([0-9]{4}|[0-9]{2})$",date)
    if valid and (int(valid.group(2)) <= day_dict[int(valid.group(1))] or (int(valid.group(2))==29 and int(valid.group(1))==2 and int(valid.group(3))%4 == 0)):
        month,day,year = (int(d) for d in valid.groups())
        year = (year+2000 if year < 100 else year)
        day = (1 if (day >= day_dict[month] and not(year%4 == 0 and month ==2 and day == 28))else day + 1)
        day = (1 if (month == 2 and day == 30 )else day)
        month = ( (month)%12+1 if (day == 1) else month)
        year = (year+1 if (day == 1 and month == 1 )else year)
        return "{}/{}/{}".format(month,day,year)
    else:
        raise AssertionError
if __name__ == '__main__':
    import driver, prompt,traceback
    while True:
        date = prompt.for_string('Enter date to test (quit to start driver)')
        if date == 'quit':
            break;
        try:
            print('tomorrow=',tomorrow(date))
        except:
            print('tomorrow raised exception')
            traceback.print_exc()
        
    driver.driver()
