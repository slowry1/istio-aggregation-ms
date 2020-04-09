import json
import pandas as pd
from datetime import datetime

class API_One_Processor:
    def __init__(self, data):
        self._df = pd.DataFrame(data=data).set_index('Country')
        self._indexes = self._df.index.unique()
        self._output_json = {}

    def _clean(self):
        #Remove provinces with recovered
        self._df = self._df[self._df.Province != 'Recovered']

        #Remove all rows with NaN values
        self._df = self._df.dropna(
            subset=['Confirmed', 'Deaths', 'Recovered', 'Active']
        )

        #format date and times
        self._time_date_formatter()

    def _build(self):
        for en in self._indexes:
            self._create_output_json(en)
        return self._output_json
    
    def _create_output_json(self, en):
        if en in self._output_json:
            pass
        else:
            build_output_obj = {}

            #Total Deaths
            build_output_obj['total deaths'] = int(self._df.loc[
                en, ['Deaths']].max().Deaths)
            
            #Total Confirmed
            build_output_obj['total confirmed'] = int(self._df.loc[
                en, ['Confirmed']].max().Confirmed)
            
            #Total Recovered
            build_output_obj['total recovered'] = int(self._df.loc[
                en, ['Recovered']].max().Recovered)
            
            #Total Active
            build_output_obj['total active'] = int(self._df.loc[
                en, ['Active']].max().Active)
            
            #Get lat/lon Dataframe
            lat_lon_df = self._df.loc[en, ['Lat', 'Lon']]
            lat_lon_obj = lat_lon_df.iloc[0][['Lat', 'Lon']]
            
            #Store lat/lon in obj
            build_output_obj['lat'] = float(lat_lon_obj['Lat'])
            build_output_obj['lon'] = float(lat_lon_obj['Lon'])
            
            #Get countrycode
            country_code_df = self._df.loc[en, ['CountryCode']]
            build_output_obj['country code'] = country_code_df.iloc[0][
                ['CountryCode']]['CountryCode']
            
            #Add it to output object
            self._output_json[en] = build_output_obj

    def _time_date_formatter(self, t_format="%Y-%m-%dT%H:%M:%SZ"):
        #format time to datetime obj
        dates = [datetime.strptime(
            t, t_format) for t in self._df['Date']
        ]

        #Covert to UTC
        self._df['Date'] = pd.to_datetime(dates, 
        errors='coerce').tz_localize('UTC').tz_convert('US/Pacific')
        
        #Remove any rows with invalid date. 
        self._df = self._df.dropna(subset=['Date'])

        #Covert completely to date. Remove time
        self._df['Date'] = self._df['Date'].dt.date
        

    def process(self):
        #clean
        self._clean()

        #format time
        #self._means()

        #Build output object
        return json.dumps(self._build())
        

