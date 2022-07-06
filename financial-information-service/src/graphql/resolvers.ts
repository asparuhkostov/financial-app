import Customer from "../data/Customer";

export default {
  Query: {
    customer: async (_: any, { customerId }: { customerId: string }) => {
      const cust = await Customer.query().findById(customerId);
      if (cust) {
        return cust;
      }
    },
  },
  Mutation: {},
};
