import argparse
import json
from dotenv import dotenv_values
from requests_cache import CachedSession
from datetime import timedelta
from argparse import ArgumentParser
import logging

class IPQualityScore:
    ip = str

    def __init__(self):
        self.session = CachedSession('requests', backend='sqlite', allowable_methods=("GET"))
        self.session.settings.expire_after = timedelta(weeks=1)
        self.session.settings.stale_if_error = True

        self.logging = logging
        self.logging.basicConfig(level='INFO')

        self.config = dotenv_values()

    def viewcache(self):
        print(self.session.cache.urls())

    def query(self):
        return self.session.get(f"https://ipqualityscore.com/api/json/ip/{self.config['IPQS_API_KEY']}/{self.ip}").json()

    def is_crawler(self):
        return self.ipqs['is_crawler']

    def is_vpn(self):
        return self.ipqs['vpn']

    def is_tor(self):
        return self.ipqs['tor']

    def is_proxy(self):
        return self.ipqs['proxy']

    def active_tor(self):
        return self.ipqs['active_tor']

    def active_vpn(self):
        return self.ipqs['active_vpn']

    def isp(self):
        return self.ipqs['ISP']

    def organization(self):
        return self.ipqs['organization']

    def all(self):
        query = self.query()
        result = {
            'ip': self.ip,
            'host': query['host'],
            'message': query['message'],
            'ISP': query['ISP'],
            'organization': query['organization'],
            'country_code': query['country_code'],
            'city': query['city'],
            'region': query['region'],
            '-': '-',
            'is_crawler': query['is_crawler'],
            'is_mobile': query['mobile'],
            'is_proxy': query['proxy'],
            'is_tor': query['tor'],
            'is_bot': query['bot_status'],
            'recent_abuse': query['recent_abuse'],
            'fraud_score': query['fraud_score'],
        }
        print(json.dumps(result, indent=4))

if __name__ == "__main__":
    ipqs = IPQualityScore()

    arg = argparse.ArgumentParser()
    arg.add_argument('ip_address', help='IP Address to lookup')
    a = arg.parse_args()

    ipqs.ip = a.ip_address
    ipqs.all()
