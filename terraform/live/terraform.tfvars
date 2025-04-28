apps = {
  pod-info-app = {
    image    = "tomerleib/pod-info-app"
    tag      = "pod-info-app_v0.1.3"
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

