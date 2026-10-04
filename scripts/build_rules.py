#!/usr/bin/env python3
"""Build only the direct-routing dataset; never copy upstream templates."""
import datetime
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import time
import urllib.request

SOURCES = {
    'china_domains': 'https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/direct-list.txt',
    'private_domains': 'https://raw.githubusercontent.com/Loyalsoldier/domain-list-custom/release/private.txt',
    'china_ip': 'https://raw.githubusercontent.com/Loyalsoldier/geoip/release/text/cn.txt',
}
LOCAL_NETWORKS = [
    '0.0.0.0/8', '10.0.0.0/8', '100.64.0.0/10', '127.0.0.0/8',
    '169.254.0.0/16', '172.16.0.0/12', '192.168.0.0/16',
    '224.0.0.0/4', '::/128', '::1/128', 'fc00::/7', 'fe80::/10', 'ff00::/8',
]
DOMAIN = re.compile(r'^[-_a-zA-Z0-9]+(?:\.[-_a-zA-Z0-9]+)*$')


def fetch(url):
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'vpsct-direct-rules-builder'})
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read(16 * 1024 * 1024)
                assert response.status == 200 and data
                return data.decode('utf-8')
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def domains(text):
    exact, suffix = set(), set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(('#', '//')):
            continue
        if line.startswith(('regexp:', 'keyword:')):
            continue
        target = exact if line.startswith('full:') else suffix
        if line.startswith(('full:', 'domain:')):
            line = line.split(':', 1)[1]
        if line.startswith('.'):
            line = line[1:]
            target = suffix
        assert DOMAIN.fullmatch(line), 'invalid_domain_source_line'
        target.add(line.lower())
    return exact, suffix


def main():
    raw = {name: fetch(url) for name, url in SOURCES.items()}
    exact, suffix = domains(raw['china_domains'])
    assert len(exact) + len(suffix) > 1000, 'china_domain_dataset_empty_or_truncated'
    private_exact, private_suffix = domains(raw['private_domains'])
    assert private_exact or private_suffix, 'private_domain_dataset_empty'
    exact.update(private_exact)
    suffix.update(private_suffix | {'local', 'lan', 'home.arpa'})
    exact.add('localhost')
    networks = set(LOCAL_NETWORKS)
    china_network_count = 0
    for line in raw['china_ip'].splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        network = ipaddress.ip_network(line, strict=False)
        assert network.prefixlen != 0, 'universal_direct_route_forbidden'
        networks.add(str(network))
        china_network_count += 1
    assert china_network_count > 1000, 'china_ip_dataset_empty_or_truncated'
    ordered_networks = sorted(networks, key=lambda n: (ipaddress.ip_network(n).version,
                                                      int(ipaddress.ip_network(n).network_address),
                                                      ipaddress.ip_network(n).prefixlen))
    output = Path('generated')
    output.mkdir(exist_ok=True)
    rules = ['# Domestic and local DIRECT dataset. Other traffic uses the client proxy.']
    rules += ['DOMAIN,' + name for name in sorted(exact)]
    rules += ['DOMAIN-SUFFIX,' + name for name in sorted(suffix)]
    rules += [('IP-CIDR6' if ':' in network else 'IP-CIDR') + ',' + network + ',no-resolve'
              for network in ordered_networks]
    (output / 'direct.list').write_text('\n'.join(rules) + '\n')
    source = {'version': 3, 'rules': [{'domain': sorted(exact)},
                                     {'domain_suffix': sorted(suffix)},
                                     {'ip_cidr': ordered_networks}]}
    (output / 'direct.json').write_text(json.dumps(source, separators=(',', ':')) + '\n')
    manifest = {
        'generated_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'domestic_and_local_direct_only', 'sources': SOURCES,
        'source_sha256': {name: hashlib.sha256(text.encode()).hexdigest() for name, text in raw.items()},
        'counts': {'exact_domains': len(exact), 'suffix_domains': len(suffix), 'ip_prefixes': len(networks)},
        'files': {name: hashlib.sha256((output / name).read_bytes()).hexdigest()
                  for name in ['direct.list', 'direct.json']},
        'application_or_country_groups_generated': False,
        'client_templates_generated': False,
    }
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    assert set(p.name for p in output.iterdir()) == {'direct.list', 'direct.json', 'manifest.json'}
    print(json.dumps(manifest['counts']))


if __name__ == '__main__':
    main()
