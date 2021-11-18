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
        console.log(typeof(rank))
        rank_ = clean(rank)
        for(let i=0;i<rank_.length;i+=2){
            $('#response').append('<p>Documento:'+rank_[i]+' Peso:'+rank_[i+1]+'</p><br>')
        }
        $('#reload').show()
    })

})

function clean(string){
    to_delete = ['(',')','[',']']
    let cleanS = ""
    for(c of string){
        if(to_delete.includes(c) == false){
            cleanS += c
        }
    }
    return cleanS.split(",")
}