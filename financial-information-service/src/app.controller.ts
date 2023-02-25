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

  @Get('/financial_overview/:national_identification_number')
  async financial_overview(
    @Param() parameters,
    @Headers() headers,
    @Res() response,
  ) {
    const { national_identification_number } = parameters;
    const { authorization } = headers;

    return await this.appService.get_user_financial_overview(
      national_identification_number,
      authorization,
      response,
    );
  }
}
