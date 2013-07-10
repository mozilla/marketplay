import json
import re


rules = [
    ('http_endpoint',
     r'\.\. http:(?P<method_name>GET|POST|DELETE|PUT):: (?P<url>.+)'),
    ('http_request_scope', r'\*\*Request\*\*'),
    ('http_response_scope', r'\*\*Response\*\*'),
    ('http_endpoint_note', r'\.\. note:: (?P<note_text>.+)'),
    ('param', r':param (?P<optional>(optional|required) )?' + (
        r'(?P<param_name>.+?): (?P<param_desc>.+)')),
    ('param_type', r':type (?P<param_name>.+?): (?P<param_type_value>.+)'),
    ('response_status', r':status code:( (?P<code>\d+))?'),
]

no_match_line = r'.+?(\n|$)'

def strip_junk(match):
    return ''

class Parser(object):
    def __init__(self, string):
        self.endpoints = []
        self.string = string
        self.scope = None
        self.current_endpoint = None

    def _new_http_endpoint(self, match):
        url = match.group('url')
        self.endpoints.append({'url': url,
                               'method': match.group('method_name')})
        self.current_endpoint = self.endpoints[len(self.endpoints) - 1]

        args_regex = r'\/\((.+?)\)\/'
        matches = re.findall(args_regex, url)
        url_args = []
        for args in matches:
            # for multiple args
            split_matches = args.split('|')
            arg_regex = r'(?P<arg_type>.+?):(?P<arg_name>.+)'
            arg_names = []
            arg_types = []

            for spm in split_matches:
                secondary_match = re.match(arg_regex, spm.strip('()'))
                arg_names.append(secondary_match.group('arg_name'))
                arg_types.append(secondary_match.group('arg_type'))

            args_name = '|'.join(arg_names)
            url_args.append({'name': args_name,
                             'type': '|'.join(arg_types)})

        self.current_endpoint['url_args'] = url_args

    def _new_param(self, match):
        # scope = request | respone
        scope = self.scope
        param_name = match.group('param_name').strip()
        param_desc = match.group('param_desc')
        if not scope:
            raise Exception('Param out of scope.')

        optional = True if match.group('optional') == 'optional' else False

        self.current_endpoint[scope]['params'].append({'name': param_name,
            'desc': param_desc, 'optional': optional})

    def _new_param_type(self, match):
        scope = self.scope
        params = self.current_endpoint[scope]['params']
        param_name = match.group('param_name').strip()

        found = None
        for param in params:
            if param['name'] == param_name:
                param['type'] = match.group('param_type_value')
                found = True

        if not (scope and (found)):
            raise Exception('invalid param name mentioned.')

    def _new_http_request_scope(self, match):
        self.scope = 'request'
        self.current_endpoint['request'] = {'params': []}

    def _new_response_status(self, match):
        self.current_endpoint['response']['status'] = {
            'code': match.group('code')}

    def _new_http_response_scope(self, match):
        self.scope = 'response'
        self.current_endpoint['response'] = {'params': []}

    def _new_http_endpoint_note(self, match):
        if not self.endpoints:
            return

        self.current_endpoint['notes'] = match.group('note_text')

    def get_json(self):
        return json.dumps(self.endpoints)

    def get_array(self):
        return self.endpoints

    def parse(self):
        string = self.string.lstrip()
        while string:
            match = None
            for name, regex in rules:
                match = re.match(regex, string, re.IGNORECASE)
                if match:
                    getattr(self, '_new_%s' % name)(match)
                    string = string[match.end():].strip()
                    break

            # Strip the current line if we could not match.
            if not match:
                string = re.sub(no_match_line, strip_junk, string,
                                count=1).lstrip()

        return True
