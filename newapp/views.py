import os

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .utils.file_proccessing import FileExploration


def upload_file(request):
    try:
        if request.method == 'POST' and request.FILES['file']:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            print(f"filepath>>>>>{filepath}", flush=True)
            explore = FileExploration(filepath)
            file_info = explore.parse_and_display_info()
            print(f"file_info>>>>>{file_info}", flush=True)
            return render(request, 'file_info.html', {'file_info': file_info})
        return render(request, 'upload.html')
    except:
        return render(request, 'upload.html')
    

def detailed(request):
    if request.method == 'POST':
        library = request.POST.get('library')
        num_words = request.POST.get('num_words')
        num_chars = request.POST.get('num_chars')
        data = {
            'library': library,
            'num_words': num_words,
            'num_chars': num_chars
        }
        return render(request, 'detailed_info.html', {'data': data})
    else:
        return render(request, 'error_page.html')
