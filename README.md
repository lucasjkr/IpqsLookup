# ipqs.py

A command-line tool to query IP info from IpQualityScore.com. Utilizes caching (1 week expiration) in order not to use up 
free IPQS queries to keep us under the threshold.

## Installation
* clone repository
* install requirements
* `pip install -r requirements.txt`
* copy .env.example to .env (`cp .env.example .env`)
* edit .env and add your valid IPQS_API_KEY 

## Usage
Lookup an ip:

`python3 ipqs.py lookup 1.1.1.1`

Report a malicious ip:

`python3 ipqs.py report 1.1.1.1`