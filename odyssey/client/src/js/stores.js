// Library imports
import { writable } from 'svelte/store'

export const username = writable('');

export const loggedIn = writable(false);

export const isCreator = writable(false);