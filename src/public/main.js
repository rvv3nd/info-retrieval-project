$(function(){
    socket = io();
    const searchForm = $('#search-form')
    const query = $('#query')

    //eventos

    searchForm.submit(e =>{
        e.preventDefault()
        //console.log("sending query...")
        $('.main_container').hide()
        $('#loading').show()
        socket.emit('send query',query.val())
        query.val('')
    })

    socket.on('getting ranking',function(rank){
        $('#loading').hide()
        for(element of rank){
            $('#response').append('<p>'+element+'</p><br>')
        }
        $('#reload').show()
    })

})