resource "digitalocean_firewall" "rag_api_fw" {
  name = "rag-api-firewall"

  droplet_ids = [digitalocean_droplet.portfolio-rag-mvp-vm.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = [var.your_local_ip]  # For SSH access only from your IP
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "8000"
    source_addresses = ["0.0.0.0/0"]  # You can restrict this to trusted IPs later
  }

  outbound_rule {
    protocol           = "tcp"
    port_range         = "all"
    destination_addresses = ["0.0.0.0/0"]
  }

  outbound_rule {
    protocol           = "udp"
    port_range         = "all"
    destination_addresses = ["0.0.0.0/0"]
  }
}