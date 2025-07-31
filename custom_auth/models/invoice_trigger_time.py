from django.db import  models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class InvoiceTimeTriggerManager(models.Manager):
    def getinvoice_time_trigger_by_paymentday(self,payment_day,company_id):
        try:
            return self.get(Q(payment_terms_from__lte=payment_day) & Q(payment_terms_to__gte=payment_day) & Q(company_id=company_id) & Q(status=1))
        except ObjectDoesNotExist:
            return ""


class InvoiceTimeTrigger(models.Model):
    CHOICE = (
        (2, 'Minutes'),
        (0, 'Hours'),
        (1, 'Days')
    )
    payment_terms_from = models.IntegerField(null=True,blank=True)
    payment_terms_to = models.IntegerField(null=True,blank=True)
    time_unit = models.SmallIntegerField(choices=CHOICE,null=True, blank=True)
    time_allotted = models.IntegerField(null=True, blank=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True,default=1)
    objects=InvoiceTimeTriggerManager()

    # def __str__(self):
    #     return self.payment_terms_from