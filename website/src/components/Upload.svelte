<script>
  import { io } from "socket.io-client"
  import { url } from "../lib/socket"
  import { supabase } from "../lib/supabase"
  import AudioPlayer from "./AudioPlayer.svelte"
  import { onMount } from "svelte"
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
    if (info.hasOwnProperty("error")) {
      alert(JSON.parse(info.error).message)
    }
    if (info.hasOwnProperty("url")) {
      videourl = info.url
    }
  })
  socket.on("sound_progress", async (info) => {
    console.log(info)
    todo.processSound = info.progress
    if (info.hasOwnProperty("error")) {
      alert(JSON.parse(info.error).message)
    }
    // if (info.hasOwnProperty("url")) {
    //   videourl = info.url
    // }
  })
  socket.on("send_response", async (info) => {
    console.log(info)
    todo.uploadSound = info.progress
    if (info.hasOwnProperty("error")) {
      alert(JSON.parse(info.error).message)
    }
    // if (info.hasOwnProperty("url")) {
    //   videourl = info.url
    // }
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
  let rotation = 0
  let offset = 0
  onMount(() => {
    setInterval(() => {
      rotation = Math.sin(offset) * 10
      offset += 0.01
    }, 10)
  })
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
        <p>Use headphones for the best experience.</p>
        <label for="file">Upload Video</label>
        <input
          type="file"
          id="file"
          name="file"
          on:input={upload}
          accept=".mp4"
        />

        <svg
          id="Layer_2"
          data-name="Layer 2"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="0 0 385.18 328.32"
          style="transform: rotate({rotation}deg);"
        >
          <defs>
            <style>
              .cls-1 {
                fill: #9451a0;
              }

              .cls-1,
              .cls-2,
              .cls-3,
              .cls-4 {
                stroke-width: 0px;
              }

              .cls-2 {
                fill: #7d4287;
              }

              .cls-5 {
                fill: #fff;
              }

              .cls-5,
              .cls-6,
              .cls-7 {
                stroke: #231f20;
                stroke-linecap: round;
                stroke-miterlimit: 10;
                stroke-width: 9px;
              }

              .cls-6 {
                fill: #231f20;
              }

              .cls-7,
              .cls-3 {
                fill: none;
              }

              .cls-8 {
                clip-path: url(#clippath-1);
              }

              .cls-9 {
                opacity: 0.15;
              }

              .cls-4 {
                fill: #9c86a0;
              }

              .cls-10 {
                clip-path: url(#clippath);
              }
            </style>
            <clipPath id="clippath">
              <rect class="cls-3" width="192.59" height="273.86" />
            </clipPath>
            <clipPath id="clippath-1">
              <rect
                class="cls-3"
                x="192.59"
                y="0"
                width="192.59"
                height="273.86"
              />
            </clipPath>
          </defs>
          <g id="Layer_1-2" data-name="Layer 1">
            <g>
              <circle class="cls-1" cx="194.17" cy="187.59" r="140.73" />
              <circle class="cls-2" cx="161.7" cy="104.1" r="37.79" />
              <circle class="cls-2" cx="249.78" cy="135.99" r="23.97" />
              <circle class="cls-2" cx="99.94" cy="187.59" r="23.97" />
              <circle class="cls-2" cx="279.65" cy="231.19" r="29.87" />
              <circle class="cls-2" cx="196.66" cy="201.67" r="19.15" />
              <circle class="cls-2" cx="133.58" cy="253.79" r="13.4" />
              <circle class="cls-2" cx="205.96" cy="284.81" r="13.4" />
              <g class="cls-9">
                <path
                  class="cls-4"
                  d="m296.25,90.74c-22.93-16.21-50.93-25.74-81.15-25.74-77.72,0-140.73,63.01-140.73,140.73,0,37.51,14.68,71.6,38.62,96.83-36.03-25.48-59.55-67.47-59.55-114.96,0-77.72,63-140.73,140.72-140.73,40.19,0,76.45,16.85,102.09,43.87Z"
                />
              </g>
              <g>
                <g
                  id="_Mirror_Repeat_"
                  data-name="&amp;lt;Mirror Repeat&amp;gt;"
                >
                  <g class="cls-10">
                    <path
                      class="cls-4"
                      d="m46.38,159.96h-24.35c.43-13.54,3.67-65.15,44.47-108.46C118.02-3.19,187.71-.37,197.78.21l-1.7,27.91c-9.62-.64-58.67-2.92-101.19,33.73-43.98,37.91-47.96,89-48.5,98.1Z"
                    />
                    <rect
                      class="cls-2"
                      y="129.48"
                      width="59.74"
                      height="144.38"
                      rx="9.16"
                      ry="9.16"
                    />
                  </g>
                </g>
                <g
                  id="_Mirror_Repeat_-2"
                  data-name="&amp;lt;Mirror Repeat&amp;gt;"
                >
                  <g class="cls-8">
                    <path
                      class="cls-4"
                      d="m338.8,159.96h24.35c-.43-13.54-3.67-65.15-44.47-108.46C267.16-3.19,197.47-.37,187.4.21l1.7,27.91c9.62-.64,58.67-2.92,101.19,33.73,43.98,37.91,47.96,89,48.5,98.1Z"
                    />
                    <rect
                      class="cls-2"
                      x="325.43"
                      y="129.48"
                      width="59.74"
                      height="144.38"
                      rx="9.16"
                      ry="9.16"
                      transform="translate(710.61 403.34) rotate(180)"
                    />
                  </g>
                </g>
              </g>
              <path
                class="cls-7"
                d="m209.36,284.13c5.5.7,23.61,2.3,41.87-8.85,21.77-13.29,27.78-34.95,28.94-39.49"
              />
              <circle class="cls-6" cx="128.85" cy="184.55" r="30.81" />
              <circle class="cls-6" cx="236.77" cy="156.78" r="30.81" />
              <circle class="cls-5" cx="138.07" cy="189.28" r="17.89" />
              <circle class="cls-5" cx="244.76" cy="164.63" r="17.89" />
              <circle class="cls-5" cx="114.96" cy="171.39" r="8.94" />
              <circle class="cls-5" cx="222.46" cy="146.74" r="8.94" />
            </g>
          </g>
        </svg>
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
  svg {
    height: 40vh;
    position: absolute;
    right: 3rem;
    bottom: -6rem;
    transform: rotate(10deg);
    opacity: 0.6;
    z-index: -1;
  }
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
    svg {
      height: 30vh;
      opacity: 0.3;
      right: auto;
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
