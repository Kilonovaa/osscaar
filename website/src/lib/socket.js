import { writable } from "svelte/store"
import { io } from "socket.io-client"
export const socketObject = writable(io("ws://localhost:8000", {}))