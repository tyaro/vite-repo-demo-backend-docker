FROM postgrest/postgrest

ENV PGRST_DB_URI postgres://postgres:postgres@postgres:5432/postgres
ENV PGRST_OPENAPI_SERVER_PROXY_URI http://postgrest:5433
ENV PGRST_DB_SCHEMA: public
ENV PGRST_DB_ANON_ROLE: "postgrest"
ENV PGRST_SERVER_PORT: 5433