from ..models import UserDepartment,UserGroup,InvoiceTimeTrigger,WccTimeTrigger
from InvoiceGuard.models import Right
def user_data(company):
        # Predifined User Groups
        group_data=[UserGroup(group=i,company=company) for i in ['Middle Level Management (Senior)', 'Middle Level Management (Junior)', 'Front Line Management']]
        UserGroup.objects.bulk_create(group_data)

        # Predifined User Departments
        department_data=[UserDepartment(department=i,company=company) for i in ['Management', 'Finance', 'Treasury', 'Drilling and Completions', 'Human Resources and Administration', 'Subsurface and Reservoir Engineering', 'Contracts and Procurement', 'Facilities and Projects', 'Production and Operations', 'Geology', 'Legal', 'ICT', 'QHSE & Community Development', 'Business Development & Sales and Development', 'Insurance', 'External Auditors', 'External Personnel/Consultant', 'Internal Auditors', 'Others(Bank Personnel)']]
        UserDepartment.objects.bulk_create(department_data)

        # Predifined Rights
        rights_and_slug={'invoice-notification':'Initial Invoice Receipt Notifications','invoice-view': 'View/Comment On Invoice','invoice-proceed': 'Proceed Invoice','invoice-approve': 'Approve Invoice','invoice-return': 'Return Invoice','invoice-reject': 'Reject Invoice', 'invoice-override':'Override Invoice Approval','tax-confirmation': 'Tax Confirmation','generate-payment': 'Generate Payment Instructions', 'approve-payment':'Approve Payment Instructions','received-approval': 'Receive Approved Instructions','manage-invoice': 'Manage Invoice Payment','communicate-with-vendor': 'Communicate with Vendor','communicate-with-officer': 'Communicate with Account Officer','confirm-cost-code': 'Confirm Cost Code', 'wcc-view':'View/Comment on WCC','wcc-approve': 'Approve WCC','wcc-return': 'Return WCC','wcc-reject':'Reject WCC','wcc-override':'Override WCC Approval'}
        right_data=[Right(right_name=j,company=company,slug=i) for i,j in rights_and_slug.items()]
        Right.objects.bulk_create(right_data)

        inv_time_data=[(0, 0, 0, 1, 1),(1, 10, 1, 1, 1),(11, 20, 1, 1, 1),(21, 45, 1, 1, 1),(46, 65, 1, 1, 1),(66, 90, 1, 1, 1),(91, 120, 1, 1, 1),(121, 180, 1, 1, 1)]
        invoice_time_trigger=[InvoiceTimeTrigger(payment_terms_from=i[0],payment_terms_to=i[1],time_unit=i[2],time_allotted=i[3],status=i[4],company=company) for i in inv_time_data]
        InvoiceTimeTrigger.objects.bulk_create(invoice_time_trigger)

        wcc_time_data=[(1, 3, 1, 1, 1)]
        wcc_time_trigger=[WccTimeTrigger(payment_terms_from=i[0],payment_terms_to=i[1],time_unit=i[2],time_allotted=i[3],status=i[4],company=company) for i in wcc_time_data]
        WccTimeTrigger.objects.bulk_create(wcc_time_trigger)
        return True
 