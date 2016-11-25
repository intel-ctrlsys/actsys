""" Tests ListExpander Class"""
from unittest import TestCase
from ..cluster_configuration_parser import ListExpander

class TestListExpander(TestCase):
    """ Tests ListExpander Class"""
    def test___is_expandable(self):
        pattern = 'host, host001, hos[3:2-4], node[3:1-3],, nodi[3:1-8]-as'
        self.assertIsNotNone(ListExpander.is_expandable(pattern))

    def test___expand_list(self):
        pattern = 'host, host001, host[3:2-3], host[3:1-3]tail,' \
                  '[3:1-3]host, [3:1-3]host[3:1-3], 192.168.1.254,' \
                  '192.168.[1:100-101].33,192.168.[1:100-101].[1:35-36],' \
                  '100,100a,host[:-],host[3:10-7],'
        expected_list = ['host', 'host001',
                         'host002', 'host003',
                         'host001tail', 'host002tail', 'host003tail',
                         '001host', '002host', '003host',
                         '001host001', '001host002', '001host003',
                         '002host001', '002host002', '002host003',
                         '003host001', '003host002', '003host003',
                         '192.168.1.254',
                         '192.168.100.33', '192.168.101.33',
                         '192.168.100.35', '192.168.100.36',
                         '192.168.101.35', '192.168.101.36',
                         '100', '100a', 'host[:-]']
        result_list = ListExpander.expand_list(pattern)
        self.assertEqual(len(result_list), len(expected_list))
        intersection = frozenset(expected_list).intersection(result_list)
        self.assertEqual(len(expected_list), len(intersection))

