/// **Infra**
///
/// **What should be there**:
/// The infra folder contains the implementation details
/// of external dependencies like database access, external API calls, etc.
///
/// **How to interact with other modules or microservices**:
/// The infra layer provides concrete implementations for interacting with external systems.
/// It abstracts away the details of these interactions from the rest of the application.
///
/// **Dependencies**:
/// The infra layer typically depends on the domain layer to access and manipulate domain entities.
///

mod db;
mod config;