window.addEventListener('load', function(){


    function ajax_dj(){
        let lastItemId = $('.last_item').attr('data-itemid')

        let data = {
            'lastId': lastItemId
        }
        $('.items').removeClass('last_item')
        $('.items').removeAttr('data-itemid')
        $.ajax({
            method : 'GET',
            dataType : 'json',
            data: data,
            url: 'dj_wait_mod',
            success: function(data){
                let result = data['data']
                if(!result){
                    console.log('новых заказов нет')
                }else{
                    $.each(result, function(key, obj){
                        if(obj['last_item']){
                            $('.mod__list').append(
                                '<li class="mod__item " >'+
                                    '<a href="/dj/' + obj['id'] + '" class="mod__preview items last_item" data-itemid="'+ obj['id'] +'">'+
                                        '<span class="mod__icon">'+ obj['table'] + '</span>'+
                                        '<span class="mod__text">'+ obj['name']+'</span>'+
                                    '</a>'+
                                '</li>'
                            )
                        }else{
                            $('.mod__list').append(
                                '<li class="mod__item">'+
                                    '<a href="/dj/' + obj['id'] + '" class="mod__preview items">'+
                                        '<span class="mod__icon">'+ obj['table'] + '</span>'+
                                        '<span class="mod__text">'+ obj['name']+'</span>'+
                                    '</a>'+
                                '</li>'
                            )
                        }
                    })
                }
            }

        })
    }

    setInterval(ajax_dj, 10000)
})

