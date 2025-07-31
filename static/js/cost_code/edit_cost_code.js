$(document).ready( function () {
    cost_code_type= $('#costcode_type').val()

    // $(document).on('change', '.remaining_levels', function() {
    //     var original_value=$(this).closest('td').find('.oldcostcode').val()
    //     var current=$(this)
    //     var cost_code=''
    //     var index=current.closest('tr').index()
    //     cost_code=current.find('option:selected').attr('cost_code')
    //     current.closest('td').find('.costcode').val(cost_code)
    //     level1_cost_code=$('#level1_costcode').val()
    //     level2_cost_code=$('#level2_costcode').val()
    //     cost_code =level1_cost_code+cost_code_type+level2_cost_code+cost_code_type
    //     level_count= current.closest('tr').find('.costcode').length
    //     console.log("level_count"+level_count)
    //     console.log(current.closest('tr').find('.costcode'))
    //     current.closest('tr').find('.costcode').each((index, element) => {
    //       if($(element).val()){
    //         console.log("value"+$(element).val())
    
    //         cost_code=cost_code+$(element).val()
    //         if (index !== level_count - 1) {
    //           cost_code=cost_code+cost_code_type
    
    //         }
    //       }
    //     });
    //     checkcostcode_exist(current,original_value,cost_code)
    // }) 
    $(document).on('change', '#level1_category', function() {
        var development_id=$(this).val();
        var id_array=development_id.split('_')
        var original_value=$('#level1_costcode').val()
        var current=$(this)
        level2_cost_code=$('#level2_costcode').val()
        $.ajax({
            type:"GET",
            url:'/cost_code/level1costcode',
            data:{'discipline_id':id_array[0],'development_id':id_array[1]},
            success: function(data){
              var cost_code=''
              cost_code=data.cost_code+cost_code_type+level2_cost_code+cost_code_type
              $('#level1_costcode').val(data.cost_code)
              $('#cost_code_table').find('tr').each((index, row) => {
                level_count= $(row).find('.costcode').length
                $(row).find('.costcode').each((index, column) => {
                  if($(column).val()){            
                    cost_code=cost_code+$(column).val()
                    if (index !== level_count - 1) {
                      cost_code=cost_code+cost_code_type
                    }
                  }
                })
                $(row).find('.cost_code_preview').html(cost_code)
                $(row).find('.costcodepreview').val(cost_code)
                discipline=''
                discipline += '<option value=" " selected>--Select--</option>'
                $.each(data.data,function(key,val){
                  discipline +='<option value='+val.id+'>'+val.discipline_subtype+'</option>'
                })
                discipline +='</select>'
                $('#level2_category').html(discipline);

              })

            }
        })
    })
    $(document).on('change', '#level2_category', function() {
      var level2_disciplineid=$(this).val()
      level1_cost_code=$('#level1_costcode').val()

      $.ajax({
        type:"GET",
        url:'/cost_code/getlevel2_costcode',
        data:{'discipline_id':level2_disciplineid},
        success: function(data){
          $('#level2_costcode').val(data.cost_code)
          var cost_code=''
          cost_code=level1_cost_code+cost_code_type+data.cost_code+cost_code_type
          $('#cost_code_table').find('tr').each((index, row) => {
            level_count= $(row).find('.costcode').length
            $(row).find('.costcode').each((index, column) => {
              if($(column).val()){            
                cost_code=cost_code+$(column).val()
                if (index !== level_count - 1) {
                  cost_code=cost_code+cost_code_type
                }
              }
            })
            $(row).find('.cost_code_preview').html(cost_code)
            $(row).find('.costcodepreview').val(cost_code)

          })
        }
      })
    })
    $('#edit_costcode_form').submit(function(e) {
      let validation=false
      $('#cost_code_table').find('tr').each((index, row) => {
        $(row).find('.remaining_levels').each((index, column) => {
          if(!$(column).val()){   
             validation=true 
            $(column).css("border", "1px solid red");
          }else{
            $(column).css("border", "");
  
          }
        })
      })
      if(validation==false){
        this.submit();
      }else{
        return false
  
      }

    })
})
function checkcostcode_exist(current,original_value,cost_code){
  var submitclass = $('.final-cls')
    $.ajax({
        type:"GET",
        url:'/cost_code/check_costcode_exists',
        data:{'cost_code':cost_code},
        success: function(data){
           if(data.status==true){
            current.closest('tr').find('.cost_code_preview').html('<span class="waring-err">Cost Code Already Exists</span>')
            current.val(original_value)
            submitclass.attr('disabled',true)
           }else{
            current.closest('tr').find('.cost_code_preview').html(cost_code)
            current.closest('tr').find('.costcodepreview').val(cost_code)
            submitclass.attr('disabled',false)
          }
        }
      })
}

$(document).ready(function(){
  var level1=$('#level1_category').val()
  $('.level_1_type').val(level1)
  var level2=$('#level2_category').val()
  $('.level_2_type').val(level2)
})

