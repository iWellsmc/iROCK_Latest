

$(document).ready(function() {
  $('.bank-cls').summernote({
    toolbar: false,
    height: 100,
    });
  });
  
  
  $('form').on('submit',function(e){
    $('.userfield').each(function(index,val) {
      console.log('thisval',$(this).val())
      if ($(this).val() == '') {
        $(this).addClass('con_error')
      }
      else{
        $(this).removeClass('con_error')
      }
    })
            
     if ($('.con_error').length > 0){
          return false
      }
    
   
   });
  
  
   // prevent from open new window with new tab when clicked shift+enter key
  //  $(document).on('keypress','.bank_name,.acnumber,.contact_person',function(e){
  //     if (e.key === 'Enter' && e.shiftKey) {
  //         return false;
  //     }
  // });
  
  $(document).on('click','#adduser',function(){
   
    let userfield =`<tr class="usertr">
    <td> <input type="hidden" class="userid form-control" name="userid" value=""><select name="usertitle" class="form-control usertitle userfield">
      <option  value="" selected>--Select--</opiton>
      <option value='Mr'>Mr</opiton>
      <option value='Mrs'>Mrs</opiton>
      <option value='Ms'>Ms</opiton>
      </select>
    </td>
      <td><input type="text" class="userfirstname form-control userfield" name="userfirstname"></td>
      <td><input type="text" class="userlastname form-control userfield" name="userlastname"></td>
      <td><input type="email" class="useremail form-control userfield" name="useremail"></td>
      <td><input type="text" class="userdesignation form-control userfield" name="userdesignation"> </td>
      <td><button id="adduser" class='btn btn-clr  adduser' type='button' value='Add'> <i class="fa fa-plus"></i> <button id="removeuser" class='ml-2 btn btn-clr  removeuser' type='button'> <i class="fa fa-minus"></i> </button> </td>
  </tr>`
    let position = $(this).closest('tbody')
    position.append(userfield)
  })
  
  $(document).on('click','.removeuser',function(){
    $(this).closest('tr').remove()
  })
  
  $(document).on('click','.removeolduser',function(){
    get_tr=$(this).closest('table').find('tbody tr').length
    if(get_tr > 1){
        indexleg = $(this).closest('tbody').find('tr').length
        var userid = $(this).closest('tr').find('.userid').val()
        var dataid = $(this).closest('tr').find('.userid').attr('data-id')
        var usertitle =$(this).closest('tr').find('.usertitle').val()
        var userfirstname =$(this).closest('tr').find('.userfirstname').val()
        var userlastname =$(this).closest('tr').find('.userlastname').val()
        let position = $(this).closest('tbody')
      Swal.fire({
        title: `Are you sure you want to remove ${usertitle} ${userfirstname} ${userlastname} details?`,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, I Confirm',
        cancelButtonText: 'No',
      }).then((result) => {
        if (result.isConfirmed) {
          $.ajax({
            url:`/finance/removebankusers/`,
            headers: { 'X-CSRFToken': csrf_token },
            data: {
                'userid': userid,
                'dataid':dataid
            },
            type: "POST",
            success: function (data) {
              if(data.status){
                location.reload();  
              }  
              if (indexleg <= 1){
                let userfield =`<tr class="usertr">
                    <td> <input type="hidden" class="userid form-control" name="userid" value=""><select name="usertitle" class="form-control usertitle userfield">
                      <option  value="" selected>--Select--</opiton>
                      <option value='Mr'>Mr</opiton>
                      <option value='Mrs'>Mrs</opiton>
                      <option value='Ms'>Ms</opiton>
                      </select>
                    </td>
                      <td><input type="text" class="userfirstname form-control userfield" name="userfirstname"></td>
                      <td><input type="text" class="userlastname form-control userfield" name="userlastname"></td>
                      <td><input type="email" class="useremail form-control userfield" name="useremail"></td>
                      <td><input type="text" class="userdesignation form-control userfield" name="userdesignation"> </td>
                      <td><button id="adduser" class='btn btn-clr  adduser' type='button' value='Add'> <i class="fa fa-plus"></i> <button id="removeuser" class='ml-2 btn btn-clr  removeuser' type='button'> <i class="fa fa-minus"></i> </button> </td>
                  </tr>`
                  position.append(userfield)
                  console.log('userfield',userfield)
                  console.log('position',position)
              }        
            }
          });
        }
      })
    }
  })
  
  $(document).on('change','.useremail',function(){
    var currentloc=$(this)
    var emailval = $.trim($(this).val())
    var userid =$(this).closest('tr').find('.userid').val()
    
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token},
      url:"/finance/validateduplicateemail/",
      data: {
          "email":emailval,
          "userid":userid
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