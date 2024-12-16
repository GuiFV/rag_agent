import unittest
from app import app


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the test client for Flask app."""
        self.client = app.test_client()

    def test_index(self):
        """Test the index endpoint."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_cv_generator_get(self):
        """Test the cv_generator endpoint with a GET request."""
        response = self.client.get('/cv_generator')
        self.assertEqual(response.status_code, 200)

    def test_cv_generator_post(self):
        """Test the cv_generator endpoint with a POST request."""
        response = self.client.post('/cv_generator', data={'job_description': 'Test job description'})
        self.assertEqual(response.status_code, 200)

    def test_basic_gpt_get(self):
        """Test the basic_gpt endpoint with a GET request."""
        response = self.client.get('/basic_gpt')
        self.assertEqual(response.status_code, 200)

    def test_basic_gpt_post(self):
        """Test the basic_gpt endpoint with a POST request."""
        response = self.client.post('/basic_gpt', data={'user_input': 'Hello, GPT!'})
        self.assertEqual(response.status_code, 200)

    def test_basic_rag(self):
        """Test the basic_rag endpoint."""
        response = self.client.get('/basic_rag')
        self.assertEqual(response.status_code, 200)

    def test_reset_chat(self):
        """Test the reset_chat endpoint."""
        response = self.client.post('/reset_chat')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "Chat history reset."})


if __name__ == '__main__':
    unittest.main()
