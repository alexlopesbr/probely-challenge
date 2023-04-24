import json

from django.test import RequestFactory, TestCase
from django.urls import reverse

from core.models import Finding
from core.views import FindingListView


class FindingListViewTest(TestCase):
    def setUp(self):
        self.url = 'finding-list'
        self.factory = RequestFactory()

    def test_get_all_findings(self):
        sample_finding(definition_id='abc', scans=['123'])
        sample_finding(definition_id='def', scans=['456'])

        url = reverse(self.url)
        request = self.factory.get(
            url,
        )

        response = FindingListView.as_view()(request)
        json_data = response.content.decode('utf-8')
        data_dict = json.loads(json_data)

        # check if all findings are returned
        self.assertEqual(len(data_dict), 2)

    def test_filter_findings_by_definition_id(self):
        sample_finding(definition_id='abc', scans=['123'])
        sample_finding(definition_id='def', scans=['456'])

        url = reverse(self.url)
        request = self.factory.get(
            url,
            {'definition_id': 'abc'}
        )

        response = FindingListView.as_view()(request)
        json_data = response.content.decode('utf-8')
        data_dict = json.loads(json_data)

        # check that only one finding is returned
        self.assertEqual(len(data_dict), 1)
        self.assertEqual(data_dict[0]['definition_id'], 'abc')

    def test_filter_findings_by_scan(self):
        sample_finding(definition_id='abc', scans=['123'])
        sample_finding(definition_id='def', scans=['456'])

        url = reverse(self.url)
        request = self.factory.get(
                url,
                {'scan': '123'}
            )

        response = FindingListView.as_view()(request)
        json_data = response.content.decode('utf-8')
        data_dict = json.loads(json_data)

        # check that only one finding is returned
        self.assertEqual(len(data_dict), 1)
        self.assertEqual(data_dict[0]['scans'], ['123'])


def sample_finding(definition_id: str, scans: list) -> Finding:
    return Finding.objects.create(
        target_id=1,
        definition_id=definition_id,
        scans=scans,
        url='http://test.com',
        path='http://test.com',
        method='get'
    )
