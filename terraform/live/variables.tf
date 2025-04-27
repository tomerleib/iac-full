variable "apps" {
  description = "Map of applications to deploy"
  type = map(object({
    image                = string
    tag                  = string
    replicas             = optional(number, 2)
    namespace            = optional(string, "default")
    rbac_enabled         = optional(bool, false)
    service_account_name = optional(string, "default")
    ingress_path         = optional(string, "/")
  }))
}
