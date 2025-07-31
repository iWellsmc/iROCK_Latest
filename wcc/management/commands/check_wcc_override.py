from django.core.management.base import BaseCommand
from wcc.models import WorkCompletionCost,WorkCompletionValue,WccApproval,WccPerStation,WccStationUsers
from datetime import datetime,timedelta
from custom_auth.models import WccTimeTrigger
from django.utils import timezone
from InvoiceGuard.models import RoleRight
from notifications.signals import notify 
from custom_auth.models import User


class Command(BaseCommand):
    help = 'check wcc autoremainder'

    def handle(self, *args, **kwargs):
        self.checkoverride_wcc()
    

    def checkoverride_wcc(self):
        current_timestamp = datetime.now().timestamp()
        current_datetime = timezone.now()

        pending_wcc = list(WorkCompletionCost.objects.get_wcc_approval_check(
        1,0).values_list('id', flat=True))
        for wcc in pending_wcc:

            wcc_detail=WorkCompletionCost.objects.get_by_id(wcc)
            wcc_work_value=WorkCompletionValue.objects.get_by_wcc(wcc_detail.id)    
            wcc_approval_flow=WccApproval.objects.filter_by_wcc(wcc_detail.id).last()

            last_notification=wcc_detail.last_notification
            wcctime_trigger=WccTimeTrigger.objects.getwcctime_trigger_bycompany(wcc_detail.company_id)
            if last_notification:
                time_difference = current_timestamp - last_notification 

            if wcctime_trigger.time_unit == 2:
                sequence_type='minutes'
            elif wcctime_trigger.time_unit == 0:
                sequence_type='hours'
            else:
                sequence_type='days'

            notification_interval = timedelta(**{sequence_type: wcctime_trigger.time_allotted})
            notification_interval_seconds = notification_interval.total_seconds()
            if not last_notification:
                time_difference = notification_interval_seconds
    
            if not last_notification or time_difference >= notification_interval_seconds:
                sender = User.objects.getclientadmin_by_companyid(wcc_detail.company_id)

                if current_datetime > wcc_approval_flow.notification_at:
                    wcc_per_station_data=WccPerStation.objects.filter(project_id=wcc_detail.project.id,status=1,wcc_flow_level_id=wcc_approval_flow.wcc_per_station.wcc_flow_level.id)
                    for station_data in wcc_per_station_data:
                        check_right=RoleRight.objects.filter(role_id=station_data.role_id,right__slug="wcc-override",status=1).first()
                        if (check_right):
                            get_override_users=WccStationUsers.objects.filter(wcc_per_station_id=station_data.id,status=1)
                            for over_ride_user in get_override_users:
                                if (WccApproval.objects.filter(wcc_id=id,wcc_per_station_id=wcc_approval_flow.wcc_per_station.id,user_id=over_ride_user.user.id).exists()):
                                    print('sa',over_ride_user.user)
                                else:
                                    print('no',over_ride_user.user)
                                    #create override user
                                    WccApproval.objects.create_override_user(wcc_detail.id,over_ride_user.wcc_flow.id,over_ride_user.user.id,wcc_approval_flow.wcc_per_station.id,calculate_time)
                                sender = get_company_user
                                recipient=over_ride_user.user
                                url="https://irockinfo.mo.vc/wcc/approvalwcclist"
                                notify.send(sender, recipient=recipient,data=url, verb='Indication Mail', description=f'Wcc {wcc_work_value.wcc_number} Still Pending')
                    WorkCompletionCost.objects.updatelast_notification(wcc_detail.id,current_timestamp)



     
   




















        





    
