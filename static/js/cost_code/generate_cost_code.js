$(document).ready(function(){
    $('.check_type').each(function(){
      if($(this).children().length == 0){
        $(this).text('-')
      }
    })

    var levelstartwithlen = levelstartwith.toString().length
    $('.leveloneoptions').each(function(){
       if(levelstartwith.toString().length < levelstartwithlen){
        levelstartwith=String(levelstartwith).padStart(levelstartwithlen, '0');
      }
      $(this).attr('data-id',levelstartwith)
      levelstartwith = parseInt(levelstartwith) + (parseInt(levelonesequencegap)+1)
    })


})
$(document).on('click','#level2_category',function(){
  // console.log('disciplinestartwith',disciplinestartwith)
  let iterate = disciplinestartwith
  var levelstartwithlen = iterate.toString().length
  $('.leveltwooptions').each(function(){
    if(iterate.toString().length < levelstartwithlen){
      iterate=String(iterate).padStart(levelstartwithlen, '0');
    }
       $(this).attr('data-id',iterate)
       iterate = parseInt(iterate) + (parseInt(disciplineseq)+1)
  })
 
 })
$(document).ready( function () {
  $('#subcat_levels').hide()
  
  $(document).on('change', '#level1_category', function() {
    var development_id=$(this).val();
    var master_count=$('#master_count').val()
    var id_array=development_id.split('_')
    var discipline=''
    level1=$('#level1_category').val()
    level2=$('#level2_category').val()
    if(master_count == 0){
      swal.fire('Create Levels in Cost Code Master')
      $(this).val('')
    }
    else{
    if(level1 != '' && level2 != ''){
      $('#subcat_levels').show()
    }
    $.ajax({
      type:"GET",
      url:'/projects/getprojectdiscipline_and_costcode',
      data:{'discipline_id':id_array[0],'development_id':id_array[1]},
      success: function(data){
          var start_with=data.start_with

          discipline += '<option value="" selected>--Select--</option>'
          $.each(data.data,function(key,val){
            discipline +='<option value='+val.id+'_'+start_with+'>'+val.discipline_subtype+'</option>'
            start_with=sumCostCode(start_with,parseInt(data.sequence)+1)


          })
          discipline +='</select>'
          $('#level2_category').html(discipline);
          // $('#level1_costcode').val(data.cost_code) 
      }
    })
  }
  })
  function sumCostCode(costcode, sequence_gap) {
    let newCostCode = (parseInt(costcode, 10) + parseInt(sequence_gap, 10)).toString();
    const paddingLength = costcode.length - newCostCode.length;
  
    if (paddingLength > 0) {
        newCostCode = '0'.repeat(paddingLength) + newCostCode;
    }
    
    return newCostCode;
  }

  $(document).on('change','#level1_category',function(){
    levoneselectedval = $('#level1_category :selected').attr('data-id')
    $('#level1_costcode').val(levoneselectedval)
    $('#level2_category').val('')
   
  })
  $(document).on('change', '#level2_category', function() {
    
    var discipline_id=$(this).val()
    var costcode_type=$('.costcode_type').val()
    level1=$('#level1_category').val()
    level1_cost_code_val=$('#level1_category').closest('div').find('.level1_costcode').val()
    level2_val = $('#level2_category :selected').attr('data-id')
    
    level2=$('#level2_category').val()
    if(level1 != '' && level2 != ''){
      $('#subcat_levels').show()
    }
    $.ajax({
      type:"GET",
      url:'/cost_code/getlevel2_costcode',
      data:{'discipline_id':discipline_id},
      success: function(data){
        $('#level2_costcode').val(level2_val)
        $('#costcode_type').val(data.cost_code_type)
        $('.editabletr').each(function(){
          let final_val=''+level1_cost_code_val+''+data.cost_code_type+''+level2_val+''+data.cost_code_type+''
          // console.log('level2_costcode',level2_val)
          values_in_class=$(this).find('.commoncls')
         
          values_in_class.each(function(){
            var code_generate = $(this).closest('td').find('.cost_code_static').val()
              // console.log('final_val',final_val)
              // console.log('code_generate',code_generate)
              // console.log('costcode_type',costcode_type)
            if(code_generate == undefined){
              // console.log('ifloop')
              final_val=''
              return false
            }
            else{
              // console.log('elseloop')
              final_val+=code_generate+costcode_type
            }
            
          })
          
          $('.editabletr').each(function(){
            cost_code=final_val
            // console.log($(this).find('.costcode'),'console')
            $(this).find('.costcode').each((index, element) => {
              level_count= $(this).closest('tr').find('.costcode').length
              if($(element).val()){        
                cost_code=cost_code+$(element).val()
                if (index !== level_count - 1) {
                  cost_code=cost_code+cost_code_type
                }
              }
            });
          // $(this).find('td .cost_code_preview').text(cost_code)
          // $(this).find('td .costcodepreview').val(cost_code)
          // console.log('cost_code',cost_code)
          })
          
        })
      }
    })


  })



  $(document).on('click', '#addnew-level', function() {
    var rowCount = $('#cost_code_table >tbody >tr').length;
    // alert(rowCount);
    console.log("rowCount "+rowCount)
    var current_index=rowCount-1
    // console.log("current_index"+current_index)
    var firstrow = $('#cost_code_table').find('tr:eq(0)').clone();
    firstrow.append('<td><button type="button" class="btn btn-clr remove-btn">Remove</button></td>')
    // console.log('firstrow',firstrow)
    firstrow.find('.new_level_cls').css('display', 'none');
    firstrow.find('.new_level_cls').val('')
    firstrow.find('.remaining_levels').css('display', 'block');
    firstrow.find('.old_text').val('');

    firstrow.find('span').remove();
    firstrow.find('.new_level_cls').removeClass('con_error')
    $('#cost_code_table').append(firstrow)
    // console.log($('#cost_code_table').find('tr:eq('+current_index+')').find('.cost_code_preview'))
    $('#cost_code_table').find('tr:eq('+rowCount+')').find('.cost_code_preview').html('')
    $('#cost_code_table').find('tr:eq('+rowCount+')').find('.costcode').val('')
    $('#cost_code_table').find('tr:eq('+rowCount+')').find('.remaining_levels').val('')
    $('#cost_code_table').find('tr:eq('+rowCount+')').find('.remaining_levels').attr('name', 'remaining_levels'+rowCount+'');
    $('#cost_code_table').find('tr:eq('+rowCount+')').find('.new_level_cls').attr('name', 'new_level'+rowCount+'');
    $('#cost_code_table').find('tr:eq('+rowCount+')').find('.costcode').attr('name', 'costcode'+rowCount+'');
    $('#cost_code_table').find('tr:eq('+rowCount+')').find('.costcodepreview').attr('name', 'costcodepreview'+rowCount+'');
    $('#cost_code_table').find('tr:eq('+rowCount+')').find('.masterId').attr('name', 'masterId'+rowCount+'');
    $('#cost_code_table').find('tr:eq('+rowCount+')').find('.cost_code_static').attr('name', 'maxcode'+rowCount+'');

    $('#total_rows').val(rowCount)
  })


  $(document).on('click','.remove-btn',function(){
    var rowCount = $('#cost_code_table >tbody >tr').length;
    let data= $(this).closest('tr')
    let seqGap = parseInt(levelonesequencegap)
    // console.log('REMOVE',$(this).closest('tr').find('.new_level_cls:hidden').length)
    let tr_val=$(this).closest('tr').find('.cost_code_preview').text()
    // console.log('tr_valllllll',tr_val)
    let trLength = $(this).closest('tr').nextAll('tr').filter(".new_level_cls [style$='display: none;']").closest('tr').lenght
    // console.log({'trLength':trLength})
    if (!($(this).closest('tr').find('.new_level_cls').css('display') === 'none')) {
      // console.log('iF')
      $('.new_level_cls:visible').each(function() {
        // console.log('newlevel');
      });
      
      
    data.nextAll('tr').each(function(index, tr) {   
          // console.log('tr_valllllll',$(this))
          if (!($(this).find('.new_level_cls').css('display') === 'none')) {
            $(tr).find('.cost_code_preview').text(tr_val)
            $(tr).find('.costcodepreview').val(tr_val)
            let lastSegment = tr_val.split(".").pop();
            let increaseSeq = parseInt(lastSegment)+seqGap
            let segments = tr_val.split(".");
            let secondLastSegment = segments.slice(0, -1).join(".");
            tr_val = `${secondLastSegment}.${increaseSeq}`  
            // console.log('newSeq',tr_val)
          }
    });
  }
  if(data.find('.costcodelevel').hasClass('con_error')) {
    $('.final-cls').attr('disabled',false)
  }

  if(rowCount>1){
      $(this).closest('tr').remove()
    }
  })

 
  $('#costcodeform').submit(function(e) {
    e.preventDefault(); 
    let level1=$('#level1_category').val()
    let level2=$('#level2_category').val()
    let allcostcode_preview=[]
    let validation=false
    $('#cost_code_table').find('tr').each((index, row) => {
      $(row).find('.remaining_levels').each((index, column) => {
        // console.log('val',$(column).val())
        if(!$(column).val()){   
           validation=true 
          $(column).css("border", "1px solid red");
        }else{
          // console.log('1stif',validation)
          $(column).css("border", "");

        }
      })
      $(row).find('.new_level_cls').not(':hidden').each((index, column) => {
        if(!$(column).val()){   
          validation=true 
          $(column).css("border", "1px solid red");
        }else{
          // console.log('2ndif',validation)
          $(column).css("border", "");
         }
      })
      $(row).find('.costcodepreview').each((index, costcodepreview) => {
        allcostcode_preview.push($(costcodepreview).val())
      })
    })
    if(level1 ==''){
      $('#level1_category').css("border", "1px solid red");
    }
    if(level2 ==''){
      $('#level2_category').css("border", "1px solid red");
    }
    // console.log('validation',validation)
    // console.log('allcostcode_preview',allcostcode_preview)

    checkcost_code=checkduplicatevalue(allcostcode_preview)
    // console.log('checkcost_code',checkcost_code)
    // console.log('errorlen',$('.con_error').length)
    if(level1 != '' && level2!='' && validation==false && checkcost_code==false && $('.con_error').length == 0){
      this.submit();
      $('.final-cls').attr('disabled',true)

    }else{
      return false

    }
  })

  
    


$(document).on('change','#level1_category,#level2_category,#remaining_levels',function(){
  if($(this).val() !=''){
    $(this).css("border", "");
  }
})


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

// $(document).on('click','.remaining_levels',function(){
//   let value=$(this).find(':selected').val()
//   if (value == 'create'){
//     $(this).hide(500)
//     $(this).next('.new_level_cls').show(500)
//   }
// })

// var previous;
//   $(document).on('focus', '.remaining_levels', function() {
//   //$("select").on('focus', function () {
//     // Store the current value on focus and on change
//     //previous = ''
//     previous = $(this).val();
// })

  // $(document).on('change','#remaining_levels',function(){
  //   var filteredSelectTags = $(document).find('#cost_code_table tbody tr').find('.remaining_levels').filter(function() {
  //     return $(this).find('option[value="create"]').is(':selected')
  //   });
  //   let lenght = filteredSelectTags.closest('tr').length
  //   // if (lenght == 1){
  //         var current=$(this)
  //         var selectedValue = $(this).val();
  //         let select_id=$(this).attr('data-id')
  //         masterId=$(this).closest('td').find('.masterId').val()
  //         current_id=$(this).closest('td').attr('data-id')
  //         var selected_cc=current.closest('td').find('.costcode_val').val()
  //         if (selectedValue == 'create'){
  //         $(this).hide(500)
  //         $(this).next('.new_level_cls').show(500)
  //           $.ajax({
  //             type: 'GET',
  //             data:{
  //               'masterId':masterId,
  //               'current_id':current_id
  //             },
  //             url: '/cost_code/getmaxval/',
  //             success: function(response) {
                
  //               let max_value=response.data
  //               index_value=current.attr('index')
  //               cost_code_li=[parseInt(max_value)-parseInt(response.sequencegap)]
  //               $('.class'+index_value+'').not(current).each(function(){
  //                 if (!$(this).is(':visible')) {
  //                   var cost_code_val=$(this).closest('td').find('.cost_code_static').val()
  //                   cost_code_li.push(parseInt(cost_code_val))
  //                 }
  //               })
  //               maxValue = Math.max.apply(Math,cost_code_li)
  //               finalValue=parseInt(maxValue)+parseInt(response.sequencegap)
  //               if(finalValue.toString().length < response.no_digits){
  //                 var correct_len= response.no_digits - finalValue.toString().length
  //                 get_num=String(finalValue).padStart(response.no_digits, '0');
  //               }
  //               if(finalValue.toString().length == response.no_digits){
  //                 get_num=parseInt(maxValue)+parseInt(response.sequencegap)
  //               }
  //               if(finalValue.toString().length > response.no_digits){
  //                 Swal.fire('Max Limit Reached')
  //                 current.closest('td').find('.new_level_cls').css('display','none')
  //                 current.show(500)
  //                 current.val(previous)
  //                 get_num=selected_cc
  //                 current.next('.new_level_cls').hide(10)
  //               }
  //               console.log('finalValue',finalValue)
  //               console.log({'max_value':max_value,'index_value':index_value,'cost_code_li':cost_code_li,'maxValue':maxValue})
  //               console.log('finalValue',finalValue)
  //               cost_code=current.find('option:selected').attr('cost_code',get_num)
  //               // console.log('max_value',max_value)
  //               current.closest('td').find('.costcode').val(get_num)
  //               current.closest('td').find('.cost_code_static').val(get_num)
  //               level1_cost_code=$('#level1_costcode').val()
  //               level2_cost_code=$('#level2_costcode').val()
  //               cost_code_type= $('#costcode_type').val()
  //               cost_code =level1_cost_code+cost_code_type+level2_cost_code+cost_code_type
  //               level_count= current.closest('tr').find('.costcode').length
  //               console.log('level_count',level_count)
  //               // if(max_value.length == current_id ){
  //               current.closest('tr').find('.costcode').each((index, element) => {
  //                 if($(element).val()){
  //                   cost_code=cost_code+$(element).val()
  //                   if (index !== level_count - 1) {
  //                     cost_code=cost_code+cost_code_type
  //                     // console.log('cost_code',cost_code)
  //                   }
  //                 }
  //               });
  //                 current.closest('tr').find('.cost_code_preview').text(cost_code)
  //                 current.closest('tr').find('.costcodepreview').val(cost_code)
                 
  //               // cost_code=this_row.find('option:selected').attr('cost_code',max_value)
  //               // // console.log('max_value',max_value)
  //               // this_row.closest('td').find('.costcode').val(max_value)
  //               // this_row.closest('td').find('.cost_code_static').val(max_value)
  //               // level1_cost_code=$('#level1_costcode').val()
  //               // level2_cost_code=$('#level2_costcode').val()
  //               // cost_code_type= $('#costcode_type').val()
  //               // cost_code =level1_cost_code+cost_code_type+level2_cost_code+cost_code_type
  //               // level_count= this_row.closest('tr').find('.costcode').length
  //               // console.log('level1_cost_code',level1_cost_code)
  //               // console.log('level2_cost_code',level2_cost_code)
  //               // console.log('cost_code_type',cost_code_type)
  //               // console.log('cost_code',cost_code)
  //               // console.log('level_count',level_count)
  //               // if(max_value.length == select_id ){
  //               // this_row.closest('tr').find('.costcode').each((index, element) => {
  //               //   if($(element).val()){
  //                   // console.log("value"+$(element).val().length)
  //                   // console.log('element-',$(element).val())
  //           //         cost_code=cost_code+$(element).val()
  //           //         // console.log('cost_code-',cost_code)
  //           //         // console.log('cost_code_type-',cost_code_type)
  //           //         if (index !== level_count - 1) {
  //           //           cost_code=cost_code+cost_code_type
  //           //         }
  //           //       }
  //           //     });
  //           //   }
  //           // else{
  //           //   Swal.fire('Max Limit Reached')
  //           //   this_row.closest('tr').find('.new_level_cls').css('display','none')
  //           //   this_row.show(500)
  //           //   this_row.val('')
  //           // }
  //           //     console.log("cost_codessss---",cost_code)
  //           //     this_row.closest('tr').find('.cost_code_preview').text(cost_code)
  //           //     this_row.closest('tr').find('.costcodepreview').val(cost_code)
  //             },
  //             error: function(xhr, status, error) {
  //             }
  //           });
  //         }
  //   // }
  // })

  allcostcode_list=[]

  $(document).on('blur','.remaining_levels',function(){

    var old_text=$(this).closest('td').find('.old_text').val()
    var rowindex=$(this).closest('tr').index()
    console.log("old_text"+old_text)
    var level_index=parseInt($(this).attr('index'))+2;
    var current_index = $(this).closest("td").index();

    console.log("current_index "+current_index)
    var level_id=$(this).attr('level_id')
    var level1=$('#level1_category').val()
    var level2=$('#level2_category').val()
    var component_name=$(this).val()
    console.log("component_name "+component_name)
    var startfrom=$(this).attr('startfrom')
    var level1_split=level1.split('_');
    var level2_split=level2.split('_');
    var cost_code_type= $('#costcode_type').val()
    var current_element=$(this)
    var pre_cost_code=$(this).closest('td').prev().find('.costcode').val();
    var pre_component_name=$(this).closest('td').prev().find('.remaining_levels').val();
    if(component_name !== old_text){
      // alert("fdsg")
      if(component_name != ''){
        $.ajax({
          type:"GET",
          url:'/cost_code/check_costcode',
          data:{'component_name':component_name,'level_id':level_id,'level_index':level_index,'level1':level1,'level2':level2,'pre_cost_code':pre_cost_code,'pre_component_name':pre_component_name},
          success: function(data){
            data_to_append={}
  
            current_element.closest('td').find('.sequence_gap').val(data.sequence_gap)
            current_element.closest('td').find('.costcode_type').val(data.code_type)
            current_element.closest('td').find('.no_of_digits').val(data.no_digits)
            current_element.closest('td').find('.old_text').val(component_name)
  
  
            cost_code =level1_split[2]+cost_code_type+level2_split[1]+cost_code_type
            if(rowindex == 0){
              current_element.closest('td').find('.costcode').val(data.last_code)
              current_element.closest('tr').find('.costcode').each((index, element) => {
                var add_index=index+3
                var current_component_name=current_element.closest('tr').find('td:eq("'+index+'") .remaining_levels').val()
  
                if($(element).val()){
                  cost_code=cost_code+$(element).val()
                  data_to_append['level'+add_index+'_code'] = $(element).val()
                  if (index !== remaining_level_count - 1) {
                    cost_code=cost_code+cost_code_type
                  }
                  data_to_append['level'+add_index+'_name'] = current_component_name
                } 
              });
              data_to_append['costcode']=cost_code
              allcostcode_list[rowindex]=data_to_append
  
            }else{
              current_element.closest('tr').find('.costcode').each((index, element) => {
  
                var add_index=index+3
                var current_component_name=current_element.closest('tr').find('td:eq("'+index+'") .remaining_levels').val()
                // alert(current_component_name)
                var current_sequence_gap=current_element.closest('tr').find('td:eq("'+index+'") .sequence_gap').val()
                var current_costcode_type=current_element.closest('tr').find('td:eq("'+index+'") .costcode_type').val()
                var current_no_of_digits=current_element.closest('tr').find('td:eq("'+index+'") .no_of_digits').val()
  
                if(current_component_name){
                  if(index == 0){
                    var current_component=current_element.closest('tr').find('td:eq("'+index+'") .remaining_levels').val()
  
                    var previous_component=current_element.closest('tr').prev().find('td:eq("'+index+'") .remaining_levels').val()
                    var previous_costcode=current_element.closest('tr').prev().find('td:eq("'+index+'") .costcode').val()
                    if(data.code_type == 'old'){
                      if(index == current_index){
                        start_with=data.last_code
                      }else{
                        start_with= $(element).val()
                      }
                    }
                    else{
                      var check_component_exist=findcostcode_exist_by_componentname(allcostcode_list,'level'+add_index+'_name',current_component_name)
                      // console.log("check_component_exist "+check_component_exist)
                      if(check_component_exist.length > 0){
                        start_with=check_component_exist[0]['level'+add_index+'_code']
                      }
                      else{
                      if(current_costcode_type == 'old'){
                        start_with= $(element).val()
  
                      }else{
                        // console.log("allcostcode_list "+JSON.stringify(allcostcode_list))
                        if(allcostcode_list.length == 1){
                          var new_costcode_array=allcostcode_list
  
                        }else{
                          var new_costcode_array=allcostcode_list.slice(0,-1)
                        }
                        // console.log("new_costcode_array"+new_costcode_array)
                        var levelcodes = new_costcode_array.map(item => parseInt(item['level'+add_index+'_code'], 10));
                        // console.log("levelcodes "+levelcodes)
                        var maxNumber = Math.max(...levelcodes);
                        let maxNumber_string = maxNumber.toString();
                        const paddingLength = current_no_of_digits - maxNumber_string.length;
  
                        if (paddingLength > 0) {
                          newCostCode = '0'.repeat(paddingLength) + maxNumber_string;
                        }
  
                        start_with=sumCostCode(newCostCode,parseInt(current_sequence_gap)+1)
                      }
                       
                      }
                    }
                  }
                  else{
                    var previous_td_index=index-1
                    var current_previous_component=current_element.closest('tr').find('td:eq("'+previous_td_index+'") .remaining_levels').val()
                    var previous_previous_component=current_element.closest('tr').prev().find('td:eq("'+previous_td_index+'") .remaining_levels').val()
                    var previous_costcode=current_element.closest('tr').prev().find('td:eq("'+index+'") .costcode').val()
                    if(data.code_type == 'old'){
                      if(index == current_index){
                        start_with=data.last_code
                      }else{
                        start_with= $(element).val()
                      }
                    }else{
                      var check_component_exist=findcostcode_exist_by_componentname(allcostcode_list,'level'+add_index+'_name',current_component_name)
                      // console.log("index "+index)
                      console.log(check_component_exist)
                      if(check_component_exist.length > 0){
                        var previous_index=add_index-1
                        check_previous_costcode = allcostcode_list.slice(0, -1).filter(item => item['level'+previous_index+'_name'] === current_previous_component);
                        if(check_previous_costcode.length > 0){
                          // console.log(JSON.stringify(check_previous_costcode))
                          start_with=check_previous_costcode[0]['level'+add_index+'_code']
                        }else{
                          if(index == current_index){
                            start_with=data.last_code
                          }
                          else{
                            start_with= $(element).val()
      
                          }
                        }
  
                      }else{
                        if(current_previous_component.trim().toLowerCase() == previous_previous_component.trim().toLowerCase()){ 
                          start_with=sumCostCode(previous_costcode,parseInt(current_sequence_gap)+1)
                        }else{
                          if(index == current_index){
                            var previous_index=add_index-1
                            check_previous_costcode = allcostcode_list.slice(0, -1).filter(item => item['level'+previous_index+'_name'] === current_previous_component);
                            if(check_previous_costcode.length > 0){
                              var levelcodes = check_previous_costcode.map(item => parseInt(item['level'+add_index+'_code'], 10));
                              var maxNumber = Math.max(...levelcodes);
                              let maxNumber_string = maxNumber.toString();
                              const paddingLength = current_no_of_digits - maxNumber_string.length;
                              if (paddingLength > 0) {
                                newCostCode = '0'.repeat(paddingLength) + maxNumber_string;
                              }
    
                              start_with=sumCostCode(newCostCode,parseInt(current_sequence_gap)+1)
  
  
                            }else{
                              start_with=data.last_code
                            }
      
                          }
                          else{
                            start_with= $(element).val()
      
                          }
                        }
  
  
  
  
  
                      }
                    
                    }
                    // console.log("start_with "+start_with)
                  }
                  $(element).val(start_with)
                  cost_code=cost_code+start_with
                  if (index !== remaining_level_count - 1) {
                    cost_code=cost_code+cost_code_type
                  }
                  data_to_append['level'+add_index+'_name'] = current_component_name
                  data_to_append['level'+add_index+'_code'] = start_with
  
                }
      
              });
              data_to_append['costcode']=cost_code
              allcostcode_list[rowindex]=data_to_append
              
            }
            checkcostcode = allcostcode_list.slice(0, -1).filter(item => item['costcode'] === cost_code);
            console.log("checkcostcode "+checkcostcode)
            
            if(checkcostcode.length > 0){
              current_element.closest('tr').find('.cost_code_preview').html('<span class="waring-err">Cost Code Already Exists</span>')
              current_element.closest('tr').find('.costcodepreview').val('')
            }
            else{
              current_element.closest('tr').find('.cost_code_preview').html(cost_code)
              current_element.closest('tr').find('.costcodepreview').val(cost_code)
            }
    
        
          
            checkcostcode_exist_database(current_element,cost_code,allcostcode_list,rowindex)
            // checkcostcode_exist_local(current_element,cost_code,allcostcode_list,rowindex)
  
        
          
  
  
          }
        })
      }
    }
   
  })

 
  function findcostcode_exist_by_componentname(allcostcode_array,level_name,component_name) {

    checkcostcode = allcostcode_array.slice(0, -1).filter(item => item[level_name].trim().toLowerCase() === component_name.trim().toLowerCase());
    // console.log("checkcostcode"+checkcostcode)
    return checkcostcode
  }
  function checkcostcode_exist_local(current,cost_code,allcostcode_array,rowindex){
    console.log("rowindex"+rowindex)
    checkcostcode = allcostcode_array.slice(0, -1).filter(item => item['costcode'] === cost_code);
    if(checkcostcode.length > 0){
      var currentRow=$('#cost_code_table tr:eq('+rowindex+')');
      currentRow.find('.cost_code_preview').html('<span class="waring-err">Cost Code Already Exists</span>')
    }

  }
  function checkcostcode_exist_database(current,cost_code,allcostcode_array,rowindex){
    $.ajax({
        type:"GET",
        url:'/cost_code/check_costcode_exists',
        data:{'cost_code':cost_code},
        success: function(data){
            if(data.status==true){
              current.closest('tr').find('.cost_code_preview').html('<span class="waring-err">Cost Code Already Exists</span>')
            }
            // // console.log("allcostcode_array "+JSON.stringify(allcostcode_array))
            // // console.log("cost_code "+cost_code)
            // console.log("current "+current.closest('tr').index())
            // checkcostcode = allcostcode_array.slice(0, -1).filter(item => item['costcode'] === cost_code);

            // // console.log("checkcostcode "+JSON.stringify(checkcostcode))
            // if(checkcostcode.length > 0){
            //   var current_index=current.closest('tr').index()
            //   // alert(rowindex)
            //   var currentRow=$('#cost_code_table tr:eq('+current_index+')');
            //   currentRow.find('.cost_code_preview').html('<span class="waring-err">Cost Code Already Exists</span>')

            // }

        

        }
      })
  }

$(document).on('click','.project_delete',function(){
var delete_id=$(this).attr('costcodemain-id')
var order_id=$(this).attr('data-id')
        Swal.fire({
          title: 'Are you sure you want to delete ',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, I Confirm',
          cancelButtonText: 'No',
        }).then((result) => {
          if (result.isConfirmed) {
              $.ajax({
              type: "GET",
              url:'/cost_code/deletecostcode/'+order_id+'/'+delete_id+'',
              data: {
                "id":delete_id,
              },
              success: function(data)
              {
                // console.log(data)
                setTimeout(function(){  
                location.reload();  
                },1000);
              }
              });
            Swal.fire('Deleted Successfully')
          }
        })


})


$(document).on('keyup','.costcodelevel',function(){
  currentval = $(this).val()
  currentposition=$(this)
  tdposition = $(this).closest('td').index()
  currentposition.closest('td').find('span').remove();
  // console.log({'currentval':currentval})
      // $(this).closest('table tbody').find('tr').not($(this).closest('tr')).each(function(index,val){
      //     let getEle = $(val).find(`td`).eq(tdposition).find('.costcodelevel:visible')
      //     index = getEle.prop("tagName").toLowerCase() == 'select' ? $(getEle).find('option:selected').text() : getEle.val()
      //         if(currentval==index){
      //             currentposition.addClass('con_error')
      //             $('.final-cls').attr('disabled',true)
      //         } 
      //         else{ 
      //             // getEle.removeClass('con_error')
      //             currentposition.removeClass('con_error')
      //             $('.final-cls').attr('disabled',false)
      //         }
      //   })
    })
})

$(document).on('keyup','.new_level_cls',function(){
 //checking newlevel data with db
//  console.log('csrf_token',csrf_token)
 levelid = $(this).closest('td').find('.masterId').val()
//  console.log('currentval',$(this).val())
//  console.log('levelid',levelid)
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

$(document).on('change','.new_level_cls ',function(){
 currentpos = $(this)
 currentval = $(this).val()
 currentlev = $(this).closest('td').find('.masterId').val()
 let duplicatecount=0
 $('.new_level_cls').each(function(){
    if($(this).closest('td').find('.masterId').val() == currentlev && $(this).val() != ''){
      // console.log('value',$(this).val())
      if(currentval == $(this).val()){
        duplicatecount++;
      }
    }
      if(duplicatecount > 1){
        currentpos.css("border", "1px solid red");
        savebtb.attr('disabled',true)
      }
      else{
        currentpos.css("border", "");
        savebtb.attr('disabled',false)
      }
  })
})

$('form').submit(function(){
 
return true;
});

$(document).on('change','#level1_category,#level2_category',function(){
  if($(this).val() != ' '){
    $(this).removeClass('con_error')
    var level1=$('#level1_category').val()
    var level2=$('#level2_category').val()
    var level1 = 'level1='+level1+'';
    var level2 = 'level2='+level2+'';
    var newHref = '/cost_code/downloadcostcode_template?' + level1 + '&' + level2 ;
    $('.download_template_btn').attr('href', newHref);
  }
})
                               
$(document).on('click','.addbtn',function(){

  var scrollTo = $(document).height() - $(window).height();
  $('html, body').animate({ scrollTop: scrollTo }, 'slow');
})

