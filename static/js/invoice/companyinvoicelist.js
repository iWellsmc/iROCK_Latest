// var table = $('#comp_ven_invoice').DataTable({ 
//     // "dom": '<"row"<"col-sm-4"l><"col-sm-4 text-center"p><"col-sm-4"f>>tip',
//     // order: [[5, 'desc']],
//     ordering: false,
//     language: {
//         search: "",
//         searchPlaceholder:"search",
//       }
// },  

// );
$(document).ready(function(){
    $(".top-profile").click(function(){
      $(".creat-link-page").toggle();
    });
  });  


  
$(document).ready(function() {
    $('#loader').show();
    // Initialize DataTable
    var dataTable = $('#comp_ven_invoice').DataTable({
    serverSide: true,
    ajax: {
        url: "/invoice/getunpaidinvoices",                    
        type: 'GET',
        data: function(d) {
            // Add filter parameters to the AJAX request
            d.payment_type = payment_type; // Assuming payment_type is defined somewhere in your JavaScript
            d.vendorname = $('#vendorname').val(); // Assuming you have a dropdown for vendor name
            d.servicetype = $('#servicetype').val(); // Assuming you have a dropdown for service type
        }
    },
    language: {
      emptyTable: "---"
    },
    "rowCallback": function(row, data) {
        $(row).attr('data-id', data.id);
    },
    columns: [
    { data: 's_no' },
    { data: 'vin' },
    { data: 'vendor_name' },
    { data: 'service_name' },
    {
     data: null,
       render: function (data, type, row) {
         actions_html=''
         paid_count=0
         $(data.instruction_number).each(function(ind,val){
            actions_html+='<div class="get_paid_invcost" style="display: none;">'+val["cost_number"]+'<input type="hidden" id="inv_cost_id" value="'+val["cost_id"]+'"></div>'
            paid_count++
          })
         $(data.inv_number).each(function(ind,val){
          actions_html+='<div>'+val+'</div>'
        })
        actions_html+="<input type='hidden' class='input_tag' value='{\"id\":" + data.id + ", \"len\":" + paid_count + ", \"file\":[]}' >"
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
           $(data.approval_status).each(function(ind,val){
           actions_html+='<div>'+val+'</div>'
           })
       return actions_html  
       }
    },
    // {
    //     data: null,
    //    render: function (data, type, row) {
    //     actions_html=''
    //        $(data.payment_status).each(function(ind,val){
    //        actions_html+='<div>'+val+'</div>'
    //        })
    //    return actions_html  
    //    }
    // },
  { data: null,
         render: function (data, type, row) {
            actions_html=''
            actions_html+='<a class="btn px-1" href="/invoice/invoiceview/'+data.id+'"><i class="fa fa-eye" title="View"></i></a>'  
            if (payment_type == 1){
            // actions_html+='<a class="btn px-1" href="/invoice/getinvoicesplit/'+data.id+'"><button type="button" class="btn btn-clr">View Invoice</button></a>'
            }
            
                    if (data.invoiceapproval_dispute > 0){
                        actions_html+='<a class="btn his-oty px-1" href="/invoice/invoicequeryhistory/'+data.id+'"><i class="fa fa-history" title="History" aria-hidden="true"></i></a>'
                    }
                    if(payment_type != 3){
                            if(payment_type != 3){
                                $(data.checkpermission_bank).each(function(ind,val){
                                    actions_html+='<a class="btn px-1 check_sign all-icon-same-clr" href="/invoice/bankuserview/'+data.id+'/'+val+'" data_id="'+data.id+'"><button type="button" class="btn btn-clr invoice-pay-btn">Invoice for Payment</button></a>'
                                })
                            if (data.checkpermission_bank > 0){
                                actions_html+='<a class="btn px-1 check_sign all-icon-same-clr" href="/invoice/bankuserview/'+data.id+'" data_id="'+data.id+'"><button type="button" class="btn btn-clr invoice-pay-btn">Invoice for Payment</button></a>'
                            }
                            }
                            if (data.module1_override > 0){
                                actions_html+='<a class="btn px-1 inv_app_cls assign-user all-icon-same-clr" href="/invoice/invoiceoverrideusers/'+data.id+'" data_id="'+data.id+'"><img src="/static/images/over-ride-user.png" title="Override Users"></a>'
                            }
                            else{
                                if (data.inv_receipt > 0){
                                    actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/checklist/'+data.id+'" data_id="'+data.id+'"><i class="fa-solid fa-list-check" title="Invoice Receipt"></i></a>'
                                }
                            }
                            if (data.module2_override > 0){
                                actions_html+='<a class="btn px-1 inv_app_cls assign-user all-icon-same-clr" href="/invoice/invoiceoverrideusers/'+data.id+'" data_id="'+data.id+'"><img src="/static/images/over-ride-user.png" title="Override Users"></a>'
                            }
                            else{
                                if (data.inv_approval > 0){
                                    actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/invoiceapproval/'+data.id+'" data_id="'+data.id+'"><i class="fa-solid fa-file-invoice" title="Invoice Approval"></i></a>'
                                }
                            }
                            if(payment_type != 3){
                            if (data.module3_override > 0){
                                actions_html+='<a class="btn px-1 inv_app_cls assign-user all-icon-same-clr" href="/invoice/invoiceoverrideusers/'+data.id+'" data_id="'+data.id+'"><img src="/static/images/over-ride-user.png" title="Override Users"></a>'
                            }
                            else{
                                if (data.tax_confirm > 0){
                                    actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/exchangerate/'+data.id+'" data_id="'+data.id+'"><i class="fa-brands fa-stack-exchange" title="Tax Confirmation"></i></a>'
                                }
                            }
                            if (data.module4_override > 0){
                                actions_html+='<a class="btn px-1 inv_app_cls assign-user all-icon-same-clr" href="/invoice/invoiceoverrideusers/'+data.id+'" data_id="'+data.id+'"><img src="/static/images/over-ride-user.png" title="Override Users"></a>'
                            }
                            else{
                                if (data.payment_gn > 0){
                                    actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/generatepayment/'+data.id+'" data_id="'+data.id+'"><i class="fa-brands fa-creative-commons-share" title="Payment Generation"></i></a>'
                                }
                            }
                            if (data.module5_override > 0){
                                actions_html+='<a class="btn px-1 inv_app_cls assign-user all-icon-same-clr" href="/invoice/invoiceoverrideusers/'+data.id+'" data_id="'+data.id+'"><img src="/static/images/over-ride-user.png" title="Override Users"></a>'
                            }
                            else{
                                $(data.payment_apl).each(function(ind,val){
                                    actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/signatory/'+data.id+'/'+val+'" data_id="'+data.id+'"><i class="fa-solid fa-file-signature" title="Payment Approval"></i></a>'
                                })
                        
                            }
                            if (data.module6_override > 0){
                                actions_html+='<a class="btn px-1 inv_app_cls assign-user all-icon-same-clr" href="/invoice/invoiceoverrideusers/'+data.id+'" data_id="'+data.id+'"><img src="/static/images/over-ride-user.png" title="Override Users"></a>'
                            }
                            else{
                                $(data.payment_cfn).each(function(ind,val){
                                    actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/accountpayable/'+data.id+'/'+val+'" data_id="'+data.id+'" title="Payment Confirmation"><svg xmlns="http://www.w3.org/2000/svg" width="1.4em" height="1.4em" style="margin-top: -6px;" viewBox="0 0 384 512"><path fill="#95183a" d="M64 0C28.7 0 0 28.7 0 64v384c0 35.3 28.7 64 64 64h256c35.3 0 64-28.7 64-64V160H256c-17.7 0-32-14.3-32-32V0H64zm192 0v128h128L256 0zM64 80c0-8.8 7.2-16 16-16h64c8.8 0 16 7.2 16 16s-7.2 16-16 16H80c-8.8 0-16-7.2-16-16zm0 64c0-8.8 7.2-16 16-16h64c8.8 0 16 7.2 16 16s-7.2 16-16 16H80c-8.8 0-16-7.2-16-16zm128 72c8.8 0 16 7.2 16 16v17.3c8.5 1.2 16.7 3.1 24.1 5.1c8.5 2.3 13.6 11 11.3 19.6s-11 13.6-19.6 11.3c-11.1-3-22-5.2-32.1-5.3c-8.4-.1-17.4 1.8-23.6 5.5c-5.7 3.4-8.1 7.3-8.1 12.8c0 3.7 1.3 6.5 7.3 10.1c6.9 4.1 16.6 7.1 29.2 10.9l.5.1c11.3 3.4 25.3 7.6 36.3 14.6c12.1 7.6 22.4 19.7 22.7 38.2c.3 19.3-9.6 33.3-22.9 41.6c-7.7 4.8-16.4 7.6-25.1 9.1V440c0 8.8-7.2 16-16 16s-16-7.2-16-16v-17.8c-11.2-2.1-21.7-5.7-30.9-8.9c-2.1-.7-4.2-1.4-6.2-2.1c-8.4-2.8-12.9-11.9-10.1-20.2s11.9-12.9 20.2-10.1c2.5.8 4.8 1.6 7.1 2.4c13.6 4.6 24.6 8.4 36.3 8.7c9.1.3 17.9-1.7 23.7-5.3c5.1-3.2 7.9-7.3 7.8-14c-.1-4.6-1.8-7.8-7.7-11.6c-6.8-4.3-16.5-7.4-29-11.2l-1.6-.5c-11-3.3-24.3-7.3-34.8-13.7c-12-7.2-22.6-18.9-22.7-37.3c-.1-19.4 10.8-32.8 23.8-40.5c7.5-4.4 15.8-7.2 24.1-8.7V232c0-8.8 7.2-16 16-16z"/></svg></a>'
                                })
                                
                            }
                            if (data.module7_override > 0){
                                actions_html+='<a class="btn px-1 inv_app_cls assign-user all-icon-same-clr" href="/invoice/invoiceoverrideusers/'+data.id+'" data_id="'+data.id+'"><img src="/static/images/over-ride-user.png" title="Override Users"></a>'
                            }
                            else{
                                $(data.payment_recept).each(function(ind,val){
                                    actions_html+='<a class="btn px-1 check_sign inv_app_cls file_uploading upload'+data.id+'" class="pay_rec_cls " pay_id="'+val+'"  data-toggle="modal" id="file_uploading" data-target="#exampleModalCenter" data_id="'+data.id+'"><i class="fa-solid fa-receipt" style="color: #95183a; font-size: 17px;" title="Payment Receipt Confirmation"></i></a>'

                                    // actions_html+='<a class="btn px-1 check_sign all-icon-same-clr" href="/invoice/bankuserview/'+data.id+'/'+val+'" data_id="'+data.id+'"><button type="button" class="btn btn-clr invoice-pay-btn">Invoice for Payment</button></a>'
                                })
                            
                            }
                            if (data.returned_user == 1){
                                actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/checklist/'+data.id+'" data_id="'+data.id+'"><i class="fa-solid fa-list-check" title="Invoice Receipt"></i></a>'
                            }
                            else if(data.returned_user == 2){
                                actions_html+='<a class="btn px-1 inv_app_cls check_sign all-icon-same-clr" href="/invoice/invoiceapproval/'+data.id+'" data_id="'+data.id+'"><i class="fa-solid fa-file-invoice" title="Invoice Approval"></i></a>'
                            }
                            if(data.get_credit_notes > 0){
                                actions_html+='<a class="btn px-1 waves-effect waves-float waves-light" href="/invoice/viewcreditnotes/'+data.id+'" data_id="'+data.id+'" title="View Credit Notes"><div class="credit_note"><svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" style="margin-top: -6px;" viewBox="0 0 14 14"><path fill="none" stroke="#95183a" stroke-linecap="round" stroke-linejoin="round" d="M8 13.5H1.5a1 1 0 0 1-1-1v-11a1 1 0 0 1 1-1H9m1.5 3l1.5-3l1.5 3V12a1.5 1.5 0 0 1-3 0Zm0 6h3m-10-9v13M6 4h2"/></svg></div></a>'
                            }
                }
            
        }
            return actions_html  
         }
        }
  ],
  initComplete: function(settings, json) {
    // Hide the loader once DataTable is initialized and data is rendered
    $('#loader').hide();
}
  });
  $('#vendorname, #servicetype').on('change', function() {
    // Reload the DataTable when dropdown options change
    dataTable.ajax.reload();
});

});

$(document).on('click','.file_uploading',function(){
    let val=parseInt($('#user_sign').val())
    console.log({'val-val':val})
    if (val > 0){
        $('.modal-backdrop').css("display","none")
        $('.my-modal').css("display","none")
    }
    else{
        let inv_id=$(this).attr('data_id')
        let pay_id=$(this).attr('pay_id')
        let text_sling=$(this).closest('tr').find('.input_tag')
        let input_value = text_sling.val();
        let parsed_value = JSON.parse(input_value);
        let id = parsed_value.id;
        let len = parsed_value.len;
        let file = parsed_value.file;
        $('.submit_cls').show()
        $('.modal-body').html('')
        $('.modal-body').append('<input type="hidden" name="invoice" value="'+inv_id+'">')
        $('.modal-body').append('<input type="hidden" name="payment_id" value="'+pay_id+'">')
        let new_id=$(this).closest('tr').attr('data-id')
        if (file.length>0){
            $(new Array(file)).each(function(){
            })
        }
        else{
            li=[]
            inv_cost_list=[]
            $('form').attr('data-id',new_id)
            let test_val=$(this).closest('tr').find('.get_paid_invcost')
            console.log('test_val',test_val)
            test_val.each(function(){
                let text_key=$(this).text()
                let inv_cost_id=$(this).find('#inv_cost_id').val()
                $('.modal-body').append('<input type="hidden" name="invoice_cost" value="'+inv_cost_id+'">')
                li.push(text_key)
                inv_cost_list.push(inv_cost_id)
            })
            $(new Array(len)).each(function(key,value){
                
                $('.modal-body').append(`<table class="upload-choose-file"><tbody class="val_details"><tr><td>${li[key]}</td></tr><tr class="flex_val"><td><input type="number" name="payment_percentage_${inv_cost_list[key]}" placeholder="%" class="form-control payment-precentage"></td><td><input type="file" accept="image, .png, .jpeg, .pdf, .jpg" name="file_${inv_cost_list[key]}[]" class="form-control filecls inp-voice3 filesize"><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></td><td><button class="add" data_id=${inv_cost_list[key]}><i class="fa fa-plus"></i></button></td></tr></tbody></table>`)
            })
            if (test_val.length == 0){
                $('.modal-body').html('No Invoice Verified by Bank User')
                $('.submit_cls').hide()
            }
        }
    }
})


    $(document).on('click','.check_sign',function(event){
      
        let val=parseInt($('#user_sign').val())
        if (val > 0){
            event.preventDefault();
            swal.fire('Please add signature in User Details')
        }
    })

$(document).on('click','.add',function(event){
    let data_id=$(this).attr('data_id')
    event.preventDefault();
    $(`<tr class="flex_val"><td><input type="number"  name="payment_percentage_${data_id}" placeholder="%" class="form-control payment-precentage"></td><td><input type="file" accept="image, .png, .jpeg, .pdf, .jpg" name="file_${data_id}[]" class="form-control filecls inp-voice3 filesize"><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></td><td><button class="delete"><i class="fa fa-minus"></i></button></td></tr>`).insertAfter($(this).closest('tr')) 
})

$(document).on('click','.delete',function(event){
    event.preventDefault();
    append_item=$(this).closest('tr').remove()
    
})


$(document).ready(function(){
    $('tr').each(function(key,value){
        values=$(this).attr('data-id')
        cos_in=$(this).closest('tr').find('.get_paid_invcost').length || 0
        new_li=[]
        $(value).append("<input type='hidden' class='input_tag' value='{\"id\":" + values + ", \"len\":" + cos_in + ", \"file\":[]}' >");
    })

    
})



$(document).on('click','.submit_cls',function(e){
    //new_text=$(this).closest('form').find('.flex_val')
    //e.preventDefault()
   /* var inp = document.getElementsByClassName('filecls');
    inp.each(function(){
        if($(this).files.length == 0){
            alert("Attachment Required");
       $(this).focus();
        return false;
        }
    }) */
    let count = 0;
    $('.filecls,.payment-precentage').each(function(index,value){
        //console.log($(value).val())
        if ($(value).val() == ''){
            $(value).addClass('con_error')
            e.preventDefault()

        }
        else{
            e.preventDefault()
        }
    })
    if($('.con_error').length==0){
        $(this).attr('disabled',true)
        $('form').submit()
    }
})


$(document).on('change','.filecls',function(){
    if($(this).val() != ''){
        $(this).removeClass('con_error')
    }
})
// $(document).ready(function(){
       
    $(".top-profile").click(function(){
    
      $(".creat-link-page").toggle();
    });
//   });

  function decimal_value(val){
    if (val != ''){
        if (val == Math.floor(val)){
            console.log('a')
        return val
        }
        else{
        console.log('b')
        return parseFloat(val).toFixed(2)
        }
    }

}

  $(document).on('change','.payment-precentage',function(){
    $(this).removeClass('con_error')
    var current_val = $(this).val()
    if (current_val != ''){
        if (!$.isNumeric(current_val)){ 
            swal.fire('Accept only Numbers')
            $(this).val('')
        }
    }
    var count=0
    var newarray=[]
    $(this).closest('table').find('.payment-precentage').each(function(index,value){
        var value=parseFloat($(this).val())|| 0
        count += value
        if (value == 0){
            newarray.push(index)
        }
    })
    // $('#invoicetblcls > tbody > tr').each(function(index, tr) { 
    //     var value=parseFloat($(this).find('td:eq(2)').find('.payment-precentage').val())|| 0
    //     count += value
    //     if (value == 0){
    //         newarray.push(index)
    //     }
    //  });
     if (count > 100){
        Swal.fire('Percentage Limit Reached')
        $(this).val('')
        // $('#submitid').prop('disabled',true)
    }
    else{
        $('#submitid').prop('disabled',false)
        var balance_value=100-count
        if (newarray.length == 1){
            $(this).closest('table').find('.payment-precentage').each(function(index,value){
                if (newarray[0] == index){
                    $(this).val(decimal_value(balance_value))
                }
            })
            // $('#invoicetblcls > tbody > tr').each(function(index, tr) { 
            //     if (newarray[0] == index){
            //         $(this).find('td:eq(2)').find('.payment-precentage').val(decimal_value(balance_value))
            //     }
            // })
        }
       
        $(this).val(decimal_value(current_val))
    }
    
    })


/*
{% comment %} 
$(function()
{
  $('#payment_form').validate(
    {
    rules:
      { 
        file:
        {
          required:true, 
          extension:"doc|docx|pdf|txt" 
        }
      },
    messages: 
        {
            file: "Please enter your Name",                   
        
        }, 
   
    });
     
    });
     {% endcomment %}
  



{% comment %} $(document).on('click','.submit_cls ',function(){
var tr_val=$(this).closest('form').attr('data-id')
var forms=$(this).closest('form')
var formData = new FormData(forms);

$.ajax({
    url: '/invoice/fileupload/' + tr_val + '/',
    data: {
        'pk': tr_val,
        'data1':formData
        
    },
    headers: { "X-CSRFToken": "{{ csrf_token }}"},
    type: 'POST',
    success: function(response) {
      if (response.success) {
       
    }
}
        })
        }) {% endcomment %}
    


*/   
     /********** pop choose file **********/    
/* For Filter option */
     $(document).ready(function() {
        $('.filter-btn').click(function() {
            var table = $(this).closest('table');
            var rows = table.find('tbody > tr').get();
            var idx = $(this).closest('th').index();
            var filter = $(this).data('filter');
            var icon = $(this).find('i');
    
            // Remove active class from other filter buttons
            $('.filter-btn').not(this).removeClass('active');
    
            // Toggle active class for the clicked filter button
            $(this).toggleClass('active');
    
            rows.sort(function(a, b) {
                var A, B;
    
                switch (filter) {
                    case 'vin-number':
                        A = $(a).children('td').eq(1).text().toUpperCase();
                        B = $(b).children('td').eq(1).text().toUpperCase();
                        break;
                    case 'vendor':
                        A = $(a).children('td').eq(2).text().toUpperCase();
                        B = $(b).children('td').eq(2).text().toUpperCase();
                        break;
                    case 'services':
                        A = $(a).children('td').eq(3).text().toUpperCase();
                        B = $(b).children('td').eq(3).text().toUpperCase();
                        break;
                    case 'invoice-number':
                        A = $(a).children('td').eq(4).text().toUpperCase();
                        B = $(b).children('td').eq(4).text().toUpperCase();
                        break;
                    case 'submitted-date':
                        A = new Date(convertDateFormat($(a).children('td').eq(5).text())).getTime();
                        B = new Date(convertDateFormat($(b).children('td').eq(5).text())).getTime();
                        break;
                    case 'approval-status':
                        A = $(a).children('td').eq(6).text().toUpperCase();
                        B = $(b).children('td').eq(6).text().toUpperCase();
                        break;
                    case 'payment-status':
                        A = $(a).children('td').eq(7).text().toUpperCase();
                        B = $(b).children('td').eq(7).text().toUpperCase();
                        break;
                    default:
                        break;
                }
    
                // Determine sorting order based on the presence of 'fa-sort-up' or 'fa-sort-down' class
                if (icon.hasClass('fa-sort-up')) {
                    return (A < B) ? 1 : -1;
                } else {
                    return (A > B) ? 1 : -1;
                }
            });
    
            $.each(rows, function(index, row) {
                table.children('tbody').append(row);
            });
    
            // Toggle between 'fa-sort-up' and 'fa-sort-down' classes for the icon
            icon.toggleClass('fa-sort-up fa-sort-down');
            $(this).closest('th').siblings().find('i').removeClass('fa-sort-up fa-sort-down').addClass('fa-sort');
        });
    });
    
    // Function to convert date format from DD-MM-YYYY to YYYY-MM-DD
    function convertDateFormat(dateString) {
        var parts = dateString.split('-');
        return parts[2] + '-' + parts[1] + '-' + parts[0];
    }     


    $(document).ready(function() {
        // $('#vendorvin').select2({
        //     placeholder: "select Vin",
        // })
        $('#vendorname').select2({
         placeholder: "Select Vendor ",
        });
        $('#servicetype').select2({
         placeholder: "Select Service",
        });
        $('#paid').select2({
            placeholder: "Select paid",
        });
      });


    $(document).on('click','.file_uploader',function(){
        let val=parseInt($('#user_sign').val())
        console.log({'val-val':val})
        if (val > 0){
            $('.modal-backdrop').css("display","none")
            $('.my-modal').css("display","none")
        }
        else{
            let inv_id=pk
            let this_tb=$(this).closest('table')
            let pay_id=$(this).closest('table').find('.payment_term').val()
            let total_len=this_tb.find('.file_upload').length
            $('.submit_cls').show()
            $('.modal-body').html('')
            $('.modal-body').append('<input type="hidden" name="invoice" value="'+inv_id+'">')
            $('.modal-body').append('<input type="hidden" name="payment_id" value="'+pay_id+'">')
            if (total_len > 0){
            this_tb.find('.file_upload').each(function(){
                let data_name=$(this).attr('data_name')
                let pay_percentage=$(this).attr('data_id')
                let payment_id=$(this).val()
                let invoice_cost=$(this).attr('invoice_cost')
                $('.modal-body').append(`<table class="upload-choose-file"><tbody class="val_details"><input type="hidden" value="${invoice_cost}" name="invoice_cost"><input type="hidden" value="${payment_id}" name="paymentinstruct_id"><tr><td>${data_name}</td></tr><tr class="flex_val"><td><input type="number"  name="payment_percentage_${invoice_cost}"  placeholder="%" value="${pay_percentage}" class="form-control payment-precentage"></td><td><input type="file" accept="image, .png, .jpeg, .pdf, .jpg"  class="form-control filecls inp-voice3" name="file_${invoice_cost}[]"><span class="maxmp">(Max: 25MB)</span></td><td><button class="add" data_id="${invoice_cost}" ><i class="fa fa-plus"></i></button></td></tr></tbody></table>`)
            })
            }
            else{
                $('.modal-body').html('No Invoice Verified by Bank User')
                $('.submit_cls').hide()
            }
        }
    })