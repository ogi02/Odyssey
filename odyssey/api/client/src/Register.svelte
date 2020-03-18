<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();
  import { fetchPost } from "./helpers.js";
  
  let username = "";
  let password = "";
  let confirmPassword = "";
  let name = "";
  let email = "";
  let login = true;
  

  async function loginUser() {
    const response = await fetchPost(
      "/login", {username: username, password: password}
    );
    if (!response.success) {
      return false;
    }
  }
  

  async function registerUser() {
    if (password !== confirmPassword) {
      dispatch("display-error", "Passwords do not match");
      return false;
    }
    const response = await fetchPost(
      "/register", {username: username, password: password, name: name, email: email}
    );
    if (!response.success) {
      dispatch("display-error", response.message);
      return false;
    }
    errorShow = false;
    dispatch("login-user", response);
  }

  function toggleLogin() {
    login = !login;
  }

</script>

<div id="card">
  <div class="header">
    {#if login}
      <h1>Login</h1>
    {:else}
      <h1>Register</h1>
    {/if}
  </div>
  
  <div class="form">
    <form>

      <input type="text" placeholder="Username" value={username} on:input={event => username = event.target.value} />

      <input type="password" placeholder="Password" value={password} on:input={event => password = event.target.value} />

    {#if !login}

      <input type="password" placeholder="Confirm Password" value={confirmPassword} on:input={event => confirmPassword = event.target.value}/>

      <input type="text" placeholder="Name" value={name} on:input={event => name = event.target.value}/>

      <input type="email" placeholder="Email" value={email} on:input={event => email = event.target.value}/>

      <button type="submit" on:click={registerUser}>Sign Up</button>

      <div on:click={toggleLogin}>Log in</div>

    {:else}

      <button type="submit" on:click={loginUser}>Login</button>

      <div on:click={toggleLogin}>Register</div>

    {/if}

    </form>
  </div>
</div>

<style>
  input {
    display: block;
  }
</style>