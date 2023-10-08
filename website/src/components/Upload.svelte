<script>
  import { io } from "socket.io-client"
  import { url } from "../lib/socket"
  import { supabase } from "../lib/supabase"
  const socket = io(url)
  let progress = 0

  socket.on("upload_response", async (info) => {
    console.log(info)
    progress = 0
    // document.getElementById("file").value = ""
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
