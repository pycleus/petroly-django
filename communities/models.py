from typing import Text
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from django_choices_field import TextChoicesField


class CloudinaryFieldCostom(CloudinaryField):
    """
    This is needed to modify to_python, to deal with the FileInput from `graphene`.
    """

    def to_python(self, value):
        if isinstance(value, dict):
            # ignore it
            pass
        else:
            return super().to_python(value)


class Community(models.Model):
    class Meta:
        verbose_name = _("community")
        verbose_name_plural = _("Communities")

    class CategoryEnum(models.TextChoices):
        EDU = "edu", _("Educational")
        SEC = "section", _("Section")
        ENT = "entertaining", _("Entertaining")

    class PlatformEnum(models.TextChoices):
        WHAT = "whatsapp", _("Whatsapp")
        DISC = "discord", _("Discord")
        TELE = "telegram", _("Telegram")

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(
        _("Description"), max_length=500, default="", blank=True
    )
    link = models.URLField(_("Link"), unique=True)
    date = models.DateField(_("Date"), auto_now_add=True)
    category = TextChoicesField(choices_enum=CategoryEnum, default="")
    platform = TextChoicesField(choices_enum=PlatformEnum, default="")
    section = models.CharField(_("Section"), max_length=10, default="", blank=True)
    verified = models.BooleanField(_("Verified"), default=True)
    archived = models.BooleanField(_("Archived"), default=False)
    icon = CloudinaryFieldCostom(
        _("icon"), default=None, null=True, blank=True, max_length=350
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("likes"),
        related_name="liked_communities",
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="owned_communities",
        verbose_name=_("owner"),
        null=True,
    )

    def __str__(self):
        return f"{self.name}"


class Report(models.Model):
    reasons = (
        ("content", _("inappropriate content")),
        ("link", _("invalid link")),
        ("other", _("other")),
    )
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateField(_("Created on"), auto_now_add=True)
    reason = models.CharField(_("Reason"), max_length=8, choices=reasons)
    other_reason = models.CharField(
        _("Other_reason"), max_length=100, default="", blank=True
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name=_("community"),
    )


@receiver(post_save, sender=Report)
def archive_community(sender, instance, created, **kwargs):
    """To archieve a community if it has many reports"""
    if created and instance.community.reports.count() >= 3:
        instance.community.archived = True
        instance.community.save()
