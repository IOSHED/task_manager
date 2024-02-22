use crate::infra::config::env::Environment;
use crate::infra::config::structs::Settings;

pub fn get_configuration() -> Result<Settings, config::ConfigError> {
    let mut settings = config::Config::default();

    let base_path = std::env::current_dir().expect("Failed to getting current dir for settings");
    let config_dir = base_path.join("configuration");


    // Add configuration values from a file named `configuration`.
    // It will look for any top-level file with an extension
    // that `config` knows how to parse: yaml, json, etc.

    // Read `default` config file.
    settings.merge(config::File::from(config_dir.join("base")).required(true))?;

    let env: Environment = std::env::var("APP_ENVIRONMENT")
        .unwrap_or_else(|_| "local".into())
        .try_into()
        .expect("Failed to read APP_ENVIRONMENT");

    settings.merge(config::File::from(config_dir.join(env.as_str())).required(true))?;

    // Add in settings from environment variables (with a prefix of APP and '__' as separator)
    // E.g. `APP_APPLICATION__PORT=5001 would set `Settings.application.port`
    settings.merge(config::Environment::with_prefix("app").separator("__"))?;

    // Try to convert the configuration values it read into
    // our Settings type
    settings.try_into()
}

