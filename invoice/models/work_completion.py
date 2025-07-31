from django.db import models 

class workcompletionvaluesManager(models.Manager):
    def getworkcompletion(self,pk):
        return self.filter(invoice_id=pk,status=1)
 

class workcompletionvalues(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    workcompletion=models.CharField(max_length=255,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    objects=workcompletionvaluesManager()