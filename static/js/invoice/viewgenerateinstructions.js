$(document).ready(function() {
    $('.status_cls').click(function() {
      var allViewIconsClicked = $('.pi_file .fa-eye').length === $('.pi_file .fa-eye.clicked').length;
      if (!allViewIconsClicked) {
        $('.confirm_btn').removeAttr('data-target');
        swal.fire('Please view all pdf');
      } else {
        $('.confirm_btn').attr({'data-target':'#exampleModalCenter'});
      }
    });
  
    $('.pi_file .fa-eye').click(function() {
      $(this).addClass('clicked');
    });
  });