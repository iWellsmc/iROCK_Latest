$(document).on('click','.inv_file',function(){

    $('.inv_file').removeClass('inv-high-cls')
    var inv_name=$(this).closest('tr').find('.inv_name').text()
    $('.hd-inv').text(inv_name)
    var url=$(this).attr('value')
    $(this).addClass('inv-high-cls')
    // $('#navbar').show();
    // var setfullurl=currentdomain+'/media/invoicedocuments/'+url+'#toolbar=0'
    //var setfullurl=currentdomain+'/media/invoicedocuments/'+url+''
    var setfullurl = url.slice((url.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/invoicedocuments/${url}` : `${currentdomain}/media/invoicedocuments/${url}`;
    setfullurl = setfullurl.replace(/ /g, "_");
    $('.doc_invhidcls').attr({'src':setfullurl,height:'590px !important'})
})

/* pdf js
//     var _PDF_DOC,
//     _CURRENT_PAGE,
//     _TOTAL_PAGES,
//     _PAGE_RENDERING_IN_PROGRESS = 0,
//     _CANVAS = document.querySelector('#pdf-canvas');

// // initialize and load the PDF
// async function showPDF(pdf_url) {
//     document.querySelector("#pdf-loader").style.display = 'block';

//     // get handle of pdf document
//     try {
//         _PDF_DOC = await pdfjsLib.getDocument({ url: pdf_url });
//     }
//     catch(error) {
//         alert(error.message);
//     }

//     // total pages in pdf
//     _TOTAL_PAGES = _PDF_DOC.numPages;
    
//     // Hide the pdf loader and show pdf container
//     document.querySelector("#pdf-loader").style.display = 'none';
//     document.querySelector("#pdf-contents").style.display = 'block';
//     document.querySelector("#pdf-total-pages").innerHTML = _TOTAL_PAGES;
    
//     // show the first page
//     showPage(1);
// }

// // load and render specific page of the PDF
// async function showPage(page_no) {
//     _PAGE_RENDERING_IN_PROGRESS = 1;
//     _CURRENT_PAGE = page_no;

//     // disable Previous & Next buttons while page is being loaded
//     document.querySelector("#pdf-next").disabled = true;
//     document.querySelector("#pdf-prev").disabled = true;

//     // while page is being rendered hide the canvas and show a loading message
//     document.querySelector("#pdf-canvas").style.display = 'none';
//     document.querySelector("#page-loader").style.display = 'block';

//     // update current page
//     document.querySelector("#pdf-current-page").innerHTML = page_no;
    
//     // get handle of page
//     try {
//         var page = await _PDF_DOC.getPage(page_no);
//     }
//     catch(error) {
//         alert(error.message);
//     }

//     // original width of the pdf page at scale 1
//     var pdf_original_width = page.getViewport(1).width;
    
//     // as the canvas is of a fixed width we need to adjust the scale of the viewport where page is rendered
//     var scale_required = _CANVAS.width / pdf_original_width;

//     // get viewport to render the page at required scale
//     var viewport = page.getViewport(scale_required);

//     // set canvas height same as viewport height
//     _CANVAS.height = viewport.height;

//     // setting page loader height for smooth experience
//     document.querySelector("#page-loader").style.height =  _CANVAS.height + 'px';
//     document.querySelector("#page-loader").style.lineHeight = _CANVAS.height + 'px';

//     // page is rendered on <canvas> element
//     var render_context = {
//         canvasContext: _CANVAS.getContext('2d'),
//         viewport: viewport
//     };
        
//     // render the page contents in the canvas
//     try {
//         await page.render(render_context);
//     }
//     catch(error) {
//         alert(error.message);
//     }

//     _PAGE_RENDERING_IN_PROGRESS = 0;

//     // re-enable Previous & Next buttons
//     document.querySelector("#pdf-next").disabled = false;
//     document.querySelector("#pdf-prev").disabled = false;

//     // show the canvas and hide the page loader
//     document.querySelector("#pdf-canvas").style.display = 'block';
//     document.querySelector("#page-loader").style.display = 'none';
// }

// // click on "Show PDF" buuton
// // document.querySelector(".show-pdf-button").addEventListener('click', function() {
// var scheme="{{request.scheme}}"
// var gethost="{{request.get_host}}"
// var currentdomain=scheme+'://'+gethost
// $(document).on('click','.show-pdf-button',function(){
//     let url=this.getAttribute('value')
//     console.log(url)
//     extension = url.split('.').pop();
//     console.log(extension)
//     if (extension == "jpeg"){
//         var ctx = $("canvas")[0].getContext("2d"),
//         img = new Image();
//         ctx.canvas.width = 600; ctx.canvas.height = 849; 
//         img.onload = function() { 
//             ctx.drawImage(img, 0, 0,600,849); 
//         }; 
//         img.src = currentdomain+url;
//         // img.onload = function(){
//         //     ctx.drawImage(img, 0, 0, 1000, 1000);
//         // };
//         // img.src = "http://localhost:8000"+url;
//         }
//         else{
//             showPDF(currentdomain+url);
//         }
//     // this.style.display = 'none';
//     // showPDF('http://localhost:8000/'+url)

// });

// // click on the "Previous" page button
// document.querySelector("#pdf-prev").addEventListener('click', function() {
//     if(_CURRENT_PAGE != 1)
//         showPage(--_CURRENT_PAGE);
// });

// // click on the "Next" page button
// document.querySelector("#pdf-next").addEventListener('click', function() {
//     if(_CURRENT_PAGE != _TOTAL_PAGES)
//         showPage(++_CURRENT_PAGE);
// });

*/
$(document).on('click','.commonbtn',function(){
    $('.commonbtn').removeClass('support_high-cls')
    $('.doc_selinvhidcls').attr('src','')
    var val=$(this).attr('dataid')
    $(this).addClass('support_high-cls')
    var gettext=$(this).text()
    let wcc_id=$(this).attr('wcc_id') || ''

    $.ajax({
            type:"GET",
            data:{'supportid':val,'invoiceid':invoiceid,'wcc_id':wcc_id},
            url:'/invoice/getsupportfiles',
            success: function(data){
                var html="" 
                if (val == "9"){
                    if(data.contracttype != 'original'){
                        if (data.con_file.length > 1){
                            console.log('length > 1')
                            $(data.con_file).each(function(index,value){
                                // if (value.amendment_addendum_id != null){
                                //     html +='<div><span>Amendment/Addendum : </span><span class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</span></div>'
                                // }
                                // else{
                                // html +='<div><span>Original Contract : </span><span class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</span></div>'
                                // }
                                if (value.amendment_addendum_id != null){
                                    html +='<div class="confile-cls file-style" type='+1+'>Amendment/Addendum : '+value.original_file_name+'</div>'
                                    }
                                    else{
                                    html +='<div class="confile-cls file-style" type='+2+'>Original Contract : '+value.original_file_name+'</div>'
                                    }
                            })
                        }                    
                    }
                    else{

                    // $('.doc_selinvhidcls').attr('src','')
                    // // var setfullurl=currentdomain+'/media/'+data.con_file+'#toolbar=0'
                    // var setfullurl= data.con_file.slice((data.con_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.con_file}` : `${currentdomain}/media/${data.con_file}`
                    // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        $(data.con_file).each(function(index,value){
                            html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'    
                        })
                    }
                }
                else if(val == "10"){
                    if(data.contracttype != 'original'){
                        if (data.price_file.length > 1){
                            $(data.price_file).each(function(index,value){
                                // if (value.amendment_addendum_id != null){
                                //     html +='<div><span>Amendment/Addendum : </span><span class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</span></div>'
                                // }
                                // else{
                                // html +='<div><span>Original Price Table : </span><span class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</span></div>'
                                // }
                                if (value.amendment_addendum_id != null){
                                    html +='<div class="confile-cls file-style" type='+1+'>Amendment/Addendum : '+value.original_file_name+'</div>'
                                }
                                else{
                                    html +='<div class="confile-cls file-style" type='+2+'>Original Price Table: '+value.original_file_name+'</div>'
                                }
                            })
                        }
                    }
                    else{
                        // $('.doc_selinvhidcls').attr('src','')
                        // // var setfullurl=currentdomain+'/media/'+data.price_file+'#toolbar=0'
                        // var setfullurl= data.price_file.slice((data.price_file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${data.price_file}` : `${currentdomain}/media/${data.price_file}`

                        // $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'}) 
                        $(data.price_file).each(function(index,value){
                            html +='<div class="confile-cls file-style" type='+index+'>'+value.original_file_name+'</div>'    
                        })
                    }
                }
               

                else{
                    if (data.filecount > 1){

                        if (val == "2"){
                            $(data.files).each(function(index,value){
                                if (value.wcc_file_name){
                                    let remove_name="";
                                    get_name=(value.wcc_file_name).replace("invoicedocuments/","")
                                    
                                    get_name1=(value.wcc_file).replace("invoicedocuments/","")//newly1 added
                                    remove_name=(get_name).replace("wccfile/","")
                                    remove_name1=(get_name1).replace("wccfile/","")//newly1 added
                                    html += '<div class="fil-cls-wcc file-style" data-support-file="' + remove_name1 + '">' + remove_name + '</div>';
                                }else{
                                    let remove_name="";
                                    get_name=(value.file_name).replace("invoicedocuments/","")
                                  
                                    get_name1=(value.support_file).replace("invoicedocuments/","")//newly1 added
                                    remove_name=(get_name).replace("wccfile/","")
                                    remove_name1=(get_name1).replace("wccfile/","")//newly1 added
                                    html += '<div class="fil-cls file-style" data-support-file="' + remove_name1 + '">' + remove_name + '</div>';
                                }
                                            
                                             
                                            
                          })
                        }
                        else{
                            $(data.files).each(function(index,value){
                                if (value.wcc_support_file_name){
                                    let remove_name="";
                                    get_name=(value.wcc_support_file_name).replace("invoicedocuments/","")
                                    
                                    get_name1=(value.support_file).replace("invoicedocuments/","")//newly1 added
                                    remove_name=(get_name).replace("wccfile/","")
                                    remove_name1=(get_name1).replace("wccfile/","")//newly1 added
                                    html += '<div class="fil-cls-wcc file-style" data-support-file="' + remove_name1 + '">' + remove_name + '</div>';
                                }else{
                                    let remove_name="";
                                    get_name=(value.file_name).replace("invoicedocuments/","")
                                  
                                    get_name1=(value.support_file).replace("invoicedocuments/","")//newly1 added
                                    remove_name=(get_name).replace("wccfile/","")
                                    remove_name1=(get_name1).replace("wccfile/","")//newly1 added
                                    html += '<div class="fil-cls file-style" data-support-file="' + remove_name1 + '">' + remove_name + '</div>';
                                }
                                            
                                             
                                            
                          })
                        }
                       
                    }
                    else if (data.filecount == 1){ 
                        $('.doc_selinvhidcls').attr('src','')
                        var setfullurl=""
                        $(data.files).each(function(index,value){
                            // setfullurl=currentdomain+'/media/'+value.support_file+'#toolbar=0'
                            //setfullurl=currentdomain+'/media/'+value.support_file+''
                            // alert(value.support_file)
                            let file_path="";
                            if (wcc_id & val == "2"){
                                file_path=value.wcc_file
                            }
                            else if(val=="2"){
                                file_path=value.support_file
                            }
                            else{
                                file_path=value.support_file
                            }
                            
                            setfullurl= file_path.slice((file_path.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${file_path}` : `${currentdomain}/media/${file_path}`


                        })
                        $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})  
                    }
                    else{
                        html +='<div class="file-style">No Files in '+gettext+'</div>'
                    }
                }
                $('.show_file_cls').html(html)
            }
            })
})
function cleanFileName(fileName) {
    return fileName.replace(/[^.-\w\s]/gi, '').replace(/\s+/g, '_');
}
$(document).on('click','.fil-cls',function(){
    $('.fil-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    // var file=$(this).text()
    var supportFile = $(this).data('support-file');

    // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    //var setfullurl=currentdomain+'/media/invoicedocuments/'+file+''
    var setfullurl= supportFile.slice((supportFile.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/invoicedocuments/${supportFile}` : `${currentdomain}/media/invoicedocuments/${supportFile}`
    setfullurl = setfullurl.replace(/ /g, "_");

    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})

$(document).on('click','.fil-cls-wcc',function(){
    $('.fil-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    // var file=$(this).text()
    var supportFile = $(this).data('support-file');

    // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    //var setfullurl=currentdomain+'/media/invoicedocuments/'+file+''
    var setfullurl= supportFile.slice((supportFile.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/wccfile/${supportFile}` : `${currentdomain}/media/wccfile/${supportFile}`
    setfullurl = setfullurl.replace(/ /g, "_");

    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})
$(document).on('click','.confile-cls',function(){
    $('.confile-cls').removeClass('sel-file-cls')
    $(this).addClass('sel-file-cls')
    $('.doc_selinvhidcls').attr('src','')
    var file=$(this).text()
    let type=$(this).attr('type')
    if (type == 1){
        file=file.replace("Amendment/Addendum : ","")
    }
    else{
        file=file.replace("Original Contract : ","")
        file=file.replace("Original Price Table: ","")
    }
    // var setfullurl=currentdomain+'/media/invoicedocuments/'+file+'#toolbar=0'
    file = file.replace(/[()]/g, '');
    var setfullurl= file.slice((file.lastIndexOf(".") - 1 >>> 0) + 2) == 'pdf' ? `${package_src}?file=${currentdomain}/media/${file}` : `${currentdomain}/media/${file}`
    setfullurl = setfullurl.replace(/ /g, "_");
    $('.doc_selinvhidcls').attr({'src':setfullurl,height:'590px !important'})
})
// $(document).on('click','#submit',function(){
//     $.ajax({
//             type: "GET",
//             url:"/invoice/invoicecompleted",
//             data: {
//                 'invoiceid':invoiceid,'vendor_id':vendor_id,'contract_id':contract_id,'contract_type':contract_type,
//             },
//             // cache: false,
//             success: function(data)
//             { 
//                 console.log(data)
//                 window.location.href = '../invoicelist';
//             }
//     })
// })

//selectedfilecls

// function zoomin(){
//         var myImg = document.getElementById("file_zoom");
//         var currWidth = myImg.clientWidth;
//         if(currWidth == 2500) return false;
//          else{
//             myImg.style.width = (currWidth + 100) + "px";
//         } 
//     }
//     function zoomout(){
//         var myImg = document.getElementById("file_zoom");
//         var currWidth = myImg.clientWidth;
//         if(currWidth == 100) return false;
// 		 else{
//             myImg.style.width = (currWidth - 100) + "px";
//         }
//     }
$(document).ready(function(){
     $('.inv_file').each(function(){
        $(this).addClass('inv_file');
    });

     $('.inv_file:first').click();

     $('.inv_file').click(function(){
     });
});
