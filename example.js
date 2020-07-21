$(document).ready(function(){
    function is_url(str)
    {
      regexp =  /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;
            if (regexp.test(str))
            {
              return true;
            }
            else
            {
              return false;
            }
    }
    $("#activate").trigger("click");

    $('img').hover(function(){
        $('h2').toggleClass('transform');
    });
    $('.dropdown-toggle').click(function(){
        $('.dropdown-menu').toggle(200);
    });
    $('nav').mouseleave(function(){
       $('.dropdown-menu').hide(200);
    });
    
    function done(){ 
    $("#done").trigger("click");
 }

    $("#agree").on("click",function(){
        setTimeout(done,2000);
    });
    
    $("#reload").click(function(){
        location.reload(true);
    });
   
    
    function matchImgQuery(url){
        return url.includes('images') || url.includes('image') || url.includes('images?') || url.includes('image?');

    }
    

    $("#insert").click(function(){         
        var ht = $("#varval").val();
        if(ht == ""){
            $(".invalid-feedback").css('display','inline');
            $("#varval").addClass('invalid');
        }
        else if((ht != "" && !is_url(ht)) && matchImgQuery(ht)){
            $("#2").css('display','inline');
            $("#varval").addClass('invalid');
        }
        else{
            $(".invalid-feedback").css('display','none');
            $("#varval").addClass('valid')
        $(".img-holder img").attr('src', ht);
        }
    });
    $("#varval").val("")
    setTimeout($("#varval").removeClass('valid'),200);

});