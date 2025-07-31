from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ContractMaster,Amendment,ContractMasterVendor
from custom_auth.models import User
from notifications.signals import notify
from custom_auth.models import User
from datetime import datetime
@receiver(pre_save, sender=ContractMaster)
def reference_number_changed(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # print(f"Reference number created: {instance.reference_number}")
        return
    if old_instance.reference_number != instance.reference_number:
        if instance.updated_by:
            vendorcontract=ContractMasterVendor.objects.get(id=old_instance.contractvendor.id)
            get_userby_vin = User.objects.filter(cin_number=vendorcontract.vin)
            sender = User.objects.get(id=instance.updated_by.id)
            url = f'/projects/contractlist'
            notify.send(sender, recipient=get_userby_vin,data=url, verb='Contract Reference No Updated', description=f'Reference No Updated from {old_instance.reference_number} to {instance.reference_number} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
    else:
        if instance.updated_by:
            project_id = int(instance.projects_id) if instance.projects_id != '' else None
            project_id_old = int(old_instance.projects_id) if old_instance.projects_id != None else None
            project_descipline_id = int(instance.projectdiscipline_id) if instance.projectdiscipline_id != '' else None
            project_descipline_id_old = int(old_instance.projectdiscipline_id) if old_instance.projectdiscipline_id != None else None
            project_descipline_type_id = int(instance.projectdisciplinetype_id) if instance.projectdisciplinetype_id != '' else None
            project_descipline_type_id_old = int(old_instance.projectdisciplinetype_id) if old_instance.projectdisciplinetype_id != None else None
            executed_date = datetime.strptime(instance.executed_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date() if instance.executed_date is not None else None
            executed_date_old = datetime.strptime(old_instance.executed_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date() if old_instance.executed_date is not None else None
            currency_id = int(instance.currency_id) if instance.currency_id != '' else None
            currency_id_old = int(old_instance.currency_id) if old_instance.currency_id != None else None
            amount = instance.amount if instance.amount != '' else None
            amount_old = old_instance.amount if old_instance.amount != '' else None
            upload_contract = instance.upload_contract if instance.upload_contract != '' else None
            upload_contract_old = old_instance.upload_contract if old_instance.upload_contract != '' else None
            upload_pricetable = instance.upload_pricetable if instance.upload_pricetable != '' else None
            upload_pricetable_old = old_instance.upload_pricetable if old_instance.upload_pricetable != '' else None
            name_service = instance.name_service if instance.name_service != '' else None
            name_service_old = old_instance.name_service if old_instance.name_service != '' else None
            vendorcontract=ContractMasterVendor.objects.get(id=old_instance.contractvendor.id)
            get_userby_vin = User.objects.filter(cin_number=vendorcontract.vin)
            sender = User.objects.get(id=instance.updated_by.id)
            url = f'/projects/contractlist'
            if project_id_old != project_id:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Contract Project Name Updated', description=f'Project Name Updated from {old_instance.projects} to {instance.projects} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif project_descipline_id_old != project_descipline_id:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Contract Project Discipline Updated', description=f'Project Discipline Updated by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif project_descipline_type_id_old != project_descipline_type_id:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Contract Project Discipline Type Updated', description=f'Project Discipline Type Updated by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif executed_date_old != executed_date:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Contract Executed Date Updated', description=f'Executed Date Updated from {executed_date_old if executed_date_old != None else ""} to {executed_date if executed_date != None else ""} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif currency_id_old != currency_id:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Contract Currency Updated', description=f'Currency Updated by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif amount_old != amount:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Contract Amount Updated', description=f'Amount Updated from {old_instance.amount} to {instance.amount} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif upload_contract_old != upload_contract:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Contract File Updated', description=f'Contract File Updated from {old_instance.upload_contract} to {instance.upload_contract} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif upload_pricetable_old != upload_pricetable:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Pricetable File Updated', description=f'Pricetable File Updated from {old_instance.upload_pricetable} to {instance.upload_pricetable} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif name_service_old != name_service:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Contract Service Name Updated', description=f'Service Name Updated from {old_instance.name_service} to {instance.name_service} by {sender.name} {sender.lastname if sender.lastname != None else ""}')

@receiver(pre_save, sender=Amendment)
def Amendmentreference_number_changed(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    if old_instance.amendment_reference_number != instance.amendment_reference_number:
        if instance.updated_by:
            url = f'/projects/contractlist'
            vendorcontract=ContractMasterVendor.objects.get(id=old_instance.contractvendor.id)
            get_userby_vin = User.objects.filter(cin_number=vendorcontract.vin)
            sender = User.objects.get(id=instance.updated_by.id)
            notify.send(sender, recipient=get_userby_vin,data=url, verb='Amendment Reference No Updated', description=f'Reference No Updated from {old_instance.amendment_reference_number} to {instance.amendment_reference_number}by {sender.name} {sender.lastname if sender.lastname != None else ""}')
    else:
        if instance.updated_by:
            amendment_type = instance.amendment_type if instance.amendment_type != '' else None
            amendment_type_old = old_instance.amendment_type if old_instance.amendment_type != '' else None
            amendment_reference_number = instance.amendment_reference_number if instance.amendment_reference_number != '' else None
            amendment_reference_number_old = old_instance.amendment_reference_number if old_instance.amendment_reference_number != '' else None
            amendment_executed_date = datetime.strptime(instance.amendment_executed_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date() if instance.amendment_executed_date is not None else None
            amendment_executed_date_old = datetime.strptime(old_instance.amendment_executed_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date() if old_instance.amendment_executed_date is not None else None
            amendment_currency_id = int(instance.amendment_currency_id) if instance.amendment_currency_id != '' else None
            amendment_currency_id_old = int(old_instance.amendment_currency_id) if old_instance.amendment_currency_id != None else None
            amendment_amount = instance.amendment_amount if instance.amendment_amount != '' else None
            amendment_amount_old = old_instance.amendment_amount if old_instance.amendment_amount != '' else None
            amendment_upload_contract = instance.amendment_upload_contract if instance.amendment_upload_contract != '' else None
            amendment_upload_contract_old = old_instance.amendment_upload_contract if old_instance.amendment_upload_contract != '' else None
            amendment_upload_price_table = instance.amendment_upload_pricetable if instance.amendment_upload_pricetable != '' else None
            amendment_upload_price_table_old = old_instance.amendment_upload_pricetable if old_instance.amendment_upload_pricetable != '' else None
            url = f'/projects/contractlist'
            vendorcontract=ContractMasterVendor.objects.get(id=old_instance.contractvendor.id)
            get_userby_vin = User.objects.filter(cin_number=vendorcontract.vin)
            sender = User.objects.get(id=instance.updated_by.id)
            if amendment_type_old != amendment_type:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Amendment/Addendum Type Updated', description=f'Amendment/Addendum Type Updated from {old_instance.amendment_type} to {instance.amendment_type} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif amendment_reference_number_old != amendment_reference_number:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Amendment/Addendum Reference No Updated', description=f'Amendment/Addendum Reference No Updated from {old_instance.amendment_reference_number} to {instance.amendment_reference_number} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif amendment_executed_date_old != amendment_executed_date:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Amendment/Addendum Executed date Updated', description=f'Amendment/Addendum Executed date Updated from {amendment_executed_date_old} to {amendment_executed_date} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif amendment_currency_id_old != amendment_currency_id:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Amendment/Addendum Currency Updated', description=f'Amendment/Addendum Currency Updated by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif amendment_amount_old != amendment_amount:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Amendment/Addendum Amount Updated', description=f'Amendment/Addendum Amount Updated from {old_instance.amendment_amount} to {instance.amendment_amount} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif amendment_upload_contract_old != amendment_upload_contract:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Amendment/Addendum Contract File Updated', description=f'Amendment/Addendum Contract File Updated from {old_instance.amendment_upload_contract} to {instance.amendment_upload_contract} by {sender.name} {sender.lastname if sender.lastname != None else ""}')
            elif amendment_upload_price_table_old != amendment_upload_price_table:
                return notify.send(sender, recipient=get_userby_vin,data=url, verb='Amendment/Addendum Price Table File Updated', description=f'Amendment/Addendum Price Table File Updated from {old_instance.amendment_upload_pricetable} to {instance.amendment_upload_pricetable} by {sender.name} {sender.lastname if sender.lastname != None else ""}')