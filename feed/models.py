from django.db import models
from django.conf import settings


class Ad(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ad"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} - {self.author.name}"


class Comment(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="comment")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment"
    )
    text = models.CharField(
        max_length=255, null=False, blank=False, verbose_name="контент"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.ad.name} - {self.author.name} - {self.text}"
