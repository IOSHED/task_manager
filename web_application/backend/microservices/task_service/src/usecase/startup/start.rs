use std::net::TcpListener;
use sqlx::PgPool;
use actix_web::dev::Server;
use actix_web::{App, HttpServer, web, dev::Service as _};
use tracing_actix_web::TracingLogger;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

use crate::usecase::swager::ApiDoc;
use crate::interface::http::routers::{add_task, health_check};

pub fn run(listener: TcpListener, db_pool: PgPool) -> Result<Server, std::io::Error> {
    let db_pool = web::Data::new(db_pool);
    let openapi = ApiDoc::openapi();

    let server = HttpServer::new(move || {
        App::new()
            .wrap(TracingLogger::default())
            .wrap_fn(|req, srv| {
                let fut = srv.call(req);

                async {
                    let mut res = fut.await?;
                    Ok(res)
                }
            })
            .route("/health_check", web::get().to(health_check))
            .route("/task", web::post().to(add_task))
            .service(SwaggerUi::new("/docs/{_:.*}").url("/docs/openapi.json", openapi.clone()), )
            .app_data(db_pool.clone())
    })
        .listen(listener)?
        .run();

    Ok(server)
}
