$(function(){
    $('#search').keyup(function(){
        $.ajax('/searchingUser/',{
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'text': $('#search').val()
            },
            'success': function(data){
                document.getElementById('result').innerHTML = data;

            }
        })
    })
})



