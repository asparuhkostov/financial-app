<script>
	import axios from 'axios';

	const CONNECTION_STAGES = {
		INITIAL: 'initial',
		BANK_ID: 'bank_id',
		CONNECTING: 'connecting',
		DONE: 'done'
	};

	const ERRORS = {
		GENERAL: "We're experiencing technical difficulties, please try again later.",
		TIMEOUT: 'Our attempt to connect took too long, please try again later.'
	};

	const BASE_API_URL = 'http://localhost:3000';
	const INIT_AUTH_URL = `${BASE_API_URL}/init_auth`;
	const VERIFY_AUTH_URL = `${BASE_API_URL}/verify_auth`;
	const VERIFY_CONNECTION_URL = `${BASE_API_URL}/verify_connection`;
	const CONNECT_URL = `${BASE_API_URL}/connect`;

	let connection_stage = CONNECTION_STAGES.INITIAL;

	// Only SEB is supported for now, so no dropdown
	let bank = 'seb';
	let bankIdAutoStartToken = '';
	let error = '';
	let authRequestId = '';

	let authPollAttempts = 0;
	let connectionPollAttempts = 0;

	async function startBankLogin() {
		await axios({
			method: 'POST',
			url: INIT_AUTH_URL,
			data: { bank },
			headers: {
				Authorization: document.cookie.split('=')[1]
			}
		})
			.then((res) => {
				const { auth_request_id, bank_id_autostart_token } = res.data;
				authRequestId = auth_request_id;
				bankIdAutoStartToken = bank_id_autostart_token;

				connection_stage = CONNECTION_STAGES.BANK_ID;
				pollForAuthStatus();
			})
			.catch((e) => {
				error = ERRORS.GENERAL;
			});
	}

	async function pollForAuthStatus() {
		await axios({
			method: 'POST',
			url: VERIFY_AUTH_URL,
			data: {
				bank,
				authRequestId
			},
			headers: {
				Authorization: document.cookie.split('=')[1]
			}
		})
			.then((res) => {
				const { is_complete } = res.data;
				if (is_complete && !error.length) {
					connection_stage = CONNECTION_STAGES.CONNECTING;
					triggerConnection();
					pollForConnectionStatus();
				} else {
					authPollAttempts++;
					if (authPollAttempts > 15) {
						error = ERRORS.TIMEOUT;
						return;
					}
					setTimeout(pollForAuthStatus, 3000);
				}
			})
			.catch((e) => {
				error = ERRORS.GENERAL;
			});
	}

	async function triggerConnection() {
		await axios({
			method: 'POST',
			url: CONNECT_URL,
			data: {
				bank,
				authRequestId
			},
			headers: {
				Authorization: document.cookie.split('=')[1]
			}
		}).catch((e) => {
			error = ERRORS.GENERAL;
		});
	}

	async function pollForConnectionStatus() {
		await axios({
			method: 'POST',
			url: VERIFY_CONNECTION_URL,
			data: {
				bank
			},
			headers: {
				Authorization: document.cookie.split('=')[1]
			}
		})
			.then((res) => {
				const { is_complete } = res.data;
				if (is_complete && !error.length) {
					connection_stage = CONNECTION_STAGES.DONE;
				} else {
					connectionPollAttempts++;
					if (connectionPollAttempts > 15) {
						error = ERRORS.TIMEOUT;
						return;
					}
					setTimeout(pollForConnectionStatus, 3000);
				}
			})
			.catch((e) => {
				error = ERRORS.GENERAL;
			});
	}
</script>

<h1>Connect to your bank</h1>

{#if error.length}
	<h3>{error}</h3>
{/if}

{#if !error}
	{#if connection_stage == CONNECTION_STAGES.INITIAL}
		<form>
			<button on:click={startBankLogin}>Start</button>
		</form>
	{/if}

	{#if connection_stage == CONNECTION_STAGES.BANK_ID}
		<p>Waiting for you to authorise the connection with BankID!</p>
		<br />
		<p>
			Open <a
				href={`bankid:///?autostarttoken=${bankIdAutoStartToken}`}
				target="_blank"
				rel="noreferrer">BankID</a
			>
		</p>
	{/if}

	{#if connection_stage == CONNECTION_STAGES.CONNECTING}
		<p>Connecting to your bank, please wait...</p>
	{/if}

	{#if connection_stage == CONNECTION_STAGES.DONE}
		<p>
			Success! You can now <a href="/overview">see your financial overview</a>.
		</p>
	{/if}
{/if}
