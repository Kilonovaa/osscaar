import { writable } from "svelte/store"
import { io } from "socket.io-client"
// export const socketObject = writable(io("localhost:8000"), {transports: ['websocket', 'polling', 'flashsocket']})
export const socketObject = writable(io("wsnasa2023.lazar.lol"), {
  transports: ["websocket", "polling", "flashsocket"],
})
