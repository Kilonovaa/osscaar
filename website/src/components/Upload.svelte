<script>
  import { io } from "socket.io-client"
  import { url } from "../lib/socket"
  import { supabase } from "../lib/supabase"
  const socket = io(url)
  let progress = 0

  socket.on("upload_response", async (info) => {
    console.log(info)
    progress = info.progress
    if (progress >= 100) {
      document.getElementById("file").value = ""
    }
    if (info.hasOwnProperty("error")) {
      alert(JSON.parse(info.error).message)
    }
  })

  function upload() {
    progress = 0
    const file = document.getElementById("file").files[0]
    console.log(file)
    const reader = new FileReader()
    reader.readAsArrayBuffer(file)

    reader.onload = (fileEvent) => {
      const arrayBuffer = fileEvent.target.result
      const uint8Array = new Uint8Array(arrayBuffer)
      socket.emit("upload", uint8Array, (response) => {})
    }

    reader.onprogress = (event) => {
      if (event.lengthComputable) {
        progress = Math.round((event.loaded / event.total) * 100)
      }
    }
  }
</script>

<section>
  <input type="file" id="file" name="file" on:input={upload} accept=".mp4" />
  {#if progress > 0 && progress < 100}
    <progress value={progress} max="100" />
  {/if}
</section>

<style>
  section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 4rem;
    border-radius: 1rem;
    min-width: fit-content;
    background-color: white;
    color: black;
    width: clamp(20rem, 50vw, 50rem);
    margin: 3rem auto;
  }
</style>
