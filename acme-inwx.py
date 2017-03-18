#!/usr/bin/env python

import pprint
import re
import sys

from inwx import domrobot, prettyprint, getOTP
from inwxcredentials import *

def main(inwxcredentials, args):
    pp = pprint.PrettyPrinter(indent=4)
    targetdomain = args[1]
    challenge = args[2] if len(args)>2 else None

    # Remove TXT name
    if targetdomain.startswith('_acme-challenge.'):
        targetdomain = targetdomain[16:]

    print("Input:")
    pp.pprint([ targetdomain, challenge ])

    # Create api connection and login
    inwx_conn = domrobot(inwxcredentials["url"], False)
    loginRet = inwx_conn.account.login({'lang': 'en', 'user': inwxcredentials["username"], 'pass': inwxcredentials["password"] })

    # Perform OTP login if necessary
    if 'tfa' in loginRet['resData'] and loginRet['resData']['tfa'] == 'GOOGLE-AUTH':
        inwx_conn.account.unlock({'tan': getOTP(inwxcredentials["otpsecret"])})

    print("Searching nameserver zone for "+targetdomain)

    # Extract second level domain from given domain
    sldmatch = re.search(ur"(^|\.)([^\.]+\.[^\.]+)$", targetdomain)

    if sldmatch is None:
        print("Could not extract second level domain");
        return False

    # Build domain filter for api request
    apisearchpattern = "*"+sldmatch.group(2)
    print("API search pattern: "+apisearchpattern)

    # Fetch all domains from api
    domains = inwx_conn.nameserver.list({ 'domain': apisearchpattern })

    # Search domain in nameserver
    matchdomain = None
    matchsublevel = None

    for domain in domains['resData']['domains']:
        sld = domain['domain']
        try:
            rgx = re.compile(ur"^(?P<sublevel>.+?)?(^|\.)"+re.escape(sld)+ur"$", re.UNICODE)
            rgxmatch = rgx.search(targetdomain)
            if rgxmatch:
                matchdomain = sld
                matchsublevel = rgxmatch.group('sublevel')
                break
        except UnicodeEncodeError:
            print("TODO: Support unicode domains")

    # Check match
    if matchdomain is None:
        print("Nameserver not found")
        return False

    print("Nameserver match: "+matchdomain)

    # Prepare
    rname = "_acme-challenge"
    rtype = "TXT"
    rvalue = challenge

    # Append sublevel part if exist
    if matchsublevel is not None:
        rname = rname+"."+matchsublevel

    # Debug info
    print("Debug:")
    pp.pprint([ rname, rtype, rvalue ])

    # Check TXT record exist
    existscheck = inwx_conn.nameserver.info({ 'domain': matchdomain, 'type': rtype, 'name': rname })

    # Delete if exist
    try:
        record = existscheck["resData"]['record'][0]
        print("TXT record exists -> delete")
        pp.pprint(record)
        result = inwx_conn.nameserver.deleteRecord({ 'id': record['id'] })
        pp.pprint(result)
    except KeyError:
        pass

    # Create if challenge given
    if rvalue is not None:
        print("Create new TXT record")
        result = inwx_conn.nameserver.createRecord({ 
            'domain': matchdomain, 
            'type': rtype, 
            'name': rname,
            'content': rvalue,
            'ttl': 300
        })

        pp.pprint(result)

    return True


# Main
if __name__ == '__main__':
    if main(inwxcredentials, sys.argv) == True:
        sys.exit(0)
    else:
        sys.exit(1)

# EOF

