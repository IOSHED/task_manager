use task_service::infra::config::get_configuration;
use task_service::infra::logger::{get_logger, init_logger};

fn main() {
    let _config = get_configuration();
    let logger = get_logger("task_service".into(), "info".into(), std::io::stdout);
    init_logger(logger);

}

