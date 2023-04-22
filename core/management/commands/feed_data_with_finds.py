import http.client
import json
import requests
from pathlib import os

from django.core.management.base import BaseCommand
from core.models import Finding


class Command(BaseCommand):
    help = 'Feeds the Finding model with the endpoint response to the list of finds'

    def handle(self, *args, **options):
        main_url = 'https://api.probely.com/findings/'
        headers = {'Authorization': f'JWT {str(os.getenv("KEY_ACCESS"))}'}
        params = {'page': 1}

        response = requests.get(main_url, headers=headers, params=params)
        if response.status_code == 200:
            response = response.json()
            results = response.get('results')

        for result in results:
            if result:
                target_id: int = int(result.get('id'))
                definition_id: str = result.get('definition', {}).get('id')
                scans: list = result.get('scans', [])
                url: str = result.get('url')
                path: str = result.get('path')
                method: str = result.get('method')
