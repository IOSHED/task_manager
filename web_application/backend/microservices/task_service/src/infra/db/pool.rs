use sqlx::PgPool;
use sqlx::postgres::PgPoolOptions;
use crate::infra::config::DatabaseSettings;

pub fn get_connection_pool(configuration: &DatabaseSettings) -> PgPool {
    PgPoolOptions::new()
        .acquire_timeout(std::time::Duration::from_secs(2))
        .connect_lazy_with(configuration.with_db())
}
