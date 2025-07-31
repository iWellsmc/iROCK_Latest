$('#project_create').submit(function(e){
  if ($('#sign_settings :selected').val()== 1){
    $('form')[0].submit();
  }
  if($('#sign_settings :selected').val()== 2){
    $('.common_cls').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    $('.common_select').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    // if any input field is invalid then return false
    if ($('.con_error').length > 0) {
      e.preventDefault();
    }
    if($('.con_error').length == 0){
      // if all the input fields are valid then call the ajax function
      $(document).find('table tbody tr input[name="newtr"]').each(function(index,value){
        $(value).closest('tr').find('.currency, .without-invoice').attr('name',`new_currency${index+1}`)
        $(value).closest('tr').find('.min_amount, .min_amountn').attr('name',`new_min_amount${index+1}`)
        $(value).closest('tr').find('.max_amount, .max_amountn').attr('name',`new_max_amount${index+1}`)
        $(value).closest('tr').find('.new_tr').attr('name',`new_invoice_type${index+1}`)
        $(value).closest('tr').find('.signatory-user').attr('name',`new_newuser${index+1}`)
      })
      $('form')[0].submit();
    }
  }
  // validate the form all fields are required
    
});


$(document).on('keyup','.min_amount,.min_amountn,.max_amount,.max_amountn',function(){
  let check_limit=$(this).val().length
  if (check_limit>=19){
    new swal({
      title: "Maximum Amount",
      button: "Ok",
    })
    $(this).val('')
  }
})


$(document).on('change','.without-invoice, .currency',function(){
  let currency_id = $(this).val()
  let this_element = $(this)
  console.log({'this currency':$(this).val()})
  //$('.without-invoice option[value="' + currency_id + '"]').filter('option:selected').each(function(index,value){
  //console.log({'this1234':$(value).val()})
  if($('.without-invoice option[value="' + currency_id + '"]:selected').length > 0) {
    console.log($('.without-invoice').length,true)
    $('.without-invoice, .currency').not($(this)).each(function(index,value){
      console.log('each functtion value ',$(value).val(), currency_id)
      // if any currency is matched with value of each currency then show the alert
      
      if($(value).val() == currency_id){
        new swal({
          title: "Data already Exists for Selected Currency",
          button: "Ok",
        })
        this_element.val('')
      }
    })
  
  }
  
  })


  $(document).on('change','.max_amount,.max_amountn',function(){
      let val_of_max=$(this).closest('tr').find('.min_amount,.min_amountn').val();
      if(val_of_max==''){
        new swal({
          title: "Enter Min Invoice Amount",
          button: "Ok",})
        $(this).val('')
      }
      console.log({'val of max':val_of_max})
      let min_amount = parseInt($(this).closest('tr').find('.min_amount').val());
      let max_amount = parseInt($(this).val());
      if(min_amount > max_amount){
          new swal({
          title: "Min Invoice Amount should be Lesser than Max Invoice Amount",
          button: "Ok",
        });
        // empty the max amount
        $(this).val('')
      }
    })

    $(document).on('change','.max_amount,.max_amountn',function(){
      const this_value=$(this).val()
      const closest_val=$(this).closest('tr').find('.min_amount,.min_amountn').val()
      if(this_value==closest_val){
        new swal({
            title: "Same Invoice Amount Selected",
            button: "Ok",
          });
          $(this).val('')
      }
      if(parseInt(this_value) < parseInt(closest_val)){
        new swal({
          title: "Max Invoice Amount Should be greater than Min Invoice Amount",
          button: "Ok",
        });
        $(this).val('')
      }
    })


    
$(document).on('change','.min_amount,.min_amountn',function(){
const this_value=$(this).val()
const closest_val=$(this).closest('tr').find('.max_amount,.max_amountn').val()
if(this_value==closest_val){
new swal({
    title: "Same Invoice Amount Selected",
    button: "Ok",
  });
  $(this).val('')
}
if(closest_val!=''){
if(parseInt(closest_val) < parseInt(this_value)){
  new swal({
    title: "Max Invoice Amount Should be greater than Min Invoice Amount",
    button: "Ok",
  });
  $(this).val('')
}
}
})

$(document).on('change','.max_amount ',function(){
let min_val = parseFloat($(this).val().replace(/,/g, ''));
const this_value=$(this)
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})

$('.min_amount').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})
})


// signatory-user select tag click
$(document).on('change','.signatory-user',function(){
let user_id = $(this).val()
let this_element = $(this)
// if user is already selected in same row then disable option
$(this).closest('tr').find('.signatory-user').not($(this)).each(function(index,value){
  if (parseInt($(value).val()) === parseInt(user_id) && $(value).val() !== ''){
    Sweetalert2.fire({
    title: "User Already Selected",
  //  button: "Ok",
  });
  // empty the user
  this_element.val('')
}
})
})


// delete user
$(document).on('click','.delete-usaved-tr',function(){
// remove tr
$(this).closest('tr').remove()
})

$(document).on('change','.currency',function(){
$(this).closest('tr').find('.min_amount,.max_amount,.max_amountn,.min_amountn').val('')

})


$(document).on('click','.delete-unsaved-user',function(){
let this_element = $(this)
let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
$(this).closest('.row').remove()
//let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
//let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
})

$(document).on('change','.min_amount,.max_amount',function(){
let this_value=$(this)
let thisElement = $(this).val()
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})
$('.min_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})

})


$(document).on('change', '.min_amount, .min_amountn, .max_amount,.max_amountn', function(){
let thisElement = $(this)
console.log({'this element':thisElement})
const this_value = $(this).val()
console.log({'this_val':this_value})
const this_tr = $(this).closest('tr')
console.log({'this tr':this_tr})
const this_currency_id = this_tr.find('.currency').val()
console.log({'this currency id':this_currency_id})
$('.currency option[value="' + this_currency_id + '"]').filter('option:selected').not(thisElement.closest('tr')).each(function(index,value){
if($(value).val() == this_currency_id && $(value).closest('tr') !== this_tr) {
  max = $(value).closest('tr').find('.max_amount,.max_amountn').val()
  console.log({'max':max})
  let parsedMax = parseInt(max.replace(/,/g, ''));
  min = $(value).closest('tr').find('.min_amountn , .min_amount').val()
  let parsedMin = parseInt(min.replace(/,/g, ''));
  if (!isNaN(parsedMax) && !isNaN(parsedMin)) {
    console.log({'numberInRange':[parsedMin, parsedMax]})
    if (this_value != parsedMax && this_value != parsedMin){
    numberInRange(this_value, parsedMin, parsedMax, thisElement)
    }
  }
}
})
})

function numberInRange(num, first, second, thisElement) {
let max = Math.max(first, second);
let min = Math.min(first, second);
console.log({'min':min,'max':max});
if (num >= min && num <= max) {
swal.fire({
  text: "Invoice Amount Range already exists",
  showCancelButton: false,
  confirmButtonText: "Ok",
  confirmButtonColor: '#3085d6',
});
thisElement.val('')
}
return false;
}


$(document).on('change','select',function(){
$(this).removeClass('con_error')
})
// remove the class con_error on change
$(document).on('keyup','input',function(){
$(this).removeClass('con_error')
})

$(document).on('click','.delete_new_row',function(){
$(this).closest('tr').remove()
})






$(document).on('change','.settings_sign',function(){
  var value_tye=$(this).val()
  console.log('value_tye',value_tye)
  if(value_tye=='1'){
      $('.project_sign').removeAttr('style')
      $('.Default_sign').addClass('style').css('display', 'none');
      }
  else{
      $('.project_sign').addClass('style').css('display', 'none');
  }
  if(value_tye=='2'){
      $('.Default_sign').removeAttr('style')
  }
  else{
      $('.Default_sign').addClass('style').css('display', 'none');
  }
})

$(document).on('click','.delete-saved-tr',function(){
  const  get_data_id = $(this).data('id')
  const remove_tr = $(this).closest('tr')
  swal.fire({
  text: "Are you sure you want to delete this Record?",
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes',
  cancelButtonText: 'No',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatory",
      data: {'pk':get_data_id},
      success: function(data){
        remove_tr.remove()
      }
    });
  }
});
})


$(document).on('click','#delete-user',function(){
  var  get_data_id = $(this).data('id')
  console.log('get_data_id',get_data_id)
  let user_id = $(this).closest('td').find(`select[id="sign-user-id${get_data_id}"]`).val()
  // call the ajax function POST method
  // sweet alert for confirmation of delete if clicked yes then delete the user call the ajax function
  let this_element = $(this).closest('.row')
  let row_length = $(this).closest('tr').find('.row').length
  let del_user_val=$(this).closest('tr').find('.no_of_users')
  
  if (row_length > 1){
  swal.fire({
  text: "Are you sure you want to delete this user?",
  showCancelButton: true,
  confirmButtonText: "Yes",
  cancelButtonText: "No",
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatoryuser",
      data: {'pk':get_data_id},
      success: function(data){
        let get_no_of_user = del_user_val.val()
        let set_no_of_user=del_user_val.val(parseInt(get_no_of_user)-1)
        this_element.remove()
      }
    });
  }
});
  }
  else{
      return false;
  }
})


$(document).on('change','.select-invoice',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice').css('display','none')
    $('.without_invoice').removeAttr('style')
  }
  else{
    $('.without_invoice').css('display','none')
    $('.with_invoice').removeAttr('style')
  }
})

$(document).on('change','.select-invoice-project',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice_project').css('display','none')
    $('.without_invoice_project').removeAttr('style')
  }
  else{
    $('.without_invoice_project').css('display','none')
    $('.with_invoice_project').removeAttr('style')
  }
});
$('#project_create').submit(function(e){
  if ($('#sign_settings :selected').val()== 1){
    $('form')[0].submit();
  }
  if($('#sign_settings :selected').val()== 2){
    $('.common_cls').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    $('.common_select').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    // if any input field is invalid then return false
    if ($('.con_error').length > 0) {
      e.preventDefault();
    }
    if($('.con_error').length == 0){
      // if all the input fields are valid then call the ajax function
      $(document).find('table tbody tr input[name="newtr"]').each(function(index,value){
        $(value).closest('tr').find('.currency, .without-invoice').attr('name',`new_currency${index+1}`)
        $(value).closest('tr').find('.min_amount, .min_amountn').attr('name',`new_min_amount${index+1}`)
        $(value).closest('tr').find('.max_amount, .max_amountn').attr('name',`new_max_amount${index+1}`)
        $(value).closest('tr').find('.new_tr').attr('name',`new_invoice_type${index+1}`)
        $(value).closest('tr').find('.signatory-user').attr('name',`new_newuser${index+1}`)
      })
      $('form')[0].submit();
    }
  }
  // validate the form all fields are required
    
});


$(document).on('keyup','.min_amount,.min_amountn,.max_amount,.max_amountn',function(){
  let check_limit=$(this).val().length
  if (check_limit>=19){
    new swal({
      title: "Maximum Amount",
      button: "Ok",
    })
    $(this).val('')
  }
})


$(document).on('change','.without-invoice, .currency',function(){
  let currency_id = $(this).val()
  let this_element = $(this)
  console.log({'this currency':$(this).val()})
  //$('.without-invoice option[value="' + currency_id + '"]').filter('option:selected').each(function(index,value){
  //console.log({'this1234':$(value).val()})
  if($('.without-invoice option[value="' + currency_id + '"]:selected').length > 0) {
    console.log($('.without-invoice').length,true)
    $('.without-invoice, .currency').not($(this)).each(function(index,value){
      console.log('each functtion value ',$(value).val(), currency_id)
      // if any currency is matched with value of each currency then show the alert
      
      if($(value).val() == currency_id){
        new swal({
          title: "Data already Exists for Selected Currency",
          button: "Ok",
        })
        this_element.val('')
      }
    })
  
  }
  
  })


  $(document).on('change','.max_amount,.max_amountn',function(){
      let val_of_max=$(this).closest('tr').find('.min_amount,.min_amountn').val();
      if(val_of_max==''){
        new swal({
          title: "Enter Min Invoice Amount",
          button: "Ok",})
        $(this).val('')
      }
      console.log({'val of max':val_of_max})
      let min_amount = parseInt($(this).closest('tr').find('.min_amount').val());
      let max_amount = parseInt($(this).val());
      if(min_amount > max_amount){
          new swal({
          title: "Min Invoice Amount should be Lesser than Max Invoice Amount",
          button: "Ok",
        });
        // empty the max amount
        $(this).val('')
      }
    })

    $(document).on('change','.max_amount,.max_amountn',function(){
      const this_value=$(this).val()
      const closest_val=$(this).closest('tr').find('.min_amount,.min_amountn').val()
      if(this_value==closest_val){
        new swal({
            title: "Same Invoice Amount Selected",
            button: "Ok",
          });
          $(this).val('')
      }
      if(parseInt(this_value) < parseInt(closest_val)){
        new swal({
          title: "Max Invoice Amount Should be greater than Min Invoice Amount",
          button: "Ok",
        });
        $(this).val('')
      }
    })


    
$(document).on('change','.min_amount,.min_amountn',function(){
const this_value=$(this).val()
const closest_val=$(this).closest('tr').find('.max_amount,.max_amountn').val()
if(this_value==closest_val){
new swal({
    title: "Same Invoice Amount Selected",
    button: "Ok",
  });
  $(this).val('')
}
if(closest_val!=''){
if(parseInt(closest_val) < parseInt(this_value)){
  new swal({
    title: "Max Invoice Amount Should be greater than Min Invoice Amount",
    button: "Ok",
  });
  $(this).val('')
}
}
})

$(document).on('change','.max_amount ',function(){
let min_val = parseFloat($(this).val().replace(/,/g, ''));
const this_value=$(this)
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})

$('.min_amount').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})
})


// signatory-user select tag click
$(document).on('change','.signatory-user',function(){
let user_id = $(this).val()
let this_element = $(this)
// if user is already selected in same row then disable option
$(this).closest('tr').find('.signatory-user').not($(this)).each(function(index,value){
  if (parseInt($(value).val()) === parseInt(user_id) && $(value).val() !== ''){
    Sweetalert2.fire({
    title: "User Already Selected",
  //  button: "Ok",
  });
  // empty the user
  this_element.val('')
}
})
})


// delete user
$(document).on('click','.delete-usaved-tr',function(){
// remove tr
$(this).closest('tr').remove()
})

$(document).on('change','.currency',function(){
$(this).closest('tr').find('.min_amount,.max_amount,.max_amountn,.min_amountn').val('')

})


$(document).on('click','.delete-unsaved-user',function(){
let this_element = $(this)
let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
$(this).closest('.row').remove()
//let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
//let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
})

$(document).on('change','.min_amount,.max_amount',function(){
let this_value=$(this)
let thisElement = $(this).val()
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})
$('.min_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})

})


$(document).on('change', '.min_amount, .min_amountn, .max_amount,.max_amountn', function(){
let thisElement = $(this)
console.log({'this element':thisElement})
const this_value = $(this).val()
console.log({'this_val':this_value})
const this_tr = $(this).closest('tr')
console.log({'this tr':this_tr})
const this_currency_id = this_tr.find('.currency').val()
console.log({'this currency id':this_currency_id})
$('.currency option[value="' + this_currency_id + '"]').filter('option:selected').not(thisElement.closest('tr')).each(function(index,value){
if($(value).val() == this_currency_id && $(value).closest('tr') !== this_tr) {
  max = $(value).closest('tr').find('.max_amount,.max_amountn').val()
  console.log({'max':max})
  let parsedMax = parseInt(max.replace(/,/g, ''));
  min = $(value).closest('tr').find('.min_amountn , .min_amount').val()
  let parsedMin = parseInt(min.replace(/,/g, ''));
  if (!isNaN(parsedMax) && !isNaN(parsedMin)) {
    console.log({'numberInRange':[parsedMin, parsedMax]})
    if (this_value != parsedMax && this_value != parsedMin){
    numberInRange(this_value, parsedMin, parsedMax, thisElement)
    }
  }
}
})
})

function numberInRange(num, first, second, thisElement) {
let max = Math.max(first, second);
let min = Math.min(first, second);
console.log({'min':min,'max':max});
if (num >= min && num <= max) {
swal.fire({
  text: "Invoice Amount Range already exists",
  showCancelButton: false,
  confirmButtonText: "Ok",
  confirmButtonColor: '#3085d6',
});
thisElement.val('')
}
return false;
}


$(document).on('change','select',function(){
$(this).removeClass('con_error')
})
// remove the class con_error on change
$(document).on('keyup','input',function(){
$(this).removeClass('con_error')
})

$(document).on('click','.delete_new_row',function(){
$(this).closest('tr').remove()
})






$(document).on('change','.settings_sign',function(){
  var value_tye=$(this).val()
  console.log('value_tye',value_tye)
  if(value_tye=='1'){
      $('.project_sign').removeAttr('style')
      $('.Default_sign').addClass('style').css('display', 'none');
      }
  else{
      $('.project_sign').addClass('style').css('display', 'none');
  }
  if(value_tye=='2'){
      $('.Default_sign').removeAttr('style')
  }
  else{
      $('.Default_sign').addClass('style').css('display', 'none');
  }
})

$(document).on('click','.delete-saved-tr',function(){
  const  get_data_id = $(this).data('id')
  const remove_tr = $(this).closest('tr')
  swal.fire({
  text: "Are you sure you want to delete this Record?",
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes',
  cancelButtonText: 'No',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatory",
      data: {'pk':get_data_id},
      success: function(data){
        remove_tr.remove()
      }
    });
  }
});
})


$(document).on('click','#delete-user',function(){
  var  get_data_id = $(this).data('id')
  console.log('get_data_id',get_data_id)
  let user_id = $(this).closest('td').find(`select[id="sign-user-id${get_data_id}"]`).val()
  // call the ajax function POST method
  // sweet alert for confirmation of delete if clicked yes then delete the user call the ajax function
  let this_element = $(this).closest('.row')
  let row_length = $(this).closest('tr').find('.row').length
  let del_user_val=$(this).closest('tr').find('.no_of_users')
  
  if (row_length > 1){
  swal.fire({
  text: "Are you sure you want to delete this user?",
  showCancelButton: true,
  confirmButtonText: "Yes",
  cancelButtonText: "No",
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatoryuser",
      data: {'pk':get_data_id},
      success: function(data){
        let get_no_of_user = del_user_val.val()
        let set_no_of_user=del_user_val.val(parseInt(get_no_of_user)-1)
        this_element.remove()
      }
    });
  }
});
  }
  else{
      return false;
  }
})


$(document).on('change','.select-invoice',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice').css('display','none')
    $('.without_invoice').removeAttr('style')
  }
  else{
    $('.without_invoice').css('display','none')
    $('.with_invoice').removeAttr('style')
  }
})

$(document).on('change','.select-invoice-project',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice_project').css('display','none')
    $('.without_invoice_project').removeAttr('style')
  }
  else{
    $('.without_invoice_project').css('display','none')
    $('.with_invoice_project').removeAttr('style')
  }
});
$('#project_create').submit(function(e){
  if ($('#sign_settings :selected').val()== 1){
    $('form')[0].submit();
  }
  if($('#sign_settings :selected').val()== 2){
    $('.common_cls').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    $('.common_select').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    // if any input field is invalid then return false
    if ($('.con_error').length > 0) {
      e.preventDefault();
    }
    if($('.con_error').length == 0){
      // if all the input fields are valid then call the ajax function
      $(document).find('table tbody tr input[name="newtr"]').each(function(index,value){
        $(value).closest('tr').find('.currency, .without-invoice').attr('name',`new_currency${index+1}`)
        $(value).closest('tr').find('.min_amount, .min_amountn').attr('name',`new_min_amount${index+1}`)
        $(value).closest('tr').find('.max_amount, .max_amountn').attr('name',`new_max_amount${index+1}`)
        $(value).closest('tr').find('.new_tr').attr('name',`new_invoice_type${index+1}`)
        $(value).closest('tr').find('.signatory-user').attr('name',`new_newuser${index+1}`)
      })
      $('form')[0].submit();
    }
  }
  // validate the form all fields are required
    
});


$(document).on('keyup','.min_amount,.min_amountn,.max_amount,.max_amountn',function(){
  let check_limit=$(this).val().length
  if (check_limit>=19){
    new swal({
      title: "Maximum Amount",
      button: "Ok",
    })
    $(this).val('')
  }
})


$(document).on('change','.without-invoice, .currency',function(){
  let currency_id = $(this).val()
  let this_element = $(this)
  console.log({'this currency':$(this).val()})
  //$('.without-invoice option[value="' + currency_id + '"]').filter('option:selected').each(function(index,value){
  //console.log({'this1234':$(value).val()})
  if($('.without-invoice option[value="' + currency_id + '"]:selected').length > 0) {
    console.log($('.without-invoice').length,true)
    $('.without-invoice, .currency').not($(this)).each(function(index,value){
      console.log('each functtion value ',$(value).val(), currency_id)
      // if any currency is matched with value of each currency then show the alert
      
      if($(value).val() == currency_id){
        new swal({
          title: "Data already Exists for Selected Currency",
          button: "Ok",
        })
        this_element.val('')
      }
    })
  
  }
  
  })


  $(document).on('change','.max_amount,.max_amountn',function(){
      let val_of_max=$(this).closest('tr').find('.min_amount,.min_amountn').val();
      if(val_of_max==''){
        new swal({
          title: "Enter Min Invoice Amount",
          button: "Ok",})
        $(this).val('')
      }
      console.log({'val of max':val_of_max})
      let min_amount = parseInt($(this).closest('tr').find('.min_amount').val());
      let max_amount = parseInt($(this).val());
      if(min_amount > max_amount){
          new swal({
          title: "Min Invoice Amount should be Lesser than Max Invoice Amount",
          button: "Ok",
        });
        // empty the max amount
        $(this).val('')
      }
    })

    $(document).on('change','.max_amount,.max_amountn',function(){
      const this_value=$(this).val()
      const closest_val=$(this).closest('tr').find('.min_amount,.min_amountn').val()
      if(this_value==closest_val){
        new swal({
            title: "Same Invoice Amount Selected",
            button: "Ok",
          });
          $(this).val('')
      }
      if(parseInt(this_value) < parseInt(closest_val)){
        new swal({
          title: "Max Invoice Amount Should be greater than Min Invoice Amount",
          button: "Ok",
        });
        $(this).val('')
      }
    })


    
$(document).on('change','.min_amount,.min_amountn',function(){
const this_value=$(this).val()
const closest_val=$(this).closest('tr').find('.max_amount,.max_amountn').val()
if(this_value==closest_val){
new swal({
    title: "Same Invoice Amount Selected",
    button: "Ok",
  });
  $(this).val('')
}
if(closest_val!=''){
if(parseInt(closest_val) < parseInt(this_value)){
  new swal({
    title: "Max Invoice Amount Should be greater than Min Invoice Amount",
    button: "Ok",
  });
  $(this).val('')
}
}
})

$(document).on('change','.max_amount ',function(){
let min_val = parseFloat($(this).val().replace(/,/g, ''));
const this_value=$(this)
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})

$('.min_amount').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})
})


// signatory-user select tag click
$(document).on('change','.signatory-user',function(){
let user_id = $(this).val()
let this_element = $(this)
// if user is already selected in same row then disable option
$(this).closest('tr').find('.signatory-user').not($(this)).each(function(index,value){
  if (parseInt($(value).val()) === parseInt(user_id) && $(value).val() !== ''){
    Sweetalert2.fire({
    title: "User Already Selected",
  //  button: "Ok",
  });
  // empty the user
  this_element.val('')
}
})
})


// delete user
$(document).on('click','.delete-usaved-tr',function(){
// remove tr
$(this).closest('tr').remove()
})

$(document).on('change','.currency',function(){
$(this).closest('tr').find('.min_amount,.max_amount,.max_amountn,.min_amountn').val('')

})


$(document).on('click','.delete-unsaved-user',function(){
let this_element = $(this)
let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
$(this).closest('.row').remove()
//let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
//let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
})

$(document).on('change','.min_amount,.max_amount',function(){
let this_value=$(this)
let thisElement = $(this).val()
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})
$('.min_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})

})


$(document).on('change', '.min_amount, .min_amountn, .max_amount,.max_amountn', function(){
let thisElement = $(this)
console.log({'this element':thisElement})
const this_value = $(this).val()
console.log({'this_val':this_value})
const this_tr = $(this).closest('tr')
console.log({'this tr':this_tr})
const this_currency_id = this_tr.find('.currency').val()
console.log({'this currency id':this_currency_id})
$('.currency option[value="' + this_currency_id + '"]').filter('option:selected').not(thisElement.closest('tr')).each(function(index,value){
if($(value).val() == this_currency_id && $(value).closest('tr') !== this_tr) {
  max = $(value).closest('tr').find('.max_amount,.max_amountn').val()
  console.log({'max':max})
  let parsedMax = parseInt(max.replace(/,/g, ''));
  min = $(value).closest('tr').find('.min_amountn , .min_amount').val()
  let parsedMin = parseInt(min.replace(/,/g, ''));
  if (!isNaN(parsedMax) && !isNaN(parsedMin)) {
    console.log({'numberInRange':[parsedMin, parsedMax]})
    if (this_value != parsedMax && this_value != parsedMin){
    numberInRange(this_value, parsedMin, parsedMax, thisElement)
    }
  }
}
})
})

function numberInRange(num, first, second, thisElement) {
let max = Math.max(first, second);
let min = Math.min(first, second);
console.log({'min':min,'max':max});
if (num >= min && num <= max) {
swal.fire({
  text: "Invoice Amount Range already exists",
  showCancelButton: false,
  confirmButtonText: "Ok",
  confirmButtonColor: '#3085d6',
});
thisElement.val('')
}
return false;
}


$(document).on('change','select',function(){
$(this).removeClass('con_error')
})
// remove the class con_error on change
$(document).on('keyup','input',function(){
$(this).removeClass('con_error')
})

$(document).on('click','.delete_new_row',function(){
$(this).closest('tr').remove()
})






$(document).on('change','.settings_sign',function(){
  var value_tye=$(this).val()
  console.log('value_tye',value_tye)
  if(value_tye=='1'){
      $('.project_sign').removeAttr('style')
      $('.Default_sign').addClass('style').css('display', 'none');
      }
  else{
      $('.project_sign').addClass('style').css('display', 'none');
  }
  if(value_tye=='2'){
      $('.Default_sign').removeAttr('style')
  }
  else{
      $('.Default_sign').addClass('style').css('display', 'none');
  }
})

$(document).on('click','.delete-saved-tr',function(){
  const  get_data_id = $(this).data('id')
  const remove_tr = $(this).closest('tr')
  swal.fire({
  text: "Are you sure you want to delete this Record?",
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes',
  cancelButtonText: 'No',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatory",
      data: {'pk':get_data_id},
      success: function(data){
        remove_tr.remove()
      }
    });
  }
});
})


$(document).on('click','#delete-user',function(){
  var  get_data_id = $(this).data('id')
  console.log('get_data_id',get_data_id)
  let user_id = $(this).closest('td').find(`select[id="sign-user-id${get_data_id}"]`).val()
  // call the ajax function POST method
  // sweet alert for confirmation of delete if clicked yes then delete the user call the ajax function
  let this_element = $(this).closest('.row')
  let row_length = $(this).closest('tr').find('.row').length
  let del_user_val=$(this).closest('tr').find('.no_of_users')
  
  if (row_length > 1){
  swal.fire({
  text: "Are you sure you want to delete this user?",
  showCancelButton: true,
  confirmButtonText: "Yes",
  cancelButtonText: "No",
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatoryuser",
      data: {'pk':get_data_id},
      success: function(data){
        let get_no_of_user = del_user_val.val()
        let set_no_of_user=del_user_val.val(parseInt(get_no_of_user)-1)
        this_element.remove()
      }
    });
  }
});
  }
  else{
      return false;
  }
})


$(document).on('change','.select-invoice',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice').css('display','none')
    $('.without_invoice').removeAttr('style')
  }
  else{
    $('.without_invoice').css('display','none')
    $('.with_invoice').removeAttr('style')
  }
})

$(document).on('change','.select-invoice-project',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice_project').css('display','none')
    $('.without_invoice_project').removeAttr('style')
  }
  else{
    $('.without_invoice_project').css('display','none')
    $('.with_invoice_project').removeAttr('style')
  }
});
$('#project_create').submit(function(e){
  if ($('#sign_settings :selected').val()== 1){
    $('form')[0].submit();
  }
  if($('#sign_settings :selected').val()== 2){
    $('.common_cls').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    $('.common_select').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    // if any input field is invalid then return false
    if ($('.con_error').length > 0) {
      e.preventDefault();
    }
    if($('.con_error').length == 0){
      // if all the input fields are valid then call the ajax function
      $(document).find('table tbody tr input[name="newtr"]').each(function(index,value){
        $(value).closest('tr').find('.currency, .without-invoice').attr('name',`new_currency${index+1}`)
        $(value).closest('tr').find('.min_amount, .min_amountn').attr('name',`new_min_amount${index+1}`)
        $(value).closest('tr').find('.max_amount, .max_amountn').attr('name',`new_max_amount${index+1}`)
        $(value).closest('tr').find('.new_tr').attr('name',`new_invoice_type${index+1}`)
        $(value).closest('tr').find('.signatory-user').attr('name',`new_newuser${index+1}`)
      })
      $('form')[0].submit();
    }
  }
  // validate the form all fields are required
    
});


$(document).on('keyup','.min_amount,.min_amountn,.max_amount,.max_amountn',function(){
  let check_limit=$(this).val().length
  if (check_limit>=19){
    new swal({
      title: "Maximum Amount",
      button: "Ok",
    })
    $(this).val('')
  }
})


$(document).on('change','.without-invoice, .currency',function(){
  let currency_id = $(this).val()
  let this_element = $(this)
  console.log({'this currency':$(this).val()})
  //$('.without-invoice option[value="' + currency_id + '"]').filter('option:selected').each(function(index,value){
  //console.log({'this1234':$(value).val()})
  if($('.without-invoice option[value="' + currency_id + '"]:selected').length > 0) {
    console.log($('.without-invoice').length,true)
    $('.without-invoice, .currency').not($(this)).each(function(index,value){
      console.log('each functtion value ',$(value).val(), currency_id)
      // if any currency is matched with value of each currency then show the alert
      
      if($(value).val() == currency_id){
        new swal({
          title: "Data already Exists for Selected Currency",
          button: "Ok",
        })
        this_element.val('')
      }
    })
  
  }
  
  })


  $(document).on('change','.max_amount,.max_amountn',function(){
      let val_of_max=$(this).closest('tr').find('.min_amount,.min_amountn').val();
      if(val_of_max==''){
        new swal({
          title: "Enter Min Invoice Amount",
          button: "Ok",})
        $(this).val('')
      }
      console.log({'val of max':val_of_max})
      let min_amount = parseInt($(this).closest('tr').find('.min_amount').val());
      let max_amount = parseInt($(this).val());
      if(min_amount > max_amount){
          new swal({
          title: "Min Invoice Amount should be Lesser than Max Invoice Amount",
          button: "Ok",
        });
        // empty the max amount
        $(this).val('')
      }
    })

    $(document).on('change','.max_amount,.max_amountn',function(){
      const this_value=$(this).val()
      const closest_val=$(this).closest('tr').find('.min_amount,.min_amountn').val()
      if(this_value==closest_val){
        new swal({
            title: "Same Invoice Amount Selected",
            button: "Ok",
          });
          $(this).val('')
      }
      if(parseInt(this_value) < parseInt(closest_val)){
        new swal({
          title: "Max Invoice Amount Should be greater than Min Invoice Amount",
          button: "Ok",
        });
        $(this).val('')
      }
    })


    
$(document).on('change','.min_amount,.min_amountn',function(){
const this_value=$(this).val()
const closest_val=$(this).closest('tr').find('.max_amount,.max_amountn').val()
if(this_value==closest_val){
new swal({
    title: "Same Invoice Amount Selected",
    button: "Ok",
  });
  $(this).val('')
}
if(closest_val!=''){
if(parseInt(closest_val) < parseInt(this_value)){
  new swal({
    title: "Max Invoice Amount Should be greater than Min Invoice Amount",
    button: "Ok",
  });
  $(this).val('')
}
}
})

$(document).on('change','.max_amount ',function(){
let min_val = parseFloat($(this).val().replace(/,/g, ''));
const this_value=$(this)
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})

$('.min_amount').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})
})


// signatory-user select tag click
$(document).on('change','.signatory-user',function(){
let user_id = $(this).val()
let this_element = $(this)
// if user is already selected in same row then disable option
$(this).closest('tr').find('.signatory-user').not($(this)).each(function(index,value){
  if (parseInt($(value).val()) === parseInt(user_id) && $(value).val() !== ''){
    Sweetalert2.fire({
    title: "User Already Selected",
  //  button: "Ok",
  });
  // empty the user
  this_element.val('')
}
})
})


// delete user
$(document).on('click','.delete-usaved-tr',function(){
// remove tr
$(this).closest('tr').remove()
})

$(document).on('change','.currency',function(){
$(this).closest('tr').find('.min_amount,.max_amount,.max_amountn,.min_amountn').val('')

})


$(document).on('click','.delete-unsaved-user',function(){
let this_element = $(this)
let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
$(this).closest('.row').remove()
//let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
//let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
})

$(document).on('change','.min_amount,.max_amount',function(){
let this_value=$(this)
let thisElement = $(this).val()
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})
$('.min_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})

})


$(document).on('change', '.min_amount, .min_amountn, .max_amount,.max_amountn', function(){
let thisElement = $(this)
console.log({'this element':thisElement})
const this_value = $(this).val()
console.log({'this_val':this_value})
const this_tr = $(this).closest('tr')
console.log({'this tr':this_tr})
const this_currency_id = this_tr.find('.currency').val()
console.log({'this currency id':this_currency_id})
$('.currency option[value="' + this_currency_id + '"]').filter('option:selected').not(thisElement.closest('tr')).each(function(index,value){
if($(value).val() == this_currency_id && $(value).closest('tr') !== this_tr) {
  max = $(value).closest('tr').find('.max_amount,.max_amountn').val()
  console.log({'max':max})
  let parsedMax = parseInt(max.replace(/,/g, ''));
  min = $(value).closest('tr').find('.min_amountn , .min_amount').val()
  let parsedMin = parseInt(min.replace(/,/g, ''));
  if (!isNaN(parsedMax) && !isNaN(parsedMin)) {
    console.log({'numberInRange':[parsedMin, parsedMax]})
    if (this_value != parsedMax && this_value != parsedMin){
    numberInRange(this_value, parsedMin, parsedMax, thisElement)
    }
  }
}
})
})

function numberInRange(num, first, second, thisElement) {
let max = Math.max(first, second);
let min = Math.min(first, second);
console.log({'min':min,'max':max});
if (num >= min && num <= max) {
swal.fire({
  text: "Invoice Amount Range already exists",
  showCancelButton: false,
  confirmButtonText: "Ok",
  confirmButtonColor: '#3085d6',
});
thisElement.val('')
}
return false;
}


$(document).on('change','select',function(){
$(this).removeClass('con_error')
})
// remove the class con_error on change
$(document).on('keyup','input',function(){
$(this).removeClass('con_error')
})

$(document).on('click','.delete_new_row',function(){
$(this).closest('tr').remove()
})






$(document).on('change','.settings_sign',function(){
  var value_tye=$(this).val()
  console.log('value_tye',value_tye)
  if(value_tye=='1'){
      $('.project_sign').removeAttr('style')
      $('.Default_sign').addClass('style').css('display', 'none');
      }
  else{
      $('.project_sign').addClass('style').css('display', 'none');
  }
  if(value_tye=='2'){
      $('.Default_sign').removeAttr('style')
  }
  else{
      $('.Default_sign').addClass('style').css('display', 'none');
  }
})

$(document).on('click','.delete-saved-tr',function(){
  const  get_data_id = $(this).data('id')
  const remove_tr = $(this).closest('tr')
  swal.fire({
  text: "Are you sure you want to delete this Record?",
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes',
  cancelButtonText: 'No',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatory",
      data: {'pk':get_data_id},
      success: function(data){
        remove_tr.remove()
      }
    });
  }
});
})


$(document).on('click','#delete-user',function(){
  var  get_data_id = $(this).data('id')
  console.log('get_data_id',get_data_id)
  let user_id = $(this).closest('td').find(`select[id="sign-user-id${get_data_id}"]`).val()
  // call the ajax function POST method
  // sweet alert for confirmation of delete if clicked yes then delete the user call the ajax function
  let this_element = $(this).closest('.row')
  let row_length = $(this).closest('tr').find('.row').length
  let del_user_val=$(this).closest('tr').find('.no_of_users')
  
  if (row_length > 1){
  swal.fire({
  text: "Are you sure you want to delete this user?",
  showCancelButton: true,
  confirmButtonText: "Yes",
  cancelButtonText: "No",
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatoryuser",
      data: {'pk':get_data_id},
      success: function(data){
        let get_no_of_user = del_user_val.val()
        let set_no_of_user=del_user_val.val(parseInt(get_no_of_user)-1)
        this_element.remove()
      }
    });
  }
});
  }
  else{
      return false;
  }
})


$(document).on('change','.select-invoice',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice').css('display','none')
    $('.without_invoice').removeAttr('style')
  }
  else{
    $('.without_invoice').css('display','none')
    $('.with_invoice').removeAttr('style')
  }
})

$(document).on('change','.select-invoice-project',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice_project').css('display','none')
    $('.without_invoice_project').removeAttr('style')
  }
  else{
    $('.without_invoice_project').css('display','none')
    $('.with_invoice_project').removeAttr('style')
  }
});
$('#project_create').submit(function(e){
  if ($('#sign_settings :selected').val()== 1){
    $('form')[0].submit();
  }
  if($('#sign_settings :selected').val()== 2){
    $('.common_cls').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    $('.common_select').not('[readonly]').each(function(index,val) {
      // validate the input fields if empty then add the class
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    // if any input field is invalid then return false
    if ($('.con_error').length > 0) {
      e.preventDefault();
    }
    if($('.con_error').length == 0){
      // if all the input fields are valid then call the ajax function
      $(document).find('table tbody tr input[name="newtr"]').each(function(index,value){
        $(value).closest('tr').find('.currency, .without-invoice').attr('name',`new_currency${index+1}`)
        $(value).closest('tr').find('.min_amount, .min_amountn').attr('name',`new_min_amount${index+1}`)
        $(value).closest('tr').find('.max_amount, .max_amountn').attr('name',`new_max_amount${index+1}`)
        $(value).closest('tr').find('.new_tr').attr('name',`new_invoice_type${index+1}`)
        $(value).closest('tr').find('.signatory-user').attr('name',`new_newuser${index+1}`)
      })
      $('form')[0].submit();
    }
  }
  // validate the form all fields are required
    
});


$(document).on('keyup','.min_amount,.min_amountn,.max_amount,.max_amountn',function(){
  let check_limit=$(this).val().length
  if (check_limit>=19){
    new swal({
      title: "Maximum Amount",
      button: "Ok",
    })
    $(this).val('')
  }
})


$(document).on('change','.without-invoice, .currency',function(){
  let currency_id = $(this).val()
  let this_element = $(this)
  console.log({'this currency':$(this).val()})
  //$('.without-invoice option[value="' + currency_id + '"]').filter('option:selected').each(function(index,value){
  //console.log({'this1234':$(value).val()})
  if($('.without-invoice option[value="' + currency_id + '"]:selected').length > 0) {
    console.log($('.without-invoice').length,true)
    $('.without-invoice, .currency').not($(this)).each(function(index,value){
      console.log('each functtion value ',$(value).val(), currency_id)
      // if any currency is matched with value of each currency then show the alert
      
      if($(value).val() == currency_id){
        new swal({
          title: "Data already Exists for Selected Currency",
          button: "Ok",
        })
        this_element.val('')
      }
    })
  
  }
  
  })


  $(document).on('change','.max_amount,.max_amountn',function(){
      let val_of_max=$(this).closest('tr').find('.min_amount,.min_amountn').val();
      if(val_of_max==''){
        new swal({
          title: "Enter Min Invoice Amount",
          button: "Ok",})
        $(this).val('')
      }
      console.log({'val of max':val_of_max})
      let min_amount = parseInt($(this).closest('tr').find('.min_amount').val());
      let max_amount = parseInt($(this).val());
      if(min_amount > max_amount){
          new swal({
          title: "Min Invoice Amount should be Lesser than Max Invoice Amount",
          button: "Ok",
        });
        // empty the max amount
        $(this).val('')
      }
    })

    $(document).on('change','.max_amount,.max_amountn',function(){
      const this_value=$(this).val()
      const closest_val=$(this).closest('tr').find('.min_amount,.min_amountn').val()
      if(this_value==closest_val){
        new swal({
            title: "Same Invoice Amount Selected",
            button: "Ok",
          });
          $(this).val('')
      }
      if(parseInt(this_value) < parseInt(closest_val)){
        new swal({
          title: "Max Invoice Amount Should be greater than Min Invoice Amount",
          button: "Ok",
        });
        $(this).val('')
      }
    })


    
$(document).on('change','.min_amount,.min_amountn',function(){
const this_value=$(this).val()
const closest_val=$(this).closest('tr').find('.max_amount,.max_amountn').val()
if(this_value==closest_val){
new swal({
    title: "Same Invoice Amount Selected",
    button: "Ok",
  });
  $(this).val('')
}
if(closest_val!=''){
if(parseInt(closest_val) < parseInt(this_value)){
  new swal({
    title: "Max Invoice Amount Should be greater than Min Invoice Amount",
    button: "Ok",
  });
  $(this).val('')
}
}
})

$(document).on('change','.max_amount ',function(){
let min_val = parseFloat($(this).val().replace(/,/g, ''));
const this_value=$(this)
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})

$('.min_amount').each(function(){
let currency_val=$(this).closest('tr').find('.currency').val()
if(min_val!=$(this).val().replace(/,/g, '')){
  let max_val=this_value.closest('tr').find('.min_amount,.min_amountn').val()
  if(!(min_val< parseFloat($(this).val().replace(/,/g, ''))) &&max_val<parseFloat($(this).val().replace(/,/g, ''))){
      if(currency_val==this_currency_id){
        new swal({
        title: "Existing Range Selected",
        button: "Ok",
      });
          this_value.val('');

    }
  }

}
})
})


// signatory-user select tag click
$(document).on('change','.signatory-user',function(){
let user_id = $(this).val()
let this_element = $(this)
// if user is already selected in same row then disable option
$(this).closest('tr').find('.signatory-user').not($(this)).each(function(index,value){
  if (parseInt($(value).val()) === parseInt(user_id) && $(value).val() !== ''){
    Sweetalert2.fire({
    title: "User Already Selected",
  //  button: "Ok",
  });
  // empty the user
  this_element.val('')
}
})
})


// delete user
$(document).on('click','.delete-usaved-tr',function(){
// remove tr
$(this).closest('tr').remove()
})

$(document).on('change','.currency',function(){
$(this).closest('tr').find('.min_amount,.max_amount,.max_amountn,.min_amountn').val('')

})


$(document).on('click','.delete-unsaved-user',function(){
let this_element = $(this)
let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
$(this).closest('.row').remove()
//let set_no_of_user = $(this).closest('tr').find('.no_of_users').val(parseInt(get_no_of_user)-1)
//let get_no_of_user = $(this).closest('tr').find('.no_of_users').val()
})

$(document).on('change','.min_amount,.max_amount',function(){
let this_value=$(this)
let thisElement = $(this).val()
const this_currency_id = $(this).closest('tr').find('.currency').val()
$('.min_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amountn').each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
  let currency_val=$(this).closest('tr').find('.currency').val()
  console.log('val',currency_val)
  if(currency_val==this_currency_id){
    swal.fire({
      text: "Invoice Amount Range already exists",
      showCancelButton: false,
      confirmButtonText: "Ok",
      confirmButtonColor: '#3085d6',
    });
    this_value.val('')
  }
}
})
$('.max_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})
$('.min_amount').slice(0, -1).each(function(){
if(thisElement==$(this).val().replace(/,/g, '')){
let currency_val=$(this).closest('tr').find('.currency').val()
console.log('val',currency_val)
if(currency_val==this_currency_id){
  swal.fire({
    text: "Invoice Amount Range already exists",
    showCancelButton: false,
    confirmButtonText: "Ok",
    confirmButtonColor: '#3085d6',
  });
  this_value.val('')
}
}
})

})


$(document).on('change', '.min_amount, .min_amountn, .max_amount,.max_amountn', function(){
let thisElement = $(this)
console.log({'this element':thisElement})
const this_value = $(this).val()
console.log({'this_val':this_value})
const this_tr = $(this).closest('tr')
console.log({'this tr':this_tr})
const this_currency_id = this_tr.find('.currency').val()
console.log({'this currency id':this_currency_id})
$('.currency option[value="' + this_currency_id + '"]').filter('option:selected').not(thisElement.closest('tr')).each(function(index,value){
if($(value).val() == this_currency_id && $(value).closest('tr') !== this_tr) {
  max = $(value).closest('tr').find('.max_amount,.max_amountn').val()
  console.log({'max':max})
  let parsedMax = parseInt(max.replace(/,/g, ''));
  min = $(value).closest('tr').find('.min_amountn , .min_amount').val()
  let parsedMin = parseInt(min.replace(/,/g, ''));
  if (!isNaN(parsedMax) && !isNaN(parsedMin)) {
    console.log({'numberInRange':[parsedMin, parsedMax]})
    if (this_value != parsedMax && this_value != parsedMin){
    numberInRange(this_value, parsedMin, parsedMax, thisElement)
    }
  }
}
})
})

function numberInRange(num, first, second, thisElement) {
let max = Math.max(first, second);
let min = Math.min(first, second);
console.log({'min':min,'max':max});
if (num >= min && num <= max) {
swal.fire({
  text: "Invoice Amount Range already exists",
  showCancelButton: false,
  confirmButtonText: "Ok",
  confirmButtonColor: '#3085d6',
});
thisElement.val('')
}
return false;
}


$(document).on('change','select',function(){
$(this).removeClass('con_error')
})
// remove the class con_error on change
$(document).on('keyup','input',function(){
$(this).removeClass('con_error')
})

$(document).on('click','.delete_new_row',function(){
$(this).closest('tr').remove()
})






$(document).on('change','.settings_sign',function(){
  var value_tye=$(this).val()
  console.log('value_tye',value_tye)
  if(value_tye=='1'){
      $('.project_sign').removeAttr('style')
      $('.Default_sign').addClass('style').css('display', 'none');
      }
  else{
      $('.project_sign').addClass('style').css('display', 'none');
  }
  if(value_tye=='2'){
      $('.Default_sign').removeAttr('style')
  }
  else{
      $('.Default_sign').addClass('style').css('display', 'none');
  }
})

$(document).on('click','.delete-saved-tr',function(){
  const  get_data_id = $(this).data('id')
  const remove_tr = $(this).closest('tr')
  swal.fire({
  text: "Are you sure you want to delete this Record?",
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes',
  cancelButtonText: 'No',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatory",
      data: {'pk':get_data_id},
      success: function(data){
        remove_tr.remove()
      }
    });
  }
});
})


$(document).on('click','#delete-user',function(){
  var  get_data_id = $(this).data('id')
  console.log('get_data_id',get_data_id)
  let user_id = $(this).closest('td').find(`select[id="sign-user-id${get_data_id}"]`).val()
  // call the ajax function POST method
  // sweet alert for confirmation of delete if clicked yes then delete the user call the ajax function
  let this_element = $(this).closest('.row')
  let row_length = $(this).closest('tr').find('.row').length
  let del_user_val=$(this).closest('tr').find('.no_of_users')
  
  if (row_length > 1){
  swal.fire({
  text: "Are you sure you want to delete this user?",
  showCancelButton: true,
  confirmButtonText: "Yes",
  cancelButtonText: "No",
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
}).then(function(result) {
  if (result.value) {
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: "/invoiceguard/deletesignatoryuser",
      data: {'pk':get_data_id},
      success: function(data){
        let get_no_of_user = del_user_val.val()
        let set_no_of_user=del_user_val.val(parseInt(get_no_of_user)-1)
        this_element.remove()
      }
    });
  }
});
  }
  else{
      return false;
  }
})


$(document).on('change','.select-invoice',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice').css('display','none')
    $('.without_invoice').removeAttr('style')
  }
  else{
    $('.without_invoice').css('display','none')
    $('.with_invoice').removeAttr('style')
  }
})

$(document).on('change','.select-invoice-project',function(){
  if (parseInt($(this).val()) == 2){
    $('.with_invoice_project').css('display','none')
    $('.without_invoice_project').removeAttr('style')
  }
  else{
    $('.without_invoice_project').css('display','none')
    $('.with_invoice_project').removeAttr('style')
  }
})
