output "droplet_ip" {
  description = "Public IP address of the deployed droplet"
  value       = digitalocean_droplet.portfolio-rag-mvp-vm.ipv4_address
}