resource "digitalocean_firewall" "api_firewall" {
  name = "api-firewall"

  droplet_ids = [digitalocean_droplet.portfolio-rag-mvp-vm.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = [var.my_ip]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "8000"
    source_addresses = [var.my_ip]
  }

  inbound_rule {
  protocol         = "tcp"
  port_range       = "6333"
  source_addresses = [var.my_ip]
}

  outbound_rule {
    protocol         = "tcp"
    port_range       = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
