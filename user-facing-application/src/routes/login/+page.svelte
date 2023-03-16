<script>
	import axios from 'axios';

	const LOGIN_URL = 'http://localhost:3000/login';
	let logged_in = false;
	let national_identification_number, password;

	async function submit() {
		let res = await axios.post(LOGIN_URL, {
			national_identification_number,
			country_of_residence: 'SE',
			password
		});
		// TO-DO, add proper client & error handling here.
		if (res.status == 200) {
			logged_in = true;
			const response_json = res.data;
			document.cookie = `auth=${response_json['auth_cookie']}`;
		}
	}
</script>

<h1>Log in</h1>

{#if logged_in}
	<p>
		Success! You can now <a href="/connect">connect a bank</a> or, if you've already done that,
		<a href="/overview">see your financial overview</a>.
	</p>
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
