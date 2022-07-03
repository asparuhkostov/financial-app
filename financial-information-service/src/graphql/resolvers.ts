import Customer from "../data/Customer";

export default {
  Query: {
    customer: async (
      _: any,
      { customerId }: { customerId: string },
      context: any
    ) => {
      const cust = await Customer.query().findById(customerId);
      if (cust) {
        return cust;
      }
    },
  },
  Mutation: {},
};
