<script>
  import { io } from "socket.io-client"
  import { url } from "../lib/socket"
  import { supabase } from "../lib/supabase"
  import AudioPlayer from "./AudioPlayer.svelte"
  const socket = io(url)
  let videourl = ""
  let soundUrl = ""
  let progress = 0
  let show = 0

  let todo = {
    processFile: 0,
    uploadFIle: 0,
    processSound: 0,
    uploadSound: 0,
  }
  let names = {
    processFile: "Preparing File",
    uploadFIle: "Uploading File",
    processSound: "Generation Sound",
    uploadSound: "Uploading Sound",
  }

  socket.on("upload_response", async (info) => {
    console.log(info)
    progress = info.progress
    todo.uploadFIle = progress
    // if (progress >= 100) {
    //   document.getElementById("file").value = ""
    // }
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
    show = 1
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
        todo.processFile = progress
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
  function frame(event) {
    var vid = document.getElementById("video")
    console.log(event)
    vid.currentTime = event.detail
  }
  function play(event) {
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
      {#if show == true}
        {#each Object.entries(todo) as [key, value]}
          <div class="item">
            <progress {value} max="100" />
            <p>{names[key]}</p>
          </div>
        {/each}
      {:else}
        <h1>Selenotone, listen to the unknown.</h1>
        <p>Use headphones for best experience.</p>
        <label for="file">Upload Video</label>
        <input
          type="file"
          id="file"
          name="file"
          on:input={upload}
          accept=".mp4"
        />
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
          on:paused={play}
          on:change={frame}
        />
      </div>
    {:catch error}
      <p>{error.message}</p>
    {/await}
  {/if}
</section>

<style>
  h1 {
    font-size: clamp(2.5rem, 5vw, 4rem);
    text-align: center;
    margin: 0;
    line-height: 1;
  }
  input {
    display: none;
  }
  label {
    display: inline-block;
    padding: 0.5em 1em;
    text-decoration: none;
    background: var(--accent);
    color: #fff;
    border-radius: 0.5rem;
    width: clamp(2rem, 50%, 10rem);
    text-align: center;
    transition: background-color 250ms ease-out;
  }
  label:hover {
    background: var(--accent-hover);
  }
  section {
    padding-block: 2rem;
    padding-inline: 2rem;
    border-radius: 1rem;
    min-width: fit-content;
    width: clamp(1rem, 80vw, 70rem);
    min-height: 60vh;
    margin: 3rem auto;
    position: relative;
    display: grid;
    place-content: center;
  }
  div {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
    align-items: center;
    gap: 2rem;
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
  .item {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  progress {
    width: 50vw;
    height: 16px;
    border-radius: 16px;
    color: var(--accent);
  }
  progress::-webkit-progress-bar {
    border-radius: 16px;
    background-color: white;
  }
  progress::-webkit-progress-value {
    border-radius: 16px;
    background: var(--accent);
  }
</style>
