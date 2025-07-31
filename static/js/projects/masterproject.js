$(document).ready(function() {
     
  $(".showtoggle").on('click', function() {
 
    let nxttr = $(this).closest('tr').next('tr');
    console.log(nxttr)
    $(this).closest('table tbody').find('.collapse').not(nxttr.find('.collapse')).removeClass('show');
  });

});
$(document).ready( function () {
  $('.projectmaster_delete').click(function() {
    var get_id=$(this).attr('data-id');
    var project_name=$(this).attr('project-name')
  Swal.fire({
    title: 'Are you sure you want to delete   '+project_name,
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, I Confirm',
    cancelButtonText: 'No',
  }).then((result) => {
    if (result.isConfirmed) {
       $.ajax({
      type: "GET",
      url:'/projects/masterprojectdelete',
      data: {
        "id":get_id,
      },
      cache: false,
      success: function(data)
      {
        setTimeout(function(){  
          location.reload();  
          },1000);
      }
    });
    Swal.fire(project_name,'Deleted Successfully') 
    }
  })
  })
//
  $('#country_id').change(function(){
    var country_id=$(this).val();
    var projects='';
    if (country_id != ' '){
      $.ajax({
        type:"GET",
        url:'/projects/getproject',
        data:{'country_id':country_id},
        success: function(data){
            // console.log(data.data)
            projects += '<option value=" " selected>--Select Project--</option>'
            $.each(data.data,function(key,val){
              projects +='<option value='+val.id+'>'+val.name+'</option>'
            })
            $('#project_id').html(projects);
        }
      })
    }
    else{
      $('#project_id').html('<option value=" " selected>--Select Project--</option>')
      
    }
  })

  $(document).on('change', '#project_id', function() {
    var project_id=$(this).val();
    var block='';
    $.ajax({
      type:"GET",

      url:'/projects/getblocks',
      data:{'project_id':project_id},
      success: function(data){
          console.log(data.data)
          block +='<label for="block">Block Name:</label>'
          block +='<select id="block_id">'
          block += '<option value=" " selected>--Select Block--</option>'
          $.each(data.data,function(key,val){
            block +='<option value='+val.id+'>'+val.block_name+'</option>'
          })
          block +='</select>'
          $('#blocks').html(block);
      }
    })
  })
});

$(document).on('click', '.block-cls', function() {
  var block_id=$(this).attr('data-id');
  currentelement=$(this)
  $('.block-cls').removeClass("tree_menu active");
  var field='';
  $('.field-id').html(' ');
  $('.environment-id').html(' ')
  $('.cluster-id').html(' ');
  $('.wells-id').html(' ');
  $('.wells-sub').html(' ');
  $('.wells_name_cls').html(' ')
  $('.welltype-cls').html(' ')
  $('.wells-cls-'+block_id+'').html(' ')
  $(this).addClass('tree_menu active')
  $.ajax({
    type:"GET",

    url:'/projects/getfield',
    data:{'block_id':block_id},
    success: function(data){
        console.log(data.data)
        $.each(data.data,function(key,val){
          field +='<p class="field-cls prjt-viewfont" data-id='+val.id+' block_id='+block_id+'>'+val.field_name+'</p>'
        })
        $('#field_div'+block_id+'').html(field)

    }
  })

  
})
$(document).on('click', '.field-cls', function() {
  var data_id=$(this).attr('data-id');
  var block_id=$(this).attr('block_id');
  currentelement=$(this)
  $('.field-cls').removeClass("tree_menu active");
  var cluster='';
  $('.cluster-id').html(' ');
  $('.wells-id').html(' ');
  $('.wells-sub').html(' ');
  $('.wells_name_cls').html(' ')
  $('.environment-id').html(' ')
  $('.wells-cls-'+block_id+'').html(' ')
  
  $(this).addClass('tree_menu active')
  $.ajax({
    type:"GET",

    url:'/projects/getcluster',
    data:{'field_id':data_id},
    success: function(data){
        var environmentdata=data.environment
        var html=''
        var value=''
        $.each(environmentdata,function(key,val){
            html +='<div class="environment_cls prjt-viewfont" data-id="'+val.id+'" block_id='+block_id+'>'+val.project_environment+'-'+val.project_environment_subtype+'</div>'
          })
        $('#environment_div'+block_id+'').html(html)
    }
  })
})



$(document).on('click', '.environment_cls', function() {
  var data_id=$(this).attr('data-id');
  var block_id=$(this).attr('block_id');
  $('.environment_cls').removeClass("tree_menu active");
  $('.cluster-id').html(' ');
  $('.wells-id').html(' ');
  $('.wells-sub').html(' ');
  $('.wells_name_cls').html(' ')
  $('.wells-cls-'+block_id+'').html(' ')
  var cluster='';
  $(this).addClass('tree_menu active')
  $.ajax({
    type:"GET",
    url:'/projects/getclusterenvironment',
    data:{'environment_id':data_id},
    success: function(data){
      console.log(data.data);
        var clusterdata=data.data
        $.each(clusterdata,function(key,val){
          $.each(val,function(key1,val1){
            cluster +='<div class="row"><div class="col-5 tree_heading clu-master">'+key1+'</div></div>';
            $.each(val1,function(key2,val2){
              console.log(val2)
              cluster +='<div class="row"><div class="col-5 colum-line"> <div class="tree-content hand-icon cluster_name prjt-viewfont" data-id='+val2.id+' block_id='+block_id+'>'+val2.cluster_subname+'</div></div> <div class="col-7 dev-cls-'+block_id+'" id="develop-'+val2.id+'"></div></div>';
            })
          })
        })
        // $('#cluster-id').html(cluster);/
        $('#cluster_div'+block_id+'').html(cluster);
    
    }
  })

})


$(document).on('click', '.cluster_name', function() {
  var cluster_id=$(this).attr('data-id');
  var block_id=$(this).attr('block_id');
  currentelement=$(this)
  $('.cluster_name').removeClass("tree_menu active");
  $('.wells-id').html(' ');
  $('.wells-sub').html(' ');
  $('.wells_name_cls').html(' ')
  $('.dev-cls-'+block_id+'').html(' ')
  $('.wells-cls-'+block_id+'').html(' ')
  $(this).addClass('tree_menu active')
  var development=''
  $.ajax({
    type:"GET",
    url:'/projects/get_development',
    data:{'clustersub_id':cluster_id},
    success: function(data){
      var dev_data=data.data
      console.log(dev_data)
        $.each(dev_data,function(key,val){
        var get_dev_type=val.development_type
        var dev_type=get_dev_type.replace('_',' ') 
        development +='<div class="row"><div class="tree-content hand-icon dev-type-cls prjt-viewfont" block_id='+block_id+' data-id='+val.id+'>'+dev_type+'</div></div>'
        })
        if (dev_data.length !=0 ){
          $('#develop-'+cluster_id+'').html(development);
        }
       else{
          $('#develop-'+cluster_id+'').html(' ');
       }
      }
  })
  // $.ajax({
  //   type:"GET",

  //   url:'/projects/getwell',
  //   data:{'clustersub_id':cluster_id},
  //   success: function(data){
  //       var welldata=data.data
  //       $.each(welldata,function(key,val){
  //         well +='<div class="tree-content hand-icon wells-type" block_id='+block_id+' data-id='+val.id+'>'+val.well_name+'</div>';
  //       })
  //       if (welldata.length !=0 ){
  //         $('#well_div'+block_id+'').html(well);
  //       }
  //       else{
  //         $('#well_div'+block_id+'').html(' ');
  //       }
  //   }
  // })
})

$(document).on('click','.dev-type-cls',function(){
  var development_id=$(this).attr('data-id')
  var block_id=$(this).attr('block_id');
  currentelement=$(this)
  $('.wells-cls-'+block_id+'').html(' ')
  $('.dev-type-cls').removeClass("tree_menu active");
  $(this).addClass('tree_menu active')
  $.ajax({
  type:"GET",

  url:'/projects/getmasterwell',
  data:{'development_id':development_id},
  success: function(data){
      var welldata=data.data
      var well ='<div class="row wells-cls-'+block_id+'"><div class="col-5"><h5 class="list-txt">Well Type</h5></div><div class="col-6"><h5 class="list-txt">Well Name</h5></div></div>'
      $.each(welldata,function(key,val){
        well +='<div class="row wells-cls-'+block_id+'"><div class="col-5 colum-line"><div class="tree-content hand-icon wells-type prjt-viewfont" data-id='+val.id+'>'+val.well_name+'</div></div><div class="col-7 colum-line well-name-cls" id="wellname'+val.id+'"></div></div>';
      })
      $('#welltype'+block_id+'').html(well);
  }
  })
})


$(document).on('click', '.wells-type', function() {
  var well_id=$(this).attr('data-id');
  var block_id=$(this).attr('block_id');
  currentelement=$(this)
  $('.well-name-cls').html(' ')
  $('.wells-type').removeClass("tree_menu active");
  $(this).addClass('tree_menu active')
  var well_type=$(this).text()

  var wellsub=''
  $.ajax({
    type:"GET",

    url:'/projects/getwellsub',
    data:{'well_id':well_id},
    success: function(data){
        var wellsubdata=data.data
        console.log(wellsubdata)

      var si=1
        $.each(wellsubdata,function(key,val){
          wellsub +='<div class="tree-content hand-icon wells-name well-tick prjt-viewfont" data-id='+val.id+'>'+val.well_subname+'</div>';
          si+=1
        })
        if (wellsubdata.length !=0 ){
          $('#wellname'+well_id+'').html(wellsub);
          // $('.wells_name_cls').html('<label>'+well_type+'</label>')
        }
        else{
          $('#wellname'+well_id+'').html(' ');
          // $('.wells_name_cls').html(' ')
        }
    }
  })
}) 