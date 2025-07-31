$(document).on('click','.add_button',function(e){
  e.preventDefault();
  let html=$(this).closest('tr').clone();
  html.find('.design').val('')
  html.find('.get_users').removeClass('con_error')
  html.find('.get_users').val('')
  html.find('.designation').val('')
  html.find('.dep').val('')
  html.find('.grp').val('')
  html.find('.email').val('')
  $(this).closest('tbody').append(html)
})

$(document).on('click','.del_button',function(e){
  e.preventDefault();
  $(this).closest('tr').remove()
})

$(document).on('click','.del_user',function(e){
  let this_row=$(this)
  let get_id=$(this).attr('data-id')
  $.ajax({
    url: "deletedisputeuser",
    type: "POST",
    data: {
      "user_id": get_id,
    },
    headers: {'X-CSRFToken': csrftoken },
    success: function (data) {
      if (data.status){
        this_row.closest('tr').remove();
      }
    }
  });

})


$(document).on('change','.get_users',function(){
  const this_row=$(this)
  let count=0
  $('.get_users').not(this_row).each(function(){
    if($.trim($(this).val()) != ''){
    if($(this).val() == this_row.val()){
      count++
    }
    }
  })
  this_row.removeClass('con_error')
  let get_id=$(this).val()
  if(get_id != ''){
    $.ajax({
      url: "duplicateusercheck",
      type: "POST",
      data: {
        "user_id": get_id,
        'type_dispute':1,
      },
      headers: {'X-CSRFToken': csrftoken },
      success: function (data) {
        console.log(data)
        if (data.status || count>=1){
          swal.fire('Existing User Selected')
          this_row.val('')
        }
        else{
          this_row.closest('tr').find('.designation').val(data.userlist[0]['designation_role'])
          this_row.closest('tr').find('.dep').val(data.deparment)
          this_row.closest('tr').find('.grp').val(data.group)
          this_row.closest('tr').find('.email').val(data.userlist[0]['email'])
        }
      }
    })
  }
  
})


$(document).on('click','.mainsave',function(e){
  let count=0
  $('.get_users').each(function(){
    if($(this).find('option:selected').val() == ''){
      $(this).addClass('con_error')
      count++
    }
  })
  if(count == 0){
    $('#addmembers').submit()
  }
  else{
    e.preventDefault();
    return false
  }
})

$(document).on('change','.edit_users_committee',function(){
  const this_row=$(this)
  this_row.removeClass('con_error')
  let get_id=$(this).val()
  if(get_id != ''){
    console.log('host')
    $.ajax({
      url: `${currentdomain}/duplicateusercheck`,
      type: "POST",
      data: {
        "user_id": get_id,
        'type_dispute':2,
        'pk':pk,
      },
      headers: {'X-CSRFToken': csrftoken },
      success: function (data) {
        if (data.status){
          swal.fire('Existing User Selected')
          this_row.val('')
          this_row.closest('tr').find('.designation').val('')
          this_row.closest('tr').find('.dep').val('')
          this_row.closest('tr').find('.grp').val('')
          this_row.closest('tr').find('.email').val('')
        }
        else{
          this_row.closest('tr').find('.designation').val(data.userlist[0]['designation_role'])
          this_row.closest('tr').find('.dep').val(data.deparment)
          this_row.closest('tr').find('.grp').val(data.group)
          this_row.closest('tr').find('.email').val(data.userlist[0]['email'])
        }
      }
    })
  }
  
})
$(document).on('click','.assigned_projects',function(){

  $('.assigned_projects_table').toggle();
  $('.user_profile').toggle();
    console.log('HIIIII');


})