<script>
	import axios from 'axios';

	let overviewData = '';
	let error = '';

	async function loadOverview() {
		await axios({
			method: 'GET',
			url: 'http://localhost:3000/financial_overview',
			headers: {
				Authorization: document.cookie.split('=')[1]
			}
		})
			.then((res) => {
				overviewData = res.data;
			})
			.catch((e) => {
				console.log(e);
				error = "We're experiencing technical difficulties, please try again later.";
			});
	}
</script>

<h1>Overview</h1>

{#if !overviewData}
	<button on:click={loadOverview}>Load overview</button>
{/if}

{#if error.length}
	<h3>{error}</h3>
{/if}

{#if !error.length && overviewData?.seb}
	{#each overviewData.seb as accountData}
		<table>
			<thead>
				<tr>
					<td> Bank </td>
					<td> Currency </td>
					<td> Name </td>
					<td> IBAN </td>
				</tr>
			</thead>
			<tbody>
				<td> {accountData.account.bank} </td>
				<td> {accountData.account.currency} </td>
				<td> {accountData.account.name} </td>
				<td> {accountData.account.iban} </td>
			</tbody>
		</table>
		<table>
			<thead>
				<tr>
					<td> Date </td>
					<td> Amount </td>
					<td> Name </td>
				</tr>
			</thead>
			{#each accountData.transactions as t}
				{#each JSON.parse(t.transactions).transactions.booked as bT}
					<tbody>
						<td> {bT.bookingDate} </td>
						<td> {bT.transactionAmount.amount} </td>
						<td> {bT.descriptiveText} </td>
					</tbody>
				{/each}
			{/each}
		</table>
	{/each}
{/if}

<style>
	td {
		border: 1px solid black;
	}

	table {
		margin-top: 1em;
		margin-bottom: 1em;
	}
</style>
