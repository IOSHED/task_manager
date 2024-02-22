use sqlx::postgres::{PgConnectOptions, PgSslMode};
use sqlx::ConnectOptions;
use serde_aux::prelude::deserialize_number_from_string;

/// # Assembly of all components
#[derive(serde::Deserialize, Clone)]
pub struct Settings {
    pub database: DatabaseSettings,
    pub application: ApplicationSettings,
}

/// # App
/// ```port```: port which starting app
/// ```host```: host which starting app
#[derive(serde::Deserialize, Clone)]
pub struct ApplicationSettings {
    #[serde(deserialize_with = "deserialize_number_from_string")]
    pub port: u16,
    pub host: String,
}

/// # Database
/// - ```username```: name account registered in db
/// - ```password```: password from username
/// - ```port```: port starting db
/// - ```host```: host starting db
/// - ```database_name```: name for main db
#[derive(serde::Deserialize, Clone)]
pub struct DatabaseSettings {
    pub username: String,
    pub password: String,
    #[serde(deserialize_with = "deserialize_number_from_string")]
    pub port: u16,
    pub host: String,
    pub database_name: String,
    pub require_ssl: bool,
}

impl DatabaseSettings {
    /// Getting database URL for tests without ```database_name```
    pub fn without_db(&self) -> PgConnectOptions {
        let ssl_mode = match self.require_ssl {
            true => PgSslMode::Require,
            false => PgSslMode::Prefer,
        };
        PgConnectOptions::new()
            .host(&self.host)
            .username(&self.username)
            .password(&self.password)
            .port(self.port)
            .ssl_mode(ssl_mode)
    }

    /// Getting database URL
    pub fn with_db(&self) -> PgConnectOptions {
        self.without_db()
            .database(&self.database_name)
            .log_statements(log::LevelFilter::Trace)
    }
}
