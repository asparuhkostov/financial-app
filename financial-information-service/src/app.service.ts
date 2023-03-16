import { HttpStatus, Injectable } from '@nestjs/common';
import { hash, compare } from 'bcrypt';
import { sign, verify } from 'jsonwebtoken';
import { v4 } from 'uuid';

import { dbClient } from './lib/database';
import BankIntegrationServiceClient from './lib/bank_integration_service';

@Injectable()
export class AppService {
  getHello(): number {
    return HttpStatus.OK;
  }

  // TO-DO: move the login & registration paths
  // into a user module
  async register(
    national_identification_number,
    country_of_residence,
    password,
    response,
  ) {
    let new_user;

    const existing_user = await dbClient.user.findUnique({
      where: { national_identification_number },
    });

    if (existing_user) {
      // Rather than letting whoever triggered this know,
      // that a user with this username exists,
      // we error out with a generic code.
      response.status(HttpStatus.INTERNAL_SERVER_ERROR).send();
      return;
    }

    try {
      await hash(password, 10, async (err, hash) => {
        if (err) {
          response.status(HttpStatus.INTERNAL_SERVER_ERROR).send();
        } else {
          new_user = await dbClient.user.create({
            data: {
              id: v4(),
              password: hash,
              country_of_residence,
              national_identification_number,
            },
          });
          response.status(HttpStatus.OK).send();
        }
      });
    } catch (e) {
      response.status(HttpStatus.INTERNAL_SERVER_ERROR).send();
    }
  }

  async login(national_identification_number, password, response) {
    let user = await dbClient.user.findUnique({
      where: { national_identification_number },
    });

    if (!user) {
      return response.status(HttpStatus.NOT_FOUND).send();
    }

    compare(password, user.password, (err, result) => {
      if (err) {
        response.status(HttpStatus.INTERNAL_SERVER_ERROR).send();
      } else {
        if (result) {
          const auth_cookie = sign(
            {
              data: { identity: user.id },
              exp: Math.floor(Date.now() / 1000) + 60 * 60,
            },
            process.env.SERVER_SECRET,
          );
          response.status(HttpStatus.OK).send({ auth_cookie });
        } else {
          response.status(HttpStatus.FORBIDDEN).send();
        }
      }
    });
  }

  // TO-DO: move the financial connection & overview paths
  // into their own module
  // TO-DO: move authorization 1 layer above,
  // the controller should handle this
  async initAuth(authorization, bank, response) {
    const decoded_auth = verify(authorization, process.env.SERVER_SECRET);
    const id = decoded_auth.data.identity;
    let res;

    if (id) {
      // TO-DO: move this client instantiation\
      // into a separate method - it's being repeated
      // for every step of the connection process
      let user = await dbClient.user.findUnique({
        where: { id },
      });
      const national_identification_number =
        user.national_identification_number;
      const client = new BankIntegrationServiceClient(
        national_identification_number,
      );

      const query_result = await client.initAuth(bank);
      if (query_result) {
        res = query_result;
      } else {
        res = HttpStatus.INTERNAL_SERVER_ERROR;
      }
    } else {
      res = HttpStatus.FORBIDDEN;
    }

    response.send(res);
  }

  async verifyAuth(authorization, bank, authRequestId, response) {
    const decoded_auth = verify(authorization, process.env.SERVER_SECRET);
    const id = decoded_auth.data.identity;
    let res;

    if (id) {
      let user = await dbClient.user.findUnique({
        where: { id },
      });
      const national_identification_number =
        user.national_identification_number;
      const client = new BankIntegrationServiceClient(
        national_identification_number,
      );

      const query_result = await client.verifyAuth(bank, authRequestId);
      if (query_result) {
        res = query_result;
      } else {
        res = HttpStatus.INTERNAL_SERVER_ERROR;
      }
    } else {
      res = HttpStatus.FORBIDDEN;
    }

    response.send(res);
  }

  async connect(authorization, bank, authRequestId, response) {
    const decoded_auth = verify(authorization, process.env.SERVER_SECRET);
    const id = decoded_auth.data.identity;
    let res;

    if (id) {
      let user = await dbClient.user.findUnique({
        where: { id },
      });
      const national_identification_number =
        user.national_identification_number;
      const client = new BankIntegrationServiceClient(
        national_identification_number,
      );

      const query_result = await client.connect(bank, authRequestId);
      if (query_result) {
        res = query_result;
      } else {
        res = HttpStatus.INTERNAL_SERVER_ERROR;
      }
    } else {
      res = HttpStatus.FORBIDDEN;
    }

    response.send(res);
  }

  async verifyConnection(authorization, bank, response) {
    const decoded_auth = verify(authorization, process.env.SERVER_SECRET);
    const id = decoded_auth.data.identity;
    let res;

    if (id) {
      let user = await dbClient.user.findUnique({
        where: { id },
      });
      const national_identification_number =
        user.national_identification_number;
      const client = new BankIntegrationServiceClient(
        national_identification_number,
      );

      const query_result = await client.verifyConnection(bank);
      if (query_result) {
        res = query_result;
        if (query_result?.is_complete) {
          client.populateFinancialRecords(bank);
        }
      } else {
        res = HttpStatus.INTERNAL_SERVER_ERROR;
      }
    } else {
      res = HttpStatus.FORBIDDEN;
    }

    response.send(res);
  }

  async getFinancialOverview(authorization, response) {
    const decoded_auth = verify(authorization, process.env.SERVER_SECRET);
    const id = decoded_auth.data.identity;
    let res;

    if (id) {
      let user = await dbClient.user.findUnique({
        where: { id },
      });
      const national_identification_number =
        user.national_identification_number;
      const client = new BankIntegrationServiceClient(
        national_identification_number,
      );

      const query_result = await client.getFinancialOverview();
      if (query_result) {
        res = query_result;
      } else {
        res = HttpStatus.INTERNAL_SERVER_ERROR;
      }
    } else {
      res = HttpStatus.FORBIDDEN;
    }

    response.send(res);
  }
}
