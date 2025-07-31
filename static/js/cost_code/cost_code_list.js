var scheme = $('.scheme').val()
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val()

console.log('scheme',scheme)
var gethost = $('.gethost').val()
var csrf_token = $('.csrf_token').val()

$(document).ready( function () {
  setSerialNumber();

  $("form[id='specific_contract']").validate({ 
    rules: {
      level_1:{required: true},
      level_2:{required: true},

    },
    errorPlacement: function(error, element) {
    },
    highlight: function(element) {
      if ($(element).is('select')) {
        $(element).addClass('red_outline');
      }
    },
    unhighlight: function(element) {
      if ($(element).is('select')) {
        $(element).removeClass('red_outline');
      }
    }
  });




})

function setSerialNumber(){
  $(document).on('#costcodelist_table tbody').find('tr').not('tr:first').each((index, row) => {
    $(row).find('.s_no').html(index+1)
  })
}

$(document).on('change','#datafilters',function(e){
  let query = $('#myInput').val();
  console.log('query',query)
  //let page = $(this).attr('data-id')
  let pageperdata = $(this).val()
  console.log('pageperdata',pageperdata)
  searchList(query,1,pageperdata)
});


$(document).on('input', "#myInput", function () {
   
   
  let query = $(this).val()
  let pageperdata = $('#datafilters').val()
  
  setTimeout(function () {
      searchList(query,1,pageperdata)
      }, 100);

});

$(document).on('click','.pg-circle',function(e){
  e.preventDefault();
  let query = $('#myInput').val();
  let page = $(this).attr('data-id')
  let pageperdata = $('#datafilters').val()
  console.log({'pageperdata':  pageperdata })
  searchList(query,page,pageperdata)
})

$(document).on('change','.changevalue',function(e){
    
  let query = $('#myInput').val();
  //let page = $(this).attr('data-id')
  let pageperdata = $(this).val()
  console.log({'csrf_tokensearchList':  pageperdata })
  searchList(query,1,pageperdata)
});

function searchList(query,page,pageperdata) {
  console.log({'csrf_tokensearchList':  pageperdata })
  $.ajax({
      url: "/cost_code/costcodelist",
      headers: {'X-CSRFToken': csrftoken },
      data: { 
          'q': query,
          'page':page,
          'pageperdata':pageperdata
      },
      type: 'POST',
      success: function (response) {
          if (response.status) {
              console.log('right')
              console.log(response)
              $('section').replaceWith(response.html)
              $('.check_type').each(function(){
                if($(this).children().length == 0){
                   $(this).text('-')
                }
              })
              let focusElement = $(document).find('#myInput')
              let elementLength = focusElement.val().length;
              focusElement[0].focus();
              focusElement[0].setSelectionRange(elementLength,elementLength);
              $('#datafilters').val($('.entries').val())
              setSerialNumber()
          } else {
              console.log('wrong')
          }
      },
      error: function () {
          // Error message
      }
  });
}

$(document).on('change', '#level1_category', function() {
  var development_id=$(this).val();
  var id_array=development_id.split('_')
  var discipline=''
  level1=$('#level1_category').val()
  level2=$('#level2_category').val()
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
          start_with=sumCostCode(start_with,data.sequence)
        })
        discipline +='</select>'
        $('#level2_category').html(discipline);
        $('#level1_costcode').val(data.cost_code)
    }
  })
})

function sumCostCode(costcode, sequence_gap) {
  let newCostCode = (parseInt(costcode, 10) + parseInt(sequence_gap, 10)).toString();
  const paddingLength = costcode.length - newCostCode.length;

  if (paddingLength > 0) {
      newCostCode = '0'.repeat(paddingLength) + newCostCode;
  }
  
  return newCostCode;
}

$(document).on('change', '#level2_category', function() {
  var discipline_id=$(this).val()
  level1=$('#level1_category').val()
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


    }
  })

})



$( document ).ready(function() {
  $('#submitbtn').prop('disabled', true);
  var notyf = new Notyf({
      duration: 2000,
      position: {
        x: 'right',
        y: 'top',
      },
      types: [
        {
          type: 'success',
          background: '#D3D3D',
          icon: {
            className: 'fa fa-check-circle',
            tagName: 'i',
            color: '#000',
          },
        },
      ]
    });

  var msg=$('.msg-cls').text();
  if (msg){
    notyf.open({
    type: 'success',
    message: msg,
  }); 
  }

  $('#costcodelist_table').DataTable({
    serverSide: true,
    "ordering": false,
    ajax: {
        url: "/cost_code/getcost_code",                    
        type: 'GET',
        dataSrc: function(response) {
         
          return response.data;
      }
    },

    columns: [
        { data: 's_no' },
        { data: 'costcode' },
        { data: 'codecode_component' },
        {
          data: null,
          render: function (data, type, row) {
            actions_html=''
            actions_html +='<a class="add_sequence_costcode align-icons" data-id='+data.order+' costcode_main='+data.costcode_main_id+' data-toggle="modal" href="#addsequence_modal_popup"><span class="add_sequence"><i class="fa fa-plus" title="Add Sequence" style="font-size: 17px; color: #95183a;"></i></span></a>'     
            if(data.status == 1){
              actions_html +='<a class="text-decoration-none" href="/cost_code/editcostcode/'+data.order+'/'+data.costcode_main_id+'"><span class="action-edit align-icons"><i class="fa fa-pencil" title="Edit"></i></span></a>'    
            }
            // actions_html +='<a class="project_delete align-icons" data-id='+data.order+' costcodemain-id='+data.costcode_main_id+' ><span class="action-delete"><i class="fa fa-trash-o" title="Delete"></i></span></a>' 
            if(data.status == 1){
              actions_html +='<label class="switch">'
                actions_html +='<input type="checkbox" class="inpt costcode_checkbox" value='+data.order+' costcode_mainid='+data.costcode_main_id+' checked>'
                actions_html +='<span class="slider round"  id="input1" title="Active"></span>'
              actions_html +='</label>'

            }else{
              actions_html +='<label class="switch">'
                actions_html +='<input type="checkbox" class="inpt costcode_checkbox" value='+data.order+' costcode_mainid='+data.costcode_main_id+'>'
                actions_html +='<span class="slider round" id="input1" title="Inactive"></span>'
              actions_html +='</label>'


            }

            
            

            return actions_html  
          }
        }

    ],
    language: {
      emptyTable: "---"
    },
    drawCallback: function(settings) {
      var api = this.api();
      var sequence_gap_level_count = api.ajax.json().extra_data.sequence_gap_level_count;

      if (sequence_gap_level_count === 0) {
          $('.add_sequence_costcode').hide(); 
      } else {
          $('.add_sequence_costcode').show(); 
      }
  }
  });










})

$(document).on('change','.costcode_checkbox',function(){
  var order=$(this).val();
  var costcode_mainid=$(this).attr('costcode_mainid');
  var status = $(this).is(':checked') ? 1 : 0; 

  var current_element=$(this)
  $.ajax({
    type: "GET",
    url:'/cost_code/update_costcode_status',
    data: {
      "order":order,
      'costcode_mainid':costcode_mainid,
      'status':status
    },
    success: function(data)
    {
      if(data.status == true){
        window.location.reload();
      }else{
        current_element.prop('checked', true);
        Swal.fire({
          icon: 'error',
          title: 'Error...',
          text: 'Cost Code Already Assigned to vendor',
        })
      }


    }
  })
 
})


$(document).on('change','#cost_cost_file',function(){
  var val=$(this).val()
  if (val !="" && val.split('.').pop()=='xlsx'){
    $('#submitbtn').prop('disabled', false);
  }
  else{
    $('#submitbtn').prop('disabled', true);
  }
})







$(document).on('click','#submitbtn',function(e){
  let level_1=$('#level1_category').val()
  let level_2=$('#level2_category').val()
  if((level_1 == '' && level_2=='') || (level_2==null) || (level_2=='')  || (level_1=='')){
    e.preventDefault()
  }
  else{
    //  $('#submitbtn').prop('disabled', true);
    $('#loader').removeClass('hidden')
    return true
    
  }
  if(level_1 == ''){
    $('#level1_category').css("border", "1px solid red");
  }
  if(level_2 == ''){
    $('#level2_category').css("border", "1px solid red");
  }
})

$(document).on('change','#level1_category,#level2_category',function(){
  if($(this).val != ''){
    $(this).css("border", "");
  }
})

$(document).on('click','.generatebtn',function(){
  Swal.fire({
    icon: 'error',
    title: 'Error...',
    text: 'Please Add the Cost Code information ',
    })
})

$(document).on('click','.cctemplate',function(event){
   if($('#level1_category').find(":selected").val() == '' || $('#level1_category').find(":selected").val() == 'undefined'){
    $('#level1_category').addClass('con_error')
    event.preventDefault(); 
  }
  else{
    $('#level1_category').removeClass('con_error')
   }
  if($('#level2_category').find(":selected").val() == '' || $('#level2_category').find(":selected").val() == 'undefined'){
    $('#level2_category').addClass('con_error')
    event.preventDefault(); 
  }
  else{
    $('#level2_category').removeClass('con_error')
    }
})
$(document).on('click','.add_sequence_costcode',function(event){
  var order=$(this).attr('data-id')
  var costcode_main=$(this).attr('costcode_main')
  $('#costcode_main_id').val(costcode_main)
  $('#order').val(order)
  $.ajax({
    url: "/cost_code/check_sequence_exist",
    data: { 
        'order': order,
        'costcode_main':costcode_main
    },
    type: 'GET',
    success: function (response) {
      console.log(response.data)
      var option_html=''
      option_html +='<option value="">Select Level</option>'
      $.each(response.data, function(index, value) {
        option_html +='<option value='+value.level_index+' level_id='+value.level_index+'>'+value.name+'</option>'
      });
      $('#sequence_level').html(option_html)
    },
    error: function () {
        // Error message
    }
  });

})

$(document).on('change','.costcode_sequence_level',function(event){
  var sequence_level=$(this).val()
  var selected_level= $(this).find('option:selected').attr('level_id');
  var remaining_level_html=''
  for(var i=selected_level;i<=totallevel;i++){
    remaining_level_html +='<div>'
    remaining_level_html +='<h4>Level '+i+'</h4>'

    remaining_level_html +='<input type="text" name="level'+i+'" class="form-control sequence_level_input">'
    remaining_level_html +='</div>'

  }
  $('.remaining_level_inputs').html(remaining_level_html)

})

var costCodeMasterListUrl = $('script[src$="cost_code_list.js"]').data('url');

$(document).on('click', '.empty_list', function () {
  Swal.fire({
    text: 'Cost Code Master is Empty ',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'OK',
  }).then((result) => {
    if (result.isConfirmed) {
      // Redirect to costcodemasterlist using the URL from data-url
      window.location.href = costCodeMasterListUrl;
    }
  });
});

$('.add_sequence_form').submit(function(e) {
  e.preventDefault();
  var isValid = true;
  $('.sequence_level_input').each(function() {
    if ($(this).val() === '') {
      isValid = false;
      $(this).addClass('red_outline');
      return false; 
    }else{
      $(this).removeClass('red_outline');
    }
  })
  if (isValid) {
    this.submit(); 
  }
})


$(document).ready(function() {
  $('.generate').on('click', function(event) {
       event.preventDefault();
       Swal.fire({
          title: '! No Company Logo',
          text: 'Company Image Is Empty .',
          icon: 'success',
          confirmButtonText: 'OK'
      });
  });
});
