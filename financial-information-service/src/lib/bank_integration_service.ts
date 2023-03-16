import axios from 'axios';

export default class BankIntegrationServiceClient {
  BASE_URL = process.env.BANK_INTEGRATION_SERVICE_URL;
  INIT_AUTH_PATH = 'start_login';
  VERIFY_AUTH_PATH = 'verify_login';
  CONNECT_PATH = 'connection';
  VERIFY_CONNECTION_PATH = 'verify_connection';
  POPULATE_FINANCIAL_RECORDS_PATH = 'populate_financial_information_records';
  FINANCIAL_OVERVIEW_PATH = 'get_financial_records';

  national_identification_number = '';

  constructor(national_identification_number) {
    this.national_identification_number = national_identification_number;
  }

  async initAuth(bank) {
    let response;

    await axios
      .post(`http://${this.BASE_URL}/${this.INIT_AUTH_PATH}`, {
        bank,
      })
      .then((res) => (response = res.data));

    return response;
  }

  async verifyAuth(bank, authRequestId) {
    let response;

    await axios
      .post(`http://${this.BASE_URL}/${this.VERIFY_AUTH_PATH}`, {
        bank,
        auth_req_id: authRequestId,
      })
      .then((res) => (response = res.data));

    return response;
  }

  async connect(bank, authRequestId) {
    let response;

    await axios
      .post(`http://${this.BASE_URL}/${this.CONNECT_PATH}`, {
        bank,
        auth_req_id: authRequestId,
        national_identification_number: this.national_identification_number,
      })
      .then((res) => (response = res.data));

    return response;
  }

  async verifyConnection(bank) {
    let response;

    await axios
      .post(`http://${this.BASE_URL}/${this.VERIFY_CONNECTION_PATH}`, {
        bank,
        national_identification_number: this.national_identification_number,
      })
      .then((res) => (response = res.data));

    return response;
  }

  populateFinancialRecords(bank) {
    axios.get(
      `http://${this.BASE_URL}/${this.POPULATE_FINANCIAL_RECORDS_PATH}/${bank}/${this.national_identification_number}`,
    );
  }

  async getFinancialOverview() {
    let response;

    await axios
      .get(
        `http://${this.BASE_URL}/${this.FINANCIAL_OVERVIEW_PATH}/${this.national_identification_number}`,
      )
      .then((res) => (response = res.data));

    return response;
  }
}
