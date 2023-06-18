# Create your views here.
import base64
import os
import tempfile
from nltk.corpus import stopwords
from collections import Counter
import re
import string
import nltk
from django.shortcuts import render
from datasets import load_dataset
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

        query_image_id = file_url # 圖片位置
        top_k = 10 # 搜尋前幾名
        top_k_image_ids, top_k_similarities, top_k_prompts = similarity.get_similar_images(query_image_id, top_k)
        image_exists = [img if os.path.isfile(f'static/images/kaggle/{img}.png') else False for img in top_k_image_ids]
        img_prompts = list(zip(image_exists, top_k_prompts, top_k_similarities))

        # 取出所有 prompt 的單詞
        all_words = []
        for prompt in top_k_prompts:
            words = clean_text(prompt)
            all_words += words

        # 取出最常出現的前 n 個單詞
        n = 10
        word_counts = Counter(all_words)
        top_n_words = word_counts.most_common(n)

        if round(top_k_similarities[0],2)*100 != 100:
            # 重組句子
            sentences = []
            for prompt in top_k_prompts:
                words = clean_text(prompt)
                sentence = ' '.join(words)
                sentences.append(sentence)

            # 取前 n 句組成新的句子
            n = 3
            new_sentence = ' '.join(sentences[:n])

            # 輸出最常出現的單詞
            print('Top {} words:'.format(n))
            for word, count in top_n_words:
                print('{}: {}'.format(word, count))

            # 輸出重組的句子
            print('New sentence: {}'.format(new_sentence))

            return render(request, 'reversal/app.html', {'status' : True, 'message' : '上傳成功！','file': encoded_data,'prompt' : new_sentence, 'img_prompts': img_prompts, 'tags': word_counts.most_common(3) , 'similarity' : round(top_k_similarities[0],2)*100})
        return render(request, 'reversal/app.html', {'status' : True, 'message' : '上傳成功！','file': encoded_data,'prompt' : top_k_prompts[0], 'img_prompts': img_prompts, 'tags': word_counts.most_common(3) , 'similarity' : round(top_k_similarities[0],2)*100})
    return render(request, 'reversal/app.html')

def clean_text(text):
    # 移除所有標點符號
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 轉成小寫
    text = text.lower()
    # 移除所有數字
    text = re.sub(r'\d+', '', text)
    # 移除停用詞
    stop_words = set(stopwords.words('english'))
    text_tokens = nltk.word_tokenize(text)
    filtered_words = [word for word in text_tokens if word.lower() not in stop_words]
    # 取出單詞
    words = [word for word in filtered_words if word.isalpha()]
    return words

def about(request):
    return render(request, 'reversal/about.html')

def prompt(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        user_prompt = request.POST['prompt']
        upload = request.FILES.get('upload')
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(upload.read())
        file_url = temp_file.name

        with open(file_url, 'rb') as f:
            encoded_data = base64.b64encode(f.read()).decode('utf-8')

        query_image_id = file_url # 圖片位置
        resultSimilarity = similarity.calculate_similarity(query_image_id,user_prompt)
        print(type(resultSimilarity))

        return render(request, 'reversal/prompt.html', {'status' : True, 'message' : '上傳成功！','file': encoded_data, 'user_prompt': user_prompt, 'similarity' : resultSimilarity})
    return render(request, 'reversal/prompt.html')