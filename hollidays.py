
import sys
from datetime import date, timedelta, datetime


# NewYearsday (01 01)              # 1 jan	Nyårsdagen
# ThirteenthNight (01, 05)        # 5 jan	Trettondagsafton
# Epiphany (01,06)  # 6 jan	Trettondedag jul


# VALBORG (4,30)                  # 30 apr	Valborgsmässoafton[Not 2]	Fast datum, 30 april
# MAYFIRST (05,01)                # 1 maj	Första maj	Fast datum, 1 maj

# NATDAY (6,6)                    # 6 jun	Sveriges nationaldag	Fast datum, 6 juni
# CHRISTMAS (12,24)               # 24 dec	Julafton[Not 3]	Fast datum, 24 december
# CHRISTMASDAY (12,25)            # 25 dec	Juldagen	Fast datum, 25 december
# CHRISTMASEVE (12,26)            # 26 dec	Annandag jul	Fast datum, 26 december
# NEWYEAR (12,31)                 # 31 dec	Nyårsafton[Not 3]	Fast datum, 31 december


# Maundy Thursday   	          Skärtorsdagen,	Rörligt datum, torsdagen före Påskdagen
# Good Friday 	                  Långfredagen	Rörligt datum, fredagen före Påskdagen
# Holy Saturday	                  Påskafton    Rörligt datum, lördagen före Påskdagen.
# Easter Day	                  Påskdagen	Rörligt datum, första söndagen efter ecklesiastisk fullmåne, efter vårdagjämningen
# Easter Monday	                  Annandag påsk	Rörligt datum, dagen efter påskdagen

# AscensionDay                    Kristi himmelsfärdsdag	Rörligt datum, sjätte torsdagen efter påskdagen
# PentecostNight                  Pingstafton	Rörligt datum, dagen före pingstdagen
# PentecostDay                    Pingstdagen	Rörligt datum, sjunde söndagen efter påskdagen

# Midsummer Eve                   Midsommarafton	Rörligt datum, fredagen mellan 19 juni och 25 juni (fredagen före midsommardagen)
# Midsummer Day	                  Midsommardagen	Rörligt datum, lördagen mellan 20 juni och 26 juni
# Halloween                       Allhelgonaafton	Rörligt datum, fredag mellan 30 oktober och 5 november
# All Saints Day                  Alla helgons dag	Rörligt datum, lördagen som infaller under perioden från 31 oktober till 6 november



class Holliday():

    Fast = {
        'NewYearsday'       :      ( 1,  1),
        'ThirteenthNight' :        ( 1,  5),
        'Epiphany' :               ( 1,  6),
        'Maundy Thursday' :        (0,0),
        'Good Friday' :            (0,0),
        'Holy Saturday' :          (0,0),
        'Easter Day' :             (0,0),
        'Easter Monday' :          (0, 0),
        'Valborg' :                (4, 30),
        'FirstOfMay' :             (5,  1),
        'NATDAY' :                 ( 6,  6),
        'CHRISTMAS' :              (12, 24),
        'CHRISTMASDAY' :           (12, 25),
        'CHRISTMASEVE' :           (12, 26),
        'NEWYEAR' :                (12, 31),
    }


    def __init__(self,year):
        self.year = year
        
        self._easterday = self.CalcEasterday()

        self._arr = self.asArray()

    def asArray(self):
        return [
            self.NewYearsday(),
            self.ThirteenthNight(),
            self.Epiphany(),
            self.MaundyThursday(),
            self.GoodFriday(),
            self.HolySaturday(),
            self.EasterDay(),
            self.EasterMonday(),
            self.Valborg(),
            self.FirstOfMay(),
            self.AscensionDay(),
            self.PentecostNight(),
            self.PentecostDay(),
            self.Natday(),
            self.MidsummerEve(),
            self.MidsummerDay(),
            self.Halloween(),
            self.AllSaintsDay(),
            self.ChristmasEve(),
            self.ChristmasDay(),            
            self.SecondDayOfChristmas(),
            self.NewYearsEve()
        ]

    def NewYearsday(self):
        return date(self.year, 1,1)

    def ThirteenthNight(self):
        return date(self.year, 1,5)

    def Epiphany(self):
        return date(self.year, 1,6)

    def MaundyThursday(self):
        return self.EasterDay() - timedelta(days=3)

    def GoodFriday(self):
        return self.EasterDay() - timedelta(days=2)

    def HolySaturday(self):
        return self.EasterDay() - timedelta(days=1)

    def EasterDay(self):
        return self._easterday

    def EasterMonday(self):
        return self.EasterDay() + timedelta(days=1)
    
    def Valborg(self):
        return date(self.year, 4, 30)

    def FirstOfMay(self):
        return date(self.year, 5, 1)

    def AscensionDay(self):
        return self.EasterDay() + timedelta(days=(4+5*7))

    def PentecostNight(self):
        return self.PentecostDay() - timedelta(days=(1))

    def PentecostDay(self):
        return self.EasterDay() + timedelta(days=(7*7))

    def Natday(self):
        return date(self.year, 6, 6)

    def MidsummerEve(self):
        return self.MidsummerDay() - timedelta(days= 1)

    def MidsummerDay(self):
        # måndag          0       => 5
        # Tisdag          1       => 4
        # Onsdag          2       => 3
        # torsdag         3       => 2   5 - x
        # fredag          4       => 1   5 - x
        # lördagen        5       => 0   5 - x + x // 6 
        # Söndag          6       => 6   5 - x + x // 6 * 7

        first = date(self.year, 6, 20)
        ret = self.getFirstAfter(5,first)
        return ret

    def Halloween(self):
        # måndag          0       => 4   4 - x 
        # Tisdag          1       => 3   4 - x
        # Onsdag          2       => 2   4 - x
        # torsdag         3       => 1   4 - x
        # fredag          4       => 0   4 - x
        # lördagen        5       => 6   4 - x + x // 5 * 7  
        # Söndag          6       => 5   4 - x + x // 5 * 7

        first = date(self.year, 10, 30)      
        # num = first.weekday()

        # delta = x - num + (num//y)*7

        # ret = first + timedelta(days= delta) 
        ret = self.getFirstAfter(4,first)

        return ret

        # måndag          0       => 1    
        # Tisdag          1       => 2   
        # Onsdag          2       => 3   
        # torsdag         3       => 4   
        # fredag          4       => 5   
        # lördagen        5       => 6    
        # Söndag          6       => 7   

    def getFirstAfter(self, weekday, searchDate):
        num = searchDate.weekday()
        
        x = weekday 
        y = weekday + 1
        delta = x - num + (num//y)*7
        
        ret = searchDate + timedelta(days= delta) 
        
        return ret 

    def AllSaintsDay(self):
        first = date(self.year, 10, 31)              
        ret = self.getFirstAfter(5,first)

        return ret

    def ChristmasEve(self):
        return date(self.year, 12, 24)

    def ChristmasDay(self):
        return date(self.year, 12, 25)

    def SecondDayOfChristmas(self):
        return date(self.year, 12, 26)

    def NewYearsEve(self):
        return date(self.year, 12, 31)

    def CalcEasterday(self):
        # 2013
        # M = 23
        # N = 5
        # a  = 2013 mod  19  => 18
        # b  = 2013 mod  4   =>  1
        # c  = 2013 mod  7   =>  4

        # d = (19 * a + m)  mod 30 =>  (19 * 18 +23) mod 30 => 5 

        # e = (2b + 4c + 6d + N ) mod 7 => 2*1 + 4*4 + 6*5 + 5) mod 7 => 4


        # if (d+e ) > 9 => 
        #  	påsk = (d+e-9) april
        # else
        # 	påsk = (22 + d + e ) mars
            

        # d + e = 5 + 4 = 9  < 10 = påsk = 22 + 5 + 4 => 31 Mars
        M = 24
        N = 5
        a = self.year % 19
        b = self.year % 4
        c = self.year % 7

        d = (19 * a + M)  % 30 

        e = (2*b + 4*c + 6*d + N ) % 7 

        if (d+e) > 9:
            day   = d + e - 9
            month = 4
        else:
            day = 22 + d + e 
            month = 3

        if (month == 4):

            if (day == 26):
                day = 19
            elif (day == 25):
                rest = (11 * M +11) % 30
                if (d == 28 and e == 6 and rest < 19):
                    day = 18

        return date(self.year,month, day)   


    def isHolliday(self, searchDate):

        ret = False
        if (searchDate.weekday() > 4):
            ret = True
        else:            
            if searchDate in self._arr:
                ret = True
        
        return ret



class Dates():
    months = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']
 
    def __init__(self):
        pass
        self.dates = {}
          
    def addD(self, d):
        year = d.year
        month = d.month-1
        if not year in self.dates:
            self.dates[year] = {}
        self.dates[year][Dates.months[month]] =  d
            

from enum import Enum
class Month(Enum):
    Janyary     = 'Januari'
    February    = 'Februari'
    March       = 'Mars'
    April       = 'April'
    May         = 'Maj'
    June        = 'Juni'
    July        = 'Juli'
    August      = 'Augusti'
    September   = 'September'
    October     = 'Oktober'
    November    = 'November'
    December    = 'December'

class PayDates():
    months = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']
 
    def __init__(self, year):
        
        self.pay = []
        self.create(year)

        #print(self.pay)

    def create(self, year):
        self.year = year

        self.pay.append({'start' : date(year, 1,  1), 'stop': self.getPayDay(year,  1, 24), 'month' : Month.December})
        self.pay.append({'start' : self.getPayDay(year, 1, 24), 'stop': self.getPayDay(year,  2, 24), 'month' : Month.Janyary})
        self.pay.append({'start' : self.getPayDay(year, 2, 24), 'stop': self.getPayDay(year,  3, 24), 'month' : Month.February})
        self.pay.append({'start' : self.getPayDay(year, 3, 24), 'stop': self.getPayDay(year,  4, 24), 'month' : Month.March})
        self.pay.append({'start' : self.getPayDay(year, 4, 24), 'stop': self.getPayDay(year,  5, 24), 'month' : Month.April})
        self.pay.append({'start' : self.getPayDay(year, 5, 24), 'stop': self.getPayDay(year,  6, 24), 'month' : Month.May})
        self.pay.append({'start' : self.getPayDay(year, 6, 24), 'stop': self.getPayDay(year,  7, 24), 'month' : Month.June})
        self.pay.append({'start' : self.getPayDay(year, 7, 24), 'stop': self.getPayDay(year,  8, 24), 'month' : Month.July})
        self.pay.append({'start' : self.getPayDay(year, 8, 24), 'stop': self.getPayDay(year,  9, 24), 'month' : Month.August})
        self.pay.append({'start' : self.getPayDay(year, 9, 24), 'stop': self.getPayDay(year, 10, 24), 'month' : Month.September})
        self.pay.append({'start' : self.getPayDay(year, 10,24), 'stop': self.getPayDay(year, 11, 24), 'month' : Month.October})
        self.pay.append({'start' : self.getPayDay(year, 11,24), 'stop': self.getPayDay(year, 12, 24), 'month' : Month.November})
        self.pay.append({'start' : self.getPayDay(year, 12,24), 'stop': date(year+1, 1, 1), 'month' : Month.December})

    def monthdelta(self,date, delta):
        m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
        if not m: m = 12
        d = min(date.day, [31,
            29 if y%4==0 and (not y%100==0 or y%400 == 0) else 28,
            31,30,31,30,31,31,30,31,30,31][m-1])
        return date.replace(day=d,month=m, year=y)
    
    def getPayDay(self, year, month, day):
        dd = date(year, month,day)
        return self._getPayDay(dd)

    
    def _getPayDay(self, searchDate):
        holliday = Holliday(searchDate.year)

        while(True):
            if (holliday.isHolliday(searchDate)):
                searchDate -= timedelta(days= 1)
            else:
                break
        
        # Spedial case when pay day on 24 or 23 and its a friday
        if searchDate.weekday() == 4 and (searchDate.day == 24 or searchDate.day == 23):
            if holliday.isHolliday(searchDate - timedelta(days= 1)) == False:
                searchDate -= timedelta(days= 1)

        # Special case johannes döpare
        #if (searchDate.month == 6 and searchDate.day == 24):
        #    if holliday.isHolliday(searchDate + timedelta(days= 1)) == False:
        #        searchDate += timedelta(days= 1)

        # Spedical case when pay day is 23 december
        if searchDate.month == 12 and searchDate.day == 23:
            searchDate = searchDate - timedelta(days= 1)
            while(True):
                if (holliday.isHolliday(searchDate)):
                    searchDate -= timedelta(days= 1)
                else:
                    break
        
        return searchDate

    def getPayMonth(self, d):
        if (d.year != self.year):
            self.create(d.year)
        month = ''

        for value in self.pay:

            #print("{} {}".format(value['start'], value['stop']))
            if value['start'] <= d < value['stop']:
                
                month = value['month'].value
                
                break
        
        return month
# =======================
#      MAIN PROGRAM
# =======================
if __name__ == "__main__":
    
    p = PayDates(2019)  
    dd = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
    
    start = datetime.strptime('2019-12-24', '%Y-%m-%d').date()
    stop = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    
    if start<= dd < stop:
       print("Betewween")

   
    print(p.getPayMonth(dd)) 
    exit(0)
    #dd = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
    #exit(0)
    payDate = Dates()
    
    payDate.addD(datetime.strptime('2019-01-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-02-22', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-03-22', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-04-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-05-23', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-06-25', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-07-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-08-22', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-09-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-10-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-11-22', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2019-12-20', '%Y-%m-%d').date())

    payDate.addD(datetime.strptime('2020-01-23', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-02-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-03-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-04-23', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-05-22', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-06-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-07-23', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-08-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-09-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-10-22', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-11-24', '%Y-%m-%d').date())
    payDate.addD(datetime.strptime('2020-12-22', '%Y-%m-%d').date())

    payDate.addD(datetime.strptime('2021-01-22', '%Y-%m-%d').date())

    calcPayDate = Dates()
    p = PayDates(2020)

    for year in [2019, 2020]:
        for month in range(1, 13):
            calcPayDate.addD(p.getPayDay(year, month, 24))

    calcPayDate.addD(p.getPayDay(2021, 1, 24))

    for year, banan in payDate.dates.items():
        for key in banan:
            print("{} {:<12}: {:<20} {:<20}".format(year, key, calcPayDate.dates[year][key].strftime('%Y-%m-%d'), payDate.dates[year][key].strftime('%Y-%m-%d')))
