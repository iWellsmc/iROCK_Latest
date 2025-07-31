$(document).on('click','.role-cls',function(){
         var id=$(this).attr('role_id')
         $('.sub-main-cls').html('')
         $('.projectblock-cls').removeClass("tree_menu active");
         $(this).addClass('tree_menu active')
       // remove active in previous clicked
       $(this).parent().parent().siblings().find('.role-cls').removeClass('hand-icon active')
       $.ajax({
           url: '/invoiceguard/getrolebasedrights/',
           headers: {'X-CSRFToken': csrf_token },
           data: {
               'role_id': id
           },
           type: 'POST',
           success: function(response) {
               var html='';
               if (response.datas.length == 0){
                   html += '---'
               }
               $.each(response.datas,function(key,val){
                   html += '<div class="row"><div class="col-12 colum-line"><p class="tree-content hand-icon projectfield-cls prjt-viewfont">'+val.right_id__right_name+'</p></div></div>'
               })
               $('.role-right-cls-'+id+'').html(html)
           },
           error: function() {
                //   Error message
           }
       });
     })


$(document).ready(function() {
    $(".showtoggle").on('click', function() {
    let nxttr = $(this).closest('tr').next('tr');
    $(this).closest('table tbody').find('.collapse').not(nxttr.find('.collapse')).removeClass('show');
   });
   
   });  