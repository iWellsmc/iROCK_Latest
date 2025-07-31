$(document).on('click','#addact',function(){
  let actno = `<div class='edit_align_items'><input type="text" class="actno form-control" name="actno"><input type="hidden" class="actno form-control" name="actnodataid" value=" "> <button id='addact' class='btn btn-clr add-btn addact ml-2 mr-1' type='button' value='Add'><i class="fa fa-plus"></i> </button><button id="deleteact" data-id="1" class="btn btn-clr delete-btn delete delete_new_row" type="button" value="delete"> <i class="fa fa-minus"></i> </button></div>`
  let position = $(this).closest('tr').find('.acountnumber')
  position.append(actno)
})

$(document).on('click','#deleteact',function(){
  $(this).closest('div').remove()
})
$(document).on('click','#deleteactexist',function(){
  $.ajax({
  type:'POST',
  headers: { "X-CSRFToken": csrf_token},
  url: "/finance/validatebankname/",
  data:{'bankname':bankname,'bankid':bankid},
  success: function(data){
    if(data.status == true){
      swal.fire("Bank Already Exists")
      currentpos.val(" ")
    }
      }
})
})
$(document).on('click','#adduser',function(){
  let userfield =`<tr><td><input type="hidden" name='userid' value=" "><input type="text" class="firstname form-control" name="firstname"></td><td><input type="text" class="lastname form-control" name="lastname"></td><td><input type="text" class="email form-control" name="email"></td>
  <td><input type="text" class="designation form-control" name="designation"></td> <td class="d-flex"><button id='addact' class='mr-1 btn btn-clr add-btn addact' type='button' value='Add'><i class="fa fa-plus"></i></button><button id="deleteuser" class="btn btn-clr delete-btn delete delete_new_row" type="button" value="delete"> <i class="fa fa-minus"></i></button></td></tr>`
  let position = $(this).closest('tbody')
  position.append(userfield)
  
})


$(document).on('click','#deleteuser',function(){
  $(this).closest('tr').remove()
})


$(document).ready(function () {
  $('.dn_currencys').on('select2:select', function (e) {
      var $select2Container = $(this).next('.select2-container');
      $select2Container.removeClass('con_error').css("border", "");
  });

  $(document).on('click', '.mainsave', function (e) {
      var selectedOptions = $('.dn_currencys').select2('data');
      var $select2Container = $('.dn_currencys').next('.select2-container');

      if (selectedOptions.length == 0) {
          $select2Container.addClass('con_error').css("border", "1px solid red");
          e.preventDefault();
      }
  });
});




$(document).on('change','.bank_name',function(){
 var bankid = $(this).attr('data-id')
  var bankname = $(this).val()
  var currentpos = $(this)
  var savebtn = $('.mainsave')
  console.log('bankid',bankid)
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
$(document).ready(function() {
  $('.otherdetails').summernote({
    toolbar: false,
    height: 100,
    });
  });
  
  $(document).on('click', '.mainsave', function(e){
    console.log('bankname',$('.bank_name').val())
    if($.trim($('.bank_name').val()) == '') {
        $('.bank_name').addClass('con_error')
      }else{
        $('.bank_name').removeClass('con_error')
      }
    
    $('.actno').each(function(index,val) {
    
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }else{
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
     
//    var selectedTexts = $('#hdn_currency').val();
  
//    if(selectedTexts.length == 0){
//      $('.select2-selection').addClass('con_error')
//      e.preventDefault();
//    }
//    else{
//      $('.select2-selection').removeClass('con_error')
//    }

  
 
//  if ($('.con_error').length > 0){
//    return false
//  }
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
 var query = $.trim($(this).val());
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

  $(document).on('keyup','.bank_name',function(){
    $(this).removeAttr('style')
    $(this).removeClass('con_error') 
  
  });
