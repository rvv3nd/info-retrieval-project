// const spawn = require('child_process').spawn
const exec =  require('child_process').exec
module.exports = function(io){
    io.on('connection', socket =>{
        console.log("Nuevo usuario conectado")
        socket.on('send query',function(query){
            let query_ = ""
            for( q of query){
                if (q != '(' && q != ')') query_ += q
            }
            let n = String(query_.split(" ").length)
            console.log(n)
            exec('python3 /Users/ruben/Desktop/RI/final/src/public/retrieval.py '+n+' '+query_+'',function(error, stdOut, stdErr){
                console.log(stdOut.toString())
                response = stdOut.toString()
                io.sockets.emit('getting ranking',response); 
                console.log(stdErr.toString())
            })

        })
    })
}