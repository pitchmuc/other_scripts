# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:00:00 2018

@author: piccini
"""
import json as _json
import datetime as _datetime
from collections import defaultdict
import pandas as _pd

class reader:
    data = {}
    entries = []
    _entryKeys = {'startedDateTime':0,'time':0,'request':0,'response':0,'cache':0,'timings':0,'serverIPAddress':0,'connection':0}
    def __init__(self,data):
        """
        Takes a har file data and loads its data in memory for futher calculation.
        data : either 
            - file name of the har 
            - text string retrieved in a variable (ie : open(myfile.har).read())
            - dictionary from the JSON of the HAR file
        """
        if type(data) == dict:
            j_data = data
        elif '.json' in data or '.txt' in data or '.har' in data:
            j_data = _json.loads(open(data,'r',encoding='utf8').read())
        elif type(data) == str :
            j_data = _json.loads(data)
        log_data = j_data['log']
        self.data = log_data
        self.entries = self.data['entries']
        for data in self.entries[0]['request']['headers']: 
            if data['name'] == 'User-Agent':
                self.userAgent = data['value']
    
    def toTimeStamp(self,string):
        """
        This methods enable you to change the entry ['startedDateTime'] to timestamp
        """
        time = _datetime.datetime.strptime(string,'%Y-%m-%dT%H:%M:%S.%fZ')
        return time.timestamp()
    
    def summary(self):
        """
        This methods returns a dictionnary that contains the aggregated data
        """
        sum_data = dict()
        sum_data['nb_entries'] = len(self.entries)
        sum_data['total_time'] = sum((self.entries[x]['time'] for x in range(len(self.entries))))
        sum_data['total_headersSize'] = sum((self.entries[x]['request']['headersSize'] for x in range(len(self.entries)) if self.entries[x]['request']['headersSize'] != -1))
        sum_data['missing_headersSize'] = abs(sum((self.entries[x]['request']['headersSize'] for x in range(len(self.entries)) if self.entries[x]['request']['headersSize'] == -1)))
        sum_data['total_bodySize'] = sum((self.entries[x]['request']['bodySize'] for x in range(len(self.entries)) if self.entries[x]['request']['bodySize'] != -1))
        sum_data['missing_bodySize'] = abs(sum((self.entries[x]['request']['bodySize'] for x in range(len(self.entries)) if self.entries[x]['request']['bodySize'] == -1)))
        sum_data['total_size'] = sum_data['total_headersSize'] + sum_data['total_bodySize']
        try:
            sum_data['average_headersSize'] = sum_data['total_headersSize'] / (len(self.entries)-sum_data['missing_headersSize'])
        except:
            sum_data['average_headersSize'] = 0
        try:
            sum_data['average_bodySize'] = sum_data['total_bodySize'] / (len(self.entries)-sum_data['missing_bodySize'])
        except:
            sum_data['average_bodySize'] = 0
        try:
            sum_data['average_totalSize'] = sum_data['total_size'] / (len(self.entries) - (sum_data['missing_bodySize'] + sum_data['missing_headersSize']))
        except:
            sum_data['average_totalSize'] = 0
        sum_data['total_responseSize'] = sum((self.entries[x]['response']['_transferSize'] for x in range(len(self.entries)) if self.entries[x]['response']['_transferSize'] != -1))
        sum_data['missing_responseSize'] = abs(sum((self.entries[x]['response']['_transferSize'] for x in range(len(self.entries)) if self.entries[x]['response']['_transferSize'] == -1)))
        try:
            sum_data['average_responseSize'] = sum_data['total_responseSize'] / (len(self.entries)-sum_data['missing_responseSize'])
        except:
            sum_data['average_responseSize'] = 0
        list_cookies_name = []
        for entry in self.entries: ##retrieving all cookie name
            try:
                list_cookies = [cookies for cookies in entry['request']['cookies']]
                if len(list_cookies) >0:
                    list_cookies_name += [cookie['name'] for cookie in list_cookies if 'name' in cookie.keys()]
            except:
                pass
        sum_data['nb_cookies'] = len(set(list_cookies_name))
        sum_data['cookies'] = list(set(list_cookies_name))
        sum_data.update({'2XX':0,'3XX':0,'4XX':0,'5XX':0})
        for entry in self.entries: 
            if entry['response']['status']>=200 and entry['response']['status']<300:
                sum_data['2XX'] +=1
            elif entry['response']['status']>=300 and entry['response']['status']<400:
                sum_data['3XX'] +=1
            elif entry['response']['status']>=400 and entry['response']['status']<500:
                sum_data['4XX'] +=1
            elif entry['response']['status']>=500:
                sum_data['5XX'] +=1
        sum_data.update({"blocked": 0,"dns": 0,"connect": 0,"send": 0,"wait": 0,"receive": 0,"ssl": 0})
        sum_data['blocked'] = sum((entry['timings']['blocked'] for entry in self.entries if entry['timings']['blocked'] != -1))
        sum_data['dns'] = sum((entry['timings']['dns'] for entry in self.entries if entry['timings']['dns'] != -1))
        sum_data['connect'] = sum((entry['timings']['connect'] for entry in self.entries if entry['timings']['connect'] != -1))
        sum_data['send'] = sum((entry['timings']['send'] for entry in self.entries if entry['timings']['send'] != -1))
        sum_data['wait'] = sum((entry['timings']['wait'] for entry in self.entries if entry['timings']['wait'] != -1))
        sum_data['receive'] = sum((entry['timings']['receive'] for entry in self.entries if entry['timings']['receive'] != -1))
        sum_data['ssl'] = sum((entry['timings']['ssl'] for entry in self.entries if entry['timings']['ssl'] != -1))
        sum_data.update({"missing_blocked": 0,"missing_dns": 0,"missing_connect": 0,"missing_send": 0,"missing_wait": 0,"missing_receive": 0,"missing_ssl": 0})
        sum_data['missing_blocked'] = abs(sum((entry['timings']['blocked'] for entry in self.entries if entry['timings']['blocked'] == -1)))
        sum_data['missing_dns'] = abs(sum((entry['timings']['dns'] for entry in self.entries if entry['timings']['dns'] == -1)))
        sum_data['missing_connect'] = abs(sum((entry['timings']['connect'] for entry in self.entries if entry['timings']['connect'] == -1)))
        sum_data['missing_send'] = abs(sum((entry['timings']['send'] for entry in self.entries if entry['timings']['send'] == -1)))
        sum_data['missing_wait'] = abs(sum((entry['timings']['wait'] for entry in self.entries if entry['timings']['wait'] == -1)))
        sum_data['missing_receive'] = abs(sum((entry['timings']['receive'] for entry in self.entries if entry['timings']['receive'] == -1)))
        sum_data['missing_ssl'] = abs(sum((entry['timings']['ssl'] for entry in self.entries if entry['timings']['ssl'] == -1)))
        return sum_data
        
        
    def sizeAnalysis(self):
        """
        This methods returns size (header + body) for each request and the tranfer size of the response.
        return a dataframe.
        """
        request_data = {'url':[],'request_size':[],'response_size':[]}
        for entry in self.entries:
            request_data['url'].append(entry['request']['url'])
            request_data['request_size'].append(entry['request']['headersSize']+entry['request']['bodySize'])
            request_data['response_size'].append(entry['response']['_transferSize'])
        df = _pd.DataFrame(request_data)
        return df
    
    def requestEntriesAnalysis(self):
        """
        Return a dataframe with detail information of your entries for your HAR file. 
        """
        entries = self.entries
        dict_data = defaultdict(list)
        columns = ['bodySize','timestamp','duration','blocked','dns','ssl','connect','send','wait','receive',
                   'blocked_queueing','ressourceType','http_response','transferSize']
        counter = 0 
        for entry in entries:
            entryName = f'{entry["request"]["url"]}_{counter}'
            dict_data[entryName].append(entry['request']['bodySize'])
            timestamp = _datetime.datetime.strptime(entry['startedDateTime'],"%Y-%m-%dT%H:%M:%S.%fZ")
            dict_data[entryName].append(timestamp.timestamp())
            dict_data[entryName].append(entry['time'])
            for el in entry['timings']:
                dict_data[entryName].append(entry['timings'][el])
            dict_data[entryName].append(entry['_resourceType'])
            dict_data[entryName].append(entry['response']['status'])
            dict_data[entryName].append(entry['response']['_transferSize'])
            counter += 1
        df = _pd.DataFrame(dict_data).T
        df.columns = columns
        return df