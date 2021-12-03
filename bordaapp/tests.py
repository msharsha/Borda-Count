from django.contrib.auth.models import User
from bordaapp.models import Post, Submission
from django.test import TestCase
import mock

from bordaapp.views import Aggregator

# Create your tests here.
class PostListViewTest(TestCase):
    def test_post_not_null(self):
        user = User.objects.create_user(username='user1', password='12345', email='user1@user.com')
        post = Post(author= user,
                title= "Post 4",
                content= "Content 4",
                date_posted= "2021-11-18",
                allowed_users= 'user1@user.com,user3@user.com,admin@admin.com,manisha@gmail.com',
                options= 'opt1,opt2,opt3,opt4')
        self.assertIsNotNone(post)

    def test_post_is_valid(self):
        user = User.objects.create_user(username='user1', password='12345', email='user1@user.com')
        post = Post(author= user,
                title= "Post 4",
                content= "Content 4",
                date_posted= "2021-11-18",
                allowed_users= 'user1@user.com,user3@user.com,admin@admin.com,manisha@gmail.com',
                options= 'opt1,opt2,opt3,opt4')
        self.assertEquals(post.title, "Post 4")

    def test_submission(self):
        user = User.objects.create_user(username='user1', password='12345', email='user1@user.com')
        post = Post(author= user,
                title= "Post 4",
                content= "Content 4",
                date_posted= "2021-11-18",
                allowed_users= 'user1@user.com,user3@user.com,admin@admin.com,manisha@gmail.com',
                options= 'opt1,opt2,opt3,opt4')
        submission = Submission(
                options="opt2,opt3,opt4,opt1",
                post_id=post,
                submitted_by=user)
        post.answered_users += user.email
        self.assertIsNotNone(Post)
        self.assertIsNotNone(submission)
    
    def test_user_in_answered_users(self):
        user = User.objects.create_user(username='user1', password='12345', email='user1@user.com')
        post = Post(author= user,
                title= "Post 4",
                content= "Content 4",
                date_posted= "2021-11-18",
                allowed_users= 'user1@user.com,user3@user.com,admin@admin.com,manisha@gmail.com',
                options= 'opt1,opt2,opt3,opt4')
        submission = Submission(
                options="opt2,opt3,opt4,opt1",
                post_id=post,
                submitted_by=user)
        post.answered_users += user.email
        print(post.answered_users, user.email)
        self.assertTrue(str(user.email) in str(post.answered_users) )

# def mocked_get_preference_schedule():
#     candidates = ['9 AM','10 AM','11 AM','2PM']
#     prefs = [['9 AM','10 AM','11 AM','2PM'],['9 AM','2PM','11 AM','10 AM']]
#     return candidates,prefs

# class YourTestCase(TestCase):
#     @mock.patch('get_preference_schedule', side_effect=mocked_get_preference_schedule())
#     def test_borda(self):
#         agg = Aggregator()
#         scores, winner = agg.borda()
#         print(scores)
#         print(winner)

    

    



#submission object by user 1
#validate borda count
#by user2
# validate borda count
#User.objects.get(id=1)