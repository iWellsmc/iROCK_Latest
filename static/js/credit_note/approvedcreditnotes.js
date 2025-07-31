$(document).on('click','.null_data',function(e){
  e.preventDefault();
  swal.fire('Approve Invoice')
})


$('#master_project_lists').DataTable({
  serverSide: true,
  ajax: {
      url: "/credit/getcreditnotes",                    
      type: 'GET',
      data:{
          'Creditnote_type':Creditnote_type,
      }
  },
  language: {
    emptyTable: "---"
  },
  columns: [
  { data: 's_no' },
  {
      data: null,
      render: function (data, type, row) {
        actions_html=''
        $(data.Credit_no).each(function(ind,val){
          actions_html+='<div>'+val+'</div>'
        })
        return actions_html  
      }
    },
  {
      data: null,
      render: function (data, type, row) {
        actions_html=''
        $(data.date).each(function(ind,val){
          actions_html+='<div>'+val+'</div>'
        })
        return actions_html  
      }
  },
  {
      data: null,
      render: function (data, type, row) {
        actions_html=''
        $(data.Credit_no).each(function(ind,val){
          actions_html+='<div>'+data.invoice_number+'</div>'
        })
        return actions_html  
      }
  },
  {
  data: null,
  render: function (data, type, row) {
      actions_html=''
      $(data.Credit_no).each(function(ind,val){
      actions_html+='<div>'+data.appr_status+'</div>'
      })
      return actions_html  
  }
  },
  {
      data: null,
      render: function (data, type, row) {
          actions_html=''
          $(data.Credit_no).each(function(ind,val){
          actions_html+='<div>'+data.apprv_date+'</div>'
          })
          return actions_html  
      }
  },
  { 
    
    data: null,
      render: function (data, type, row) {
          actions_html=''
          actions_html+='<a class="text-decoration-none" href="/credit/view/'+data.credit_id+'"><span class="action-view align-icons"><i class="fa fa-eye" title="View"></i></span></a>'
          if(data.checkpermission_creditnote_ir > 0){
              if(data.check_for_invreceipt == 0){
                  actions_html+='<a class="btn px-1 null_data" ><i class="fa-solid fa-list-check" title="Credit Note Receipt"></i></a>'
              }
              else{
                  actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/credit/checklist/'+data.credit_id+'" data_id="'+data.credit_id+'"><span class=" align-icons"><i class="fa-solid fa-list-check" title=" Credit Note Receipt"></i></span></a>'
              }
          }
          if(data.checkpermission_creditnote_ia > 0){
              if(data.check_for_invapproval == 0){
                  actions_html+='<a class="btn px-1 null_data"><i class="fa-solid fa-file-invoice" title="Credit Note Approval"></i></a>'
              }
              else{
                  actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/credit/creditapprovallist/'+data.credit_id+'" data_id="'+data.credit_id+'"><span class=" align-icons"><i class="fa-solid fa-file-invoice" title=" Credit Note Approval"></i></span></a>'
              }
          }
            if(data.returned_query > 0){
                  actions_html+='<a class="btn his-oty px-1" href="/credit/creditqueryhistory/'+data.credit_id+'" data_id="'+data.credit_id+'"><span class=" align-icons"><i class="fa fa-history" title="History"></i></span></a>'
            }else if(data.history == 2 ||data.history == "2"  ){
              actions_html='<a class="btn px-1" href="/credit/view/'+data.credit_id+'"><i class="fa fa-eye" title="View"></i></a> <a href="/credit/creditqueryhistory/'+data.credit_id+'" class="btn his-oty px-1"><i class="fa fa-history" title="History" aria-hidden="true"></i></a>'
           }
          return actions_html  
      }
  }
]
});

// $('#master_project_list').DataTable().ajax.reload();

// var table = $('#master_project_list').DataTable();
// table.destroy();