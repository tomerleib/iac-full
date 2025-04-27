apps = {
  pod-info-app = {
    image    = "tomerleib/pod-info-app"
    tag      = "v0.0.1"
    replicas = 2
  }
  pod-info-monitor = {
    image                = "tomerleib/pod-info-monitor"
    tag                  = "latest"
    replicas             = 1
    rbac_enabled         = true
    service_account_name = "pod-info-monitor"
    ingress_path         = "/app_status"
  }
}

