FROM lukemathwalker/cargo-chef:latest-rust-1.74.1 as chef
WORKDIR /app
RUN apt update && apt install lld clang -y

FROM chef as planner
COPY . .
# Compute a lock-like file for our project
RUN cargo chef prepare  --recipe-path recipe.json

FROM chef as builder
COPY --from=planner /app/recipe.json recipe.json
# Build our project dependencies, not our application!
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
ENV SQLX_OFFLINE true
RUN cargo install sqlx-cli --no-default-features --features postgres
RUN cargo build --release --bin task_service

FROM debian:bookworm-slim AS runtime
WORKDIR /app
RUN apt-get update -y && apt-get install -y --no-install-recommends openssl ca-certificates && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/cargo/bin/sqlx /usr/local/cargo/bin/sqlx
COPY --from=builder /app/target/release/task_service task_service
COPY config config
COPY migrations migrations
ENV APP_ENVIRONMENT production
ENV PATH="/usr/local/cargo/bin:${PATH}"
ENTRYPOINT ["./task_service"]
