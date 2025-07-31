
$(document).on('click', '.role-cls', function() {
    var id = $(this).attr('role_id');
    $('.sub-main-cls').html('');
    $('.projectblock-cls').removeClass('tree_menu active');
    $(this).addClass('tree_menu active');
    $(this).parent().parent().siblings().find('.role-cls').removeClass('hand-icon active')
    console.log('id',id)
    $.ajax({
    url: '/projects/getRights/',
    headers: {'X-CSRFToken': csrf_token },
    data: {
      'role_id': id
    },
    type: 'POST',
    success: function(response) {
     
      var html = '';
      var data = JSON.parse(response.datas);
var html = '';

$.each(data, function(key, val) {
  console.log('key',key);
  console.log('val',val);
  var rightName = val['fields']['right_name'];
  console.log('rightName',rightName);
  html += '<div class="row"><div class="col-12 colum-line"><p class="tree-content hand-icon projectfield-cls prjt-viewfont">' + rightName + '</p></div></div>';
});

console.log('html', html);
$('.role-right-cls-' + id).html(html);
    },
    error: function() {
    
    }
    });
    });
    