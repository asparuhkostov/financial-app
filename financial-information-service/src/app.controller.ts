import {
  Controller,
  Get,
  Headers,
  HttpStatus,
  Param,
  Post,
  Req,
  Res,
} from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(@Res() response) {
    return response.status(HttpStatus.OK).send();
  }

  @Post('/register')
  async register(@Req() request, @Res() response) {
    const { national_identification_number, country_of_residence, password } =
      request.body;

    this.appService.register(
      national_identification_number,
      country_of_residence,
      password,
      response,
    );
  }

  @Post('/login')
  async login(@Req() request, @Res() response) {
    const { national_identification_number, password } = request.body;
    this.appService.login(national_identification_number, password, response);
  }

  @Post('/init_auth')
  async initAuth(@Headers() headers, @Req() request, @Res() response) {
    const { authorization } = headers;
    const { bank } = request.body;

    return await this.appService.initAuth(authorization, bank, response);
  }

  @Post('/verify_auth')
  async verifyAuth(@Headers() headers, @Req() request, @Res() response) {
    const { authorization } = headers;
    const { bank, authRequestId } = request.body;

    return await this.appService.verifyAuth(
      authorization,
      bank,
      authRequestId,
      response,
    );
  }

  @Post('/connect')
  async connect(@Headers() headers, @Req() request, @Res() response) {
    const { authorization } = headers;
    const { bank, authRequestId } = request.body;

    return await this.appService.connect(
      authorization,
      bank,
      authRequestId,
      response,
    );
  }

  @Post('/verify_connection')
  async verifyConnection(@Headers() headers, @Req() request, @Res() response) {
    const { authorization } = headers;
    const { bank } = request.body;

    return await this.appService.verifyConnection(
      authorization,
      bank,
      response,
    );
  }

  @Get('/financial_overview')
  async financialOverview(@Headers() headers, @Res() response) {
    const { authorization } = headers;

    return await this.appService.getFinancialOverview(authorization, response);
  }
}
