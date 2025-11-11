import datetime
import random

rand_list = [random.randint(0, 100) for i in range(0, 10)]

list_comprehension_below_10 = [i for i in range(0, 10)]

# list_comprehension_below_10 =


# # send_notification_to_overdued_loans task’ını düşün:
# # Bazı durumlarda mail gönderimi başarısız olabilir (örneğin SMTP hatası).
# #
# # Görevin:
# #
# # Task hata alırsa otomatik yeniden denemesi (retry) sağlanmalı.
# #
# # Aynı kullanıcıya aynı gün içinde birden fazla mail gitmemeli (idempotency).
# #
# # Retry denemeleri loglanmalı (örnek: print veya logger).
#
# from celery import shared_task
#
# from library.models import Loan, MailIsSendAction
#
# from django.utils.timezone import now
# from django.core.mail import send_mail
# from django.conf import settings
# from django.db.models import Q
#
#
# @shared_task(bind=True, max_retries =3, default_retry_delay=60)
# def send_notification_to_overdued_loans(self):
#     loans = Loan.objects.filter(
#         is_returned=False,
#         return_date__lte=now().date()
#     ).filter(
#         Q(mail_is_send_today__isnull=True) | Q(mail_is_send_today__state=False)
#     ).distinct()
#
#     for loan in loans.iterator(chunk_size=25):
#         ia = MailIsSendAction.objects.create(loan=loan)
#
#         try:
#             over_days = (loan.return_date - now()).days
#
#             is_send = send_mail(
#                 subject=f"{loan.book.title}",
#                 message=f"{over_days} this hasn't returnde yet.",
#                 from_mail=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[loan.member.user.email],
#                 fail_silently=False,
#             )
#             if not is_send:
#                 self.retry()
#
#             else:
#                 ia.state = True
#                 ia.save()
#
#         except:
#             self.retry()
