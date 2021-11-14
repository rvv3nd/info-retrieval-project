const PORT = 3000
const http = require('http')
const express = require('express')
const socketio = require('socket.io')
const path = require('path')

const app = express()
const server = http.createServer(app)
const io = socketio(server)

app.set('port', process.env.PORT || PORT)
require('./sockets')(io)
//pasa los archivos estaticos
app.use(express.static(path.join(__dirname,'public')))

//empeiza a escuchar
server.listen(process.env.PORT || PORT,()=>{
    console.log(`server on port ${app.get('port')}`)
});