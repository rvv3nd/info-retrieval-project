// const spawn = require('child_process').spawn
const exec =  require('child_process').exec
module.exports = function(io){
    io.on('connection', socket =>{
        console.log("Nuevo usuario conectado")
        socket.on('send query',function(query){
            // console.log('query recived: '+query)
            // const py_process = spawn('py',['retrieval.py'])
            // console.log("got spawn")
            // // console.log(query)
            // //aqui se llamara a hacer el ranking con python i think
            // var response
            // py_process.stdout.on("data",function(data){
            //     console.log('got response')
            //     response = data.toString()
            // })
            // py_process.stdout.on("end",function(){
            //     console.log(response)
            //     io.sockets.emit('getting ranking',response); 
            // })
            // py_process.on('close',(code,signal)=>{
            //     console.log(`child_process: ${code} ${signal}`)
            // })
            let n = String(query.split(" ").length)
            console.log(n)
            exec('python3 /Users/ruben/Desktop/RI/final/src/public/retrieval.py '+n+' '+query+'',function(error, stdOut, stdErr){
                console.log(stdOut.toString())
                response = stdOut.toString()
                io.sockets.emit('getting ranking',response); 
                console.log(stdErr.toString())
            })

        })
    })
}