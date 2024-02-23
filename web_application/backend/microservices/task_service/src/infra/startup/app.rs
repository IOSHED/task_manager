use std::net::TcpListener;
use actix_web::dev::Server;
use crate::infra::config::Settings;
use crate::infra::db;
use crate::infra::startup::start::run;


pub struct Application {
    port: u16,
    server: Server,
}

impl Application {

    pub async fn build(configuration: Settings) -> Result<Self, std::io::Error> {
        // init db
        let connection_pool = db::get_connection_pool(&configuration.database);

        // run
        let address = format!("{}:{}", configuration.application.host, configuration.application.port);
        let listener = TcpListener::bind(&address)?;
        let port = listener.local_addr().unwrap().port();
        let server = run(listener, connection_pool)?;

        Ok(Self { port, server })
    }

    pub fn port(&self) -> u16 {
        self.port
    }

    /// A more expressive name that makes it clear that
    /// this function only returns when the application is stopped.
    pub async fn run_until_stopped(self) -> Result<(), std::io::Error> {
        self.server.await
    }
}
