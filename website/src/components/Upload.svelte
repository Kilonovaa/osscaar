<script>
  import { get } from "svelte/store"
  import { socketObject } from "../stores/socket"
  const socket = get(socketObject)

  socket.on("upload_response", (data) => {
    console.log(data)
  })
  function upload() {
    const file = document.getElementById("file").files[0]
    console.log(file)
    const reader = new FileReader()
    // reader.readAsDataURL(file)
    reader.readAsArrayBuffer(file)

    reader.onload = (fileEvent) => {
      const arrayBuffer = fileEvent.target.result
      const uint8Array = new Uint8Array(arrayBuffer)
      socket.emit("upload", uint8Array, (response) => {})
    }
  }
</script>

<input type="file" id="file" name="file" />
<input type="button" value="Upload" on:click={upload} />
