use actix_web::{HttpResponse, Responder};
use serde::Serialize;
use utoipa::ToSchema;


#[derive(Serialize, ToSchema)]
pub struct Response {
    pub status: &'static str,
    pub message: String,
}

#[utoipa::path(
    get,
    path="/health_check",
    tag="Health Checker Endpoint",
    responses(
        (status=200, description="Authenticated User", body=Response),
    )
)]
pub async fn health_check() -> impl Responder {
    HttpResponse::Ok().json(Response {
        status: "success",
        message: "Complete Restful API in Rust".to_string(),
    })
}