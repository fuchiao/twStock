import csv
#Date,Open,High,Low,Close,Volume,Adj Close
class Account():
    def __init__(self):
        self.balance = 1000000
        self.stock = 0
        self.log = []
    def buy(self, price, date):
        # if last buy earns, buy more
        if self.balance > price*1000:
            self.balance -= price*1000
            self.stock += 1
            self.log.append({"buyPrice": price, "sellPrice":0, "buyDate":date, "sellDate":None})
    def sell(self, price, date):
        # if last buy loses, sell more
        if self.stock > 1:
            self.stock -= 1
            self.balance += price *1000
            for i in range(len(self.log)):
                if self.log[i]["sellPrice"] == 0:
                    self.log[i]["sellPrice"] = price
                    self.log[i]["sellDate"] = date
                    break
    def checkStopLoss(self, price, date):
        # not effective
        for i in range(len(self.log)):
            if self.log[i][1] == 0 and self.log[i][0] * 0.9 > price:
                self.sell(price, date)

    def value(self, price):
        return self.balance + (self.stock * price*1000)
    def printLog(self):
        for i in self.log:
            print i

class Taiex():
    def __init__(self):
        self.record = []
        with open('TWII.csv', 'r') as f:
            csv.DictReader(f)
            for i in reversed(list(csv.DictReader(f))):
                i["Open"] = float(i["Open"])
                i["High"] = float(i["High"])
                i["Low"] = float(i["Low"])
                i["Close"] = float(i["Close"])
                i["Adj Close"] = float(i["Adj Close"])
                i["Volume"] = int(i["Volume"])
                self.record.append(i)

        self.lowAry = []
        self.highAry = []
        self.k = 50.0
        self.d = 50.0

    def nextDay(self, i):
        if len(self.record) <= i:
            return False
        self.lowAry.append(self.record[i]["Low"])
        self.highAry.append(self.record[i]["High"])
        while len(self.lowAry) > 9:
            del self.lowAry[0]
        while len(self.highAry) > 9:
            del self.highAry[0]
        rsv = 100 * (self.record[i]["Close"] - min(self.lowAry))/(max(self.highAry) - min(self.lowAry))
        self.k = (self.k*2 + rsv)/3
        self.d = (self.d*2 + self.k)/3
        return True

    def dailyUpdate(self):
        curr = 0
        while self.nextDay(curr):
            curr += 1
            if len(self.record) > curr:
                yield self.record[curr]["Date"], self.k, self.d
            else:
                yield None, self.k, self.d

class target():
    def __init__(self):
        self.account = Account()
        self.taiex = Taiex()
        self.target = []
        with open('0050.csv', 'r') as f:
            for i in reversed(list(csv.DictReader(f))):
                i["Open"] = float(i["Open"])
                i["High"] = float(i["High"])
                i["Low"] = float(i["Low"])
                i["Close"] = float(i["Close"])
                i["Adj Close"] = float(i["Adj Close"])
                i["Volume"] = int(i["Volume"])
                self.target.append(i)
    def getThru(self, fast, slow):
        diff = [slow[0]-fast[0], slow[1]-fast[1]]
        if diff[0] * diff[1] >= 0:
            return 0
        if diff[0] > 1:
            return 1
        elif diff[0] > -1:
            return -1
        else:
            return 0
            
    def test(self):
        i = 0
        logcd = 0
        log = []
        lastK = []
        lastD = []
        for date, k, d in self.taiex.dailyUpdate():
            if self.target[i]["Date"] > date:
                continue
            while i < len(self.target)-1 and self.target[i]["Date"] < date:
                i += 1
            lastK.append(k)
            while len(lastK) > 2:
                del lastK[0]
            lastD.append(d)
            while len(lastD) > 2:
                del lastD[0]
            if self.target[i]["Date"] == date and len(lastK) == 2 :
                if k > 80 and self.getThru(lastK, lastD) == -1:
                    self.account.sell(self.target[i]["Open"], date)
                elif k < 50 and self.getThru(lastK, lastD) == 1:
                    self.account.buy(self.target[i]["Open"], date)
                if logcd == 0:
                    log.append([self.target[i]["Date"], self.account.value(self.target[i]["Close"])])
                    logcd = 22
                else:
                    logcd -= 1
                print self.target[i]["Date"], self.account.stock, self.account.balance, self.account.value(self.target[i]["Close"])
        print log
        self.account.printLog()

def main():
    t = target()
    t.test()

if __name__ == "__main__":
    main()
