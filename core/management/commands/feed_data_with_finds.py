import requests
from pathlib import os

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Finding


class Command(BaseCommand):
    help = 'Feeds the Finding model with the endpoint response to the list of finds'

    def add_arguments(self, parser):
        parser.add_argument('arg_target_id', type=str, help='target id to be saved')

    def handle(self, *args, **options):
        target_id_to_be_save = options['arg_target_id']

        main_url = 'https://api.probely.com/findings/'
        headers = {'Authorization': f'JWT {str(os.getenv("KEY_ACCESS"))}'}
        params = {'page': 1}

        while True:
            response = self.response(main_url, headers, params)
            if response.status_code == 200:
                response = response.json()
                results = response.get('results')
                page_total = response.get('page_total')
                current_page = response.get('page')

            self.stdout.write(f'Performing request page {params["page"]} of {page_total}')

            with transaction.atomic():
                findings_to_create = []

                for result in results:
                    if result and (result.get('target', {}).get('id') == target_id_to_be_save):
                        target_id: str = result.get('target', {}).get('id')
                        definition_id: str = result.get('definition', {}).get('id')
                        scans: list = result.get('scans', [])
                        url: str = result.get('url')
                        path: str = result.get('path')
                        method: str = result.get('method')

                        finding = Finding(
                            target_id=target_id,
                            definition_id=definition_id,
                            scans=scans,
                            url=url,
                            path=path,
                            method=method
                        )
                        findings_to_create.append(finding)

                Finding.objects.bulk_create(findings_to_create)

            if page_total == current_page:
                break

            params['page'] = current_page + 1
        self.stdout.write('Data saved')

    def response(self, main_url, headers, params):
        return requests.get(main_url, headers=headers, params=params)
