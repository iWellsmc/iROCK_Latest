from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'credit'
 
urlpatterns = [
    path('create',views.create_credit_note, name='create_credit_note'), 
    path('getcontractinvoices',views.get_contract_invoices, name='getcontractinvoices'),
    path('checkcreditno',views.checkcreditno, name='checkcreditno'),
    path('filepreview/<int:pk>',views.credit_file_preview, name='credit_file_preview'),
    path('getsupportfiles',views.get_supportfiles, name='getsupportfiles'),
    path('getinvoicefiles',views.get_invoice_files, name='getinvoicefiles'),
    path('list',views.credit_note_list, name='credit_note_list'),
    path('view/<int:pk>',views.credit_view, name='credit_view'),
    path('edit/<int:pk>',views.edit_credit_note, name='edit_credit_note'),
    path('totalcost',views.totalcost,name='totalcost'),
    path('creditnotepdf/<int:pk>',views.CreditNotePDFView.as_view(), name='creditnotepdf'),    
    path('checklist/<int:pk>',views.CreditNoteChecklist.as_view(), name='creditnotechecklist'),
    path('getsupportfilescredit/',views.getSupportFilesCredit,name='getsupportfilescredit'),
    path('creditapprovallist/<int:pk>',views.CreditApprovalProcess.as_view(),name="crditapprovallist"),
    path('approvedcreditnotes',views.ViewApprovedCreditNotes.as_view(),name="approvedcreditnotes"),
    path('unapprovedcreditnotes',views.ViewUnApprovedCreditNotes.as_view(),name="unapprovedcreditnotes"),
    path('rejectedcreditnotes',views.ViewReturnedRejectedCreditNotes.as_view(),name="rejectedcreditnotes"),
    path('creditapprovaltrack/<int:pk>',views.CreditApprovalTrack.as_view(),name="creditapprovaltrack"),
    path('getcreditnotes',views.getcreditnotes,name="getcreditnotes"),
    path('creditqueryhistory/<int:pk>',views.DisputedCreditQueryHistory.as_view(),name='creditqueryhistory'),
    path('closecreditquery/<int:pk>',views.CloseCreditQuery,name='closecreditquery'),
    path('getallcreaditnote' ,views.get_creadit_note_details , name="getallcreaditnote"),
    ]