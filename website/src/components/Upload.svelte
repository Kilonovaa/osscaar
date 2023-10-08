<script>
  import { io } from "socket.io-client"
  import { url } from "../lib/socket"
  import { supabase } from "../lib/supabase"
  import AudioPlayer from "./AudioPlayer.svelte"
  const socket = io(url)
  let videourl = ""
  let soundUrl = ""
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
  socket.on("sound", async (info) => {
    console.log(info)
    if (info.hasOwnProperty("url")) {
      soundUrl = info.url
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
  function unmute(event) {
    var vid = document.getElementById("video")
    console.log(event)
    vid.currentTime = event.detail
  }
  function mute(event) {
    var vid = document.getElementById("video")
    console.log(event)
    if (event.detail == false) {
      vid.play()
    } else {
      vid.pause()
    }
  }
</script>

<section>
  {#if videourl == ""}
    <div>
      <input
        type="file"
        id="file"
        name="file"
        on:input={upload}
        accept=".mp4"
      />
      {#if progress > 0 && progress < 100}
        <progress value={progress} max="100" />
      {/if}
    </div>
  {/if}
  {#if videourl != ""}
    {#await fetchVideo(videourl)}
      <p>loading...</p>
    {:then video}
      <div class="media">
        <video preload="auto" controls="" id="video" muted>
          <source src={video} type="video/mp4" />
        </video>
        <AudioPlayer
          src={soundUrl}
          title="Lazar"
          artist="Moska"
          on:paused={mute}
          on:change={unmute}
        />
      </div>
    {:catch error}
      <p>{error.message}</p>
    {/await}
  {/if}
</section>

<style>
  section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-block: 2rem;
    padding-inline: 2rem;
    border-radius: 1rem;
    min-width: fit-content;
    background-color: #40404b;
    width: clamp(1rem, 80vw, 70rem);
    min-height: 60vh;
    margin: 3rem auto;
    position: relative;
  }
  div {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
  }
  .media {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  video {
    height: 100%;
    max-height: 50vh;
    max-width: 80vw;
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
