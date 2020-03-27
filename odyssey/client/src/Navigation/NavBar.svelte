<script>
	import { Router, Route, Link } from "svelte-routing";
	import NavLink from "./NavLink.svelte";
	import BecomeCreator from '../Authentication/BecomeCreator.svelte';
	import Profile from '../Profiles/Profile.svelte';
	export let url = "";
</script>

<Router url="{url}">
  <nav>
    <Link to="/">Profile</Link>
    <Link to="about">About</Link>
    <Link to="become_a_creator">Become a creator!</Link>
  </nav>
  <div>
    <Route path="about" component="{Profile}" />
    <Route path="become_a_creator" component="{BecomeCreator}" />
    <Route path="/" component="{Profile}" />
  </div>
</Router>

<style>
	nav {
		position: relative;
		top: 500px;
	}
</style>