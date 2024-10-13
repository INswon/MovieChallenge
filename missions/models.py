from django.db import models
from users.models import User

class Mission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    criteria = models.JSONField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Batch(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    mission = models.ForeignKey(Mission, related_name='batches', on_delete=models.CASCADE)
    condition = models.JSONField() 

    def __str__(self):
        return self.name
      
class UserMission(models.Model):
    user = models.ForeignKey(User, related_name='user_missions', on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, related_name='user_missions', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'mission')  # 同じミッションを複数回持つことを防止

    def __str__(self):
        return f"{self.user.username} - {self.mission.title}"

class UserBatch(models.Model):
    user = models.ForeignKey(User, related_name='user_batches', on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, related_name='user_batches', on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'batch')  # 同じバッチを複数回取得しないように制約
      
    def __str__(self):
        return f"{self.user.username} - {self.batch.name}"


