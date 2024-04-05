from django.db import models

# Create your models here.
from django.db import models

class Conversation(models.Model):
    user_input = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # 你可以添加其他字段来存储更多元数据，例如情感分析结果