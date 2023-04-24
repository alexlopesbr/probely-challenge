import requests
from pathlib import os

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Finding


class Command(BaseCommand):
    help = 'Save findings with a given target ID from the Probely API'

    def add_arguments(self, parser):
        parser.add_argument('arg_target_id', type=str, help='target id to be saved')

    def handle(self, *args, **options):
        target_id_to_be_save: str = options['arg_target_id']

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
                Finding.objects.bulk_create(self.findings_to_create(results, target_id_to_be_save))

            if page_total == current_page:
                break
            params['page'] = current_page + 1

        self.stdout.write('Data saved')

    def findings_to_create(self, results: dict, target_id_to_be_save: str) -> list:
        findings_to_create = []

        for result in results:
            #  checks if there is a callback and if the target id is the same as expected
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

        return findings_to_create

    def response(self, main_url, headers, params) -> str:
        return requests.get(main_url, headers=headers, params=params)
