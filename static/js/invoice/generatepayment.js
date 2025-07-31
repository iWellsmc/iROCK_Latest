$(function () {
    $(".calculator-draggable").draggable();
  });

  $(function () {
    $(".payment_instruction_form").draggable();
  });

  $(document).ready(function(){
    $(function () {
        $(".exchange-draggable").draggable();
        // $('body').removeClass('modal-open'); 
         
      });
    
      
    
    
    $(function () {
        
        $(".payment_instruction_form").draggable();
      });
    
      $(document).on('click','.generate_btn',function () {
        console.log({"modal-backdrop": $('.modal-backdrop')});
        $('.modal-backdrop').css('display', 'none');
        $('body').removeClass('modal-open');  
    });
    
    });

/*  
$(document).on('click','.gen-confirm-clss',function(e){
  // get data id from button'
  let dataId=$(this).attr('data-id')
  e.preventDefault()
  count=0
  $('.bankdetailcls').each(function(){
    if($(this).val()==''){
      $(this).addClass('con_error')
      count++
    }
    else{
      $(this).removeClass('con_error')
    }
  })
if(count==0){


  pk=$("#table_data").attr('data-id')
  var valueArray = $('.bankdetailcls').map(function() {
    return this.value;
}).get();
  var payment_percentage = $('.payment-percentage').map(function() {
    return parseFloat(this.value.replace(/[^\d.-]/g, '')).toFixed(2)
}).get();
var payable_amount = $('.payable-amount').map(function() {
    return parseFloat(this.value.replace(/[^\d.-]/g, '')).toFixed(2)
}).get();

var remaining_amount = $('.remaining-amount').map(function() {
  return parseFloat(this.value.replace(/[^\d.-]/g, '')).toFixed(2)
}).get();
var loopcount = $('.loopcount').map(function() {
  return this.value;
}).get();
var invoiceid = $('.invoiceid').map(function() {
  return this.value;
}).get();
  currency_check=$('.currency_check')
  bankdetailcls=$('.bankdetailcls')
  let serializedData = $('#payment_instruction_form').serialize();
  console.log(serializedData)
  console.log({'pk':pk})
  console.log({'valueArray':valueArray})
  console.log({'loopcount':loopcount})
  console.log({'invoiceid':invoiceid})
  $.ajax({
    url: '/invoice/savebankdata/' + pk + '/',
    data: {
        'pk': pk,
        'valueArray':valueArray,
        'payment_percentage':payment_percentage,
        'payable_amount':payable_amount,
        'remaining_amount':remaining_amount,
        'serializedData':serializedData,
        'is_editable':dataId,
        'loopcount':loopcount,
        'invoiceid':invoiceid
    },
    headers: { "X-CSRFToken":  csrf_token },
    type: 'POST',
    success: function(response) {
      if (response.success) {
        currency_check.each(function(key,index){
          v=bankdetailcls[key]
          var selectedOption = v.options[v.selectedIndex];
          var selectedopt=selectedOption.text
          $(this).text(selectedopt)
        })
        var parsed = JSON.parse(response.updated_data);
        $(parsed).each(function(index,value){
          //console.log(value.pi_number)
          //console.log(value)
          // append pi number to gen-table table Generated Instruction column
          $('.gen-table > tbody > tr').eq(index).find('td').eq(4).text(value.pi_number)
          $('.gen-table > tbody > tr').eq(index).find('td').eq(2).text(`${value.companybank__bank_name}-${value.companybank__account_number}`)
          $('.gen-table > tbody > tr').eq(index).find('td').eq(5).find('a').attr('data-id',`${value.id}`)
        })
       
      }
    
    $('.pay-hide-cls').show();
    $('.close').trigger('click');
    
    },
   
  })
}
window.location.reload();
})

*/

function newRoundOfTwoValues(number) {
  var numberStr = number.toString();
  var decimalPos = numberStr.indexOf('.');

  // If there is no decimal point, simply return the number with two decimal places
  if (decimalPos === -1) {
      return parseFloat(number).toFixed(2);
  }

  var integerPart = numberStr.substring(0, decimalPos);
  var decimalPart = numberStr.substring(decimalPos + 1);
  var newDecimalPart;
  
  if (decimalPart.length > 2) {
      // Check the third digit to determine whether to round up or not
      if (parseInt(decimalPart.charAt(2)) >= 5) {
          newDecimalPart = (parseInt(decimalPart.substring(0, 2)) + 1).toString().padStart(2, '0');
          
          // Check if rounding causes the decimal part to be "100", meaning we need to carry over to the integer part
          if (newDecimalPart === '100') {
              newDecimalPart = '00';
              integerPart = (parseInt(integerPart) + 1).toString();
          }
      } else {
          newDecimalPart = decimalPart.substring(0, 2);
      }
  } else if (decimalPart.length === 2) {
      // If the decimal part has exactly two digits, use them as they are
      newDecimalPart = decimalPart;
  } else {
      // If the decimal part has fewer than two digits, pad it with zeros
      newDecimalPart = decimalPart.padEnd(2, '0');
  }

  var result = integerPart + '.' + newDecimalPart;
  

  
  return parseFloat(result).toFixed(2);
}

$(document).ready(function() {
  $(document).on('click','.confirm_generate',function(event){
      swal.fire('Generate Payment Instructions');
  });
});



function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
$(document).on('click','.calbtn',function(){
  $('.modal-backdrop').css('display', 'none');
  $('body').removeClass('modal-open');

});

$(document).ready(function() {
  $(document).on('keyup','.payment-percentage',function(e){
      let value = $(this).val();

      // Remove any decimal point or any characters after the decimal
      $(this).val(value.replace(/\D/g, '')); // Allow only digits (no decimals)
  });
});


$(document).on('keyup','.payment-percentage',function(e){
  //e.preventDefault()
      // if amount above 100 open sweet alert
      let remainingPercentage = parseInt($(this).closest('tr').find('.remaining-percentage').val().replace(/,/g, ''))
     if(parseInt($(this).val())>remainingPercentage){
          new swal({
              title: "Error",
              text: `Payment percentage should not be greater than ${remainingPercentage}`,
              icon: "error",
            });
            $(this).val('')
            $(this).closest('tr').find('.payable-amount').val('')
            $(this).closest('tr').find('.remaining-amount').val('')
        // else if value is empty empty the payable amount and remaining amount
      }else if($(this).val()==''){
            $(this).closest('tr').find('.payable-amount').val('')
            $(this).closest('tr').find('.remaining-amount').val('')
      }
      else if (parseInt($(this).val())!==''){
        // let netPayableAmount = parseFloat($(this).closest('tr').find('.net-payable').val().replace(/[^\d.]/g, "")) //old code
        let netPayableAmount = parseFloat($(this).closest('tr').find('.net-payable').val().replace(/[^\d.]/g, "")) //new code
        let paidamount = parseFloat($(this).closest('tr').find('.alreadypaidamount').val().replace(/[^\d.]/g, "")) //new code
        
        netPayableAmount= newRoundOfTwoValues(netPayableAmount)
        paidamount = newRoundOfTwoValues(paidamount)
        let calulatedAmount = (parseFloat((netPayableAmount * parseFloat($(this).val()) )/ 100))
        let remainingAmount = parseFloat(netPayableAmount - calulatedAmount - paidamount)
        if (remainingAmount <= 0) {
          remainingAmount = parseFloat(0)
        }
        let currencySymbol = $(this).closest('tr').find('.currency-symbol').val()
        $(this).closest('tr').find('.payable-amount').val(`${currencySymbol} ${numberWithCommas(newRoundOfTwoValues(calulatedAmount))}`)
        $(this).closest('tr').find('.remaining-amount').val(`${currencySymbol} ${numberWithCommas(newRoundOfTwoValues(remainingAmount))}`)
      }
})


// $(document).on('click','#confirm_payment',function(e){
//   e.preventDefault()
//   $('.confirm_action').val('confirm')
//   $('#generatepayment_form').submit();
// })





// document on click of generate instruction button
$(document).on('click','.gen-confirm-clss',function(event){
  event.preventDefault()
  form_data = $('#payment_instruction_form').serialize()
  let is_error = false
  let adjust_credit=$('.adjust_credit').attr('data-id')
  if (adjust_credit == 0){
    swal.fire('Adjust Credit Note for this Invoice')
  }
  else{
    if($('#credit_note,#credit_note_datas').not(':hidden')){
      
    }
    let select_2= $('#credit_note,#credit_note_datas').find('option').length
    var select2Field = $('#credit_note,#credit_note_datas').find('option:selected').length
    if(select_2 > 0){
      if (select2Field == 0 ){
        is_error = true
      }
    }
    $('.payment-percentage,.bankdetailcls').each(function(){
      
      if($(this).closest('div').css('display') === 'block'){
      if($(this).val()==''){
         if (!$(this).prop('disabled')) {
          if(($(this).attr('data-id')) != 1){
            $(this).addClass('con_error')
            is_error = true
          }
        }
          
        
      }
    }
    })
    if(!is_error){
      console.log({'fir':form_data})
      post_data_payment(form_data)
      $('.gen-confirm-clss').attr('disabled', 'disabled');
    }
  }

})


// remove con_error class on keyup and change
$(document).on('keyup change','.payment-percentage,.bankdetailcls',function(){
  $(this).removeClass('con_error')
})

 

// document on click of generate_btn
$(document).on('click','.generate_btn',function(event){
  $('.modal-backdrop').css('display', 'none');
  $('body').removeClass('modal-open');
 
  event.preventDefault()
  get_data()

})

function post_data_payment(form_data){
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: "/invoice/postpaymentinstruction",
    data: form_data, 
    success: function(data){
      $('.close').trigger('click');
      window.location.reload();
    }
});
}

function get_data(){
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: "/invoice/getpaymentinstruction",
    data: {'pk':invoiceid,'payment_count':payment_count},
    success: function(data){
      $('.payment-instruction-data').empty()
      $('.payment-instruction-data').append(data.payment_instruction_template)
      select2Instance=$('#credit_note_datas').select2({
        placeholder: "Select Credit Notes",
      });
      $("#credit_note,#credit_note_datas").find('option:disabled').each(function(){
        selectedItems.push($(this).val())
      })
      $("#credit_note,#credit_note_datas").find('option:selected').not('option:disabled').each(function(){
          selectedItems.push($(this).val())
      })
    }
});
}

$(document).on('click','.adjust_credit',function(e){
 e.preventDefault();
 
//  Swal.fire({
//   title: 'Do You Want to Adjust Invoice with Credit Note?',
//   showCancelButton: true,
//   confirmButtonColor: '#3085d6',
//   cancelButtonColor: '#d33',
//   confirmButtonText: 'Yes, I Confirm',
//   cancelButtonText: 'No',
// }).then((result) => {
//   if (result.isConfirmed) {
//  $('.check_type').val('2')
//  $('.without_data').css('display','none')
//  $('.with_data').css('display','none')
//  $('.with_creditnote').removeAttr('style')
 
//  let get_invoice=$('.invoice_id').val()
//  $.ajax({
//   type: "POST",
//   headers: { "X-CSRFToken": csrf_token },
//   url: "/invoice/updatepaymentinstuction",
//   data: {'id':get_invoice}, 
//   success: function(data){
  
//   }
// });
//   }
// })
})



$(document).on('click','.adjust_credit',function(e){
  e.preventDefault();
  select2Instance=$('#credit_note').select2({
    placeholder: "Select Credit Notes",
  });
  Swal.fire({
      title: 'Do You Want to Adjust Invoice with Credit Note?',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, I Confirm',
      cancelButtonText: 'No',
    }).then((result) => {
    if (result.isConfirmed) {
    $(this).attr('data-id',1)
     $('.check_type').val('2')
     $('.without_data').css('display','none')
     $('.with_data').css('display','none')
     $('.with_creditnote').removeAttr('style')
     $(this).css('display','none')
    //  let get_invoice=$('.invoice_id').val()
    //  $.ajax({
    //   type: "POST",
    //   headers: { "X-CSRFToken": csrf_token },
    //   url: "/invoice/updatepaymentinstuction",
    //   data: {'id':get_invoice}, 
    //   success: function(data){
      
    //   }
    // });
    }
    })
})
var select2Instance

$(document).ready(function(){
  let bal_list=[]
    $('.balance_credit_note').each(function(){
      bal_list.push($(this).val())
    })
    // var serializedArray = JSON.stringify(bal_list);
    $('.bal_cn').val(bal_list);
})



$(document).on("select2:select", "#credit_note,#credit_note_datas",function (evt) {
  var element = evt.params.data.element;
  var lastSelectedOption = evt.params.data;
  var $element = $(element);
  $element.detach();
  $(this).append($element);

  let check_empty_val=0
  $(this).closest('div').find('table>tbody>tr .net-payable').each(function(){
    if($(this).val() == 0){
      check_empty_val=check_empty_val+1
    }
  })

if( check_empty_val == 0 ){
  check_majority=0
  selectedItems.push(lastSelectedOption.id);

  // $(this).trigger("change");
}
else{
  check_majority=1+check_majority
  swal.fire('Credit Note Value Exceeds Invoice Amount')
  // var selectedValues = $("#credit_note,#credit_note_datas").val();

  if (selectedItems.length > 0) {
    // selectedItems.pop(lastSelectedOption.id);
    select2Instance.val(selectedItems).trigger('change');
}
  // var selectedData = select2Instance.select2('data');
  //   selectedData.pop();
  //   select2Instance.select2('data', selectedData);

    // Remove the selected item from the array
    // var indexToRemove = selectedValues.indexOf(element.id);
    // if (indexToRemove === -1) {
    //   selectedValues.splice(indexToRemove, 1);
    // }

    // Update the selected values to remove the item
    // $("#credit_note,#credit_note_datas").val(selectedValues)
  
}
// if(check_majority > 0){
//   return false;

// }

  

});

$(document).on('select2:unselect','#credit_note,#credit_note_datas',function(e){
  var unselectedItem = e.params.data
  let check_empty_val=0
  $(this).closest('div').find('table>tbody>tr .net-payable').each(function(){
    if($(this).val() == 0){
      check_empty_val=check_empty_val+1
    }
  })
  if( check_empty_val == 0 ){
    check_majority=0
    // $(this).trigger("change");
  }
  else{
    check_majority=1+check_majority
  }
  let total_lists=[]
  selectedItems = $.grep(selectedItems, function(value) {
    return value !== unselectedItem.id;
});
  let credit_note_ids=$('#credit_note,#credit_note_datas').find('option:selected')
  $(credit_note_ids).each(function(){
    total_lists.push($(this).val())
  })
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: "/invoice/get_total_credit_val",
    data: {'id':total_lists,
            'invoiceid':invoiceid,
          }, 
    success: function(data){
      let li_count=data.data.length
      if(li_count > 0){
      $.each(data.data, function(index, object) {
        let credit_amount=object.contract_credit
        $('.total_credit_val').each(function(){
          let currency=$(this).attr('currency')
          if($(this).attr('data-val')== object.id){
            let initial_credit_val=parseInt($(this).attr('check_credit').replace(/\D/g, ''), 10);
            credit_val=parseInt(credit_amount.replace(/,/g, '').split('.')[0], 10)
            let total_amount=''+currency+' '+credit_val.toLocaleString('en-US')+''
            // alert(total_amount)
            $(this).html(total_amount)
            let inv_amount=parseInt($(this).closest('tr').find('.total_investment').text().replace(/[^\d.]/g, ''), 10);
            // let credit_value=parseInt(credit_amount.replace(/\D/g, ''), 10)
            let net_payable=0
            let pending_credit=0
            // console.log({'inv_amount':inv_amount,'credit_value':credit_value})
            if(inv_amount > credit_val){
              net_payable=inv_amount-credit_val
            }
            else{
              pending_credit=credit_val-inv_amount
            }
            $(this).closest('tr').find('.net-payable').val(net_payable)
            let payble_value=''+currency+' '+net_payable.toLocaleString('en-US')+''
            let credit_pending_val=''+currency+' '+pending_credit.toLocaleString('en-US')+''
            $(this).closest('tr').find('.payable_value').html(payble_value)
            $(this).closest('tr').find('.balance_credit_note').val(credit_pending_val)
            $(this).closest('tr').find('.pending_credit_val').html(credit_pending_val)
          }
        })
      });
    }
    else{
      $('.total_credit_val').each(function(){
        let currency=$(this).attr('currency')
        let cn_val=''+currency+' '+$(this).attr('check_credit')
        $(this).html(cn_val)
        let inital_bal=$(this).closest('tr').find('.intial-net-payable').val()
        let initial_credit_val=parseInt($(this).attr('check_credit').replace(/[^\d.]/g, ''), 10);
        $(this).closest('tr').find('.net-payable').val(inital_bal)
        let payble_value=''+currency+' '+inital_bal.toLocaleString('en-US')+''
        $(this).closest('tr').find('.balance_credit_note').val(cn_val)
        $(this).closest('tr').find('.pending_credit_val').html(cn_val)
        // $(this).closest('tr').find('.balance_credit_note').val($(this).closest('tr').find('.pending_credit_val').attr('initial_pending_val'))
        // $(this).closest('tr').find('.pending_credit_val').html($(this).closest('tr').find('.pending_credit_val').attr('initial_pending_val'))
        $(this).closest('tr').find('.payable_value').html(payble_value)
      })
      // $(this).closest('tr').find('.net-payable').val(initial_credit_val)
      // let payble_value=''+currency+' '+initial_credit_val.toLocaleString('en-US')+''
      //     // let credit_pending_val=''+currency+' '+pending_credit.toLocaleString('en-US')+''
      //     $(this).closest('tr').find('.payable_value').html(payble_value)
      //     // $(this).closest('tr').find('.pending_credit_val').html(credit_pending_val)
      console.log('dta',li_count)
    }
  }
 
  })
})


// function creditnotechange(){
$(document).on('change.select2','#credit_note,#credit_note_datas',function(){
  let check_empty_val=0
  $(this).closest('div').find('table>tbody>tr .net-payable').each(function(){
    if($(this).val() == 0){
      check_empty_val=check_empty_val+1
    }
  })
  if( check_empty_val == 0 ){
    check_majority=0
    // $(this).trigger("change");
  }
  else{
    check_majority=1+check_majority
  }

  let total_lists=[]
  let credit_note_ids=$('#credit_note,#credit_note_datas').find('option:selected')
  $(credit_note_ids).each(function(){
    total_lists.push($(this).val())
  })
  $(this).closest('div').find('table>tbody>tr .payment-percentage').val('')
  $(this).closest('div').find('table>tbody>tr .payable-amount').val('')
  $(this).closest('div').find('table>tbody>tr .remaining-amount').val('')
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: "/invoice/get_total_credit_val",
    data: {'id':total_lists,
            'invoiceid':invoiceid,
          }, 
    success: function(data){
      let li_count=data.data.length
      if(li_count > 0){
        if(check_majority == 0){
      $.each(data.data, function(index, object) {
        let credit_amount=object.contract_credit
        $('.total_credit_val').each(function(){
          let currency=$(this).attr('currency')
          if($(this).attr('data-val')== object.id){
            let initial_credit_val=parseInt($(this).attr('check_credit').replace(/[^\d.]/g, ''), 10);
            credit_val=parseInt(credit_amount.replace(/,/g, '').split('.')[0], 10)
            let total_amount=''+currency+' '+credit_val.toLocaleString('en-US')+''
            // alert(total_amount)
            $(this).html(total_amount)
            let inv_amount=parseInt($(this).closest('tr').find('.total_investment').text().replace(/[^\d.]/g, ''), 10);
            // let credit_value=parseInt(credit_amount.replace(/\D/g, ''), 10)
            let net_payable=0
            let pending_credit=0
            // console.log({'inv_amount':inv_amount,'credit_value':credit_value})
            if(inv_amount > credit_val){
              net_payable=inv_amount-credit_val
            }
            else{
              pending_credit=credit_val-inv_amount
            }
            $(this).closest('tr').find('.net-payable').val(net_payable)
            let payble_value=''+currency+' '+net_payable.toLocaleString('en-US')+''
            let credit_pending_val=''+currency+' '+pending_credit.toLocaleString('en-US')+''
            $(this).closest('tr').find('.payable_value').html(payble_value)
            $(this).closest('tr').find('.balance_credit_note').val(credit_pending_val)
            $(this).closest('tr').find('.pending_credit_val').html(credit_pending_val)
          }
        })
      });
        }
    }
    else{
      $('.total_credit_val').each(function(){
        let currency=$(this).attr('currency')
        let cn_val=''+currency+' '+$(this).attr('check_credit')
        $(this).html(cn_val)
        let inital_bal=$(this).closest('tr').find('.intial-net-payable').val()
        let initial_credit_val=parseInt($(this).attr('check_credit').replace(/\D/g, ''), 10);
        $(this).closest('tr').find('.net-payable').val(inital_bal)
        let payble_value=''+currency+' '+inital_bal.toLocaleString('en-US')+''
        $(this).closest('tr').find('.balance_credit_note').val(cn_val)
        $(this).closest('tr').find('.pending_credit_val').html(cn_val)
        // $(this).closest('tr').find('.balance_credit_note').val($(this).closest('tr').find('.pending_credit_val').attr('initial_pending_val'))
        // $(this).closest('tr').find('.pending_credit_val').html($(this).closest('tr').find('.pending_credit_val').attr('initial_pending_val'))
        $(this).closest('tr').find('.payable_value').html(payble_value)
      })
      // $(this).closest('tr').find('.net-payable').val(initial_credit_val)
      // let payble_value=''+currency+' '+initial_credit_val.toLocaleString('en-US')+''
      //     // let credit_pending_val=''+currency+' '+pending_credit.toLocaleString('en-US')+''
      //     $(this).closest('tr').find('.payable_value').html(payble_value)
      //     // $(this).closest('tr').find('.pending_credit_val').html(credit_pending_val)
      console.log('dta',li_count)
    }
  }
 
  });
})



$(document).on('click','.assign_signatory',function(e){
  e.preventDefault();
  swal.fire('No Designated Signatory Users')
})

 

let totalElements = [];

$('.inv_file1').each(function(index, val) {
  $(this).click(function() {
     if (totalElements.indexOf(index) === -1) {
       totalElements.push(index);
        
    }
  });
});



$('.ash_confirm').click(function(event) {
  let counter_input = $('.inv_file1:last').val();
  console.log(counter_input, "val1");
  console.log($('.inv_file1').length,'llliii');

  if (totalElements.length < $('.inv_file1').length) {
    $('.confirm_btn').removeAttr('data-target');
    swal.fire('Please view all pdf');
    event.preventDefault();
     
  } else {
    $('.confirm_btn').attr({'data-target':'#exampleModalCenter'});
  }
});

$('.save_id',).click(function() {
  let counter_input = $('.inv_file1:last').val();
  console.log(counter_input, "val1");

  if (totalElements.length < $('.inv_file1').length) {
    swal.fire('Please view all pdf');
  } else {
   }
});

$('.swal_confirm').click(function(event){

  swal.fire('Generate Payment Instructions');
  event.preventDefault();
})



// }
