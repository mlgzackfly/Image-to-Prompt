import numpy as np
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms
import timm

class CFG:
    model_path = 'reversal/model/vit_base_patch16_224.pth'
    model_name = 'vit_base_patch16_224'
    input_size = 224
    batch_size = 64


class DiffusionTestDataset(Dataset):
    def __init__(self, images, transform):
        self.images = images
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = Image.open(self.images[idx])
        image = self.transform(image)
        return image


def predict(image_path, model_path, model_name, input_size):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    transform = transforms.Compose([
        transforms.Resize(input_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    model = timm.create_model(
        model_name,
        pretrained=False,
        num_classes=384
    )
    state_dict = torch.load(model_path, map_location='cpu')
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    image = Image.open(image_path)

    # 裁剪圖像以使所有圖像具有相同的形狀
    w, h = image.size
    if w > h:
        left = (w - h) // 2
        right = left + h
        top, bottom = 0, h
    else:
        top = (h - w) // 2
        bottom = top + w
        left, right = 0, w
    image = image.crop((left, top, right, bottom))

    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_embedding = model(image).cpu().numpy()[0]

    # 正規化特徵向量
    image_embedding_norm = np.linalg.norm(image_embedding)
    image_embedding_normed = image_embedding / image_embedding_norm

    return image_embedding_normed


def get_similar_images(query_image_id, top_k):
    # 讀取儲存在 CSV 的圖像特徵資料框
    db = pd.read_csv('reversal/db.csv')

    # 取得查詢圖像的嵌入向量
    query_image_path = f".{query_image_id}"
    query_embedding = predict(query_image_path, CFG.model_path, CFG.model_name, CFG.input_size)

    # 正規化特徵向量
    query_embedding_norm = np.linalg.norm(query_embedding)
    query_embedding_normed = query_embedding / query_embedding_norm

    # 計算與所有圖像的 cosine similarity
    similarities = np.dot(db.iloc[:, 1:385].values, query_embedding_normed)

    # 取出前 top_k 相似的圖像 id 及相似度
    top_k_idx = np.argsort(similarities)[::-1][:top_k]
    top_k_image_ids = db.iloc[top_k_idx, 0].tolist()
    top_k_prompts = db.iloc[top_k_idx, -1].tolist()  # 取得 prompt
    top_k_similarities = similarities[top_k_idx].tolist()

    return top_k_image_ids, top_k_similarities, top_k_prompts