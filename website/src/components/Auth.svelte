<script>
  import { supabase } from "../lib/supabase"
  let email, password, passwordConfirm
  function register() {
    if (password !== passwordConfirm) {
      alert("Passwords do not match")
      return
    }
    supabase.auth.signUp({
      email,
      password,
    })
  }
  function login() {
    supabase.auth.signIn({
      email,
      password,
    })
  }
</script>

<h1>Login</h1>
<input type="email" bind:value={email} />
<input type="password" bind:value={password} />

<h1>Register</h1>
<input type="email" bind:value={email} />
<input type="password" bind:value={password} />
<input type="password" bind:value={passwordConfirm} />
