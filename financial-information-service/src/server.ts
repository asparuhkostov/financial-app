import express, { Express, Request, Response } from "express";
import helmet from "helmet";
import { ApolloServer } from "apollo-server-express";
import resolvers from "./graphql/resolvers";
import typeDefs from "./graphql/schema";

const WEB_SERVER_PORT = process.env.WEB_SERVER_PORT || 4000;
const webServer: Express = express();

if (process.env.NODE_ENV !== "development") {
  webServer.use(helmet());
  webServer.disable("x-powered-by");
}

async function setUpGraphQL() {
  const apolloServer: ApolloServer = new ApolloServer({
    typeDefs,
    resolvers,
    context: () => ({}),
  });
  await apolloServer.start();
  apolloServer.applyMiddleware({ app: webServer });
}
setUpGraphQL();

webServer.get("/health", (_: Request, res: Response) => res.sendStatus(200));

webServer.listen(WEB_SERVER_PORT, () =>
  console.log(`Web server listening on port ${WEB_SERVER_PORT}`)
);
