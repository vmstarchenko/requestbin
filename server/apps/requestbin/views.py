import urllib.parse as urlparse
import re
import time

from django.http import JsonResponse
from django.utils import timezone
from django.middleware.gzip import GZipMiddleware


from .models import Request, Bin
from .forms import RequestForm


def parse_headers(meta):
    headers = {
        '-'.join(map(str.title, re.sub('^HTTP_', '', header).split('_'))): value
        for header, value in meta.items()
        if header.startswith('HTTP_') or header in {
            'CONTENT_LENGTH', 'CONTENT_TYPE'}}

    x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
    ip = (
        x_forwarded_for.split(',')
        if x_forwarded_for
        else [meta.get('REMOTE_ADDR')])
    return ip, headers


def catch_request(request, bin_id, path):
    # request options
    start_time = timezone.now()
    form = RequestForm(request.GET)
    if form.is_valid():
        params = form.cleaned_data

    sleep = params.get('_sleep', 0)
    encoding = params.get('_encoding')
    status_code = params.get('_status_code', 200)
    content_type = params.get('_content_type')

    if sleep:
        time.sleep(sleep)

    url = request.build_absolute_uri()
    ip, headers = parse_headers(request.META)
    req = Request(
        bin_id=bin_id,
        url=url,
        method=request.method.upper(),
        params={k: v for k, v in request.GET.lists() if not k.startswith('_')},
        body=request.body.decode('utf-8'),
        headers=headers,
        ip=ip,
        user=request.user if request.user.is_authenticated else None,
        start_time=start_time,
        finish_time=timezone.now(),
    )
    req.save()

    resp = JsonResponse(
        {
            'url': req.url,
            'method': req.method,
            'params': req.params,
            'body': req.body,
            'headers': req.headers,
            'ip': req.ip,
            'user': req.user and req.user.id,
            'now': timezone.now(),
        },
        status=status_code,
        content_type=content_type,
    )

    if encoding == 'gzip':
        gzip_middleware = GZipMiddleware(lambda: None)
        resp = gzip_middleware.process_response(request, resp)

    return resp


def export_bin(request, bin_id):
    return JsonResponse({
        'bin': bin_id,
        'requests': [
            b.as_dict()
            for b in Bin.objects.get(pk=bin_id).requests.all()
        ],
    })

