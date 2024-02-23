/// **Interface**
///
/// **What should be there**:
/// The interfaces folder contains the input/output interfaces of your application,
/// such as HTTP handlers, CLI interfaces, etc.
///
/// **How to interact with other modules or microservices**:
/// Interfaces provide a way for external systems to interact with your microservice.
/// They handle requests, format responses.
///
/// **Dependencies**:
/// Interfaces depend on the perform business operations.
///

pub mod cli;
pub mod http;