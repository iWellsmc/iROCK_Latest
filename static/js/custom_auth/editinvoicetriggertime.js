let wcc_check=Number($('#inv_check_id').val());
$(function() {
    if (wcc_check > 0){
        Swal.fire({
            position: 'top',
            icon: 'success',
            title: 'Invoice Approval Inprogress',
            showConfirmButton: true,
            timer:6000
            }).then(function() {
                window.history.back();
            });
    }
})  
$(document).on('click','.addbtn',function(){
  console.log('Addbtn')
    let sno = parseInt($('.invoice_trigger tbody tr:last').text())+1
    let invoicefromday = parseInt($('.invoice_trigger tbody tr:last').find('.invoicetodate').val())
    let invoicetoday = invoicefromday+1
    console.log('invoicefromday',invoicefromday)
    console.log('invoicetoday',invoicetoday)
    if(invoicefromday < 0 || isNaN(invoicefromday)){
      console.log('if--')
        Swal.fire("Enter Invoice Payment To Day")
    }
    else if (invoicefromday == 365){
      console.log('elseif--')
      Swal.fire("Days Reached Maximum")
    }
    else{
      console.log('else--')
      // <input type="text"class="form-control" value="Day" readonly><input type="hidden" name="time_unit" class="form-control" value="1" readonly></input>
    let add_field = `<tr><td>${sno}</td><input type="hidden" name="pk" class="form-control" value=0><td><input type="text"name="payment_terms_from"class="form-control invoicefromdate" value=${invoicetoday} readonly></td><td><input type="text" name="payment_terms_to"class="form-control invoicetodate"></td><td><select name="time_unit" class="form-control form-select"><option value="">Select</option>"`
    let time_data=[{'key':2,'value':'Minutes'},{'key':0,'value':'Hours'},{'key':1,'value':'Days'}]
    $.each(time_data, function(index, val){
      add_field +="<option value="+val.key+">"+val.value+"</option>"
    })
    add_field +='</select></td><td class="d-flex"><input type="text" name="time_allotted" class="form-control time_allotted"><button id="delete-user" class="ml-2 btn btn-clr delete-btn"type="button" value="delete"><i class="fa fa-minus"></i></button></td><tr>'
    $('table').append(add_field)
    }
})

$(document).on('change','.invoicetodate',function(){
   let fromval = $(this).closest('tr').find('.invoicefromdate').val()
  if(parseInt($(this).val()) <= fromval){
    Swal.fire('To Day Must Be Greater Than From Day')
    $(this).val('')
  }
  if(parseInt($(this).val()) > 365){
    Swal.fire('To Day Must Be Less Than 365')
    $(this).val('')
  }
})

$(document).on('keyup','.invoicetodate,.time_allotted',function(){
  var $th = $(this);
  $th.val($th.val().replace(/[^0-9]/g, ''))
})


$(document).on('click','.delete-btn',function(){
  $(this).closest('tr').nextAll('tr').remove()
  $(this).closest('tr').remove()
})

$(document).on('change','.invoicetodate',function(){
   $(this).closest('tr').nextAll('tr').remove()
  })


$(document).on('click', '.mainsave', function(e){
  $('input').each(function(index,val) {
    if ($(this).val() == '') {
      $(this).addClass('con_error')
    }else{
      $(this).removeClass('con_error')
    }
  })

  if ($('.con_error').length > 0) {
    return false
}
// }
})

$(document).on('change','.time_allotted',function(){
 if($(this).val() > 365){
    Swal.fire('Time allowed Per Station Must Be Less Than 365')
  }
})