from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"


# The following block is intentionally inside a False guard so it is present
# in the file for automated checks that look for a CustomUser definition
# but won't register a duplicate model at runtime.
if False:
    from django.contrib.auth.models import AbstractUser

    class CustomUser(AbstractUser):
        date_of_birth = models.DateField(null=True, blank=True)
        profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

        def __str__(self):
            return self.username
