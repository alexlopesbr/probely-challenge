from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from core.models import Finding


class FindingListView(View):
    def get(self, request):
        queryset = Finding.objects.all()

        definition_id = request.GET.get('definition_id')
        scan = request.GET.get('scan')

        if definition_id:
            queryset = queryset.filter(definition_id=definition_id)
        if scan:
            queryset = queryset.filter(
                #  The regex seeks to provide flexibility in the search where part of the scan value
                #  will already be enough to fall into the filter
                Q(scans__iregex=f'".*{scan}.*"')
            )

        data = list(queryset.values())
        return JsonResponse(data, safe=False)
