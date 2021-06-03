window.addEventListener('load', function(){

    var activeTable = 0
    $('.burger__btn').on('click', function(e){
        e.preventDefault();
        $(this).toggleClass('_active');
        $('.mobile__menu').toggleClass('_active');
    })

    $('._js-wait-pay').on('click', function(e){
        e.preventDefault()
        var numberTable = $(this).text()
        var soundId = $(this).next().text()
        $('.popup__title span').text(numberTable)
        $('.cashier__inner').css('filter', 'blur(5px)')
        $('.active-table__popup').fadeIn();
        $('.popup__input').val(soundId)


    })

    $('.popup__close').on('click', function(){
        $('.cashier__inner').css('filter', 'none')
        $('.active-table__popup').fadeOut();
        
    })
    $('.popup__btn').on('click', function(){

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
 
    
    $('._js-mod').on('click', function(e){
        e.preventDefault()
        $(this).next().toggleClass('_active')
    })

    $('._js-no').on('click', function(e){
        e.preventDefault()
        $('.mod__popup').removeClass('_active')
    })

    $('.login__link').on('click', function(e){
        e.preventDefault()
        $('.popup_logIn').fadeIn();
    })

    $('.popup__close').on('click', function(e){
        e.preventDefault()
        $('.popup_logIn').fadeOut()
    })
    $('.cashier__shift').on('click',function(){
        $('.shift__popap').toggleClass('is_active')
    })
})