$( document ).ready(function() {
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
})