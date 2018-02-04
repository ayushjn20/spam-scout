from ipaddress import ip_address
from urllib.parse import urlparse
import requests

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
    except:
        final_dict['having_IP_Address'] = 0

    # URL_length
    if len(url_string < 54): final_dict['URL_length'] = 1
    if len(url_string >= 54 and url_string <= 75): final_dict['URL_length'] = 0
    if len(url_string > 75): final_dict['URL_length'] = -1
     #shortining service

    if (len(domain) < 6):
        final_dict['Shortining_Service'] = 1
    else: final_dict['Shortining_Service'] = 0

    if('@' in url_string):
        final_dict["having_At_Symbol"] = 1
    else: final_dict["having_At_Symbol"] = -1

    if (url_string.rfind('//') > 7):
        final_dict['double_slash_redirecting'] = 1
    else: final_dict['double_slash_redirecting'] = -1

    if('-' in domain): final_dict['Prefix-Suffix'] = 1
    else: final_dict['Prefix-Suffix'] = -1

    if (domain.count('.') <= 1): final_dict['having_Sub_domain'] = -1
    elif (domain.count('.') == 2): final_dict['having_Sub_domain'] = 0
    else: final_dict['having_Sub_domain'] = 1

    if(url.scheme=='http'):
        final_dict['SSLfinal_State'] = 1
    else:
        try:
            fetch = requests.get(url_string)
            if (fetch.status_code == 200): final_dict['SSLfinal_State'] = -1
        except:
            final_dict['SSLfinal_State'] = 0

    if(port):
        if(port in STD_PORTS):
            final_dict['port']
    else: pass