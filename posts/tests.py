from django.test import TestCase
from posts.models import Post

class ViewTestCase(TestCase):
    def test_mostrar_home(self):
        response = self.client.get('/')
        self.assertContains(response, 'Meu Blog', status_code=200, html=True)

    def test_mostrar_home_com_posts(self):
        post = Post()
        post.titulo = 'Post 1'
        post.conteudo = 'Primeiro post do blog'
        post.save()

        response = self.client.get('/')
        self.assertContains(response, 'Post 1', status_code=200, html=True)
        self.assertContains(response, 'Primeiro post do blog', status_code=200, html=True)

    def test_mostrar_form(self):
        response = self.client.get('/formulario/')
        self.assertContains(response, 'Cadastrar Post', status_code=200, html=True)

    def test_enviar_form(self):
        response = self.client.post('/formulario/', {'titulo': 'Test Post', 'conteudo': 'Esse post é um teste'})
        all_posts = Post.objects.filter().all()

        self.assertEqual(302, response.status_code)
        self.assertEqual(1, len(all_posts))