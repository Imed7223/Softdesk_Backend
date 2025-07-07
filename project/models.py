from django.db import models
from django.conf import settings
import uuid

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
        related_name='authored_projects',
        null=True,  #  permet que ce soit None
        blank=True  #  pour l’admin/Django Forms
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
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contributor_authors'
    )

    class Meta:
        unique_together = ('user', 'project') # Un user ne peut contribuer qu'une fois à un projet

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"

 
class Issue(models.Model):

    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]
    TAG_CHOICES = [('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')]
    STATUS_CHOICES = [('TO_DO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('FINISHED', 'Finished')]
    title = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.CharField(choices=TAG_CHOICES, max_length=20)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10, default='LOW')
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='TO_DO')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_issues', on_delete=models.CASCADE,default=1)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)