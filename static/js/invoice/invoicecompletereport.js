

periodfield=$('#period')
fromdatefield=$('.fromdate')
todatefield=$('.todate')
$(document).on('focus',".dateformat-cls", function(){
    $(this).datepicker({
                dateFormat: 'dd-M-yy',
                maxDate:new Date(),
                yearRange: '1900:+0',
                changeMonth:true,
                changeYear:true,
    });
           
}); 
$(document).ready(function() {
   
    $('#country').select2({
       placeholder: "Select Country",
      });
      $('#project').select2({
       placeholder: "Select Project",
      });
      $('#discipline').select2({
       placeholder: "Select discipline",
      });
      $('#service').select2({
       placeholder: "Select Service",
      });
      $('#vendor').select2({
       placeholder: "Select Vendor",
      });
     
      $('#approval').select2({
       placeholder: "Select Approval Status",
      });
      $('#paymentstatus').select2({
       placeholder: "Select Payment Status",
      });
      if(reportname == 'ageing_report'){
      $('#ageingperiod').select2({
        placeholder: "Select Ageing Period",
       });
    }
    if(reportname == 'paidinvoice_paymentdays' || reportname == 'unpaidinvoice_overdue'){
        $('#ageingperiod').select2({
          placeholder: "Select Days For Payment",
         });
      }
      $('#amountfilter').select2({
        placeholder: "Select Amount",
       });
       $('#exceptions').select2({
        placeholder: "Select Reason For Exceptions",
       });  
    });



    $(document).ready(function(){
        $('.snocls').each(function(){
            $(this).html(($(this).closest('tr').index())+1)
        })
    })
    $(document).on('click','.draftsave',function(){
       $('.submitfield').val('draft')
    })
    $(document).on('click','.savebtn',function(){
       $('.submitfield').val('save')
     })

$(document).on('change','.masterselect',function(){
    curentselect=$(this).val()
    selectfield=$('.secondaryselect')
    var html=''
    if(curentselect == 1){
        html +='<option>---Select---</option>'
        html +='<option value="1">Invoice Register</option>'
        html +='<option value="2">Approval Status</option>'
        html +='<option value="3">Payment Status</option>'
        html +='<option value="4">Submission Count</option>'
        html +='<option value="5">Rating Vendor</option>'
        
    } 
    else if(curentselect == 2){
        html +='<option Selected value="6">Invoice Payable</option>'
    } 
    else if(curentselect == 3){
        html +='<option Selected value="7">Invoice Ageing</option>'
    } 
    else{
        html +='<option>---Select---</option>'
        html +='<option value="8">Paid Invoices Vs Days for Payment</option>'
        html +='<option value="9">Unpaid Invoices Vs No of Days Overdue</option>'
    }
    selectfield.html(html)

    //Displaying Select Field
   
})

$(document).ready(function(){
    if(reportname == 'invoice_register'){
        $('.ageingperiod').hide();
        $('.rankingvendor').hide();
        $('.ageingperiodreport').hide()
    }
    if(reportname == 'ageing_report'){
      $('.rankingvendor').hide();
      $('.paymentstatusfield').hide()
    }
    if (reportname == 'payment_status'){
        $('.rankingvendor').hide(); 
        $('.ageingperiod').hide();
      }
    if (reportname =='submission_count' || reportname=='approval_status'){
        $('.ageingperiod').hide();
        $('.rankingvendor').hide();
        $('.amountfilter').hide()
        $('.ageingperiodreport').hide()
    }
    if(reportname == 'vendors_ranking'){
        $('.ageingperiod').hide();
        $('.amountfilter').hide()
        $('.ageingperiodreport').hide()
    }
    if(reportname == 'partially_paid'){
        $('.ageingperiod').hide();
        $('.amountfilter').hide()
        $('.ageingperiodreport').hide()
        $('.rankingvendor').hide();
        $('.paymentstatusfield').hide()
     }
     if(reportname == 'paidinvoice_paymentdays' || reportname == 'unpaidinvoice_overdue'){
        // $('.ageingperiod').hide();
        $('.amountfilter').hide()
        // $('.ageingperiodreport').hide()
        $('.rankingvendor').hide();
        $('.paymentstatusfield').hide()
     }
     if(reportname == 'exception_report'){
        $('.amountfilter').hide()
        $('.ageingperiodreport').hide()
        $('.rankingvendor').hide();
        $('.paymentstatusfield').hide()
     }
 
})


var currencySelect = $("select[name='currency']")

$(document).on('click','.generate_report',function(){
   if(currencySelect.val()==''){
    currencySelect.addClass('con_error')
    $('.generate_report').attr('disabled','disabled')
   }
   if(reportname=='vendors_ranking'){
        if($('#vendorranking').val()==''){
        $('#vendorranking').addClass('con_error')
        $('.generate_report').attr('disabled','disabled')
       }
       $('#vendorranking').change(function(){
        $(this).removeClass('con_error')
       })
   }
   periodcount=0
    fromdate=0
    todate=0
    if(periodfield.val()==''){
        periodcount++
    }
    if(fromdatefield.val()==''){
        fromdate++
    }
    if(todatefield.val()==''){
        todate++
    }
   if(reportname=='submission_count'){
        if(periodcount==1 && fromdate == 1 && todate==1){
        periodfield.addClass('con_error')
        fromdatefield.addClass('con_error')
        todatefield.addClass('con_error')
        $('.generate_report').attr('disabled','disabled')
    }
    if(fromdate == 0 && todate==1){
        $('.generate_report').attr('disabled','disabled')
        todatefield.addClass('con_error')
    }
    if(fromdate == 1 && todate==0){
        $('.generate_report').attr('disabled','disabled')
        fromdatefield.addClass('con_error')
   
   }
   }
   else{
     if(fromdatefield.val()!=''){
        if(todatefield.val()==''){
            $('.generate_report').attr('disabled','disabled')
            todatefield.addClass('con_error') 
        }
     }
     if(todatefield.val()!=''){
        if(fromdatefield.val()==''){
            $('.generate_report').attr('disabled','disabled')
            fromdatefield.addClass('con_error') 
        }
     }
   }
})
$(document).on('change',periodfield,function(){
    console.log('periodfield----',periodfield.val())
    // if(periodfield.val()!=''){
    //     fromdatefield.attr('disabled','disabled')
    //     todatefield.attr('disabled','disabled')
    // }
    // else{
    //     fromdatefield.attr('disabled',false)
    //     todatefield.attr('disabled',false)
    // }
   })
fromdatefield.on('change',function(){
    periodfield.attr('disabled','disabled')
    if(fromdatefield!=''){
        periodfield.val('')
    }
})
todatefield.on('change',function(){
    periodfield.attr('disabled','disabled')
    if(todatefield!=''){
        periodfield.val('')
    }
})
$(document).on('change',currencySelect,function(){
    currencySelect.removeClass('con_error')
    $('.generate_report').attr('disabled',false)
})

// $(document).on('change',vendorranking,function(){
//     vendorranking.removeClass('con_error')
//     $('.generate_report').attr('disabled',false)
// })
periodfield.on('change',function(){
    if(periodfield.val()!=''){
        fromdatefield.val('')
        todatefield.val('')
    }
    periodfield.removeClass('con_error')
    fromdatefield.removeClass('con_error')
    todatefield.removeClass('con_error')
   
})
fromdatefield.on('change',function(){
    periodfield.removeClass('con_error')
    fromdatefield.removeClass('con_error')
    todatefield.removeClass('con_error')
   
})
todatefield.on('change',function(){
    periodfield.removeClass('con_error')
    fromdatefield.removeClass('con_error')
    todatefield.removeClass('con_error')
})  

$(document).on('click','.download_report',function(){
   if($('.download_pdf').val() != '1'){
        swal.fire('Please Generate Report Before Downloading')
        event.preventDefault(); 
    }
})


  
 



 
//     // $('.ageingperiod').hide();
//     // $('.amountfilter').hide()
//     // $('.ageingperiodreport').hide()
//     $(document).ready(function() {
//     var generateReportButton = $("#Generate");
//     var currencySelect = $("select[name='period']");
//     var selectper = $('.select-p');
    
//     generateReportButton.click(function(e) {
//         if (currencySelect.val() === '') {
//             e.preventDefault(); // Prevent the form submission
//             currencySelect.addClass('con_error');
//         } else {
//             currencySelect.removeClass('con_error');
//         }

//         if (selectper.val() === '') {
//             e.preventDefault();
//             $('.select-p').addClass('con_error');
//         } else {
//             $('.select-p').removeClass('con_error');
//         }

        
//     });
    
//     currencySelect.change(function() {
//         if (currencySelect.val() !== '') {
//             currencySelect.removeClass('con_error');
//         }
//     });

//     selectper.change(function() {
//         if (selectper.val() !== '') {
//             selectper.removeClass('con_error');
//         }
//     });

// });  



// $(document).ready(function() {
//     var generateReportButton = $(".ven-cr");
//     var currencySelect = $("select[name='vendorranking']");
//     var reportname = 'vendors_ranking';
    
//     generateReportButton.click(function(e) {
//         if(reportname == 'vendors_ranking'){
//             $('.ageingperiod').hide();
//             $('.amountfilter').hide()
//             $('.ageingperiodreport').hide()
//             if (currencySelect.val() === '') {
//                 e.preventDefault(); // Prevent the form submission
//                 currencySelect.addClass('con_error');
//             } else {
//                 currencySelect.removeClass('con_error');
//             }
//         }

//     });
    
//     currencySelect.change(function() {
//         if (currencySelect.val() !== '') {
//             currencySelect.removeClass('con_error');
//         }
//     });
// });