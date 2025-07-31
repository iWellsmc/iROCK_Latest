var project_id='';

$('.submit-cls').click(function(){
  var button_data_id=$(this).attr('data-id');
  project_id=$(this).attr('project_id');
    if (button_data_id=="1"){
        var form=$("#edit-masterproject");
        $.ajax({
          type:"POST",
          container:"#edit-masterproject",
          url:'/projects/editmasterproject',
          data:form.serialize(),
          success: function(data){
              console.log(data.data)
            // project_id=data.data
          }
        })
    }
    else if (button_data_id=="2") {
        var form=$("#edit-block");
        $.ajax({
          type:"POST",
          container:"#edit-block",
          url:'/projects/editblock',
          data:form.serialize(),
          success: function(data){
              console.log(data.data)
          }
        })

    }
    else if (button_data_id=="3") {
      var form=$("#edit-field");
      $.ajax({
        type:"POST",
        container:"#edit-field",
        url:'/projects/editfield',
        data:form.serialize(),
        success: function(data){
            console.log(data.data)
        }
      })

  } 
  else if (button_data_id=="4") {
    var form=$("#edit-cluster");
    $.ajax({
      type:"POST",
      container:"#edit-cluster",
      url:'/projects/editcluster',
      data:form.serialize(),
      success: function(data){
          console.log(data.data)
      }
    })

}

    //sweet alert 

    if (button_data_id=="1"){
        Swal.fire({
            text: 'Do you edit/add block(s) to this project?',
            showDenyButton: true,
            confirmButtonColor: '#77d61f',
            denyButtonColor:'#AF2B50',
            confirmButtonText: 'Yes',
            denyButtonText: 'No',
            customClass: {
              actions: 'my-actions',
              confirmButton: 'order-2',
              denyButton: 'order-3',
            }
          }).then((result) => {
            if (result.isConfirmed) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace('editmasterproject/','editblock/')
              window.location.href = replace_url;
            } else if (result.isDenied) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace('editmasterproject/'+project_id+'','listmaster/')
              window.location.href = replace_url;
            }
          })
    }
    else if(button_data_id=="2"){
        Swal.fire({
            text: 'Do you edit/add field(s) to this project?',
            showDenyButton: true,
            confirmButtonText: 'Yes',
            denyButtonText: 'No',
            confirmButtonColor: '#AF2B50',
            denyButtonColor:'#AF2B50',
            customClass: {
              actions: 'my-actions',
              confirmButton: 'order-2',
              denyButton: 'order-3',
            }
          }).then((result) => {
            if (result.isConfirmed) {
              var current_url=$(location).attr("href")
              var replace_url=current_url.replace('editblock/','editfield/')
              window.location.href = replace_url;
            } else if (result.isDenied) {
              var current_url=$(location).attr("href")
              // alert(project_id)
              var replace_url=current_url.replace('editblock/'+project_id+'','listmaster/')
              window.location.href = replace_url;
            }
          })
    }
    else if(button_data_id=="3"){
      Swal.fire({
          text: 'Do you want to edit/add  Well Pad/ Well Platform/ Subsea Cluster (s) to this project?',
          showDenyButton: true,
          confirmButtonText: 'Yes',
          denyButtonText: 'No',
          confirmButtonColor: '#AF2B50',
          denyButtonColor:'#AF2B50',
          customClass: {
            actions: 'my-actions',
            confirmButton: 'order-2',
            denyButton: 'order-3',
          }
        }).then((result) => {
          if (result.isConfirmed) {
            var current_url=$(location).attr("href")
            var replace_url=current_url.replace('editfield/','editcluster/')
            window.location.href = replace_url;
          } else if (result.isDenied) {
            // alert(project_id)
            var current_url=$(location).attr("href")
            var replace_url=current_url.replace('editfield/'+project_id+'','listmaster/')
            window.location.href = replace_url;
          }
        })
  }
})

var row=1;
$(document).on("click","#block-add-row", function(){
    var new_row='<tr id="blockrow'+row+'"><input type="hidden" name="block_id" value=" "><td><input name="block_name" type="text" id="block'+row+'"class="form-control" placeholder="Block Name"/></td><td><button id="delete-row" class="btn-clr block-delete-row btn btn-primary" type="button" value="delete"><i class="fa fa-minus"></i></button></td>'
    $("#block_table").append(new_row);
    // alert(new_row)
    row++;
    return false;
})
$(document).on("click", ".block-delete-row", function () {
    $(this).closest('tr').remove();
    if(row>0) {
        $(this).closest('tr').remove();
        row--;
      }
    return false;
})
//field add

$('input[name="block_name_check"]:checked').each(function() {
  console.log(this.value); 
});
$(document).on("change","[name=block_name_check]", function(){

    var val=$(this).attr('data-id');
    var field=''
    if ($(this).is(":checked")){
        field+='<table id ="table_field-'+val+'" ><tbody><tr><td id="fieldrow0"><input type="text" name="field_name'+val+'" class="form-control" placeholder="Field Name"></td><td><button id="field-add-row" class="btn btn-clr add-btn" type="button" data-id='+val+' value="Add"><i class="fa fa-plus"></i></button></td></tr></tbody></table>'
    //     //ui next start
        let appendTable = $(this).parent().next();
        appendTable.append(field);
      
    }
    else{
        $('#table_field-'+val+'').remove();
    }
})
var row=1;
$(document).on("click","#field-add-row", function(){
    var get_table_id=$(this).attr('data-id');
    // alert(get_table_id)
    var new_row='<tr id="fieldrow'+row+'"><input type="hidden" name="field_hd'+get_table_id+'" value="" ><td><input name="field_name'+get_table_id+'" type="text" id="field'+row+'"class="form-control" placeholder="Field Name"/></td><td><button id="delete-row" class="btn-clr field-delete-row btn btn-primary" type="button" value="delete"><i class="fa fa-minus"></i></button></td>'
    $('#table_field-'+get_table_id+'').append(new_row);
    row++;
    return false;
})
$(document).on("click", ".field-delete-row", function () {
  $(this).closest('tr').remove();
  if(row>1) {
      $(this).closest('tr').remove();
      row--;
    }
  return false;
})

// clusters add
$(document).on('change','input[name="field_checkbox"]',function(){
  var data_id=$(this).attr('p_id');
  var get_check_field=$(this).next('label').text();
  var field_type=''
  if ($(this).is(":checked")){
    field_type+='<div id="fieldsub_id'+data_id+'"><h5>'+get_check_field+'</h5>'
    field_type+='<input type="checkbox" name="field_subtype'+data_id+'" id="field_subtype_id1"  data-id="'+data_id+'" data-name="well_pad" class="field-class" value="well_pad">&emsp;<label>Well Pad</label><br><input type="checkbox" name="field_subtype'+data_id+'" id="field_subtype_id2"  data-id="'+data_id+'" class="field-class" data-name="well_platform" value="well_platform">&emsp;<label>Well Platform</(label)><br><input type="checkbox" name="field_subtype'+data_id+'" id="field_subtype_id3" data-id="'+data_id+'" class="field-class" data-name="subsea_clusters" value="subsea_clusters">&emsp;<label>Subsea Clusters</label><br>'
    field_type+='<br>'
    $(".field_subtype").append(field_type);
  }
  else{
      $('#fieldsub_id'+data_id+'').remove();
  }
})