from django.db import models

class Animal(models.Model):
    TAMANHO_CHOICES = [
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Médio'),
        ('Grande', 'Grande'),
    ]
    
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Fêmea', 'Fêmea'),
    ]

    ESPECIE_CHOICES = [
        ('Cachorro', 'Cachorro'),
        ('Gato', 'Gato'),
        ('Pássaro', 'Pássaro'),
        ('Outros', 'Outros'),
    ]

    IDADE_CATEGORIA_CHOICES = [
        ('Filhote', 'Filhote'),
        ('Jovem', 'Jovem'),
        ('Adulto', 'Adulto'),
        ('Sênior', 'Sênior'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome")
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES, default='Cachorro', verbose_name="Espécie")
    foto = models.ImageField(upload_to='animais/', verbose_name="Foto")
    idade = models.PositiveIntegerField(verbose_name="Idade")
    idade_categoria = models.CharField(max_length=20, choices=IDADE_CATEGORIA_CHOICES, default='Adulto', verbose_name="Categoria de Idade")
    tamanho = models.CharField(max_length=10, choices=TAMANHO_CHOICES, verbose_name="Tamanho")
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, verbose_name="Sexo")
    caracteristicas = models.TextField(verbose_name="Características", help_text="Ex: Carinhoso, Brincalhão, Obediente")
    descricao = models.TextField(verbose_name="Descrição")
    vacinado = models.BooleanField(default=False, verbose_name="Vacinado")
    castrado = models.BooleanField(default=False, verbose_name="Castrado")

    def __str__(self):
        return self.nome

    def caracteristicas_list(self):
        if self.caracteristicas:
            return [c.strip() for c in self.caracteristicas.split(',') if c.strip()]
        return []


    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"

class InteresseAdocao(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='interesses')
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='meus_interesses')
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Interesse de Adoção"
        verbose_name_plural = "Interesses de Adoção"
        unique_together = ('animal', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} se interessou por {self.animal.nome}"
