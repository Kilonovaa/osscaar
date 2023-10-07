<script>
  import { supabase } from "../lib/supabase"
  let email, password, passwordConfirm
  async function register() {
    if (password !== passwordConfirm) {
      alert("Passwords do not match")
      return
    }
    const result = await supabase.auth.signUp({
      email,
      password,
    })
    console.log(result)
  }
  async function login() {
    const result = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    console.log(result)
  }
</script>

<h1>Login</h1>
<input type="email" bind:value={email} />
<input type="password" bind:value={password} />
<input type="button" value="Login" on:click={async () => await login()} />

<h1>Register</h1>
<input type="email" bind:value={email} />
<input type="password" bind:value={password} />
<input type="password" bind:value={passwordConfirm} />
<input type="button" value="Register" on:click={async () => await register()} />
