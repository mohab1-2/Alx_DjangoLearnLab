from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Post, Comment

User = get_user_model()

class PostModelTest(TestCase):
    """Test Post model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_post_creation(self):
        """Test creating a post"""
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post content.'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.created_at)
        self.assertTrue(post.updated_at)
        
    def test_post_str_method(self):
        """Test post string representation"""
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        expected_str = f"Test Post by {self.user.username}"
        self.assertEqual(str(post), expected_str)

class CommentModelTest(TestCase):
    """Test Comment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        
    def test_comment_creation(self):
        """Test creating a comment"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)
        
    def test_comment_str_method(self):
        """Test comment string representation"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
        expected_str = f"Comment by {self.user.username} on {self.post.title}"
        self.assertEqual(str(comment), expected_str)

class PostAPITest(APITestCase):
    """Test Post API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        self.post = Post.objects.create(
            author=self.user1,
            title='Test Post',
            content='This is a test post.'
        )
        
    def test_get_posts_list(self):
        """Test getting posts list (public access)"""
        url = reverse('post-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_create_post_authenticated(self):
        """Test creating a post with authentication"""
        self.client.force_authenticate(user=self.user1, token=self.token1)
        url = reverse('post-list-create')
        data = {
            'title': 'New Test Post',
            'content': 'This is new post content.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        
    def test_create_post_unauthenticated(self):
        """Test creating a post without authentication"""
        url = reverse('post-list-create')
        data = {
            'title': 'New Test Post',
            'content': 'This is new post content.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_post_detail(self):
        """Test getting post detail (public access)"""
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')
        
    def test_update_post_by_author(self):
        """Test updating post by author"""
        self.client.force_authenticate(user=self.user1, token=self.token1)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {
            'title': 'Updated Test Post',
            'content': 'Updated content.'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Test Post')
        
    def test_update_post_by_non_author(self):
        """Test updating post by non-author (should fail)"""
        self.client.force_authenticate(user=self.user2, token=self.token2)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {
            'title': 'Updated Test Post',
            'content': 'Updated content.'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_post_by_author(self):
        """Test deleting post by author"""
        self.client.force_authenticate(user=self.user1, token=self.token1)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
        
    def test_delete_post_by_non_author(self):
        """Test deleting post by non-author (should fail)"""
        self.client.force_authenticate(user=self.user2, token=self.token2)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_search_posts(self):
        """Test searching posts"""
        Post.objects.create(
            author=self.user1,
            title='Django Tutorial',
            content='Learning Django framework.'
        )
        url = reverse('post-list-create')
        response = self.client.get(url, {'search': 'django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_filter_posts_by_author(self):
        """Test filtering posts by author"""
        Post.objects.create(
            author=self.user2,
            title='User2 Post',
            content='Post by user2.'
        )
        url = reverse('post-list-create')
        response = self.client.get(url, {'author': self.user1.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class CommentAPITest(APITestCase):
    """Test Comment API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        self.post = Post.objects.create(
            author=self.user1,
            title='Test Post',
            content='This is a test post.'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content='This is a test comment.'
        )
        
    def test_get_post_comments(self):
        """Test getting comments for a post"""
        url = reverse('post-comments', kwargs={'post_pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_create_comment_authenticated(self):
        """Test creating a comment with authentication"""
        self.client.force_authenticate(user=self.user2, token=self.token2)
        url = reverse('post-comments', kwargs={'post_pk': self.post.pk})
        data = {'content': 'This is a new comment.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        
    def test_create_comment_unauthenticated(self):
        """Test creating a comment without authentication"""
        url = reverse('post-comments', kwargs={'post_pk': self.post.pk})
        data = {'content': 'This is a new comment.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_comment_by_author(self):
        """Test updating comment by author"""
        self.client.force_authenticate(user=self.user1, token=self.token1)
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        data = {'content': 'Updated comment content.'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment content.')
        
    def test_update_comment_by_non_author(self):
        """Test updating comment by non-author (should fail)"""
        self.client.force_authenticate(user=self.user2, token=self.token2)
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        data = {'content': 'Updated comment content.'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_comment_by_author(self):
        """Test deleting comment by author"""
        self.client.force_authenticate(user=self.user1, token=self.token1)
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

class PaginationTest(APITestCase):
    """Test pagination functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Create 15 posts for pagination testing
        for i in range(15):
            Post.objects.create(
                author=self.user,
                title=f'Test Post {i+1}',
                content=f'Content for post {i+1}'
            )
            
    def test_default_pagination(self):
        """Test default pagination (10 per page)"""
        url = reverse('post-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        
    def test_custom_page_size(self):
        """Test custom page size"""
        url = reverse('post-list-create')
        response = self.client.get(url, {'page_size': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        
    def test_second_page(self):
        """Test getting second page"""
        url = reverse('post-list-create')
        response = self.client.get(url, {'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # Remaining 5 posts