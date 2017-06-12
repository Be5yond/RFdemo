#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import Req
import tools


class OpenPhp(Req.Req):
    """
    Common Custom Library For OpenPhp Interface.
    Customized For Le_cloud project Standard VOD.
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, url, user_unique=None, secret_key=None):
        self.url = url
        self._unq = user_unique
        self._key = secret_key
        super(OpenPhp, self).__init__()

    def set_user(self, user_unique, secret_key):
        """set user.

        Params:
        | user_id | user_id |
        | secret_key | secret_key |
        :return:

        Examples:
        | SET USER | 400098 | 737c89058598258d39fe711387a7b32d |

        """
        self._unq = user_unique
        self._key = secret_key

    def get(self, **kwargs):
        """
        send get request

        Params:
        | params | query args dict |

        Return: response object
        """
        params = self._add_public_para(**kwargs)
        self.response = self.send('GET', self.url, params=params)

    def post(self, **kwargs):
        """
        send post request

        Params:
        | params | body args dict |

        Return: response object
        """
        params = self._add_public_para(**kwargs)
        self.response = self.send('POST', self.url, data=params)

    @staticmethod
    def gen_unix_time(hour=0, minute=0, second=0):
        """
        Return time in milliseconds since the Epoch base on offset, default is the current time.

        Params:
        | hour | offset hours, default 0 |
        | minute | offset minutes, default 0 |
        | second | offset seconds, default 0 |

        Return: Epoch time

        Examples:
        | GEN_UNIX_TIME |  | # return: 1484710834567 |
        | GEN_UNIX_TIME | 12 30  | # return: 1484755834567 |
        | GEN_UNIX_TIME | -2 | # return: 1484703634567 |
        """
        offset = int(hour) * 60 * 60 + int(minute) * 60 + int(second)
        return int(1000 * (time.time() + offset))

    def check_err_msg(self, code, msg):
        """
        Params:
        | code | expected errCode |
        | msg | expected errMsg |

        Examples:
        | check_err_msg | E26001 | 不存在 |
        """
        try:
            err_code = self.response.json().get('errCode')
            err_msg = self.response.json().get('errMsg')
        except ValueError as e:
            print e
        else:
            assert code == err_code, 'The expected code is {}, actually {}'.format(code, err_code)
            assert msg in err_msg, 'The expected msg -{}- is not in -{}-'.format(code, err_msg)

    def _add_public_para(self, **params):
        params['timestamp'] = str(int(1000 * time.time()))
        params['sign'] = self._gen_sign(**params)
        return params

    def _gen_sign(self, **params):
        data_list = [str(k) + str(params[k]) for k in sorted(params.keys())]
        data_list.append(self._key)
        return tools.gen_sign(*data_list)


if __name__ == '__main__':
    #print tools.gen_sign('123')
    op = OpenPhp('http://httpbin.org/get')
    op.set_user('baidddizpn', 'e66aa647de9f18b90d8bb78d0110be6b')
    data = {'api': 'video.list'}
    op.get(**data)

    # print op.gen_unix_time(1)





