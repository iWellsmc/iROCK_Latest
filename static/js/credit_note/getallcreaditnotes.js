// insert table values using ajax
 
$('#master_project_list').DataTable({
    serverSide: true,
    ajax: {
        url: "/credit/getallcreaditnote",                    
        type: 'GET',
    },
    language: {
      emptyTable: "---"
    },
    "rowCallback": function(row, data) {
      $(row).attr('data-id', data.id);
    },
    columns: [
        { data: "s_no" },
        {
            data: null,
           render: function (data, type, row) {
            actions_html=''
               $(data.credit_num).each(function(ind,val){
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
               $(data.ref_num).each(function(ind,val){
               actions_html+='<div>'+val+'</div>'
               })
           return actions_html  
           }
        },
        {
            data: null,
           render: function (data, type, row) {
            actions_html=''
               $(data.approval_status).each(function(ind,val){
               actions_html+='<div>'+val+'</div>'
               })
           return actions_html  
           }
        },
        {
            data: null,
           render: function (data, type, row) {
            actions_html=''
               $(data.approval_date).each(function(ind,val){
               actions_html+='<div>'+val+'</div>'
               })
           return actions_html  
           }
        },
        { data: "status" },
        {
            data: null,
           render: function (data, type, row) {
            actions_html=''
             actions_html='<a class="btn px-1" href="/credit/view/'+data.id+'"><i class="fa fa-eye" title="View"></i></a>'
             
             if(data.vendorid_active_status == 1){
                 if(data.vendor_status == true){
                     if(data.credit_credit_status == 1){
                        actions_html='<a class="btn px-1" href="/credit/view/'+data.id+'"><i class="fa fa-eye" title="View"></i></a> <a class="btn px-1" href="/credit/edit/'+data.id+'"><i class="fa fa-edit"></i></a>'
                     }
                 }

                 
                     if(data.history == 2 ||data.history == "2"  ){
                        actions_html='<a class="btn px-1" href="/credit/view/'+data.id+'"><i class="fa fa-eye" title="View"></i></a> <a href="/credit/creditqueryhistory/'+data.id+'" class="btn his-oty px-1"><i class="fa fa-history" title="History" aria-hidden="true"></i></a>'
                     }
                

             }
           return actions_html  
           }
          },
    ]

})

