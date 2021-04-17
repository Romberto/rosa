window.addEventListener('load', function(){

    var activeTable = 0
    $('.burger__btn').on('click', function(e){
        e.preventDefault();
        $(this).toggleClass('_active');
        $('.mobile__menu').toggleClass('_active');
    })

    $('.active-table__item').on('click', function(e){
        e.preventDefault()
        activeTable = $(this)
        $('.cashier__inner').css('filter', 'blur(5px)')
        $('.active-table__popup').fadeIn();
    })

    $('.popup__close').on('click', function(){
        $('.cashier__inner').css('filter', 'none')
        $('.active-table__popup').fadeOut();
        
    })
    $('.popup__btn').on('click', function(){
        activeTable.remove()
        $('.cashier__inner').css('filter', 'none')
        $('.active-table__popup').fadeOut();
    })

    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;
    
        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] === sParam) {
                param = typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1])
                $('.product__id').text(param)
                return param;
            }
        }
        return false;
    };

    var id = getUrlParameter('id')
 
    

 


    
})