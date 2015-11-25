"""
    Author: Jonas Straub
    Desc: Ambari Audit Log - Config
"""

import requests
import json
import getpass
import logging
import sys
import getopt


class AmbariAudit:
    def __init__(self, host, cluster_name, user, pw, use_https, config):
        self.host = host
        self.cluster_name = cluster_name
        self.cluster_url = ''
        self.api_url = ''
        self.user = user
        self.pw = pw
        self.session = None
        self.use_https = use_https
        self.config_id = config
        self.config_versions = []
        self.sort_version_by = 'version'
        self.configs = []
        self.audit_log = []

        # create cluster url
        if use_https:
            self.cluster_url = '/'.join(['https:/', host + '', 'api', 'v1', 'clusters', cluster_name])
            self.api_url = '/'.join(['https:/', host + '', 'api', 'v1'])
        else:
            self.cluster_url = '/'.join(['http:/', host + '', 'api', 'v1', 'clusters', cluster_name])
            self.api_url = '/'.join(['http:/', host + '', 'api', 'v1'])

        # create ambari session
        logging.debug('Trying to setup new Ambari session with ' + self.cluster_url)
        self.session = requests.Session()
        self.session.auth = (user, pw)
        self.session.headers.update({'X-Requested-By': 'pythonambariauditer'})


    def _retrieve_config_versions(self):
        '''
            Retrieve available config versions of supplied config item.
        '''
        r = self.session.get(self.cluster_url + '/configurations', verify=False, params={'type': self.config_id})
        res = r.json()

        # sort result
        if 'items' in res and len(res['items']):
            self.config_versions = sorted(res['items'], key=lambda item: item[self.sort_version_by])

    def _retrieve_configs(self):
        '''
            Retrieve config for each config version
        '''
        for cversion in self.config_versions:
            r = self.session.get(cversion['href'], verify=False)
            if r.status_code != 200:
                continue

            res = r.json()
            self.configs.append(res['items'][0])

    def _config_diff(self):
        '''
            Compare different configurations and
            calculate differences
        '''
        audit = []
        prev_config = {}
        # traverse configs
        for conf in self.configs:
            version = conf['version']
            config_id = self.config_id

            # traverse properties
            for key,val in conf['properties'].iteritems():
                if key not in prev_config:
                    audit.append({'version': version, 'type': config_id, 'action': 'ADDED', 'key': key, 'value': val})
                elif prev_config[key] != val:
                    audit.append({'version': version, 'type': config_id, 'action': 'CHANGED', 'key': key, 'value': val, 'old_value': prev_config[key]})

            # check for removals
            for pkey,pval in prev_config.iteritems():
                if pkey not in conf['properties']:
                    audit.append({'version': version, 'type': config_id, 'action': 'REMOVED', 'key': pkey, 'value': pval})

            # store previous
            prev_config = conf['properties']

        self.audit_log = audit

    def _finalize(self, fnout):
        '''
            Print or write final result in log format
        '''
        if fnout:
            with open(fnout, 'w') as fout:
                for line in self.audit_log:
                    fout.write(self._get_audit_log_string(line) + '\n')
        else:
            for line in self.audit_log:
                print(self._get_audit_log_string(line))

    def _get_audit_log_string(self, text):
        if not text:
            return ''

        if text['action'] != 'CHANGED':
            return '{type}: version {version} - {action} - {key} - {value}'.format(type=text['type'], action=text['action'], version=text['version'], key=text['key'], value=text['value'])
        else:
            return '{type}: version {version} - {action} - {key} - {old_value} => {value}'.format(type=text['type'], action=text['action'], version=text['version'], key=text['key'], value=text['value'], old_value=text['old_value'])

    def execute(self, fnout):
        '''
            Executes the necessary steps to calculate an audit log for
            the given config type/id.
        '''
        # retrieve config version 
        self._retrieve_config_versions()
        # retrieve configs
        self._retrieve_configs()
        # calculate diff audit
        self._config_diff()
        # self display/write result
        self._finalize(fnout)


def main(argv):
    '''
    Process script arguments if script was called directly
    '''
    target=cluster=user=fnout=config= ''
    use_https = False
    help_text = '... --target <host+port> --cluster <clustername> --user <ambari_username> --output <filename> --https [True|False] --config <config-name>'
    # try parsing arguments
    try:
        opts, args = getopt.getopt(argv, 'ht:c:u:o:s:cfg:',['help', 'target=', 'cluster=', 'user=', 'output=', 'https=', 'config='])

        # get all arguments
        for opt, arg in opts:
            if opt in('-h', '--help'):
                print(help_text)
                sys.exit(0)
            elif opt in ('-t', '--target'):
                target = arg
            elif opt in ('-c', '--cluster'):
                cluster = arg
            elif opt in ('-u', '--user'):
                user = arg
            elif opt in ('-o', '--output'):
                fnout = arg
            elif opt in ('-cfg', '--config'):
                config = arg
            elif opt in ('-s', '--https'):
                use_https = True if arg == 'True' else False

        # make sure required args were supplied
        if not target or not user or not cluster or not config:
            raise getopt.GetoptError(
                'Not all required arguments supplied. Required: cluster, target, username and config')

    except getopt.GetoptError as e:
        logging.error(help_text)
        logging.error(e)
        sys.exit(2)

    return target,cluster,user,fnout,use_https,config


if __name__ == "__main__":
    # config logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    requests.packages.urllib3.disable_warnings()

    # get script arguments
    target,cluster,user,fnout,use_https,config = main(sys.argv[1:])

    # get password
    passwd = getpass.getpass()

    # print info
    logging.info('Exporter initialized!')
    logging.info('Ambari Host: ' + target)
    logging.info('Cluster: ' + cluster)
    logging.info('User: ' + user)
    logging.info('File: ' + fnout)
    logging.info('Password: ******')
    logging.info('Config: ' + config)
    logging.info('HTTPS: ' + str(use_https))

    # start new Audit
    audit = AmbariAudit(target, cluster, user, passwd, use_https, config)
    audit.execute(fnout)

    # done
    logging.debug('Audit Done =)')


