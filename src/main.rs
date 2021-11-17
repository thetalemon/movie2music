use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use actix_web::http::header;
use actix_cors::Cors;

#[get("/")]
async fn hello() -> impl Responder {
  HttpResponse::Ok().body("Hello world from rust backend!")
}

#[post("/echo")]
async fn echo(req_body: String) -> impl Responder {
  HttpResponse::Ok().body(req_body)
}

async fn manual_hello() -> impl Responder {
  HttpResponse::Ok().body("Hey there!")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
  HttpServer::new(|| {
    let cors = Cors::default()
    .allowed_origin("http://localhost:8000")
    .allowed_methods(vec!["GET", "POST"])
    .allowed_headers(vec![header::AUTHORIZATION, header::ACCEPT])
    .allowed_header(header::CONTENT_TYPE)
    .supports_credentials()
    .max_age(3600);

    App::new()
      .wrap(cors)
      .service(hello)
      .service(echo)
      .route("/hey", web::get().to(manual_hello))
  })
  .bind("127.0.0.1:8080")?
  .run()
  .await
}