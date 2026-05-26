import torch.nn as nn
from torchvision import models

def create_achievement_model(num_classes, pretrained=False):
    # EfficientNet_V2_S を使用し、全層チューニングに対応
    weights = models.EfficientNet_V2_S_Weights.DEFAULT if pretrained else None
    model = models.efficientnet_v2_s(weights=weights)
    
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    
    return model