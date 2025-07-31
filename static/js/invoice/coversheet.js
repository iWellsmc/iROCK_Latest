$(document).ready(function(){
    let  companyaddress = $('.companyaddress').attr('data')
    var address = companyaddress.split('</p>').join('&nbsp')
    $('.companyaddress').html(address)
  })
