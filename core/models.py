from django.db import models
from django.contrib.auth.models import User

class Arquivo(models.Model):
    titulo = models.CharField(max_length=300, blank=False, null=False)
    file = models.FileField(blank=True, null=True , upload_to='files/', verbose_name="Arquivo")

    def __str__(self):
        return f'{self.titulo}'
class Comunicacao(models.Model):
    autor = models.ForeignKey("Integrante", on_delete=models.CASCADE)
    menssagem = models.TextField(blank=False, null=False)
    pdi = models.ForeignKey("Pdi", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.autor} {self.menssagem[:20]}'


class Escola(models.Model):
    nome = models.CharField(max_length=300, blank=False, null=False, verbose_name="Escola")
    endereco = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    localizacao = models.CharField(max_length=300, blank=False, null=False)
    dep_adm = models.CharField(max_length=300, blank=False, null=False)
    codigo_inep = models.CharField(max_length=300, blank=False, null=False)
    etapas = models.TextField(blank=False, null=False)




    
    def __str__(self):
        return f'{self.nome}'

class Perfil(models.Model):
    tipo = models.IntegerField(choices=[(1,'Administrador Master'), (2,'Administrador'), (3,'Professor'), (4,'Estudante'),(5,'Saúde')])
    
    def __str__(self):
        return f'{self.get_tipo_display()}'

class Estudante(models.Model):
    nome = models.CharField(max_length=300, blank=False, null=False)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome}'


class Integrante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nome = models.CharField(max_length=300, null=False, blank=False)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='perfil_integrante')
    escola = models.ManyToManyField(Escola, related_name='integrante_escolar', null=True, blank=True)
    estudante = models.ManyToManyField(Estudante, related_name='integrante_estudante', null=True, blank=True)


    def __str__(self):
        return f'{self.nome}'

class Pdi(models.Model):
    titulo = models.CharField(max_length=300, null=False, blank=False)
    data_inicial = models.DateField()
    data_final = models.DateField()
    descricao = models.TextField(null=False, blank=False)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE , related_name="estudante_pdi")
    integrante = models.ManyToManyField (Integrante)
    ativo = models.BooleanField(default=True)
    concluido = models.BooleanField(default=False)
    arquivo = models.ForeignKey(Arquivo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.titulo}'
    

    def save(self,*args, **kwargs):
        if self.data_final < self.data_inicial:
            print('A data final não pode ser maior que a incial')
            return 'A data final não pode ser maior que a incial'
        else:
            super().save(*args,**kwargs)
        


