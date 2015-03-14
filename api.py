
class client:
    import requests
    import datetime
    URL = "http://api.erail.in/{0}/"
    API_KEY = ""

    def __init__(self, apikey):
        self.API_KEY = apikey

    def __getdate(self, date):
        # erail API only expects first 3 characters
        # from the Month name (ex. sep, mar), but
        # this will work as well
        return date.strftime("%d-%B-%Y")

    def get(self, action, params=dict()):
        self.URL = self.URL.format(action)
        params["key"] = self.API_KEY
        r = self.requests.get(self.URL, params=params)
        if (r.status_code == self.requests.codes.ok):
            return r.json()
        return None

    def station_list(self):
        # get all stations
        return self.get('stations')
        
    def trains(self, stnfrom, stnto, date=None, cls=None):
        # get trains between 2 stations
        params = dict()
        params = dict()
        params['stnfrom'] = stnfrom
        params['stnto'] = stnto

        if (date):
            erail_date = self.__getdate(date)
            params['date'] = erail_date

        if (cls):
            params['class'] = cls

        return self.get('trains', params)

    def route(self, train):
        # get route of given train no.
        params = dict()
        params['trainno'] = train
        return self.get('route', params)

    def full_route(self, train):
        # same as route but returns all passing stations
        params = dict()
        params['trainno'] = train
        return self.get('route', params)

    def fare(self, train, frm, to, age, quota, date, cls=None):
        # fare from source to destination
        params = dict()
        params['trainno'] = train
        params['stnfrom'] = frm
        params['stnto'] = to
        params['age'] = age
        params['quota'] = quota
        params['date'] = self.__getdate(date)

        if cls:
            params['class'] = cls

        return self.get('fare', params)

    def pnr_status(self, pnr):
        # get details of pnr status
        params = dict()
        params['pnr'] = pnr
        return self.get('pnr', params)

    def live_status(self, train, frm, date):
        # current running status of the train
        params = dict()
        params['trainno'] = train
        params['stnfrom'] = frm
        params['date'] = self.__getdate(date)
        return self.get('live', params)

    def seat_availability(self, train, frm, to, quota, cls, date):
        # return the seat availability for a train
        params = dict()
        params['trainno'] = train
        params['stnfrom'] = frm
        params['stnto'] = to
        params['quota'] = quota
        params['class'] = cls
        params['data'] = self.__getdate(date)
        return self.get('seats', params)

    def coach_composition(self, train):
        # return information on all the coaches in train
        params = dict()
        params['trainno'] = train
        return self.get('coaches', params)

    def cancelled_trains(self, reldate):
        # return cancelled trains, reldate
        # can be TD, YS or TM
        params = dict()
        params['date'] = reldate
        return self.get('cancelled', params)

    def diverted_trains(self, reldate):
        # return diverted trains, reldate
        # can be TD, YS or TM
        params = dict()
        params['date'] = reldate
        return self.get('diverted', params)

    def rescheduled_trains(self, reldate):
        # return rescheduled trains, reldate
        # can be TD, YS or TM
        params = dict()
        params['date'] = reldate
        return self.get('rescheduled', params)

    def trains_at_station(self, frm, hr, to=None):
        # return train from station within given hours
        params = dict()
        params['stnfrom'] = frm
        params['hr'] = hr
        if (to):
            params['stnto'] = to
        return self.get('trainsatstation', params)

if __name__ == "__main__":
    import datetime
    import os
    if (os.path.isfile(".key.erail")):
        with open(".key.erail") as f:
            key = f.readline()
    else:
        key = raw_input("enter API key: ")
        with open(".key.erail", 'w') as f:
            f.write(key)

    e = client(key)
    #r = e.trains_at_station('NDLS', 1, 'BCT')
    r = e.live_status(12138, 'NDLS', datetime.date(2015, 3, 15))
    print type(r)
    print r
