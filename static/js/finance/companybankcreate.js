var formCount = 1;
var addcount=1
$(document).on('click','.add-btn',function(){
  let add_function=`<tr class='tabletr'><td><select class="form-control form-select currency" name="currency"><option value="">--Select--</option></select></td><td><select class="form-control form-select accountno" name="accountno"><option value="">--Select--</option></select></td> 
    <td><table class="inner-table usertable m-bank-user"><tbody>
    <tr class="usertr"><td class="user-title"><select name="usertitle" class="form-control form-select usertitle userfield"><option value='' selected>--Select--</opiton>
    <option value='Mr'>Mr</opiton><option value='Mrs'>Mrs</opiton><option value='Ms'>Ms</opiton>
    </select></td><td><input type="text" class="userfirstname userfield form-control" name="userfirstname"></td>
    <td><input type="text" class="userlastname userfield form-control" name="userlastname"></td><td><input type="email" class="useremail userfield form-control" name="useremail"></td><td><input type="text" class="userdesignation userfield form-control" name="userdesignation"> </td><td class="maintableuser-action-wid"><button id="adduser" class='btn btn-clr adduser' type='button' value='Add'> <i class="fa fa-plus"></i> </button></td>
    </tr></tbody></table></td>
    <td><table class="inner-table paymentinstructer m-bank-user"><td><select name="instructortitle" class="form-control form-select instructortitle"><option selected>--Select--</opiton><option value='Mr'>Mr</opiton><option value='Mrs'>Mrs</opiton>
    <option value='Ms'>Ms</opiton></select></td><td><input type="text" class="firstname form-control" name="instructorfirstname"></td><td><input type="text" class="lastname form-control" name="instructorlastname"></td></tr></tbody></table></td>
    <td><button id='add' class='btn btn-clr add-btn pha-sebtn add' type='button' value='Add'> <i class="fa fa-plus"></i><button id="delete-user" class="btn btn-clr desc-count delete-btn" data-id="1" type="button" value="delete"> <i class="fa fa-minus"></i></button><button id="delete-user" class="mt-3 btn btn-clr copyprevious_btn" data-id="1" type="button" value="delete">Copy From Previous</button></td></tr>`
  $(this).closest('tbody').append(add_function)
  $('#master_project_list').find('tr:last').find('#bank-address').summernote({toolbar: false,height: 50 })
 
  console.log('#hdn_users'+addcount)
  var data=$('#hdn_users'+addcount).select2()
  addcount++;
    console.log('data',data)
   
    $('.currency-cls').select2({
        placeholder: "Select Users"
    });
    formCount++;
   
})  

$(document).on('click','#adduser',function(){
  // firstcount = $(this).closest('tr').closest('table').closest('tr').index()
  // secondcount = $(this).closest('tr').index()
  // console.log('usercount',firstcount,secondcount)
  let userfield =`<tr class='usertr'> <td><select name="usertitle" class="usertitle userfield form-control form-select"><option value='' selected>--Select--</opiton><option value='Mr'>Mr</opiton><option value='Mrs'>Mrs</opiton>
  <option value='Ms'>Ms</opiton></select></td><td><input type="text" class="userfield userfirstname form-control" name="userfirstname"></td><td><input type="text" class="userfield userlastname form-control"name="userlastname"></td><td><input type="email" class="userfield useremail form-control" name="useremail"></td><td><input type="text" class="userfield userdesignation form-control" name="userdesignation"> </td><td><button id="adduser" class='btn btn-clr  adduser' type='button' value='Add'> <i class="fa fa-plus"></i></button><button id="delete-user" class="ml-2 btn btn-clr desc-count delete-btn" data-id="1" type="button" value="delete"> <i class="fa fa-minus"></i></button></td></tr>`
  let position = $(this).closest('tbody')
  position.append(userfield)
})

$(document).ready(function() {
$('#bank-address').summernote({
  toolbar: false,
  height: 100,
});
});

$(document).on('click','#add',function(){
    closesttr = $('.maintable').find('.tabletr:last')
    bankid = $('.select_bank').val()
    currency = closesttr.find('.currency')
    accountno = closesttr.find('.accountno')
    users = closesttr.find('.currency-cls')
   $.ajax({
type:'POST',
headers: { "X-CSRFToken": csrf_token},
url: '/finance/getbankinformation/',
data:{'bankid':bankid},
success: function(data){
  var html=''
  var act=''
  var user=''
  html +='<option value="">--Select--</option>'
  act +='<option value="">--Select--</option>'
  user +='<option value="">--Select--</option>'
  $.each(data.currency,function(key,val){
    html +='<option value='+val.id+'>'+val.currency_symbol+'-'+val.currency+'('+val.name+')'+'</option>'
  })  
  $.each(data.accountnumber,function(key,val){
    act +='<option value='+val.id+'>'+val.accountno+'</option>'
  }) 
  // $.each(data.users,function(key,val){
  //   user +='<option value='+val.id+'>'+val.name+' '+val.lastname+' -- ('+val.designation_role+')</option>'
  // }) 
  currency.html(html)
  accountno.html(act)
  // users.html(user)
}
})
})

   
$(document).on('click','.delete-btn',function(){
    let trLength = $(this).closest('.table-list').find('tr').length;
    if (trLength < 2){
      return false;
    }
    else{
      $(this).closest('tr').remove()
      return true
    }
  })
  
  

  $(document).ready(function() {
    
  $('form').on('submit',function(e){
    if ($(this).data('submitted')) {
      e.preventDefault(); // Prevent form submission if already submitted
  } else {
      $(this).data('submitted', true);
      $('#submitBtn').prop('disabled', true); // Disable the submit button
  }
    scount = 0; 
    usercount=1
    $('.currency-cls').each(function(){
      $(this).attr('name','users'+usercount)
       usercount++
    })
    var selectedTexts = $('.currency-cls').val();
    if(selectedTexts.length == 0){
    $('.select2-selection').addClass('con_error')
       e.preventDefault();
     }
   else{
       $('.select2-selection').removeClass('con_error')
    }
    if($('.select_bank').val()==''){
     $('.select_bank').addClass('con_error')
    }
    else{
     $('.select_bank').removeClass('con_error')
    }
   $('.currency, .bank_name, .accountno, .contact_pernonnel').each(function(index,value){
     scount ++;
    
       if ($(value).val() == '') {
           $(value).addClass('con_error')
         //  $('.note-editor').addClass('con_error')
         }else{
           $(value).removeClass('con_error')
       }
       });
      
       $('.bank_address').each(function(index,value){
       
         if ($(value).val() == '') {
           $(this).next('.note-editor').addClass('con_error')
         }
      }) 
     
  if ($('.con_error').length > 0){
       return false
   }
   $('.bank_address').summernote();
 var content = $('.bank_address').summernote('code');
 content = content.replace(/<br[^>]*>/g, '');
 content = content.replace(/<\/br>/g, '');
 $('.bank_address').summernote('code', content);


          

});
  });
$(document).on('click','.select_bank',function(){
if(bankcount == 0){
 Swal.fire('Please Add Bank Details')
}
})
// $(document).on('change','.bank_name,.currency,.accountno,.contact_pernonnel,.note-editor,.select_bank',function(){
//      $(this).removeClass('con_error')
//      console.log({'change':$(this)})
// })
   
 $(document).on('keyup','.acnumber',function(){
  var val=$(this).val()
  var currentelement=$(this)
  var savebtb = $('#mainsave')

  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token},
      url: "{% url 'finance:validate-actno-form' %}",
      data: {'actno':$.trim(val)},
      
      success: function(data){
          if (data.status == true){ 
                  currentelement.next('.invoicenumspn').html("<p class='ptag'>Account number Already Exists</p>")
                  var x = 1;
                  $('#mainsave').attr('disabled',true) 

           }
           else{
             currentelement.next('.invoicenumspn').html("")
             $('#mainsave').attr('disabled',false) 
           }
         }
   });
 })
 $(document).on('keyup','.note-editable',function(){
   console.log({'note-edit':$(this).closest('.note-editing-area').closest('.note-editor')})
   $(this).closest('.note-editing-area').closest('.note-editor').removeClass('con_error')
   // $('.note-editor').removeClass('con_error')
   })
 $(document).on('blur','.actno',function(){
   var $th = $(this);
   // $th.val($th.val().replace(/[^0-9A-Za-z]/g, ''))
   var val=$(this).val()||null
   var duplicatecount=0
   var spancount=0
   var currentelement=$(this)
   if (val != null){
   $('.actno').each(function(){
     if ( $.trim($(this).val()) ==  $.trim(val)){
           duplicatecount++;
       }
      
     })
   }
     $('.acnumber').each(function(){
      if ($(this).closest("tr").find("p").hasClass('ptag')) {
         spancount++
       }
       });
       if(spancount > 0)
       {
         $('#mainsave').attr('disabled',true) 
       }
       else{
         $('#mainsave').attr('disabled',false)  
       }
   console.log({"count":spancount})
   // alert(spancount)
   if (duplicatecount > 1  )
   {
     currentelement.next('.invoicenumspn').html("<p class='ptag' >Account number Already Exists</p>").show()
     $('#mainsave').attr('disabled',true) 
   }
   if (duplicatecount == 0  ){
     $('#mainsave').attr('disabled',false)   
   }
 
 })

// prevent from open new window with new tab when clicked shift+enter key
$(document).on('keypress','.bank_name,.acnumber,.contact_person',function(e){
   if (e.key === 'Enter' && e.shiftKey) {
       return false;
   }
});

 

$(document).ready(function() {
  var submissionCount = 0;
  var maxSubmissions = 2; // Change this to the desired number of submissions

  $("form").submit(function(event) {
      submissionCount++;
      if (submissionCount >= maxSubmissions) {
          $("#mainsave").prop('disabled', true);
      }
  });
});

$(document).on('change','.select_bank',function(){
bankid = $('.select_bank').val()
currency = $('.currency')
accountno = $('.accountno')
users = $('.currency-cls')
$.ajax({
type:'POST',
headers: { "X-CSRFToken": csrf_token},
url: '/finance/getbankinformation/',
data:{'bankid':bankid},
success: function(data){
 var html=''
 var act=''
 var user=''
 html +='<option value="">--Select--</option>'
 act +='<option value="">--Select--</option>'
 
 $.each(data.currency,function(key,val){
   html +='<option value='+val.id+'>'+val.currency_symbol+'-'+val.currency+'('+val.name+')'+'</option>'
 })  
 $.each(data.accountnumber,function(key,val){
   act +='<option value='+val.id+'>'+val.accountno+'</option>'
 }) 

 currency.html(html)
 accountno.html(act)

}
})
})

$(document).ready(function() {
   var data=$('#hdn_currency').select2()
   console.log(data)
   if (data != ''){
       data = data.replace("[",'');
       data = data.replace("]",'');
       data = data.replaceAll("'",'');
       data = data.replaceAll(" ",'');
       console.log(data);        
       var convert_list = data.split(',');
       console.log(convert_list)
       $(".currency-cls").val(convert_list)
   }
   $('.currency-cls').select2({
       placeholder: "Select Currency"
   });
});

$(document).on('change','.currency',function(){
$(this).closest('tr').find('.accountno').val('')
})
$(document).on('change','.accountno',function(){
let currentpos = $(this)
let actno = $(this).val()
let currency = $(this).closest('tr').find('.currency').val()
let bankid = $('.select_bank').val()
console.log('vals--',actno,currency)
duplicateact=0
duplicatecurrency=0
$('.accountno').each(function(){
 if($(this).val()==actno){
     if($(this).closest('tr').find('.currency').val() == currency ){
       duplicateact++
     }
 }
})
if(duplicateact > 1){
Swal.fire('Account Number Already Selected') 
$(this).val('')
}
$.ajax({
type:'POST',
headers: { "X-CSRFToken": csrf_token},
url: "{% url 'finance:validateduplicatebank' %}",
data:{'actnoid':actno,'currency':currency,'bankid':bankid},
success: function(data){
 if(data.status == true){
 Swal.fire('Account Number Already Exits') 
 currentpos.val('')
 }
}
})

})

$(document).on('click','#mainsave',function(){
  $('.tabletr').each(function(){
     count1=$(this).index()
      $(this).find('.usertr').each(function(){
        count2 = $(this).index()
        $(this).find('.usertitle').attr('name','usertitle'+count1)
        $(this).find('.userfirstname').attr('name','userfirstname'+count1)
        $(this).find('.userlastname').attr('name','userlastname'+count1)
        $(this).find('.useremail').attr('name','useremail'+count1)
        $(this).find('.userdesignation').attr('name','userdesignation'+count1)
      })
  })
  $('.currency').each(function(index,val) {
    if ($(this).val() == '') {
      $(this).addClass('con_error')
    }else{
      $(this).removeClass('con_error')
    }
  })
  $('.accountno').each(function(index,val) {
    if ($(this).val() == '') {
      $(this).addClass('con_error')
    }else{
      $(this).removeClass('con_error')
    }
  })
 
    if ($('.select_bank').val() == '') {
      $('.select_bank').addClass('con_error')
    }else{
      $('.select_bank').removeClass('con_error')
    }
    $('.userfield').each(function(index,val) {
      console.log('thisval',$(this).val())
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }
      else{
        $(this).removeClass('con_error')
      }
    })
  if ($('.con_error').length > 0) {
    return false
  }
})  

$(document).on('click','.copyprevious_btn',function(){
  //paymentinstructer clone
  var paymentinstructer = $(this).closest('tr').prev('tr').find('.paymentinstructer').find('tbody').clone();
  $(this).closest('tr').find('.paymentinstructer').html(paymentinstructer)
  $(this).closest('tr').find('.paymentinstructer').find('.instructortitle').val($(this).closest('tr').prev('tr').find('.paymentinstructer').find('tbody').find('.instructortitle').find(':selected').val())

  //user clone
  var usertable = $(this).closest('tr').prev('tr').find('.usertable').find('tbody').clone();
  $(this).closest('tr').find('.usertable').html(usertable)
  current_element=$(this).closest('.tabletr').find('.inner-table').find('.usertitle')
  $(this).closest('tr').prev('tr').find('.usertable').find('tbody').find('.usertitle').each(function(index,value){
    let val=$(value).find(':selected').val()
    let current_field=current_element[index]
    $(current_field).val(val);
  })
})

$(document).on('change','.useremail',function(){
  $(this).next('p').remove()
  var regexPattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i 
  inputValue = $(this).val()
  if (regexPattern.test(inputValue)) {
    $(this).removeClass('con_error')
    $(this).next('p').remove()
  } else {
    $(this).addClass('con_error')
    $(this).after('<p class="warningtag con_error">Please Provide a Valid Email ID</p>')
  }
  
})

$(document).on('change','.useremail',function(){
  var currentloc=$(this)
  var emailval = $.trim($(this).val())
  var savebtn = $('.mainsave')
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token},
    url:"/finance/validateduplicateemail/",
    data: {
        "email":emailval,
    },
   
    success: function(data)
    {
      if(data.status == true )
      {
        swal.fire("Email ID Already Exists")
        currentloc.val(" ")
      }
     }
})
})

 
