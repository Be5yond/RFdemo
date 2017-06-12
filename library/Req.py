#!/usr/bin/env python

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random
import string
from robot.api import logger
from robot.api.deco import keyword


class Req(object):
    def __init__(self):
        self.session = requests.Session()
        self.response = None
        pass

    def send(self, method, url, variable=None, params=None, data=None, headers=None, files=None):
        """
        send request.

        Params:
        | method | request method | # POST |
        | url | target url |
        | variable | kwargs in url |
        | params | kwargs for get method |
        | data | kwargs in request body |
        | headers | custom header |
        | files | # TBD |
        :return: response

        Examples:
        | send | GET | http://httpbin.org/get | params={'GID':5555} | # target URI would be 'http://httpbin.org/get?GID=5555' |
        | send | GET | http://httpbin.org/UID | variable={'UID':17951} | params={'GID':5555} | # target URI would be 'http://httpbin.org/17951?GID=5555' |
        | send | POST | http://httpbin.org/post | data={'UID':17951} | # target URI would be 'http://httpbin.org/post' body {'UID':17951} |
        """
        if variable:
            for key, value in variable.items():
                url = url.replace(key, str(value))
        req = requests.Request(method, url, params=params, data=data, headers=headers, files=files)
        prepped = self.session.prepare_request(req)

        logger.info('= <request url> = \n'+str(url))
        logger.info('= <request params> = \n'+str(params))
        logger.info('= <request data> = \n'+str(data))
        self.response = self.session.send(prepped)
        logger.info('= <response code> = \n'+str(self.response.status_code))
        logger.info('= <response content> = \n'+str(self.response.content))
        return self.response

    def _parse_json(self, path, json_object=None):
        """
        :param path: e.g. arg.0.a
        :param json_object: json_object to parse default self.response.json()
        :return: target value of given path
        :example: parse_json('arg.0.a') ==> self.response.json()['arg'][0]['a']
                 parse_json('a.b',{'a':{'b':6}},'c':4) ==> 6

        Examples:
        | parse_json | arg.0.a |
        | parse_json | a.b.0 | # {'a':{'b':[6,5,3]}},'c':4} |
        """
        json_data = json_object or self.response.json()
        arr = [int(i) if i.isdigit() else i for i in path.split('.')]
        # arr = [i.isdigit() and int(i) or i for i in path.split('.')]
        try:
            for i in arr:
                json_data = json_data[i]
        except (IndexError, KeyError):
            logger.error(self.response.json())
            logger.error('Err: wrong path: '+path)
        return json_data

    def check_status_code(self, code):
        """
        check response http code

        Params:
        | code | expected http code |

        Examples:
        | check_status_code | 400 |
        """
        assert int(code) == self.response.status_code, \
            'The expected code is {}, actually {}'.format(code, self.response.status_code)

    @keyword('Check Response By Path "${path}" Equals to "${value}"')
    def check_response_value(self, path, value):
        """
        check response json value for a given path.

        Params:
        | value | expected value |
        | path | target path in response json |

        Examples:
        | Check Response By Path "headers.Host" Equals to "httpbin" | # {"args": {},"headers": {"Host": "httpbin","Upgrade-Insecure-Requests": "1",},} |
        | Check Response By Path "a.b.1" Equals to "5" | # {'a':{'b':[6,5,3]}},'c':4} |
        """
        target_value = self._parse_json(path)
        assert value == str(target_value), \
            'The expected value is {}, actually {}'.format(value, target_value)

    @keyword('Check Response By Path "${path}" Not None')
    def check_response_val(self, path):
        """
        check response json value not None for a given path

        Params:
        | path | target path in response json |

        Examples:
        | Check Response By Path "a.b.1" Not None | # {'a':{'b':[6,5,3]}},'c':4} |
        """
        target_value = self._parse_json(path)
        assert target_value

    @keyword('Check Response By Path "${path}" Keys Equals to "${value}"')
    def check_response_keys(self, path, keys):
        """
        check response json value keys for a given path

        Params:
        | path | target path in response json |

        Examples:
        | Check Response By Path "a" Keys Equals to ['b', 'c', 'd'] | # {'a':{'b':[6,5,3]}, 'c':'st', 'd':'tu'}} |
        """
        target_dict = self._parse_json(path)
        assert set(keys) == set(target_dict.keys()), \
            'The expected value is {}, \n' \
            '             actually {}'.format(sorted(keys), sorted(target_dict.keys()))

    @staticmethod
    def gen_random_string(length, pool=string.lowercase+string.digits):
        """
        generate a random string by given length

        Params:
        | length | length |
        | pool | letters to chose from, default is a-z and 0-9 |

        Return: a string

        Examples:
        | gen_random_string | 10 | # rkd8hwrqf2 |
        | gen_random_string | 4 | 'ABCDEFG' | # GEFD |
        """
        return ''.join([random.choice(pool) for _ in range(int(length))])

    def check_fields(self, dict1, dict2):
        assert set(dict1.keys()) == set(dict2.keys())
        for k, v in dict2.items():
            if isinstance(v, dict):
                assert isinstance(dict1[k], dict)
                self.check_fields(dict1[k], v)
            if isinstance(v, list):
                if isinstance(dict1[k][0], dict):
                    self.check_fields(dict1[k][0], v[0])
        

