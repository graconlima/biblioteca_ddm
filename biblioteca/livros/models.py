from django.db import models 

class Autor(models.Model): 
    nome = models.CharField(max_length=100) 
    nacionalidade = models.CharField(max_length=50) 

    def __str__(self): 
        return self.nome 

class Livro(models.Model): 
    titulo = models.CharField(max_length=200) 
    ano_publicacao = models.IntegerField() 
    autor = models.ForeignKey(Autor, related_name="livros", on_delete=models.CASCADE) 

    def __str__(self): 
        return self.titulo 

class Dispositivo(models.Model):
    usuario = models.CharField(max_length=100)
    token = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario