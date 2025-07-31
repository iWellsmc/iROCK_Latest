$(document).ready(function(){
  // var get_master=$('.master_data').attr('data-id')
  // var total_length=parseInt(get_master)+2
  // let count_master=0
  // console.log('total_length',total_length)
  // console.log('get_master',get_master)
  // $('.editabletr').each(function(){
  //   if($(this).children().length != total_length){
  //     count_master++
  //   }
  // })
  // if ($('.search_master').children().length == 0){
  //   count_master++
  // }
  // if(count_master != 0){
  //   swal.fire({
  //     text: 'Wrong Excel Sheet Uploaded',
  //     showDenyButton: false,
  //           confirmButtonColor: '#77d61f',
  //           denyButtonColor:'#AF2B50',
  //           confirmButtonText: 'Yes',
  //           customClass: {
  //             actions: 'my-actions',
  //             confirmButton: 'order-2',
  //             denyButton: 'order-3',
  //           }
  //   }).then((result) => {
  //     if (result.isConfirmed) {
  //       var current_url=$(location).attr("href")
  //       var replace_url=current_url.replace('importcostcodegenerate/','costcodelist')
  //       window.location.href = replace_url;
  //     }
  //   })
  //   $('.final-cls').attr('disabled',true)
  // }
  $('.commoncls').each(function(){
    // let set_value=$(this).find("option:selected").attr('cost_code')
    // $(this).closest('td').find('.cost_code_static').val(set_value)
    // $(this).closest('td').find('.costcode').val(set_value)
    // $(this).closest('td').find('.costcode_val').val(set_value)
    let set_value=$(this).attr('cost_code')
    if (set_value){
      $(this).closest('td').find('.cost_code_static').val(set_value)
      $(this).closest('td').find('.costcode').val(set_value)
      $(this).closest('td').find('.costcode_val').val(set_value)
    }

  })
})

$(document).ready(function(){
  var levelstartwithlen = levelstartwith.toString().length
    $('.leveloneoptions').each(function(){
       if(levelstartwith.toString().length < levelstartwithlen){
        levelstartwith=String(levelstartwith).padStart(levelstartwithlen, '0');
      }
      $(this).attr('data-id',levelstartwith)
      console.log('levelstartwith11',levelstartwith)
      levelstartwith = parseInt(levelstartwith) + (parseInt(levelonesequencegap)+1)
  })
  let iterate = disciplinestartwith
  var levelstartwithlen = iterate.toString().length
  $('.leveltwooptions').each(function(){
    if(iterate.toString().length < levelstartwithlen){
      iterate=String(iterate).padStart(levelstartwithlen, '0');
    }
       $(this).attr('data-id',iterate)
       iterate = parseInt(iterate) + (parseInt(disciplineseq)+1)
  })
  // $('#level1_costcode').val($('#level1_category').find(':selected').attr('data-id'))
  // $('#level2_costcode').val($('#level2_category').find(':selected').attr('data-id'))
  // level1=$('#level1_category').val()
  // level2=$('#level2_category').val()
})
// $(document).on('click','#level2_category',function(){
//   console.log('disciplinestartwith',disciplinestartwith)
//   let iterate = disciplinestartwith
//   var levelstartwithlen = iterate.toString().length
//   $('.leveltwooptions').each(function(){
//     if(iterate.toString().length < levelstartwithlen){
//       iterate=String(iterate).padStart(levelstartwithlen, '0');
//     }
//        $(this).attr('data-id',iterate)
//        iterate = parseInt(iterate) + (parseInt(disciplineseq)+1)
//   })
//  })
// check below code for empty value in xl sheet
$(document).ready(function(){
  // a=/1
  $('.empty-class').each(function(index,value){
    data=$(value).attr('data-id')
    // $('.class'+a+'').attr('data-id',data)
    // a++
    $('.editabletr').each(function(){
      $(this).find('td:eq('+index+')').find('.prev_cls').attr('data-id',data)
      $(this).find('td:eq('+index+')').find('.prev_cls').addClass('mas_cls_'+data)
    })
  })
  $('.commoncls').each(function(){
    if ($(this).val() == ''){
      const type=$(this)
      const level_id=$(this).attr('data-id')
      type.removeClass('remaining_levels')
      $.ajax({
        type: "GET",
        url: "/cost_code/getlevelbyid",
        data: { 'level_id': level_id },
        success: function (data) {
          $.each(data, function(index, item) {
            var costCodeType = item.fields.component_name;
            var id = item.pk;
            type.closest('select').append('<option value='+id+' data-id='+level_id+' >'+costCodeType+'</option>');
            type.closest('select').addClass('empty_val')
        });
        }
      })
    }
  })
  var get_master_data=$('.master_data').attr('data-id')
  var costcode_type=$('#costcode_type').val()
  var level_1=$('#level1_costcode').val()
  var level_2=$('#level2_costcode').val()
  // let final_val=''+level_1+''+costcode_type+''+level_2+''+costcode_type+''
  
  $('.editabletr').each(function(){
    let final_val=''+level_1+''+costcode_type+''+level_2+''+costcode_type+''
    $(this).find('.prev_cls').each(function(index,value){
      const current_element=$(value)
      const data_id= $(value).attr('data-id')
      $.ajax({
        //     type: "GET",
          url: "/cost_code/getmasterid",
          data: { 'data_id': data_id },
          success: function (data) {
            $.each(data, function(index, item) {
              var id = item.pk;
              current_element.closest('td').find('.masterId').val(id)
              // value.attr('costmaster_id',id)
            });
            var code_generate = current_element.attr('cost_code')
            if(code_generate == undefined){
              final_val='';
              getnewpreviewcode(current_element)
              
            }
            else{
              final_val+=code_generate+costcode_type
              current_element.closest('tr').find('.cost_code_preview').text(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
              current_element.closest('tr').find('.costcodepreview').val(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
            }
          }
      })
    })
  })
  // $('.prev_cls').each(function(){
  //   // let final_val=''+level_1+''+costcode_type+''+level_2+''+costcode_type+''
  //   const value=$(this)
  //   const data_id= $(this).attr('data-id')
  //   $.ajax({
  //     type: "GET",
  //     url: "/cost_code/getmasterid",
  //     data: { 'data_id': data_id },
  //     success: function (data) {
  //       $.each(data, function(index, item) {
  //         var id = item.pk;
  //         value.closest('td').find('.masterId').val(id)
  //         value.attr('costmaster_id',id)
  //     });
  //     var code_generate = value.attr('cost_code')
  //     if(code_generate == undefined){
  //       final_val='';
  //       getnewpreviewcode(value)
  //     }
  //     else{
  //       final_val+=code_generate+costcode_type
  //       // console.log('dfinal',final_val)
  //       value.closest('tr').find('.cost_code_preview').text(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
  //       value.closest('tr').find('.costcodepreview').val(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
  //       // value.closest('tr').find('.cost_code_preview').text(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
  //       // value.closest('tr').find('.costcodepreview').val(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
  //       // value.find('td .cost_code_preview').text(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
  //       // value.find('td .costcodepreview').val(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
  //     }
  //     // console.log('dfinal',final_val)
  //     }
  //   })
  // })


})


$(document).on('change', '#level1_category', function() {
  $('#level2_category').val('')
  var development_id=$(this).val();
  var id_array=development_id.split('_')
  var discipline=''
  level1=$('#level1_category').val()
  level2=$('#level2_category').val()
  if(level1 != '' && level2 != ''){
    $('#subcat_levels').show()
  }
  // $.ajax({
  //   type:"GET",
  //   url:'/projects/getprojectdiscipline_and_costcode',
  //   data:{'discipline_id':id_array[0],'development_id':id_array[1]},
  //   success: function(data){
  //       discipline += '<option value=" " selected>--Select--</option>'
  //       $.each(data.data,function(key,val){
  //         discipline +='<option class="leveltwooptions" data-id="" value='+val.id+'>'+val.discipline_subtype+'</option>'
  //       })
  //       discipline +='</select>'
  //       $('#level2_category').html(discipline);
  //       $('#level1_costcode').val(data.cost_code)
  //   }
  // })
})


$(document).on('click','.remove-btn',function(){
  var rowCount = $('#cost_code_table >tbody >tr').length;
  if($(this).closest('tr').find('.costcodelevel').hasClass('con_error')) {
    $('.final-cls').attr('disabled',false)
  }
  
  if(rowCount>1){
    $(this).closest('tr').remove()
    // $('#cost_code_table tbody .new_comp_cls').each(function(){
    //   $(this).find('.cost_code_preview').text('')
    //   $(this).find('.costcodepreview').val('')
    // })
    // $('#cost_code_table tbody .new_comp_cls').each(function(){
    //   $(this).find('.prev_cls').each(function(index,value){
    //     // console.log(value)
    //     getnewpreviewcode($(value))
    //   })
    // })
    // var costcode_type=$('#costcode_type').val()
    // var level_1=$('#level1_costcode').val()
    // var level_2=$('#level2_costcode').val()
    // $('.editabletr').each(function(){
    //   let final_val=''+level_1+''+costcode_type+''+level_2+''+costcode_type+''
    //   $(this).find('.prev_cls').each(function(index,value){
    //     const current_element=$(value)
    //     const data_id= $(value).attr('data-id')
    //     $.ajax({
    //       //     type: "GET",
    //         url: "/cost_code/getmasterid",
    //         data: { 'data_id': data_id },
    //         success: function (data) {
    //           $.each(data, function(index, item) {
    //             var id = item.pk;
    //             current_element.closest('td').find('.masterId').val(id)
    //             // value.attr('costmaster_id',id)
    //           });
    //           var code_generate = current_element.attr('cost_code')
    //           if(code_generate == undefined){
    //             final_val='';
    //             getnewpreviewcode(current_element)
                
    //           }
    //           else{
    //             final_val+=code_generate+costcode_type
    //             current_element.closest('tr').find('.cost_code_preview').text(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
    //             current_element.closest('tr').find('.costcodepreview').val(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
    //           }
    //         }
    //     })
    //   })
    // })
  }

})

$(document).on('click','.final-cls',function(e){
  e.preventDefault()
  let row_count=$('#cost_code_table tbody tr').length
  // let row_count=$("tr").length
  $('.total_rows').val(row_count)
  console.log('asd',row_count)
  $('#costcodeform').submit()

  // e.preventDefault()
  // let row_count=$("tr").length
  // let waring_class=$('.waring-err').length
  // $('.total_rows').val(row_count)
  // var isValid = true;
  // a=0
  // $('.editabletr').each(function(){
  //   $(this).find('td .masterId').attr('name','masterId'+a+'')
  //   $(this).find('td .cost_code_static').attr('name','maxcode'+a+'')
  //   $(this).find('td .costcode').attr('name','costcode'+a+'')
  //   $(this).find('td .costcodepreview').attr('name','costcodepreview'+a+'')
  //   $(this).find('td .remaining_levels_data').attr('name','remaining_levels'+a+'')
  //   $(this).find('td .new_level_cls_data').attr('name','remaining_levels'+a+'')
  //   // $(this).find('td .new_level_cls_data').attr('name','new_level'+a+'')
  //   a++
  // })

  // $(".commoncls,#level1_category,#level2_category").each(function() {
  //   if ($(this).val() === "" || $(this).val() === " ") {
  //     $(this).addClass('con_error')
  //     isValid = false;
  //     return false; 
  //   }
  // });
  // console.log(isValid,waring_class)
  // if (!isValid) {
  //   e.preventDefault();
  // }
  // if(waring_class!=0){
  //   e.preventDefault()
  // }
})


$(document).on('change', '.remaining_levels,.empty_val', function() {
  var cost_code=''
  var current=$(this)
  var original_value=$(this).closest('td').find('.oldcostcode').val()
  var currentindex=$(this).closest('tr').index()
  cost_code=$(this).find('option:selected').attr('cost_code')
  $(this).closest('td').find('.costcode').val(cost_code)
  $(this).closest('td').find('.cost_code_static').val(cost_code)
  level1_cost_code=$('#level1_costcode').val()
  level2_cost_code=$('#level2_costcode').val()
  cost_code_type= $('#costcode_type').val()
  cost_code =level1_cost_code+cost_code_type+level2_cost_code+cost_code_type
  level_count= $(this).closest('tr').find('.costcode').length
  $(this).closest('tr').find('.costcode').each((index, element) => {
    if($(element).val()){
      cost_code=cost_code+$(element).val()
      if (index !== level_count - 1) {
        cost_code=cost_code+cost_code_type
      }
    }
  });


  // $(this).closest('tr').find('.cost_code_preview').html(cost_code)
  // $(this).closest('tr').find('.costcodepreview').val(cost_code)
  
  // $('#cost_code_table').find('tr').each((rowindex, row) => {
  //   $(row).find('.costcodepreview').each((index, costcodepreview) => {
  //     if(rowindex != currentindex){
  //       if(cost_code==$(costcodepreview).val()){
  //         $(this).closest('tr').find('.cost_code_preview').html("<span>Cost Code Already Exists</span>")
  //         $(this).closest('tr').find('.costcodepreview').val()
  //       }
  //       else{
  //         $(this).closest('tr').find('.cost_code_preview').html(cost_code)
  //         $(this).closest('tr').find('.costcodepreview').val(cost_code)
  //       }
  //     }
  //   })
  // })
  // checkcostcode_exist(current,original_value,cost_code)

})

function checkcostcode_exist(current,original_value,cost_code){     
  $.ajax({
      type:"GET",
      url:'/cost_code/check_costcode_exists',
      data:{'cost_code':cost_code},
      success: function(data){
         if(data.status==true){
          current.closest('tr').find('.cost_code_preview').html('<span class="waring-err">Cost Code Already Exists</span>')
          current.val(original_value)
         }else{
          current.closest('tr').find('.cost_code_preview').html(cost_code)
          current.closest('tr').find('.costcodepreview').val(cost_code)
          const this_row=current.closest('tr')
          const row_val=current.closest('tr').find('.costcodepreview').val()
          $('.editabletr').not(this_row).each(function(){
            var current_row=$(this).find('td .costcodepreview').val()
            if (String(row_val) == String(current_row)){
              current.closest('tr').find('.cost_code_preview').html('<span class="waring-err">Cost Code Already Exists</span>')
            }

          })
        }
      }
    })
}

$(document).on('change', '#level2_category', function() {
  
  var discipline_id=$(this).val()
  var costcode_type=$('#costcode_type').val()
  level1cc= $('#level1_category').find(':selected').attr('data-id')
  level2cc= $('#level2_category').find(':selected').attr('data-id')
  level1=$('#level1_category').val()
  level1_cost_code_val=$('#level1_category').closest('div').find('.level1_costcode').val()
  level2=$('#level2_category').val()
  if(level1 != '' && level2 != ''){
    $('#subcat_levels').show()
  }
  $.ajax({
    type:"GET",
    url:'/cost_code/getlevel2_costcode',
    data:{'discipline_id':discipline_id},
    success: function(data){
      $('#level2_costcode').val(data.cost_code)
      $('#costcode_type').val(data.cost_code_type)
      $('.editabletr').each(function(){
        let final_val=''+level1cc+''+costcode_type+''+level2cc+''+costcode_type+''
        values_in_class=$(this).find('.commoncls')
        values_in_class.each(function(){
          var code_generate = $(this).find("option:selected").attr('cost_code')
          if(code_generate == undefined){
            final_val=''
            return false
          }
          else{
            final_val+=code_generate+costcode_type
          }
          
        })
        $(this).find('td .cost_code_preview').text(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
        $(this).find('td .costcodepreview').val(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
      })
    }
  })
})

function getnewpreviewcode(current_element){
  var current=$(current_element)
  var current_id=current.closest('td').find('.masterId').val()
  var master_id=current.closest('td').find('.parent_master_id').val()
  level1_cost_code=$('#level1_costcode').val()
  level2_cost_code=$('#level2_costcode').val()
  cost_code_type=$('#costcode_type').val()
  $.ajax({
        type: 'GET',
        data:{
          'masterId':master_id,
          'current_id':current_id
        },
        async:false,
        url: '/cost_code/getmaxval/',
        success: function(response) { 
          let max_value=response.data
          let index_value=current.attr('index')
          cost_code_li=[parseInt(max_value)-parseInt(response.sequencegap)]
          $('.class'+index_value+'').not(current).each(function(){
            if (!$(this).is(':visible')) {
              var cost_code_val=$(this).closest('td').find('.cost_code_static').val()
              cost_code_li.push(parseInt(cost_code_val))
            }
          })
          maxValue = Math.max.apply(Math,cost_code_li)
          let add_val= current.closest('tr').prevAll('.new_comp_cls').length * parseInt(response.sequencegap)
          // console.log('add_val',add_val)
          var elementsWithValue1 = current.closest('tr').prevAll('.new_comp_cls').find('.mas_cls_'+current_id).not('.commoncls').length;
          finalValue=parseInt(maxValue)+parseInt(response.sequencegap) 
          finalValue += elementsWithValue1 * parseInt(response.sequencegap) 
          if(finalValue.toString().length < response.no_digits){
            var correct_len= response.no_digits - finalValue.toString().length
            get_num=String(finalValue).padStart(response.no_digits, '0');
            current.closest('td').find('.costcode_val').val(get_num)
          }
          if(finalValue.toString().length == response.no_digits){
            get_num=parseInt(maxValue)+parseInt(response.sequencegap)
            current.closest('td').find('.costcode_val').val(get_num)
          }
          if(finalValue.toString().length > response.no_digits){
            Swal.fire('Max Limit Reached')
            current.closest('td').find('.new_level_cls_data').css('display','none')
            current.show(500)
            current.val(previous)
            get_num=selected_cc
          }
          cost_code=current.find('option:selected').attr('cost_code',get_num)
          current.closest('td').find('.costcode').val(get_num)
          current.closest('td').find('.cost_code_static').val(get_num)
          cost_code =level1_cost_code+cost_code_type+level2_cost_code+cost_code_type
          level_count= current.closest('tr').find('.costcode').length
          current.closest('tr').find('.costcode').each((index, element) => {
            if($(element).val()){
              cost_code=cost_code+$(element).val()
              if (index !== level_count - 1) {
                cost_code=cost_code+cost_code_type

              }
              current.attr('cost_code',$(element).val())
            }
          });
            current.closest('tr').find('.cost_code_preview').text(cost_code)
            current.closest('tr').find('.costcodepreview').val(cost_code)
        }
      })
  // var selected_cc=$(current_element).closest('td').find('.costcode_val').val()
  // var current_id=current.attr('data-id')
  // // use below code and send tr length to ajax
  // var prev_element=current.closest('tr').prev('.new_comp_cls').find('.mas_cls_'+current_id);
  // let prev_all_val_check=current.closest('tr').prevAll('.new_comp_cls').find('.mas_cls_'+current_id)
  // var valuesArray = prev_all_val_check.map(function(index, element) {
  //   return $(element).val();
  // }).get();
  // var exists = valuesArray.indexOf(current.val()) !== -1;
  // level1_cost_code=$('#level1_costcode').val()
  // level2_cost_code=$('#level2_costcode').val()
  // cost_code_type=$('#costcode_type').val()

  // if (exists){
  //   let cost_code_val;
  //   $('.mas_cls_'+current_id).each(function(index,element){
  //     if ($(element).val() == current.val()){
  //       cost_code_val = $(element).closest('td').find('.costcode_val').val()
  //       console.log(cost_code_val)
  //       return false;
  //     }
  //   })
  //   cost_code_data =level1_cost_code+cost_code_type+level2_cost_code+cost_code_type+cost_code_val
  //   current.closest('td').find('.costcode_val').val(cost_code_val)
  //   current.closest('td').find('.cost_code_static').val(cost_code_val)
  //   current.closest('td').find('.costcode').val(cost_code_val)
  //   current.closest('tr').find('.cost_code_preview').text(cost_code_data)
  //   current.closest('tr').find('.costcodepreview').val(cost_code_data)
  // }
  // else{
  //   console.log('false')
  //   $.ajax({
  //     type: 'GET',
  //     data:{
  //       'masterId':masterId,
  //       'current_id':current_id
  //     },
  //     async:false,
  //     url: '/cost_code/getmaxval/',
  //     success: function(response) { 
  //       let max_value=response.data
  //       index_value=current.attr('index')
  //       cost_code_li=[parseInt(max_value)-parseInt(response.sequencegap)]
  //       $('.class'+index_value+'').not(current).each(function(){
  //         if (!$(this).is(':visible')) {
  //           var cost_code_val=$(this).closest('td').find('.cost_code_static').val()
  //           cost_code_li.push(parseInt(cost_code_val))
  //         }
  //       })
  //       maxValue = Math.max.apply(Math,cost_code_li)
  //       let add_val= current.closest('tr').prevAll('.new_comp_cls').length * parseInt(response.sequencegap)
  //       var elementsWithValue1 = current.closest('tr').prevAll('.new_comp_cls').find('.mas_cls_'+current_id).not('.commoncls').length;
  //       finalValue=parseInt(maxValue)+parseInt(response.sequencegap) 
  //       finalValue += elementsWithValue1 * parseInt(response.sequencegap) 
  //       if(finalValue.toString().length < response.no_digits){
  //         var correct_len= response.no_digits - finalValue.toString().length
  //         get_num=String(finalValue).padStart(response.no_digits, '0');
  //         current.closest('td').find('.costcode_val').val(get_num)
  //       }
  //       if(finalValue.toString().length == response.no_digits){
  //         get_num=parseInt(maxValue)+parseInt(response.sequencegap)
  //         current.closest('td').find('.costcode_val').val(get_num)
  //       }
  //       if(finalValue.toString().length > response.no_digits){
  //         Swal.fire('Max Limit Reached')
  //         current.closest('td').find('.new_level_cls_data').css('display','none')
  //         current.show(500)
  //         current.val(previous)
  //         get_num=selected_cc
  //       }
  //       cost_code=current.find('option:selected').attr('cost_code',get_num)
  //       current.closest('td').find('.costcode').val(get_num)
  //       current.closest('td').find('.cost_code_static').val(get_num)
  //       // level1_cost_code=$('#level1_costcode').val()
  //       // level2_cost_code=$('#level2_costcode').val()
  //       // cost_code_type= $('#costcode_type').val()
  //       cost_code =level1_cost_code+cost_code_type+level2_cost_code+cost_code_type
  //       level_count= current.closest('tr').find('.costcode').length
  //       current.closest('tr').find('.costcode').each((index, element) => {
  //         if($(element).val()){
  //           cost_code=cost_code+$(element).val()
  //           if (index !== level_count - 1) {
  //             cost_code=cost_code+cost_code_type

  //           }
  //           current.attr('cost_code',$(element).val())
  //         }
  //       });
  //         current.closest('tr').find('.cost_code_preview').text(cost_code)
  //         current.closest('tr').find('.costcodepreview').val(cost_code)
  //       },
  //       error: function(xhr, status, error) {
  //   }
  //   })
  // }
}


// $(document).ready(function(){
//   var costcode_type=$('#costcode_type').val()
//   var level_1=$('#level1_costcode').val()
//   var level_2=$('#level2_costcode').val()
//   $('.editabletr').each(function(){
//     let final_val=''+level_1+''+costcode_type+''+level_2+''+costcode_type+''
//     values_in_class=$(this).find('.prev_cls')
//     values_in_class.each(function(){
//       // var code_generate = $(value).find("option:selected").attr('cost_code')
//       const sub_value=$(this)
//       var code_generate = $(this).attr('cost_code')
//       if(code_generate == undefined){
//         final_val='';
//         // var masterId=$(value).closest('td').find('.masterId').val()
//         // var selected_cc=$(value).closest('td').find('.costcode_val').val()
//         // var current_id=current.attr('data-id')
//         // console.log('v',sub_value.closest('td').find('.masterId').val())
//         getnewpreviewcode(sub_value)
//         // return false;
//       }
//       else{
//         final_val+=code_generate+costcode_type
//       }
//     })
//     // console.log('final_val',final_val.slice(0,final_val.lastIndexOf(costcode_type)))
//     $(this).find('td .cost_code_preview').text(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
//     $(this).find('td .costcodepreview').val(final_val.slice(0, final_val.lastIndexOf(costcode_type)))
//   })
// })




$(document).on('change','.empty_val',function(){
  const datas=$(this)
  var value=$(this).val()
  var original_value=$(this).closest('td').find('.oldcostcode').val()
  $.ajax({
    type:"GET",
    url:'/cost_code/getgeneratecostcode',
    data:{'component_id':value},
    success: function(data){
      $.each(data, function(index, item) {
        var costcode_type=$('#costcode_type').val()
        var level_1=$('#level1_costcode').val()
        var level_2=$('#level2_costcode').val()
        var component_num = item.fields.component_cost_code;
        datas.closest('td').find('.cost_code_static,.costcode').val(component_num)
        var org_data=datas.closest('td').find('.cost_code_static,.costcode').val()
        change_component=datas.closest('tr').find('.commoncls')
        var fixed_val=''+level_1+''+costcode_type+''+level_2+''+costcode_type+''
        change_component.each(function(){
          fixed_values=$(this).find("option:selected").attr('cost_code')
          if (fixed_values == undefined){
            if(!$(this).val()=='')
            {
            fixed_val+=org_data+costcode_type
            $(this).find("option:selected").attr('cost_code',org_data)
            }
          }
          else{
            fixed_val+=fixed_values+costcode_type
          }
        })
        datas.closest('tr').find('td .cost_code_preview').text(fixed_val.slice(0, fixed_val.lastIndexOf(costcode_type)))   
        datas.closest('tr').find('td .costcodepreview').val(fixed_val.slice(0, fixed_val.lastIndexOf(costcode_type)))   
        checkcostcode_exist(datas,original_value,fixed_val.slice(0, fixed_val.lastIndexOf(costcode_type)))
    });
    }
  })  
})


$(document).on('change',".commoncls,#level1_category,#level2_category",function(){
 if (!($(this).val() === "" || $(this).val() === " ")){
  $(this).removeClass('con_error')
 }
})

//ajax initial call
$(document).ready(function(){
  $('.editabletr').each(function(){
    const this_tr=$(this)
    var original_value=$(this).find('td .oldcostcode').val()
    const this_code_generate=$(this).find('td .cost_code_preview').text()
    // $.ajax({
    //   type:"GET",
    //   url:'/cost_code/check_costcode_exists',
    //   data:{'cost_code':this_code_generate},
    //   success: function(data){
    //     if(data.status==true){
    //       this_tr.find('td .cost_code_preview').html('<span class="waring-err">Cost Code Already Exists</span>')
    //     }
    //     }
    //     })
    // checkcostcode_exist(this_tr,original_value,this_code_generate)
  //   $('.editabletr').not(this_tr).each(function(){
  //     var current_tr=$(this)
  //     var current_code_generate=$(this).find('td .cost_code_preview').text()
  //     if(this_code_generate !=''){
  //     if(this_code_generate == current_code_generate){
  //       // console.log({'this_code_generate':this_code_generate,'current_code_generate':current_code_generate,'$(this)':this_tr})
  //       current_tr.find('td .cost_code_preview').html('<span class="waring-err">Cost Code Already Exists</span>')
  //     }
  //   }
  //   })
  })
})
var previous;
  $(document).on('focus', '.remaining_levels', function() {
  //$("select").on('focus', function () {
    // Store the current value on focus and on change
    //previous = ''
    previous = $(this).val();
})
  //$("select").on('focus', function () {
    $(document).on('change', '.remaining_levels,.empty_val', function() {
  //$(document).on('focus', '.remaining_levels', function() {

      // Store the current value on focus and on change  
  var cost_code=''
  var current=$(this)
  var level_name=$(this).closest('td').find('.new_level_cls_data')
  var masterId=$(this).closest('td').find('.masterId').val()
  var selected_cc=current.closest('td').find('.costcode_val').val()
  var current_id=current.attr('data-id')
  var selectedValue = $(this).val();
  if (selectedValue == 'create'){
  var costcode_vals = $('.costcode_val') 
    $(this).hide(500)
    $(this).next('.new_level_cls_data').show(500)
    // console.log('masterId',masterId)
    // console.log('current_id',current_id)
        $.ajax({
          type: 'GET',
          data:{
            'masterId':masterId,
            'current_id':current_id
          },
          url: '/cost_code/getmaxval/',
          success: function(response) { 
            // console.log('success')
            let max_value=response.data
            index_value=current.attr('index')
            cost_code_li=[parseInt(max_value)-parseInt(response.sequencegap)]
            $('.class'+index_value+'').not(current).each(function(){
              if (!$(this).is(':visible')) {
                var cost_code_val=$(this).closest('td').find('.cost_code_static').val()
                cost_code_li.push(parseInt(cost_code_val))
              }
            })
            maxValue = Math.max.apply(Math,cost_code_li)
            finalValue=parseInt(maxValue)+parseInt(response.sequencegap)
            if(finalValue.toString().length < response.no_digits){
              var correct_len= response.no_digits - finalValue.toString().length
              get_num=String(finalValue).padStart(response.no_digits, '0');
            }
            if(finalValue.toString().length == response.no_digits){
              get_num=parseInt(maxValue)+parseInt(response.sequencegap)
            }
            if(finalValue.toString().length > response.no_digits){
              Swal.fire('Max Limit Reached')
              current.closest('td').find('.new_level_cls_data').css('display','none')
              current.show(500)
              current.val(previous)
              get_num=selected_cc
            }
            // if(finalValue.toString().length > response.no_digits){
            //   Swal.fire('Max Limit Reached')
            //   current.closest('tr').find('.new_level_cls_data').css('display','none')
            //   current.show(500)
            //   current.val('')
            // }
            cost_code=current.find('option:selected').attr('cost_code',get_num)
            current.closest('td').find('.costcode').val(get_num)
            current.closest('td').find('.cost_code_static').val(get_num)
            level1_cost_code=$('#level1_costcode').val()
            level2_cost_code=$('#level2_costcode').val()
            cost_code_type= $('#costcode_type').val()
            cost_code =level1_cost_code+cost_code_type+level2_cost_code+cost_code_type
            level_count= current.closest('tr').find('.costcode').length
            // if(max_value.length == current_id ){
            current.closest('tr').find('.costcode').each((index, element) => {
              if($(element).val()){
                cost_code=cost_code+$(element).val()
                if (index !== level_count - 1) {
                  cost_code=cost_code+cost_code_type
                }
              }
            });
              current.closest('tr').find('.cost_code_preview').text(cost_code)
              current.closest('tr').find('.costcodepreview').val(cost_code)
            },
            error: function(xhr, status, error) {
        }
        })
  }
})



// $(document).on('focus','.remaining_levels',function(){
//   let this_text=$(this)
//   let data_id=$(this).attr('data-id')
//   let class_name=$(this).attr('class')
//   let cost_code=$(this).attr('cost_code')
//   let this_val=$(this).val()
//   let text_val=$(this).text()
//   cost_type_val='<select>'
//   $.ajax({
//     type: "GET",
//     url: "/cost_code/getcosttypevalues",
//     data: { 'data_id': data_id },
//     success: function (data) {
//       $.each(data, function(index, item) {
//         cost_type_val+='<option>--Select--</option>'
//         $.each(data.data,function(key,val){
//           cost_type_val +='<option value='+val.id+' data-id='+data_id+' cost_code='+val.component_cost_code+'>'+val.component_name+'</option>'
//         })
//         cost_type_val +='</select>'
//         this_text.html(cost_type_val)
//         this_text.val(this_val)
//     });
//     }
//   })
// })

// $(document).on('keyup','.costcodelevel',function(){
//   currentval = $(this).val()
//   masterId=$(this).closest('td').find('.masterId').val()
//   currentposition=$(this)
//   tdposition = $(this).closest('td').index()
//   $(this).closest('table tbody').find('tr').each(function(index,val){
//    let getEle = $(val).find(`td`).eq(tdposition).find('.costcodelevel:visible')
//   index = getEle.prop("tagName").toLowerCase() == 'select' ? $(getEle).find('option:selected').text() : getEle.val()
//   if(currentval==index){
//     currentposition.addClass('con_error')
//     getEle.addClass('con_error')
// } 
// else{
//     // getEle.removeClass('con_error')
//     currentposition.removeClass('con_error')
// }

//   })
//   $.ajax({
//     type: "GET",
//     url: "/cost_code/getcosttype",
//     data: { 'value': currentval,
//   'masterId': masterId },
//     success: function (data) {
//         duplicates=data.duplicate
//         if (duplicates == 1){
//           currentposition.addClass('con_error')
//         }
//         else{
//           currentposition.removeClass('con_error')

//         }
//     }
//     })
//  })

// please below error for submit check 
//  $('#costcodeform').submit(function(e) {
//   e.preventDefault(); 
//   let level1=$('#level1_category').val()
//   let level2=$('#level2_category').val()
//   let allcostcode_preview=[]
//   let validation=false
//   $('#cost_code_table').find('tr').each((index, row) => {
//     $(row).find('.remaining_levels').each((index, column) => {
//       if(!$(column).val()){   
//          validation=true 
//         $(column).css("border", "1px solid red");
//       }else{
//         $(column).css("border", "");

//       }
//     })
//     $(row).find('.new_level_cls_data').not(':hidden').each((index, column) => {
//       if(!$(column).val()){   
//         validation=true 
//         $(column).css("border", "1px solid red");
//       }else{
//         $(column).css("border", "");
//        }
//     })
//     $(row).find('.costcodepreview').each((index, costcodepreview) => {
//       allcostcode_preview.push($(costcodepreview).val())

//     })
//   })
//   if(level1 ==''){
//     $('#level1_category').css("border", "1px solid red");
//   }
//   if(level2 ==''){
//     $('#level2_category').css("border", "1px solid red");
//   }

//   checkcost_code=checkduplicatevalue(allcostcode_preview)

//   if(level1 != '' && level2!='' && validation==false && checkcost_code==false && $('.con_error').length == 0){
//     this.submit();
//     $('.final-cls').attr('disabled', true);
//   }else{
//     return false

//   }
// })

function checkduplicatevalue(array) {
  var valueSet = new Set();
  for (var i = 0; i < array.length; i++) {
    var value = array[i];
    if (valueSet.has(value)) {
      return true; 
    }
    valueSet.add(value);
  }
  return false; 
}
$(document).on('change','.new_level_cls_data ',function(){
 
  currentpos = $(this)
  currentval = $(this).val()
  currentlev = $(this).closest('td').find('.masterId').val()
  let duplicatecount=0
  $('.new_level_cls_data').each(function(){
     if($(this).closest('td').find('.masterId').val() == currentlev && $(this).val() != ''){
      //  console.log('value',$(this).val())
       if(currentval == $(this).val()){
         duplicatecount++;
       }
     }
       if(duplicatecount > 1){
         currentpos.css("border", "1px solid red");
         $('.final-cls ').attr('disabled',true)
       }
       else{
         currentpos.css("border", "");
         $('.final-cls ').attr('disabled',false)
       }
   })
 })

 $(document).on('keyup','.new_level_cls_data',function(){
  //checking newlevel data with db
  // console.log('csrf_token',csrf_token)
  levelid = $(this).closest('td').find('.masterId').val()
  // console.log('currentval',$(this).val())
  // console.log('levelid',levelid)
  currentposition=$(this)
  savebtb=$('.final-cls')
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token},
    url: "/cost_code/validatecclevel/",
    data: {'currentval':$.trim($(this).val()),'levelid':levelid},
    success: function(data){
        if (data.status == true){ 
         
          currentposition.addClass('con_error')
          currentposition.after('<span class="waring-err">Component Name Already Exists</span>')
          savebtb.attr('disabled',true)
         }
         else{
          currentposition.removeClass('con_error')
          currentposition.closest('td').find('span').remove();
          savebtb.attr('disabled',false)
         }
     }
  });
 })

//  $(document).on('click','.add-btn',function(){
//   new_tr = $(this).closest('tr')
//   let clone =new_tr.clone()
//   // $('.subclass'+index).each(function(){
//   //  clone.find('.subclass'+index).val('')
//   // })
//   var row = clone 
//   var tds = row.find('.remaining_levels');
//   tds.each(function(index, element) {
//     $(this).val('')
//     $(this).find('option[value="create"]').remove();
//     firstrow.find('.remaining_levels').css('display', 'block');
//  });
//   clone.find('.cost_code_preview').text(' ')
//   $(this).closest('tr').after(clone)
//  })

$(document).on('click', '#addnew-level', function() {
  var rowCount = parseInt($('#cost_code_table >tbody >tr').length)+1;
  var current_index=rowCount-1
  let new_row='<tr class="editabletr new_comp_cls">'
  var firstrow = $('#cost_code_table').find('tr:last').find('.masterId').each(function(){
    let parent_id=$(this).closest('td').find('.parent_master_id').val()
    new_row+='<td><input type="hidden" class="costcode_val" name="costcode_val'+rowCount+'" value=""><input type="hidden" class="masterId" name="masterId'+rowCount+'" value='+$(this).val()+'><input type="hidden" class="parent_master_id" name="parent_master_id'+rowCount+'" value="'+parent_id+'"><input type="hidden" name="maxcode'+rowCount+'" class="cost_code_static" value=""><input type="hidden" name="costcode'+rowCount+'" class="costcode" value=""><input type="text" name="remaining_levels'+rowCount+'" class="form-control prev_cls new_level_cls_data costcodelevel" placeholder="Type New Component" data-id="" value=""></td>'
  });
  new_row+='<td><label>Code Preview</label><div class="cost_code_preview"></div><input type="hidden" name="costcodepreview'+rowCount+'" class="costcodepreview" value=""></td>'
  new_row+='<td><button type="button" class="btn btn-clr remove-btn waves-effect waves-float waves-light">Remove</button></td></tr>'
  $('#cost_code_table').append(new_row)
  console.log('aasd',new_row)
  $('.empty-class').each(function(index,value){
    data=$(value).attr('data-id')
    $('#cost_code_table tbody tr:last').each(function(){
      // $(this).find('td:eq('+index+')').find('.prev_cls').attr('data-id',data)
      // $(this).find('td:eq('+index+')').find('.prev_cls').addClass('mas_cls_'+data)
      getnewpreviewcode($(this).find('td:eq('+index+')').find('.new_level_cls_data'))
    })
  })

  $('#total_rows').val(rowCount)
})

$(document).on('click','.addnew-level',function(){
  var scrollTo = $(document).height() - $(window).height();
  $('html, body').animate({ scrollTop: scrollTo }, 'slow');
})