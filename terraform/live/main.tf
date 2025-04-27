provider "kubernetes" {

}

module "apps" {
  for_each = var.apps

  source = "../modules/apps"

  name      = each.key
  image     = "${each.value.image}:${each.value.tag}"
  namespace = each.value.namespace
  replicas  = each.value.replicas
  rbac_enabled = each.value.rbac_enabled
  service_account_name = each.value.service_account_name
  ingress_path = try(each.value.ingress_path, "/")
}
