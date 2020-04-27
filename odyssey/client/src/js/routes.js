import Home from '../Home.svelte';
import NotFound from '../Navigation/NotFound.svelte'
import MyProfile from '../Profiles/MyProfile.svelte';
import UserProfile from '../Profiles/UserProfile.svelte';
import BecomeCreator from '../Authentication/BecomeCreator.svelte';
import Authentication from '../Authentication/Authentication.svelte';

export default [
	{
		path: '/',
		component: Home
	},
	{
		path: '/login',
		component: Authentication
	},
	{
		path: '/profile',
		component: MyProfile,
		auth: true
	},
	{
		path: '/profile/:username',
		component: UserProfile,
		auth: true
	},
	{
		path: '/become_a_creator',
		component: BecomeCreator,
		auth: true
	},
	{
		path: '*',
		component: NotFound
	}
];