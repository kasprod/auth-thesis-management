from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey




class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE,
                                related_name='student')
    matricule = models.CharField(verbose_name=_("matricule"), max_length=50)
    promotion = models.CharField(verbose_name=_("promotion"), max_length=255)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}' if self.user.last_name and self.user.first_name else self.user.username


class PersonalAcademic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE,
                                related_name='personal_academic')
    fonction = models.CharField(verbose_name=_("fonction"), max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}' if self.user.last_name and self.user.first_name else self.user.username


class Searcher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE,
                                related_name='searcher')
    domain = models.CharField(verbose_name=_("domain"), max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}' if self.user.last_name and self.user.first_name else self.user.username


class Author(models.Model):
    last_name = models.CharField(_("last_name"), max_length=255)
    first_name = models.CharField(_("first_name"), max_length=255)

    # extre_fields
    is_student = models.BooleanField(_("is student"), default=False)
    is_personal_academic = models.BooleanField(_("is personal academic"), default=False)
    is_searcher = models.BooleanField(_("is searcher"), default=False)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def get_full_name(self):
        return f'{self.last_name.capitalize()} {self.first_name.capitalize()}'



class Document(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=255, blank=True, null=True)
    date_publication = models.DateField(_("date publication"), blank=True, null=True, auto_now_add=True)
    description = models.TextField(_("description"), blank=True, null=True)
    resume = models.TextField(verbose_name=_("resume"), blank=True, null=True)
    prouve = models.BooleanField(_("prouve"), default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    @property
    def document_type(self):
        return self.__class__.__name__


class Thesis(Document):
    image = models.ImageField(_("image"), upload_to='image_thesis', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, verbose_name=_("author"), on_delete=models.CASCADE,
                               related_name='thesis', blank=True)
    file = models.FileField(_("file"), upload_to='file_thesis/', blank=True, null=True)

    class Meta:
        ordering = ['-date_publication']

    def __str__(self):
        return f'Thèse-{self.title}'


class Memory(Document):
    image = models.ImageField(_("image"), upload_to='image_memories', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, verbose_name=_("author"), on_delete=models.CASCADE,
                               related_name='memory', blank=True)
    file = models.FileField(_("file"), upload_to='file_memories/', blank=True, null=True)

    class Meta:
        ordering = ['-date_publication']

    def __str__(self):
        return f'Mémoire-{self.title}'


class Commentaire(models.Model):
    contenu = models.TextField(_("contenu"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE,
                             related_name='commentaires')
    date_commentaire = models.DateTimeField(_("date_commentaire"), auto_now_add=True)

    # Champs pour les relations génériques
    content_type = models.ForeignKey(ContentType, verbose_name=_("content type"), on_delete=models.CASCADE, related_name="comments")
    object_id = models.PositiveIntegerField(_("object_id"))
    document = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-date_commentaire']

    def __str__(self):
        return f'Le commentaire de {self.user.username} vers {self.date_commentaire} sur {self.document}'
