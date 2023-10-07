import { createClient } from "@supabase/supabase-js"

const supabaseUrl = "https://nwhobhigrgxtpnwydpxj.supabase.co"
const anonKEy =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY2ODY4NTIsImV4cCI6MjAxMjI2Mjg1Mn0.PKRVhcs6GuNeAv0l8txZi9mAjC49JkFl4DjDld3QuTc"
const supabase = createClient(supabaseUrl, anonKEy)

export { supabase }
