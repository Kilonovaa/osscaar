<script>
  import { get } from "svelte/store"
  import { socketObject } from "../lib/socket"
  const socket = get(socketObject)
  let progress = 0

  socket.on("upload_response", (data) => {
    console.log(data)
    progress = 0 // reset progress after upload
    //clear file form form
    document.getElementById("file").value = ""
  })

  function upload() {
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

<input type="file" id="file" name="file" />
<input type="button" value="Upload" on:click={upload} />
<progress value={progress} max="100" />
