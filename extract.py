from ipaddress import ip_address
from datetime import datetime
import requests, ast
from keys import whois_api_key

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

STD_PORTS = [21,22,23,80,443,445,1433,1521,3306,3389]

def extract_features_from_url(url_string):
    url = urlparse(url_string)
    domain = url.netloc.split(':')[0]
    try:
        port = int(url.netloc.split(':')[1])
    except: pass
    
    final_dict = {}
    
    # having_ip_address
    try:
        ip_add = ip_address(domain)
        if (type(ip_add) == 'ipaddress.IPv4Address' or type(ip_add) == 'ipaddress.IPv6Address'):
            final_dict['having_IP_Address'] = 1
    except ValueError:
        final_dict['having_IP_Address'] = -1
    except Exception as e:
        final_dict['having_IP_Address'] = 0

    # URL_length
    if len(url_string < 54): final_dict['URL_length'] = 1
    elif len(54 <= url_string <= 75): final_dict['URL_length'] = 0
    elif len(url_string > 75): final_dict['URL_length'] = -1

    #Shortining Service
    if (len(domain) < 6):
        final_dict['Shortining_Service'] = 1
    else: final_dict['Shortining_Service'] = 0

    if('@' in url_string):
        final_dict["having_At_Symbol"] = 1
    else: final_dict["having_At_Symbol"] = -1

    if (url_string.rfind('//') > 7):
        final_dict['double_slash_redirecting'] = 1
    else: final_dict['double_slash_redirecting'] = -1

    if('-' in domain): final_dict['Prefix_Suffix'] = 1
    else: final_dict['Prefix_Suffix'] = -1

    if (domain.count('.') <= 1): final_dict['having_Sub_domain'] = -1
    elif (domain.count('.') == 2): final_dict['having_Sub_domain'] = 0
    else: final_dict['having_Sub_domain'] = 1

    # if(url.scheme=='http'):
    #     final_dict['SSLfinal_State'] = 1
    # else:
    #     try:
    #         fetch = requests.get(url_string)
    #         if (fetch.status_code == 200): final_dict['SSLfinal_State'] = -1
    #     except:
    #         final_dict['SSLfinal_State'] = 0

    final_dict['port'] = 1
    if(port):
        if(port not in STD_PORTS):
            final_dict['port'] = -1

    if (url.scheme == 'http'):
        final_dict['HTTPS_token'] = 1
    else:
        try:
            fetch = requests.get(url_string)
            if (fetch.status_code == 200): final_dict['HTTPS_token'] = -1
        except:
            final_dict['HTTPS_token'] = 0

    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen

    apiKey = whois_api_key

    x = 0
    for url in chase_redirects(url.scheme + '://' + url.netloc):
        print(url)
        x += 1
    if (x <= 1):
        final_dict['Redirect'] = -1
    elif (x >= 2 and x < 4):
        final_dict['Redirect'] = 0
    else:
        final_dict['Redirect'] = 1


    url = 'https://www.whoisxmlapi.com/whoisserver/WhoisService?' \
          + 'domainName=' + domain + '&apiKey=' + apiKey + "&outputFormat=JSON"
    try:
        whois_res = ast.literal_eval(urlopen(url).read().decode('utf8')) # a dict

        hostnames = [hn.lower() for hn in whois_res['WhoisRecord']['registryData']['nameServers']['hostNames']]
        final_dict['Abnormal_URL'] = 1
        for hn in hostnames:
            if(hn.contains(domain)):
                final_dict['Abnormal_URL'] = -1
                break

        start_date = whois_res['WhoisRecord']['registryData']['createdDate']
        end_date = whois_res['WhoisRecord']['registryData']['expiresDate']

        def __datetime(date_str):
            return datetime.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y')

        start = __datetime(start_date)
        end = __datetime(end_date)
        delta_months = int((end - start).total_seconds() * 3.80517e-7)

        if delta_months < 6:
            final_dict['age_of_domain'] = 1
        else:
            final_dict['age_of_domain'] = -1

    except Exception as e:
        final_dict['Abnormal_URL'] = 0
        final_dict['age_of_domain'] = 0



def chase_redirects(url):
    while True:
        yield url
        r = requests.head(url)
        if 300 < r.status_code < 400:
            url = r.headers['location']
        else:
            break


def extract_from_links(data, url_string):
    url = urlparse(url_string)
    domain = url.netloc.split(':')[0]

    dicct = {}

    for key, list in data:
        dicct[key] = list.count(domain)

    return dicct