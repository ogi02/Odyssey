import page from 'page.js';
import Router from './Router.svelte';
import Route from './Route.svelte';
import NotFound from './NotFound.svelte';

const redirect = path => page.redirect(path);

export { Router, Route, NotFound, redirect };