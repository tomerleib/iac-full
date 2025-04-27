variable "name" {
  description = "Name of the application"
  type        = string
}

variable "image" {
  description = "Docker image for the application"
  type        = string
}

variable "replicas" {
  description = "Number of replicas for the application"
  type        = number
  default     = 2
}

variable "namespace" {
  description = "Kubernetes namespace where the resources will be deployed"
  type        = string
  default     = "default"
}

variable "rbac_enabled" {
  description = "Enable RBAC for the application"
  type        = bool
  default     = false
}
variable "service_account_name" {
  description = "Name of the service account to use for the application"
  type        = string
  default     = "default"
}

variable "ingress_path" {
  description = "Path to the ingress for the application"
  type        = string
  default     = "/"
}

variable "ingress_class_name" {
  description = "The ingress class name to use (e.g., nginx or traefik)"
  type        = string
  default     = "nginx"
}

variable "ingress_annotations" {
  description = "Map of annotations to add to the ingress resource"
  type        = map(string)
  default     = {}
}
