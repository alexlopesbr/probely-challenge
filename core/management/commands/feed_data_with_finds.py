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

        self.stdout.write('Performing request')

        response = requests.get(main_url, headers=headers, params=params)
        if response.status_code == 200:
            response = response.json()
            results = response.get('results')

        self.stdout.write('Preparing data')
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
        self.stdout.write('Data saved')
