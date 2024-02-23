use task_service::infra::config::get_configuration;
use task_service::infra::logger::{get_logger, init_logger};
use task_service::infra::startup::Application;

#[tokio::main]
async fn main() -> std::io::Result<()> {

    let config = get_configuration().expect("Failed to read configuration.");

    let logger = get_logger("task_service".into(), "info".into(), std::io::stdout);
    init_logger(logger);

    let application = Application::build(config).await?;
    application.run_until_stopped().await?;

    Ok(())
}

