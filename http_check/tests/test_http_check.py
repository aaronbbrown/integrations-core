# -*- coding: utf-8 -*-

# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# 3p
import mock
from nose.plugins.attrib import attr

# project
from config import AGENT_VERSION
from tests.checks.common import AgentCheckTest
from util import headers as agent_headers

RESULTS_TIMEOUT = 20

AGENT_CONFIG = {
    'version': AGENT_VERSION,
    'api_key': 'toto'
}

CONFIG = {
    'instances': [{
        'name': 'conn_error',
        'url': 'https://thereisnosuchlink.com',
        'check_certificate_expiration': False,
        'timeout': 1,
    }, {
        'name': 'http_error_status_code',
        'url': 'http://httpbin.org/404',
        'check_certificate_expiration': False,
        'timeout': 1,
    }, {
        'name': 'status_code_match',
        'url': 'http://httpbin.org/404',
        'http_response_status_code': '4..',
        'check_certificate_expiration': False,
        'timeout': 1,
        'tags': ["foo:bar"]
    }, {
        'name': 'cnt_mismatch',
        'url': 'https://github.com',
        'timeout': 1,
        'check_certificate_expiration': False,
        'content_match': 'thereisnosuchword'
    }, {
        'name': 'cnt_match',
        'url': 'https://github.com',
        'timeout': 1,
        'check_certificate_expiration': False,
        'content_match': '(thereisnosuchword|github)'
    }, {
        'name': 'cnt_match_unicode',
        'url': 'https://ja.wikipedia.org/',
        'timeout': 1,
        'check_certificate_expiration': False,
        'content_match': u'メインページ'
    }, {
        'name': 'cnt_mismatch_unicode',
        'url': 'https://ja.wikipedia.org/',
        'timeout': 1,
        'check_certificate_expiration': False,
        'content_match': u'メインペーー'
    }, {
        'name': 'cnt_mismatch_reverse',
        'url': 'https://github.com',
        'timeout': 1,
        'reverse_content_match': True,
        'check_certificate_expiration': False,
        'content_match': 'thereisnosuchword'
    }, {
        'name': 'cnt_match_reverse',
        'url': 'https://github.com',
        'timeout': 1,
        'reverse_content_match': True,
        'check_certificate_expiration': False,
        'content_match': '(thereisnosuchword|github)'
    }, {
        'name': 'cnt_mismatch_unicode_reverse',
        'url': 'https://ja.wikipedia.org/',
        'timeout': 1,
        'reverse_content_match': True,
        'check_certificate_expiration': False,
        'content_match': u'メインペーー'
    }, {
        'name': 'cnt_match_unicode_reverse',
        'url': 'https://ja.wikipedia.org/',
        'timeout': 1,
        'reverse_content_match': True,
        'check_certificate_expiration': False,
        'content_match': u'メインページ'
    }
    ]
}

CONFIG_SSL_ONLY = {
    'instances': [{
        'name': 'good_cert',
        'url': 'https://github.com:443',
        'timeout': 1,
        'check_certificate_expiration': True,
        'days_warning': 14,
        'days_critical': 7
    }, {
        'name': 'cert_exp_soon',
        'url': 'https://google.com',
        'timeout': 1,
        'check_certificate_expiration': True,
        'days_warning': 9999,
        'days_critical': 7
    }, {
        'name': 'cert_critical',
        'url': 'https://google.com',
        'timeout': 1,
        'check_certificate_expiration': True,
        'days_warning': 9999,
        'days_critical': 9999
    }, {
        'name': 'conn_error',
        'url': 'https://thereisnosuchlink.com',
        'timeout': 1,
        'check_certificate_expiration': True,
        'days_warning': 14,
        'days_critical': 7
    }
    ]
}

CONFIG_EXPIRED_SSL = {
    'instances': [{
        'name': 'expired_cert',
        'url': 'https://github.com',
        'timeout': 1,
        'check_certificate_expiration': True,
        'days_warning': 14,
        'days_critical': 7
    },
    ]
}

CONFIG_CUSTOM_NAME = {
    'instances': [{
        'name': 'cert_validation_fails',
        'url': 'https://github.com:443',
        'timeout': 1,
        'check_certificate_expiration': True,
        'days_warning': 14,
        'days_critical': 7,
        'ssl_server_name': 'incorrect_name'
    }, {
        'name': 'cert_validation_passes',
        'url': 'https://github.com:443',
        'timeout': 1,
        'check_certificate_expiration': True,
        'days_warning': 14,
        'days_critical': 7,
        'ssl_server_name': 'github.com'
    }
    ],
}

CONFIG_UNORMALIZED_INSTANCE_NAME = {
    'instances': [{
        'name': '_need-to__be_normalized-',
        'url': 'https://github.com',
        'timeout': 1,
        'check_certificate_expiration': True,
        'days_warning': 14,
        'days_critical': 7
    },
    ]
}

SIMPLE_CONFIG = {
    'instances': [{
        'name': 'simple_config',
        'url': 'http://httpbin.org',
        'check_certificate_expiration': False,
    },
    ]
}

CONFIG_HTTP_HEADERS = {
    'instances': [{
        'url': 'https://google.com',
        'name': 'UpService',
        'timeout': 1,
        'headers': {"X-Auth-Token": "SOME-AUTH-TOKEN"}
    }]
}

CONFIG_HTTP_REDIRECTS = {
    'instances': [{
        'name': 'redirect_service',
        'url': 'http://github.com',
        'timeout': 1,
        'http_response_status_code': 301,
        'allow_redirects': False,
    }]
}

FAKE_CERT = {'notAfter': 'Apr 12 12:00:00 2006 GMT'}

CONFIG_POST_METHOD = {
    'instances': [{
        'name': 'post_method',
        'url': 'http://httpbin.org/post',
        'timeout': 1,
        'method': 'post',
        'data': {
            'foo': 'bar',
            'baz': ['qux','quux']
        }
    }]
}

CONFIG_POST_SOAP = {
    'instances': [{
        'name': 'post_soap',
        'url': 'http://httpbin.org/post',
        'timeout': 1,
        'method': 'post',
        'data': '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:m="http://www.example.org/stocks"><soap:Header></soap:Header><soap:Body><m:GetStockPrice><m:StockName>EXAMPLE</m:StockName></m:GetStockPrice></soap:Body></soap:Envelope>'
    }]
}

@attr(requires='skip')
class HTTPCheckTest(AgentCheckTest):
    CHECK_NAME = 'http_check'

    def tearDown(self):
        if self.check:
            self.check.stop()

    def test_http_headers(self):
        """
        Headers format.
        """
        # Run the check
        self.load_check(CONFIG_HTTP_HEADERS, AGENT_CONFIG)
        headers = self.check._load_conf(CONFIG_HTTP_HEADERS['instances'][0])[8]

        self.assertEqual(headers["X-Auth-Token"], "SOME-AUTH-TOKEN", headers)
        expected_headers = agent_headers(AGENT_CONFIG).get('User-Agent')
        self.assertEqual(expected_headers, headers.get('User-Agent'), headers)

    def test_check(self):
        """
        Check coverage.
        """
        self.run_check(CONFIG)
        # Overrides self.service_checks attribute when values are available\
        self.service_checks = self.wait_for_async(
            'get_service_checks', 'service_checks', len(CONFIG['instances']), RESULTS_TIMEOUT)

        # HTTP connection error
        tags = ['url:https://thereisnosuchlink.com', 'instance:conn_error']
        self.assertServiceCheckCritical("http.can_connect", tags=tags)

        # Wrong HTTP response status code
        tags = ['url:http://httpbin.org/404', 'instance:http_error_status_code']
        self.assertServiceCheckCritical("http.can_connect", tags=tags)

        self.assertServiceCheckOK("http.can_connect", tags=tags, count=0)

        # HTTP response status code match
        tags = ['url:http://httpbin.org/404', 'instance:status_code_match', 'foo:bar']
        self.assertServiceCheckOK("http.can_connect", tags=tags)

        # Content match & mismatching
        tags = ['url:https://github.com', 'instance:cnt_mismatch']
        self.assertServiceCheckCritical("http.can_connect", tags=tags)
        self.assertServiceCheckOK("http.can_connect", tags=tags, count=0)
        tags = ['url:https://github.com', 'instance:cnt_match']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        tags = ['url:https://ja.wikipedia.org/', 'instance:cnt_match_unicode']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        tags = ['url:https://ja.wikipedia.org/', 'instance:cnt_mismatch_unicode']
        self.assertServiceCheckCritical("http.can_connect", tags=tags)
        self.assertServiceCheckOK("http.can_connect", tags=tags, count=0)
        tags = ['url:https://github.com', 'instance:cnt_mismatch_reverse']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        self.assertServiceCheckCritical("http.can_connect", tags=tags, count=0)
        tags = ['url:https://github.com', 'instance:cnt_match_reverse']
        self.assertServiceCheckCritical("http.can_connect", tags=tags)
        tags = ['url:https://ja.wikipedia.org/', 'instance:cnt_mismatch_unicode_reverse']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        tags = ['url:https://ja.wikipedia.org/', 'instance:cnt_match_unicode_reverse']
        self.assertServiceCheckCritical("http.can_connect", tags=tags)
        self.assertServiceCheckOK("http.can_connect", tags=tags, count=0)

        self.coverage_report()

    def test_check_ssl(self):
        self.run_check(CONFIG_SSL_ONLY)
        # Overrides self.service_checks attribute when values are available
        self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 6, RESULTS_TIMEOUT)
        tags = ['url:https://github.com:443', 'instance:good_cert']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        self.assertServiceCheckOK("http.ssl_cert", tags=tags)

        tags = ['url:https://google.com', 'instance:cert_exp_soon']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        self.assertServiceCheckWarning("http.ssl_cert", tags=tags)

        tags = ['url:https://google.com', 'instance:cert_critical']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        self.assertServiceCheckCritical("http.ssl_cert", tags=tags)

        tags = ['url:https://thereisnosuchlink.com', 'instance:conn_error']
        self.assertServiceCheckCritical("http.can_connect", tags=tags)
        self.assertServiceCheckCritical("http.ssl_cert", tags=tags)

        self.coverage_report()

    @mock.patch('ssl.SSLSocket.getpeercert', **{'return_value.raiseError.side_effect': Exception()})
    def test_check_ssl_expire_error(self, getpeercert_func):
        self.run_check(CONFIG_EXPIRED_SSL)

        self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 2, RESULTS_TIMEOUT)
        tags = ['url:https://github.com', 'instance:expired_cert']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        self.assertServiceCheckCritical("http.ssl_cert", tags=tags)

        self.coverage_report()

    def test_check_hostname_override(self):
        self.run_check(CONFIG_CUSTOM_NAME)

        self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 4, RESULTS_TIMEOUT)

        tags = ['url:https://github.com:443', 'instance:cert_validation_fails']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        self.assertServiceCheckCritical("http.ssl_cert", tags=tags)

        tags = ['url:https://github.com:443', 'instance:cert_validation_passes']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        self.assertServiceCheckOK("http.ssl_cert", tags=tags)

        self.coverage_report()

    def test_check_allow_redirects(self):
        self.run_check(CONFIG_HTTP_REDIRECTS)
        # Overrides self.service_checks attribute when values are available\
        self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)

        tags = ['url:http://github.com', 'instance:redirect_service']
        self.assertServiceCheckOK("http.can_connect", tags=tags)

        self.coverage_report()

    @mock.patch('ssl.SSLSocket.getpeercert', return_value=FAKE_CERT)
    def test_mock_case(self, getpeercert_func):
        self.run_check(CONFIG_EXPIRED_SSL)
        # Overrides self.service_checks attribute when values are av
        # Needed for the HTTP headers
        self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 2, RESULTS_TIMEOUT)
        tags = ['url:https://github.com', 'instance:expired_cert']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        self.assertServiceCheckCritical("http.ssl_cert", tags=tags)
        self.coverage_report()

    def test_service_check_instance_name_normalization(self):
        """
        Service check `instance` tag value is normalized.

        Note: necessary to avoid mismatch and backward incompatiblity.
        """
        # Run the check
        self.run_check(CONFIG_UNORMALIZED_INSTANCE_NAME)

        # Overrides self.service_checks attribute when values are available
        self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 2, RESULTS_TIMEOUT)

        # Assess instance name normalization
        tags = ['url:https://github.com', 'instance:need_to_be_normalized']
        self.assertServiceCheckOK("http.can_connect", tags=tags)
        self.assertServiceCheckOK("http.ssl_cert", tags=tags)

    def test_warnings(self):
        """
        Deprecate events usage for service checks.
        """
        self.run_check(SIMPLE_CONFIG)

        # Overrides self.service_checks attribute when values are available\
        self.warnings = self.wait_for_async('get_warnings', 'warnings', 1, RESULTS_TIMEOUT)

        # Assess warnings
        self.assertWarning(
            "Using events for service checks is deprecated in "
            "favor of monitors and will be removed in future versions of the "
            "Datadog Agent.",
            count=1
        )

    def test_post_method(self):
        # Run the check
        self.run_check(CONFIG_POST_METHOD)
        self.run_check(CONFIG_POST_SOAP)
