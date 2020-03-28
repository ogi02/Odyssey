<script>
	import { Router, Route} from "svelte-routing";
	import BecomeCreator from '../Authentication/BecomeCreator.svelte';
	import Profile from '../Profiles/Profile.svelte';
  import { link, navigate } from "svelte-routing";
  import Authentication from "../Authentication/Authentication.svelte";
  import App from '../App.svelte';
	export let url = "";
  import { logoutUser, loginUser } from '../Authentication/authentication_management.js';
  import { checkLogin } from "../helpers.js";
</script>

<Router url="{url}">

  <nav>
    <a href="/" use:link>Home</a>
    <a href="about" use:link>About</a>
    {#if checkLogin()}
      <a href="become_a_creator" use:link>Become a creator!</a>
      <a href="login" use:link on:click={() => logoutUser()}>Logout</a>
    {:else}
      <a href="login" use:link>Log in</a>
    {/if}
    
  </nav>
  <div>
    <Route path="about" component="{Profile}" />
    <Route path="become_a_creator" component="{BecomeCreator}" />
    <Route path="/" component="{Profile}" />
    <Route path="login" component="{Authentication}" />


  </div>
</Router>

<style>

  nav {
      position: fixed;
      top: 0;
      left: 0;
      padding: 1.2em 0 1.2em 0;
      width: 100%;

      background-color: tomato;
  }
  nav a {
    text-decoration: none;
    color: white;
    margin: 0;
    left: 0;
    padding: 1.2em;
  }

  nav a:hover{
    text-decoration: none;
    background-color: green;

  }


</style>
