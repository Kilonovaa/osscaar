import { writable } from "svelte/store"
import { io } from "socket.io-client"
// export const socketObject = writable(io("ws://localhost:8000", {}))
export const socketObject = writable(
  io("wss://wsnasa2023.lazar.lol", {
    path: "/"
    transports: ["websocket", "polling", "flashsocket"],
  })
)
