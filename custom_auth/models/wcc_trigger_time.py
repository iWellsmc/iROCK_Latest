from django.db import  models

class WccApprovalManager(models.Manager):
    def getwcctime_trigger_bycompany(self,company_id):
        return self.get(company=company_id)


class WccTimeTrigger(models.Model):
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
