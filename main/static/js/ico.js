$(function() {
    var lengthDiv = 4;
    var current = 0;
$('a').bind('click',function(event){
    
    var $anchor = $(this);
    current = $anchor.parent().index();


    $('html, body').stop().animate({
        scrollTop: $($anchor.attr('href')).offset().top
    }, 500);

    event.preventDefault();
});
    $(document).keydown(function(e){if($(':focus').length <= 0)e.preventDefault()})
    $(document).keyup(function(e){
        var key = e.keyCode;
        if(key == 38 && current > 0){
            $('.containe').children('section').eq(current - 1).children('a').trigger('click')
        }else if(key == 40 && current < lengthDiv){
            $('.containe').children('section').eq(current + 1).children('a').trigger('click')
        }
    })
});