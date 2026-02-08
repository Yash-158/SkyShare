from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from .models import FileTransfer
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'transfers/index.html')

def upload_page(request):
    return render(request, 'transfers/upload.html')

def download_page(request):
    return render(request, 'transfers/download.html')

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        try:
            transfer = FileTransfer(
                file=file,
                name=file.name,
                size=file.size
            )
            transfer.save()
            return JsonResponse({
                'success': True,
                'code': transfer.code,
                'filename': transfer.name,
                'expires_at': transfer.expires_at.isoformat()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def download_file(request, code):
    transfer = get_object_or_404(FileTransfer, code=code)
    
    if transfer.is_expired():
        return HttpResponse("This file has expired.", status=410)
        
    response = FileResponse(transfer.file)
    # Force download
    response['Content-Disposition'] = f'attachment; filename="{transfer.name}"'
    return response
