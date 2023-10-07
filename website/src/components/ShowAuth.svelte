<script>
  import { user } from "../lib/supabase"
  import { get } from "svelte/store"
</script>

{JSON.stringify($user)}
