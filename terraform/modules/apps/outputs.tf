output "image" {
  description = "The Docker image used for the application"
  value       = var.image
}

output "namespace" {
  description = "The namespace where the application is deployed"
  value       = var.namespace
}

output "name" {
  description = "The name of the application"
  value       = var.name
}

output "service_name" {
  description = "The name of the Kubernetes service"
  value       = kubernetes_service.app.metadata[0].name
}

output "ingress_path" {
  description = "The ingress path for the application"
  value       = var.ingress_path
}
