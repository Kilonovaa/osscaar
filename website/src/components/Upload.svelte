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
  async function fetchVideo(url) {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    } else {
      const videoData = await response.blob()
      const video = URL.createObjectURL(videoData)
      return video
    }
  }
</script>

<section>
  <div>
    <input type="file" id="file" name="file" on:input={upload} accept=".mp4" />
    {#if progress > 0 && progress < 100}
      <progress value={progress} max="100" />
    {/if}
  </div>
  {#if videourl != ""}
    {#await fetchVideo(videourl)}
      <p>loading...</p>
    {:then video}
      <video controls>
        <source src={video} type="video/mp4" />
      </video>
    {:catch error}
      <p>{error.message}</p>
    {/await}
  {/if}
</section>

<style>
  section {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding-block: 2rem;
    padding-inline: 2rem;
    border-radius: 1rem;
    min-width: fit-content;
    background-color: #40404b;
    width: clamp(1rem, 80vw, 70rem);
    height: 60vh;
    margin: 3rem auto;
  }
  div {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
  }
  video {
    height: 100%;
    max-height: 50vh;
    object-fit: cover;
    border-radius: 1.5rem;
  }
  @media only screen and (max-width: 600px) {
    section {
      width: clamp(1rem, 95vw, 70rem);
      flex-direction: column;
      height: fit-content;
    }
  }
</style>
