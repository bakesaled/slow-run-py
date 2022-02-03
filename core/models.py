from django.db import models


class TimestampedModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    abstract = True
    
    # By default, order by reverse-chronological order.
    # This cal be overriden on a per-model basis.
    ordering = ['-created_at', '-updated_at']