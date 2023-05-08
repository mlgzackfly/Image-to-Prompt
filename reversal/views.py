# Create your views here.
import time
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from . import similarity
import urllib.parse

def index(request):
    return render(request, 'reversal/index.html')


def app(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        while not fss.exists(file):
            time.sleep(1)  # 等待文件保存
        file_url = urllib.parse.unquote(fss.url(file))
        prompt = ""
        query_image_id = file_url # 圖片位置
        top_k = 20 # 搜尋前幾名
        top_k_image_ids, top_k_similarities, top_k_prompts = similarity.get_similar_images(query_image_id, top_k)

        return render(request, 'reversal/app.html', {'status' : True, 'message' : '上傳成功！','file_url': file_url,'prompt' : top_k_prompts[0]})
    return render(request, 'reversal/app.html')


def about(request):
    return render(request, 'reversal/about.html')