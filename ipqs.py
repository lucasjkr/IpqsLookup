#!/usr/bin/python3
import json
from requests_cache import CachedSession
from dotenv import dotenv_values
from datetime import timedelta
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

    def lookup(self):
        query = self.session.get(f"https://ipqualityscore.com/api/json/ip/{self.config['IPQS_API_KEY']}/{self.ip}")
        result = query.json()

        if result['success'] == False:
            return False

        return {
            'ip': self.ip,
            'host': result['host'],
            'message': result['message'],
            'ISP': result['ISP'],
            'organization': result['organization'],
            'country_code': result['country_code'],
            'city': result['city'],
            'region': result['region'],
            '#': '-',
            'is_crawler': result['is_crawler'],
            'is_mobile': result['mobile'],
            'is_proxy': result['proxy'],
            'is_tor': result['tor'],
            'is_bot': result['bot_status'],
            'recent_abuse': result['recent_abuse'],
            'fraud_score': result['fraud_score'],
            '##': '-',
            'cached': query.from_cache
        }

    def report(self):
        return self.session.get(f"https://www.ipqualityscore.com/api/json/report/{self.config['IPQS_API_LEY']}?ip={self.ip}").json()

if __name__ == "__main__":
    import argparse
    ipqs = IPQualityScore()

    arg = argparse.ArgumentParser()
    arg.add_argument('action', help='IP Address to lookup')
    arg.add_argument('ip_address', help='IP Address to lookup')
    a = arg.parse_args()

    ipqs.ip = a.ip_address
    action = a.action

    if action == "lookup":
        result = ipqs.lookup()
    elif action == "report":
        result = ipqs.report()

    if result:
        print(json.dumps(result, indent=4))
    else:
        print("No result found")
