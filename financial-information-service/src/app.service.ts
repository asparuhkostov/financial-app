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
              data: { identity: user.national_identification_number },
              exp: Math.floor(Date.now() / 1000) + 60 * 60,
            },
            process.env.SERVER_SECRET,
          );
          response.send({ auth_cookie });
        } else {
          response.status(HttpStatus.FORBIDDEN).send();
        }
      }
    });
  }

  async get_user_financial_overview(
    national_identification_number,
    authorization,
    response,
  ) {
    const decoded_auth = verify(authorization, process.env.SERVER_SECRET);
    // TO-DO - move auth into higher level
    // TO-DO - sanitize headers before using in code
    if (decoded_auth?.data.identity === national_identification_number) {
      let res;
      const client = new BankIntegrationServiceClient(
        national_identification_number,
      );
      const query_result = await client.get_financial_overview();
      if (query_result) {
        res = query_result;
      } else {
        res = HttpStatus.INTERNAL_SERVER_ERROR;
      }
      response.send(res);
    } else {
      response.status(HttpStatus.FORBIDDEN).send();
    }
  }
}
