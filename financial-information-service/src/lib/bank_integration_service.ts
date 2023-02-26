import { fetchWithTimeout } from './networking';

export default class BankIntegrationServiceClient {
  BASE_URL = process.env.BANK_INTEGRATION_SERVICE_URL;
  FINANCIAL_OVERVIEW_PATH = 'get_financial_records';
  national_identification_number = '';

  constructor(national_identification_number) {
    this.national_identification_number = national_identification_number;
  }

  async get_financial_overview() {
    let response;

    const query_result = await fetchWithTimeout(
      `http://${this.BASE_URL}/${this.FINANCIAL_OVERVIEW_PATH}/${this.national_identification_number}`,
      2000,
    );

    if (query_result) {
      response = query_result.json();
    }

    return response;
  }
}
