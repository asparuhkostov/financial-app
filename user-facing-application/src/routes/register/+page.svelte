<script>
	import axios from 'axios';

	const REGISTRATION_URL = 'http://localhost:3000/register';
	let registered = false;
	let national_identification_number, password;

	async function submit() {
		let res = await axios.post(REGISTRATION_URL, {
			national_identification_number,
			country_of_residence: 'SE',
			password
		});
		// TO-DO, add proper client & error handling here.
		if (res.status == 200) {
			registered = true;
		}
	}
</script>

<h1>Register</h1>

{#if registered}
	<p>Success! You can now <a href="/login">log in.</a></p>
{:else}
	<form>
		<input
			type="text"
			placeholder="National identification number"
			bind:value={national_identification_number}
		/>
		<input type="password" placeholder="Password" bind:value={password} />
		<button on:click={submit}>Submit</button>
	</form>
{/if}
