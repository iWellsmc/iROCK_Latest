$(document).on('click','.querycls',function(){
    var val=$(this).val()
    var get_type=$(this).attr('data_name')
    var refnum=$(this).closest('tr').find('td:eq(2)').text()
    var rep_val=refnum.replace(/ /g, "_");
    var html=''
    var fileinput=''
    var $this = $(this);
    if ($this.is(':checked')){
      $.ajax({
        url: "getrelationfile",
        method: "GET",
        data: {
  
          id: val,
          contract_type: get_type,
          file_type: "1",
  
        },
  
        success: function(data) {
          val=data.data
          html+='<tr><td colspan="8" class="vend-top-boto"><div class="row"><input type="hidden" name="ref_num" value="'+rep_val+'"><input type="hidden" name="contract_type'+rep_val+'" value="'+get_type+'"><div class="col-5"><div class="rea-qu"><label class="rea-query-com">Reason for Query <span class="star-clr">*</span></label></div><textarea class="form-control rea-sonfont r-txtarea" id="reasoncls" name="reason'+rep_val+'" rows="3" cols="50"></textarea></div><div class="col-3"><div class="rea-qu"><label class="rea-type document-types">Document Type<span class="star-clr pl-1">*</span></label></div><select name="type'+rep_val+'" class="form-control form-select rea-type-cls"><option value="4">Query</option><option value="1">Replacement</option><option value="3">Reference</option></select></div><div class="col-4 file-div comp_currency"><div class="rea-qu"><label class="rea-upload-com">Upload Documents <span class="star-clr">*</span></label></div><select name="repfiles'+rep_val+'" class="mb-3 form-control form-select file_form"> <option ></option>'

          for (let key in val) {
            if (val.hasOwnProperty(key)) {
                html += '<option  value='+val[key][0].id+'>'+val[key][0].original_file_name+"</option>";

            }
          }
          html+='</select><input type="file" accept="image, .png, .jpeg, .pdf, .jpg" name="cfile'+rep_val+'" class="filesize form-control query-file filesize"><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></div></div></div></tr>'
          //html+='<tr><td colspan="4"><textarea class="form-control"  name="reason'+val+'" placeholder="Reason for Query" rows="3" cols="50"></textarea></td><td colspan="3"><input type="file" name="cfile'+val+'" class="form-control"><span class="maxmp">(Max: 25MB)</span><br><span class="file-error-message"></span></td></tr>'
          $this.closest('tr').after(html)
         
          // $(this).closest('tr').append(fileinput);
  
          
        // console.log(fileinput)
        // var fileForm = $('.file_form');
  
        // fileForm.append(fileinput);
  
  
  
          
          // Handle errors
        },
        error: function(xhr, status, error) {
          // Handle errors
          console.error(status, error);
        }
      });

   
    $.ajax({
      url: "getrelationfile",
      method: "GET",
      data: {

        id: val,
        contract_type: get_type,
        file_type: "1",

      },

      success: function(data) {
        val=data.data
       
        $(this).closest('tr').append(fileinput);

        for (let key in val) {
          if (val.hasOwnProperty(key)) {
              console.log(val[key][0].id)
               fileinput += '<option  value='+val[key][0].id+'>'+val[key][0].original_file_name+"</option>";
          }
      }
      console.log(fileinput)
      var fileForm = $this.find('.file_form');


      fileForm.html(fileinput);



        
        // Handle errors
      },
      error: function(xhr, status, error) {
        // Handle errors
        console.error(status, error);
      }
    });









      // $(this).closest('tr').next('tr').find('td:eq(0)').find('#reasoncls').summernote({ toolbar: false,});
    }
    else {
      $this.closest('tr').next('tr').remove()
    }
  })

  $(document).on('click','.querycls',function(){      
    $('#reasoncls').summernote({
      toolbar: false,
    });
  })



  $(document).on('click', '.submit-cls', function (e) {

    let total_count = 0;
    $('input.commoncls[type=checkbox]').not(':hidden').each(function () {
      if ($(this).is(':checked')) {
        total_count += check_value('rea-type-cls');
        total_count += check_value('rea-sonfont');
        total_count += check_value('query-file');
        if (total_count > 0) {
          e.preventDefault();
        }
      }
    })
  })

  function check_value(classname) {
    let count = 0;
    $("." + classname + "").each(function () {
      var val = $(this).val()
      if (classname == 'query-file') {
        var selected_value = $(this).parent().parent().find('.rea-type-cls').find(':selected').val()
        if (selected_value != '') {
          if (selected_value != '4') {
            if (val == '') {
              count++;
              $(this).addClass('con_error')
            }
          }
        }
      }
      else {
        if (val == '') {
          count++;
          $(this).addClass('con_error')
        }
      }

    })
    return count;
  }

  $(document).on('change', '.con_error', function () {
    $(this).removeClass('con_error')
  })

  $(document).on('change', '.rea-type-cls', function () {
    var val = $(this).find(':selected').val();
    if (val) {
      if (val != '4') {
        $(this).closest('tr').find('.file-div').css('display', 'block')
      }
      else {
        $(this).closest('tr').find('.file-div').css('display', 'none')
      }
    }
    else {
      $(this).closest('tr').find('.file-div').css('display', 'none');
    }
    $(this).closest('tr').find('.file-div').val('');
  })

  $(document).ready(function() {
    var counters = 1; 
    var counter = 1; 
    var counterss =1;
    $('.counter').each(function() {
        $(this).text(counter++); 
    });
    $('.counters').each(function() {
        $(this).text(counters++); 
    });
    $('.counterss').each(function() {
        $(this).text(counterss++); 
    });


});