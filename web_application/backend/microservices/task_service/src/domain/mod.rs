/// **Domain**
///
/// **What should be there**:
/// This folder contains the core business logic of your application.
/// It typically includes entities (representing domain objects),
/// repositories (interfaces for data access),
/// and services (business logic that operates on entities).
///
/// **How to interact with other modules or microservices**:
/// The domain layer should be independent of other layers.
/// It defines the business rules and entities that represent the application's domain.
/// Other layers interact with the domain layer to perform operations on these entities.
///

mod service;
mod types;

