import { createClient } from "@supabase/supabase-js"
import { writable } from "svelte/store"
const supabaseUrl = "https://jlmscnkfbmlokpvarqcv.supabase.co"
const anonKEy =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpsbXNjbmtmYm1sb2twdmFycWN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTgyNTY3NjIsImV4cCI6MjAxMzgzMjc2Mn0.GHC25IoBPGFpiiylZ6ha7JVVzU8sxUxIDZOjpGtv4FM"
const supabase = createClient(supabaseUrl, anonKEy)

export { supabase }

export const user = writable(null)

// supabase.auth.onAuthStateChange((event, session) => {
//   console.log(event, session)
//   if (event === "SIGNED_IN") {
//     user.set(session.user)
//   }
// })
