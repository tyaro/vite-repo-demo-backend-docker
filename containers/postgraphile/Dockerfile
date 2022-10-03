FROM graphile/postgraphile

ENV DATABASE_URL "postgres://postgres:postgres@postgres:5432/postgres"

RUN yarn add @graphile-contrib/pg-simplify-inflector
RUN yarn add @graphile-contrib/pg-many-to-many
# COPY start.sh start.sh

CMD [ \
      "--subscriptions",  \
      "--watch",  \
      "--dynamic-json", \
      "--no-setof-functions-contain-nulls", \
      "--no-ignore-rbac", \
      "--show-error-stack=json", \
      "--extended-errors", \
      "hint,detail,errcode", \
      "--append-plugins", \
      "@graphile-contrib/pg-simplify-inflector,@graphile-contrib/pg-many-to-many", \
      "--enhance-graphiql", \
      "--allow-explain", \
      "--enable-query-batching", \
      "--connection", \
      "postgres://postgres:postgres@postgres:5432/postgres",  \
      "--host", "postgraphile",  \
      "--port", "5434",  \
      "--schema", "public",  \
      "--default-role", "postgres"] 

EXPOSE 5434
