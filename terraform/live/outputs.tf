output "app_urls" {
  description = "The URLs where the applications can be accessed"
  value = {
    for app, app_module in module.apps :
    app => "http://localhost${app_module.ingress_path}"
  }
}

output "app_images" {
  description = "The Docker images used for the applications"
  value = {
    for app, app_module in module.apps :
    app => app_module.image
  }
}

output "namespaces" {
  description = "The namespaces where the applications are deployed"
  value = {
    for app, app_module in module.apps :
    app => app_module.namespace
  }
}
