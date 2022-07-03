import express, { Express, Request, Response } from "express";
import { ApolloServer } from "apollo-server-express";
import resolvers from "./graphql/resolvers";
import typeDefs from "./graphql/schema";

const WEB_SERVER_PORT = process.env.WEB_SERVER_PORT || 3000;
const webServer: Express = express();

async function setUpGraphQL() {
  const apolloServer: ApolloServer = new ApolloServer({ typeDefs, resolvers });
  await apolloServer.start();
  apolloServer.applyMiddleware({ app: webServer });
}
setUpGraphQL();

webServer.get("/health", (_: Request, res: Response) => res.sendStatus(200));

webServer.listen(WEB_SERVER_PORT, () =>
  console.log(`Web server listening on port ${WEB_SERVER_PORT}`)
);
