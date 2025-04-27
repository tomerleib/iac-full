resource "kubernetes_deployment" "app" {
  metadata {
    name = var.name
    labels = {
      app = var.name
    }
  }

  spec {
    replicas = var.replicas


    selector {
      match_labels = {
        app = var.name
      }
    }

    template {
      metadata {
        labels = {
          app = var.name
        }
      }

      spec {
        service_account_name = var.rbac_enabled ? var.service_account_name : "default"
        container {
          name              = var.name
          image             = var.image
          image_pull_policy = "Always"

          port {
            container_port = 8080
          }

          env {
            name = "POD_NAME"
            value_from {
              field_ref {
                field_path = "metadata.name"
              }
            }
          }

          env {
            name = "POD_IP"
            value_from {
              field_ref {
                field_path = "status.podIP"
              }
            }
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 8080
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/health"
              port = 8080
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app" {
  metadata {
    name = var.name
  }

  spec {
    selector = {
      app = var.name
    }

    port {
      port        = 80
      target_port = 8080
    }
  }
}

resource "kubernetes_ingress_v1" "app" {
  metadata {
    name = var.name
  }

  spec {

    rule {
      http {
        path {
          path      = var.ingress_path
          path_type = "Prefix"

          backend {
            service {
              name = kubernetes_service.app.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}


resource "kubernetes_service_account" "app" {
  count = var.rbac_enabled ? 1 : 0

  metadata {
    name      = var.service_account_name
    namespace = var.namespace
  }
}

resource "kubernetes_role" "app" {
  count = var.rbac_enabled ? 1 : 0

  metadata {
    name      = var.service_account_name
    namespace = var.namespace
  }

  rule {
    api_groups = ["apps"]
    resources  = ["deployments"]
    verbs      = ["get", "list"]
  }

  rule {
    api_groups = [""]
    resources  = ["pods"]
    verbs      = ["get", "list"]
  }
}

resource "kubernetes_role_binding" "app" {
  count = var.rbac_enabled ? 1 : 0

  metadata {
    name      = var.service_account_name
    namespace = var.namespace
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role.app[0].metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.app[0].metadata[0].name
    namespace = var.namespace
  }
}
