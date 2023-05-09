# Create your views here.
import base64
import tempfile
from django.shortcuts import render
from . import similarity

def index(request):
    return render(request, 'reversal/index.html')


def app(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        if not upload.name.endswith('.png'):
            return render(request, 'reversal/app.html',{'status' : False, 'message' : '只能上傳副檔名為 png 的圖片'})
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(upload.read())
        file_url = temp_file.name

        with open(file_url, 'rb') as f:
            encoded_data = base64.b64encode(f.read()).decode('utf-8')

        prompt = ""
        query_image_id = file_url # 圖片位置
        top_k = 20 # 搜尋前幾名
        top_k_image_ids, top_k_similarities, top_k_prompts = similarity.get_similar_images(query_image_id, top_k)

        return render(request, 'reversal/app.html', {'status' : True, 'message' : '上傳成功！','file': encoded_data,'prompt' : top_k_prompts[0],'similarity' : round(top_k_similarities[0],2)*100})
    return render(request, 'reversal/app.html')


def about(request):
    return render(request, 'reversal/about.html')