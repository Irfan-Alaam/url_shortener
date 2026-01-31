from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    originalUrl = models.URLField()
    shortKey = models.CharField(max_length=10, unique=True,blank=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    clickCount = models.PositiveIntegerField(default=0)
    isActive= models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "originalUrl"],
                condition=models.Q(isActive=True),
                name="unique_active_url_per_user"
            )
        ]
    def __str__(self):
        return f"{self.shortKey} -> {self.originalUrl}"