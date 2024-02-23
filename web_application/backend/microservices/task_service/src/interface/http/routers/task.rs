use actix_web::{web, HttpResponse};
use actix_web::http::header::ContentType;
use serde::{Deserialize, Serialize};
use sqlx::PgPool;
use utoipa::ToSchema;
use uuid::Uuid;

#[derive(Deserialize)]
pub struct Request {

}

#[derive(Serialize, ToSchema)]
pub struct Response {
    id_task: String,
    id_template: String,
}

#[utoipa::path(
    post,
    path="/task",
    tag="Create new task",
    responses(
        (status=201, description="Create succeed new task", body=Response),
    )
)]
#[tracing::instrument(
    name = "Adding a new task.",
    skip(pool, req),
    fields(
    )
)]
/// # Add Task
///
/// Creates a task only for the user who logged in with his username.
/// The user can specify a template for the task and fill in the template fields.
/// If the user does not specify a template for the task,
/// a template will be created based on the task name with a standard set of fields.
/// The created task will go to the queue in `RabbitMQ` to `notification_service`
/// for subsequent notification, if the task specifies that it needs to be reminded.
///
pub async fn add_task(
    pool: web::Data<PgPool>,
    req: web::Json<Request>
) -> HttpResponse {
    let res = Response {
        id_task: Uuid::new_v4().to_string(),
        id_template: Uuid::new_v4().to_string()
    };
    let body = serde_json::to_string(&res).unwrap();
    HttpResponse::Ok()
        .content_type(ContentType::json())
        .body(body)
}
