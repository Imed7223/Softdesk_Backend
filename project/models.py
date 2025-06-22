from django.db import models
from django.conf import settings

class Project(models.Model):
    TYPE_CHOICES = [
        ('BACK_END', 'Back-end'),
        ('FRONT_END', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_projects'
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contributor(models.Model):
    PERMISSION_CHOICES = [
        ('AUTHOR', 'Author'),
        ('CONTRIBUTOR', 'Contributor'),
    ]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contributions'
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='contributors'
    )
    permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES, default='CONTRIBUTOR')
    role = models.CharField(max_length=128)

    class Meta:
        unique_together = ('user', 'project')  # Un user ne peut contribuer qu'une fois à un projet

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"
