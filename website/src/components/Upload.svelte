<script>
  import { io } from "socket.io-client"
  import { url } from "../lib/socket"
  import { supabase } from "../lib/supabase"
  const socket = io(url)
  let videourl = ""
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
    if (info.hasOwnProperty("url")) {
      videourl = info.url
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
{#if videourl != ""}
  <video src={videourl} controls autoplay muted />
{/if}

<style>
  section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-block: 2rem;
    border-radius: 1rem;
    min-width: fit-content;
    background-color: white;
    color: black;
    width: clamp(1rem, 80vw, 70rem);
    height: 60vh;
    margin: 3rem auto;
  }
  @media only screen and (max-width: 600px) {
    section {
      width: clamp(1rem, 95vw, 70rem);
    }
  }
</style>
