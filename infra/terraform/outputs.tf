output "cluster_id" {
  value = digitalocean_kubernetes_cluster.rag_cluster.id
}

output "endpoint" {
  value = digitalocean_kubernetes_cluster.rag_cluster.endpoint
}

output "kubeconfig" {
  value     = digitalocean_kubernetes_cluster.rag_cluster.kube_config[0].raw_config
  sensitive = true
}