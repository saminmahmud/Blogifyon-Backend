from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image

class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/" ,blank=True, null=True, default='profile_pictures/default_pic.png')
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with Image.open(self.profile_picture.path) as img:
            target_size =300
            if img.height > target_size or img.width > target_size:
                output_size = (target_size, target_size)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)
    

    def total_posts(self):
        from post.models import Post
        return Post.objects.filter(user=self).count()
    
    def total_saved_posts(self):
        from post.models import SavedPost
        return SavedPost.objects.filter(user=self).count()
    
    
    # def my_followers(self):
    #     return self.followers.all()
    
    # def my_following(self):
    #     return self.following.all()  


STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]

class RatingandReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    rating = models.CharField(max_length=5, choices=STAR_CHOICES)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"
    
    class Meta:
        ordering = ['-created_at']
    
    
