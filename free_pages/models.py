from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class MembershipBenefits(models.Model):
    benefits = RichTextField()


class CustomUser(AbstractUser):
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class MainCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = AutoSlugField(unique=True, populate_from="name")

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="subcategories"
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = AutoSlugField(unique=True, populate_from="name")

    def __str__(self):
        return self.name


class Post(models.Model):
    main_category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="posts"
    )
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=50)
    description = models.TextField()
    content = RichTextField()
    slug = AutoSlugField(unique=True, populate_from="title")
    file = models.FileField(
        upload_to="files", null=True, blank=True, help_text="Optional"
    )
    image = models.ImageField(
        upload_to="images", null=True, blank=True, help_text="Optional"
    )
    image_description = models.CharField(
        max_length=50,
        help_text="Describe the image for search engines and screen readers",
        blank=True,
        null=True,
    )
    video = models.FileField(
        upload_to="files", null=True, blank=True, help_text="Optional"
    )

    def __str__(self):
        return self.title
