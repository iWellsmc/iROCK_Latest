$(document).ready(function(){
  let leftcol = $(".left-pdf-bank-viewer")[0].scrollHeight;
  let rightcol = $(".right-pdf-bank-viewer")[0].scrollHeight;
  var timer = setInterval(checkHeightFunction, 1000);
  function checkHeightFunction(){
    let right_height_manage = $(".right-height-manage")[0].scrollHeight;
    if(right_height_manage > 0) {
      console.log("working");
      clearInterval(timer);
      if(leftcol>rightcol){
        $(".right-pdf-bank-viewer").css("height",leftcol-right_height_manage);
      }else{
        $(".left-pdf-bank-viewer").css("height",rightcol);
      }
      return;
    }
  }

  $('.commonbtn:first').click();
})
$('.view_file').click(function(){
    let val=$(this).attr('data_id')
    // let setfullurl=currentdomain+'/media/'+filename+''
    let setfullurl= val.slice((val.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${val}` : `${currentdomain}/media/${val}`
    console.log('setfullurl',setfullurl)
    $('.doc_pay_ins_cls').attr({'src':setfullurl,height:'590px !important'})    
})

// $('.otherdocuments').click(function(){
 
// })
$('.commonbtn').click(function(){
   
    $('.commonbtn').removeClass('selected_btn')
    $(this).addClass('selected_btn')
    let val=$(this).val()
   
    console.log({'val':val})
    $('.show_file_cls').html('')
    $('.doc_invhidcls').attr('src','')
    $.ajax({
            type:"GET",
            data:{'file_type':val,'invoice_id':invoice_id},
            url:'/invoice/getallfiles',
            success: function(data){
                console.log({'data':data})
                let html='';
               
                if (data.supporting_doc == false){
                    $.each(data.files, function(index, value) {
                    let remove_name=(value.file_name).replace("invoicedocuments/","")
                   
                    html +='<p class="fil-cls file-style" data_id='+value.file_name+'>'+remove_name+'</p>'
                    })
                    $('.show_file_cls').html(html)
                    $('.fil-cls:first').click()
                }else{

                  $.each(data.files, function(index, value) {
                    $.each(value.support_file, function(index, value) {
                      var add_path=`${value.file_name}`
                      html +='<p class="fil-cls file-style" data_id='+add_path+'>'+value.file_name+'</p>'
                    })
                    $('.show_file_cls').html(html)
                    $('.fil-cls:first').click()
                  })

                }
            },})
    })

    $(document).on('click','.fil-cls',function(){
        $('.doc_invhidcls').attr('src','')
        $('.fil-cls').removeClass('selected-cls')
        $(this).addClass('selected-cls')
        let filename=$(this).attr('data_id');
        let setfullurl=currentdomain+'/media/'+filename+''
        $('.doc_invhidcls').attr({'src':setfullurl,height:'590px !important'})  

        
    })

    $(document).on('click','.fil-cls',function(){
        $('.fil-cls').removeClass('sel-file-cls')
        $(this).addClass('sel-file-cls')
        $('.doc_selinvhidcls').attr('src','')
        var file=$(this).text()
        // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
        // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+''
        


        // let setfullurl= file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/invoicedocuments/${file}` : `${currentdomain}/media/invoicedocuments/${file}`

    // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
    
        $('.doc_invhidcls').attr({'src':setfullurl,height:'590px !important'})
    })

     
// Path to the PDF file
const pdfUrl = 'http://127.0.0.1:8000/media/Invoice_PDF_18.pdf';

console.log('pdfUrl',pdfUrl)

// PDF.js viewer options
const viewerOptions = {
  viewerContainer: document.getElementById('pdf-viewer'),
};

// Initialize PDF.js viewer
pdfjsLib.getDocument(pdfUrl).promise.then(function(pdfDoc) {
  // Set the PDF document in the viewer
  viewerOptions.pdfDocument = pdfDoc;

  // Create a PDF.js viewer instance
  const pdfViewerInstance = new pdfjsViewer.PDFViewer(viewerOptions);

  // Set the viewer instance as the active viewer
  pdfViewerInstance.setDocument(pdfDoc);

  // Optional: Enable text search functionality
  pdfViewerInstance.eventBus.on('textlayerrendered', function() {
    const searchInput = document.getElementById('pdf-search');
    searchInput.addEventListener('input', function() {
      pdfViewerInstance.findController.executeCommand('find', {
        query: searchInput.value,
        phraseSearch: true,
      });
    });
  });
});