from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post


class APITest(APITestCase):
    # Set up method to create test data and user
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(author=self.user, content="Test Post", visibility='PUBLIC')
        self.api_authentication()

    # Helper method for setting the token for authentication
    def api_authentication(self):
        self.client.login(username='testuser', password='12345')

    # Testing POST to create a new resource (e.g., a new Post)
    def test_create_post(self):
        url = reverse('post-list')  # Update with your actual URL name
        data = {"content": "New Post Content", "visibility": "PUBLIC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing GET to retrieve a resource (e.g., list of Posts)
    def test_get_posts(self):
        url = reverse('post-list')  # Update with your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing PUT to update a resource (e.g., updating a Post)
    def test_update_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})  # Update with your actual URL name
        data = {"content": "Updated Content", "visibility": "PUBLIC"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing DELETE to remove a resource (e.g., a Post)
    def test_delete_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})  # Update with your actual URL name
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a test post
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Test Content')

    def test_get_posts(self):
        # Test retrieving a list of posts
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming one post in setUp

    def test_create_post(self):
        # Test creating a new post
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'Content of new post', 'author': self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_get_individual_post(self):
        # Test retrieving a specific post
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_update_post(self):
        # Test updating a specific post
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Post', 'content': 'Updated Content', 'author': self.user.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_partial_update_post(self):
        # Test partially updating a post (only changing one field)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Partially Updated Post'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Partially Updated Post')

    def test_delete_post(self):
        # Test deleting a post
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)


class UserAPITests(APITestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.client.login(username='user1', password='password1')

    def test_create_user(self):
        # Test creating a new user
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)  # Including the two users from setUp

    def test_get_user_profile(self):
        # Test retrieving a user's profile
        url = reverse('user-detail', kwargs={'pk': self.user2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user2')

    def test_update_user_profile(self):
        # Test updating a user's profile
        url = reverse('user-detail', kwargs={'pk': self.user1.pk})
        data = {'first_name': 'UpdatedName'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'UpdatedName')

    def test_delete_user(self):
        # Test deleting a user
        url = reverse('user-detail', kwargs={'pk': self.user2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)


class FriendFollowAPITests(APITestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.client.login(username='user1', password='password1')

    def test_follow_user(self):
        # Test following a user
        url = reverse('follow', kwargs={'pk': self.user2.pk})  # Assume this is the correct URL name
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user2.followers.filter(pk=self.user1.pk).exists())

    def test_unfollow_user(self):
        # Test unfollowing a user
        url = reverse('unfollow', kwargs={'pk': self.user2.pk})  # Assume this is the correct URL name
        # The user1 should follow user2 first to unfollow later
        self.user2.followers.add(self.user1)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user2.followers.filter(pk=self.user1.pk).exists())

    def test_get_followers(self):
        # Test getting list of followers for a user
        url = reverse('followers-list', kwargs={'pk': self.user2.pk})  # Assume this is the correct URL name
        # The user1 should follow user2 to have a non-empty followers list
        self.user2.followers.add(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user1.username, [follower['username'] for follower in response.data])

    def test_get_following(self):
        # Test getting list of following for a user
        url = reverse('following-list', kwargs={'pk': self.user1.pk})  # Assume this is the correct URL name
        # The user1 should follow user2 to have a non-empty following list
        self.user1.following.add(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2.username, [followee['username'] for followee in response.data])


class UserManagementTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_retrieve_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        data = {'username': 'updateduser'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_delete_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username='testuser').exists())

