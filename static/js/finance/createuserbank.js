var get_list= [];
$(document).on('click','#addact',function(){
   let actno = `<div class='create_align_items'><input type="text" class="actno form-control" name="actno"><button id="deleteact" data-id="1" class="ml-2 btn btn-clr delete-btn delete delete_new_row" type="button" value="delete"> <i class="fa fa-minus"></i> </button></div>`
   let position = $(this).closest('tr').find('.acountnumber')
   position.append(actno)
})

$(document).on('click','#deleteact',function(){
    $(this).closest('div').remove()
})

$(document).on('click','#adduser',function(){
  let userfield =`<tr><td><input type="text" class="firstname form-control" name="firstname"></td><td><input type="text" class="lastname form-control" name="lastname"></td><td><input type="text" class="email form-control" name="email"></td>
  <td><input type="text" class="designation form-control" name="designation"></td><td><button id="deleteuser" class="mt-3 btn btn-clr delete-btn delete delete_new_row" type="button" value="delete"> <i class="fa fa-minus"></i></button></td></tr>`
  let position = $(this).closest('tbody')
  position.append(userfield)
})


$(document).on('click','#deleteuser',function(){
  $(this).closest('tr').remove()
})

$(document).on('keyup','.actno',function(){
  
  $(this).removeAttr('style')
  $(this).removeClass('con_error')
  let duplicates = 0
  const this_tr=$(this)
  console.log(this_tr,'thie tr...')
  let currentval = $.trim($(this).val())
  console.log(currentval,'currentval...')
  $('.actno').not(this_tr).each(function(){
  if(currentval == $(this).val()){
    duplicates++
    this_tr.addClass('con_error')
  } 
 })



 if(duplicates == 0){
  this_tr.removeClass('con_error')
  this_tr.removeAttr('style')
  // $('.mainsave').attr('disabled',false)
 }
 else{
  this_tr.css('border', "1px solid red")
  // $('.mainsave').attr('disabled','disabled')
 }
})


$(document).on('change','.actno',function(){
  let currentval = $.trim($(this).val());

   if (!/^[a-zA-Z0-9]*$/.test(currentval)){
    $(this).addClass('con_error');
   
   }else{
    $(this).removeClass('con_error');
    
   }
  });


$(document).on('click', '.mainsave', function(e){
 
  $(".dn_currencys").each(function() {
    console.log('val-----',$(this))
    length_currency = $(this).next(".select2-container").find('.select2-selection__rendered').find('li').length
        if (length_currency == 0) {
          $(this).next(".select2-container").addClass("con_error").css("border", "1px solid red");
              $('.mainsave').attr('disabled','disabled')
              e.preventDefault();
          }else{
            $(this).next(".select2-container").removeClass("con_error").css("border", "");
          }
  });
  $('.bank_name').each(function(index,val) {
    if ($.trim($(this).val()) == '') {
      $(this).addClass('con_error')
    } else {
      $(this).removeClass('con_error');  
    }
  });

  

  $('.actno').each(function(index,val) {
  
    if ($.trim($(this).val()) == '') {
      $(this).addClass('con_error')
    } 
  })
});

 
$(document).ready(function() {
  var formSubmitted = false;
  $('#mainform').on('submit', function(e) {
    if (formSubmitted) {
      e.preventDefault();
      return;
    }
    $('.mainsave').attr('disabled', 'disabled');
    formSubmitted = true;
  });
});

//   $('.otherdetails').each(function(index,value){
       
//     if ($(value).val() == '') {
//       $(this).next('.note-editor').addClass('con_error')
//     }
//     else{
//       $(this).next('.note-editor').removeClass('con_error')
//     }
//  }) 

// if ($('.con_error').length > 0){
//   return false
// }
// $('.otherdetails').summernote();
// var content = $('.otherdetails').summernote('code');
// content = content.replace(/<br[^>]*>/g, '');
// content = content.replace(/<\/br>/g, '');
// $('.otherdetails').summernote('code', content);

// })


$(document).ready(function() {
  $('.otherdetails').summernote({
    toolbar: false,
    height: 100,
  });
  var data=$('#hdn_userss').select2()
  $('.currency-clss').select2({
        placeholder: "Select Currency"
    });
    $(".currency-clss option").each(function(key,value) {

      get_list.push({'id':$(this).val(),'name':$(this).text()}); 
      console.log({'get list':get_list})      
  });
  });
  
var addcount=1;
$(document).on('click','.addbtn',function(){
  let clone = `<tr class="tabletr"><td class="from-invoice"><input type="text" class="bank_name form-control" name="bankname"></td><td class="from-invoice"><select class="currency-cls selectcurrency dn_currencys form-control gener-hd-input"  id="hdn_currency${addcount}" multiple="multiple"  name="currency" placeholder="Currency"></select></td><td class="add-sign acountnumber"><div class='create_align_items'><input type="text" class="actno form-control" name="actno"><button id='addact' class='btn btn-clr add-btn addact ml-2' type='button' value='Add'><i class="fa fa-plus"></i> </button></div></td><!-- <td class="from-invoice"><input type="text" class="otherdetails form-control" name="otherdetails"></td> --><td class="text-left"><textarea class="form-control otherdetails bankotherdetails" name="otherdetails" id="bank-address" type="text" ></textarea></td><td><button id='add' class='btn btn-clr add-btn pha-sebtn mt-3 addbtn' type='button' value='Add'> <i class="fa fa-plus"></i>
  <button  class="mt-3 btn btn-clr desc-count delete-btn" data-id="1" type="button" value="delete"> <i class="fa fa-minus"></i> </button></td></tr>`
   let position = $(this).closest('tbody')
   position.append(clone)
   $('#master_project_list').find('tr:last').find('.otherdetails').summernote({toolbar: false,height: 50 })  
   var data= $('#master_project_list').find('tr:last').find('#hdn_users'+addcount).select2()
   addcount++;
   $('#master_project_list').find('tr:last').find('.currency-cls').select2({
        placeholder: "Select Currency"
    });
  
    var get_element=$('#master_project_list').find('tr:last').find('.currency-cls')
    var option='<option value="">--Select--</option>'
    $(get_list).each(function (key,val) {
        option += '<option value="'+val.id+'">'+val.name+'</option>'
    })
    get_element.append(option);
  })

$(document).on('keyup','.bank_name,.actno,.panel',function(){
  countWithStyle=0
  $('.bank_name,.actno,.panel').each(function () {
    // Check if the current input element has the 'style' attribute with the specific value
    if ($(this).attr('style') === '1px solid red') {
      countWithStyle++;
    }
    else if($(this).hasClass('con_error')){
      countWithStyle++;
    }
});
if(countWithStyle == 0){
  $('.mainsave').removeAttr('disabled')
}
})

$(document).on('click','.delete-btn',function(){
  countWithStyle=0
  $('.bank_name,.actno,.otherdetails').each(function () {
    // Check if the current input element has the 'style' attribute with the specific value
    if ($(this).attr('style') === '1px solid red') {
      countWithStyle++;
    }
    else if($(this).hasClass('con_error')){
      countWithStyle++;
    }
});
if(countWithStyle == 0){
  $('.mainsave').removeAttr('disabled')
}
  $(this).closest('tr').remove()
})
$('#mainform').submit(function(event) {
  $('.tabletr').each(function(){
    count=$(this).index()
    $(this).find('.selectcurrency').attr('name','currency'+count)
    $(this).find('.actno').attr('name','actno'+count)
   })
})

$(document).on('change','.bank_name',function(){
  const this_tr=$(this)
  let duplicates = 0
  let currentval = $.trim($(this).val())
  $('.bank_name').not($(this)).each(function(){
  if(currentval.toLowerCase() == $.trim($(this).val()).toLowerCase()){
    duplicates++
  }
 })
 if(duplicates >= 1){
  this_tr.addClass('con_error')
  // $(this).css('border',"1px solid red")
  // $('.mainsave').attr('disabled','disabled')
 }
 else{
  this_tr.removeClass('con_error')
  // $(this).css('border', "")
  // $('.mainsave').attr('disabled',false)
 }
})
$(document).on('keyup','.panel',function(){
  $(this).removeAttr('style')
  $(this).removeClass('con_error')
})

$(document).on('change','.bank_name',function(){
  var bankid =''
  var bankname = $.trim($(this).val())
  var currentpos = $(this)
  var savebtn = $('.mainsave')
  $.ajax({
    type:'POST',
    headers: { "X-CSRFToken": csrf_token},
    url: "/finance/validatebankname/",
    data:{'bankname':bankname,'bankid':bankid},
    success: function(data){
      if(data.status == true){
        swal.fire("Bank Already Exists")
        currentpos.val("")
      }
        }
  })
})

$(document).on('click', '.mainsave', function(e){
  console.log('bankname',$('.bank_name').val())
  if($.trim($('.bank_name').val()) == '') {
      $('.bank_name').addClass('con_error')
    }else{
      $('.bank_name').removeClass('con_error')
    }

    $('.bank_name').each(function(index,val) {
  
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
        $(this).removeClass('con_error')
      }
    })
    
  
  $('.actno').each(function(index,val) {
  
    if ($(this).val() == '') {
      $(this).addClass('con_error')
    }else if (!/^[a-zA-Z0-9]*$/.test($(this).val())){
      $(this).addClass('con_error');
     } 
    
    else{
      $(this).removeClass('con_error')
    }
  })
  if ($('.con_error').length > 0) {
    
    return false
  }
  

  $('.tabletr').each(function(){
    count=$(this).index()
    $(this).find('.selectcurrency').attr('name','currency'+count)
    $(this).find('.actno').attr('name','actno'+count)
   })
   
 var selectedTexts = $('#hdn_currency').val();

 if(selectedTexts.length == 0){
   $('.select2-selection').addClass('con_error')
   e.preventDefault();
 }
 else{
   $('.select2-selection').removeClass('con_error')
 }



// if ($('.con_error').length > 0){
//   alert('ll');
  
//  return false
// }

$('.otherdetails').summernote();
var content = $('.otherdetails').summernote('code');
content = content.replace(/<br[^>]*>/g, '');
content = content.replace(/<\/br>/g, '');
$('.otherdetails').summernote('code', content);
})

$(document).on('keyup','.actno',function(){
  $(this).removeAttr('style')
  $(this).removeClass('con_error')
  let duplicates = 0
  const this_tr=$(this)
  let currentval = $.trim($(this).val())
  $('.actno').not(this_tr).each(function(){
  if(currentval == $(this).val()){
    duplicates++
    this_tr.addClass('con_error')
  }
 })
 if(duplicates == 0){
  this_tr.removeClass('con_error')
  this_tr.removeAttr('style')
  $('.mainsave').attr('disabled',false)
 }
 else{
  this_tr.css('border', "1px solid red")
  $('.mainsave').attr('disabled',true)
 }
 var currentpos = $(this)
 var query = $(this).val();
     $.ajax({
         url: '/projects/check_accountno/',  
         type: 'GET',
         data: {
             'account_no': query , 
         },
         success: function(data) {
          if(data.account_num == true){
            swal.fire("Account number already exists")
            currentpos.val("")
          }
         },
         error: function(xhr, status, error) {
             console.log('Error: ' + error); 
         }
     });
 

})



  $(document).on("change", ".select2-container", function() {
    

    if ($(".select2-container").val()) {
            $(".select2-container").css("border", "");
        } 
    });

$(document).on("click", ".select2-container.con_error", function() {
    $(this).removeClass("con_error").css({
        "border": "",
        
    });
});

$(document).on('change','.dn_currencys',function(){
  $('.mainsave').attr('disabled',false)
})

$(document).on('click', ".addbtn", function() {
    $('.mainsave').attr('disabled', false); 
});

$(document).on('keyup','.bank_name',function(){
  $(this).removeAttr('style')
  $(this).removeClass('con_error') 

});

$(document).on('keyup', '.actno', function(){
  let currentval = $.trim($(this).val());
  let errorMessageElement = $(this).siblings('.error-message'); 
  
  console.log(currentval);

  if(errorMessageElement.length === 0) {
    $(this).after('<span class="error-message"></span>');
    errorMessageElement = $(this).siblings('.error-message');
  }

  if (!/^[a-zA-Z0-9]*$/.test(currentval)){
    $(this).addClass('con_error');
    errorMessageElement.text('Please type only numbers.');
    errorMessageElement.css('color', 'red');
  } else {
    $(this).removeClass('con_error');
    errorMessageElement.text('');
  }
});




$(document).ready(function() {
  function validateBankName(input) {
      var bankname = $(input).val();
      var new_name = bankname.replace(/[^a-zA-Z\s]+/g, "");
      $(input).val(new_name);
  }
  $('.bank_name').on('input', function() {
      validateBankName(this);
  });
  $('#master_project_list').on('input', '.bank_name', function() {
      validateBankName(this);
  });

  function validateAccountNumber(input) {
    var banknumber = $(input).val();
    var new_number = banknumber.replace(/[^a-zA-Z0-9]+/g, ""); 
    $(input).val(new_number);
  }



  $('.actno').on('input', function() {
      validateAccountNumber(this);
  });


  $('#master_project_list').on('input', '.actno', function() {
      validateAccountNumber(this);
  });

  function validateDetails(input) {
    var bankdetails = $(input).val();
    var new_number = bankdetails.replace(/[^a-zA-Z0-9]+/g, ""); 
    $(input).val(new_number);
  }
  $('.bankotherdetails').on('input', function() {
    validateDetails(this);
});


$('#master_project_list').on('input', '.bankotherdetails', function() {
  validateDetails(this);
});
  
});