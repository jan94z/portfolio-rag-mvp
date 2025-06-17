resource "digitalocean_firewall" "api_firewall" {
  name = "api-firewall"

  droplet_ids = [digitalocean_droplet.portfolio-rag-mvp-vm.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses =  ["0.0.0.0/0"] # [var.my_ip] 

  }

  # inbound_rule {
  #   protocol         = "tcp"
  #   port_range       = "8000"
  #   source_addresses = [var.my_ip]
  # }

  inbound_rule {
  protocol         = "tcp"
  port_range       = "6333"
  source_addresses = [var.my_ip]
  }

  # inbound_rule {
  # protocol         = "tcp"
  # port_range       = "8501"
  # source_addresses = [var.my_ip]
  # }

  inbound_rule {
  protocol         = "tcp"
  port_range       = "5432"
  source_addresses = [var.my_ip]
  }

  inbound_rule {
  protocol         = "tcp"
  port_range       = "80"
  source_addresses = ["0.0.0.0/0"]
  }

  inbound_rule {
  protocol         = "tcp"
  port_range       = "443"
  source_addresses = ["0.0.0.0/0"]
  }

  outbound_rule {
    protocol         = "tcp"
    port_range       = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
