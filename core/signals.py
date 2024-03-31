# from time import sleep
# from django.db.models.signals import post_save, m2m_changed
# from django.dispatch import receiver
# from django.core.exceptions import ValidationError
# from .models import Estudante
# from django.db.transaction import on_commit
# import logging

# log = logging.getLogger(__name__)


# @receiver(post_save, sender=Estudante)
# def validar_integrante_escola(sender, instance, **kwargs):
#     escola_do_estudante = instance.escola
#     integrantes = instance.integrante.all()
#     log.info(integrantes)
#     if integrantes is not None:
#         for integrante in integrantes:
#             if escola_do_estudante in integrante.escola.all():
#                 break
#             else:
#                 on_commit(lambda: instance.integrante.remove(integrante))
#     else:
#         pass

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.transaction import on_commit
import logging
from .models import Estudante

log = logging.getLogger(__name__)


@receiver(m2m_changed, sender=Estudante.integrante.through)
def validar_integrante_escola(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action == "post_add":
        escola_do_estudante = instance.escola
        for integrante_pk in pk_set:
            integrante = model.objects.get(pk=integrante_pk)
            if escola_do_estudante not in integrante.escola.all():
                on_commit(lambda: instance.integrante.remove(integrante))
                log.info(
                    f"O integrante {integrante} não atua na escola do estudante {instance}."
                )
