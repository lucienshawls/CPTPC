import yaml
import sys
import os
import requests
import re
if getattr(sys, 'frozen', False):
    MYDIR=os.path.dirname(os.path.abspath(sys.executable))
    PAUSE_BEFORE_EXIT = True
else:
    MYDIR=os.path.dirname(os.path.abspath(__file__))
    PAUSE_BEFORE_EXIT = False
MYDIR = MYDIR.replace('\\', '/')

def fetch_info():
    url = ''
    provider = 'DEFAULT-PROVIDER'; owner = 'DEFAULT-USER'
    try:
        provider = sys.argv[1]; owner = sys.argv[2]
    except:
        pass
    return {'provider':provider, 'owner':owner}

def convert(provider,owner):
    filename = '%s/%s_%s_ALL.yaml' %(MYDIR,provider,owner)
    with open('%s/match.yaml' %(MYDIR),'r',encoding='utf-8')as f:
        matches = yaml.full_load(f.read())
    with open(filename,'r',encoding='utf-8') as g:
        proxies = yaml.full_load(g.read())['proxies']
    for area in matches['areas']: # area is a dict
        area_name = area['name']
        proxies_in_area = {'proxies':[]}
        if not area['include']:
            continue
        else:
            with_phrases = area['with']
            without_phrases = area['without']
            indispensable_phrases = []
            if with_phrases is None:
                with_phrases = []
            if without_phrases is None:
                without_phrases = []
            if matches['global']['include']:
                if matches['global']['with'] is not None:
                    with_phrases += matches['global']['with']
                if matches['global']['indispensable'] is not None:
                    indispensable_phrases += matches['global']['indispensable']
                if matches['global']['without'] is not None:
                    without_phrases += matches['global']['without']
            for proxy in proxies:
                accept_positive = False
                for with_phrase in with_phrases: # accept if it matches any
                    if with_phrase is None:
                        continue
                    if re.search(str(with_phrase), str(proxy['name'])):
                        accept_positive = True
                        break
                for indispensable_phrase in indispensable_phrases:
                    if indispensable_phrase is None:
                        continue
                    if not re.search(str(indispensable_phrase), str(proxy['name'])):
                        accept_positive = False
                        break
                accept_negative = True
                for without_phrase in without_phrases: # do not accept if it matches these
                    if without_phrase is None:
                        continue
                    if re.search(str(without_phrase), str(proxy['name'])):
                        accept_negative = False
                        break
                if accept_positive and accept_negative:
                    proxies_in_area['proxies'].append(proxy)
        if not os.path.exists('%s/conversion' %(MYDIR)):
            os.mkdir('%s/conversion' %(MYDIR))
        with open('%s/conversion/%s_%s_%s.yaml' %(MYDIR,provider,owner,area_name), 'w', encoding='utf-8') as f:
            yaml.dump(data=proxies_in_area, stream=f, allow_unicode=True, sort_keys=False)
    
def main():
    info = fetch_info()
    convert(provider=info['provider'],owner=info['owner'])

if __name__ == '__main__':
    main()
