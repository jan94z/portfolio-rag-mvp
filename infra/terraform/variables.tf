variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "DigitalOcean region for the cluster"
  type        = string
  default     = "fra1"
}

variable "cluster_name" {
  description = "Name of the Kubernetes cluster"
  type        = string
  default     = "rag-k8s-cluster"
}

variable "node_size" {
  description = "Droplet size for cluster nodes"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "node_count" {
  description = "Number of nodes in the pool"
  type        = number
  default     = 1
}

variable "k8s_version" {
  description = "DOKS version (see DO docs for available versions)"
  type        = string
  default     = "1.32.2-do.3"
}
