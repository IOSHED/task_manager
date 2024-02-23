use utoipa::OpenApi;
use crate::interface::http::routers::{
    __path_health_check,
    __path_add_task,
};
use crate::interface::http::routers::{
    health_check,
    task,
};

#[derive(OpenApi)]
#[openapi(
    paths(
        health_check,
        add_task,
    ),
    components(
        schemas(health_check::Response),
        schemas(task::Response),
    ),
    tags(
        (name = "Rust REST API", description = "Task in Rust Endpoints")
    ),
)]
pub struct ApiDoc;
