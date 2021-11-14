module.exports = function(io){
    io.on('connection', socket =>{
        console.log("Nuevo usuario conectado")

        socket.on('send query',function(query){
            console.log(query)
            //aqui se llamara a hacer el ranking con pythoon i think
            let response = ["doc1","doc2","doc3"]
            setTimeout(function(){ 
                io.sockets.emit('getting ranking',response); 
            }, 3000);
            
        })


    })
}