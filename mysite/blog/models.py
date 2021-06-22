from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    # Linking an author to an authorised user so when create a super user will be someone that can create a new post
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length= 200)
    text = models.TextField()
    # This allows you to get the local time that post was created depending on your time zone
    created_date = models.DateTimeField(default=timezone.now)
    # The below can be blank in case you don't want to publish it yet or null in case you don't have a publication date
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        """Publication date method that when you decide to publish it automatically grabs the time from your
        local time zone"""
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        """This filters comments to see those that are approved"""
        return self.comments.filter(approved_comment= True)

    def get_absolute_url(self):
        """Function that tells django to redirect users to detail page of the post they just created oncee they hit submit button"""
        return reverse("post_detail", kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    # post variable connects each comment to an actual post
    post = models.ForeignKey('blog.Post', related_name= 'comments', on_delete=models.CASCADE)
    author = models.CharField(max_length= 200)
    text = models.TextField()
    created_date = models.DateTimeField(default= timezone.now())
    # This is a boolean(True/False) to see if a comment is approved and it is defaulted to false
    approved_comment = models.BooleanField(default= False)

    def approve(self):
        self.approved_comment= True
        self.save()

    def get_absolute_url(self):
        """Returns users to the list view of all posts once hit submit on comments as comments need to be approved"""
        return reverse('post_list')

    def __str__(self):
        self.text