from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from .models import CloudFile


def cloud_download(request, pk):
    cloud_file = get_object_or_404(CloudFile, pk=pk)
    try:
        fh = cloud_file.file.open("rb")
    except FileNotFoundError:
        raise Http404("Файл не найден на диске.")
    return FileResponse(
        fh,
        as_attachment=True,
        filename=cloud_file.original_name,
        content_type=cloud_file.mime_type or "application/octet-stream",
    )
