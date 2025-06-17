terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.55.0"
    }
  }

  required_version = ">= 1.4.0"
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "portfolio-rag-mvp-vm" {
  name       = var.droplet_name
  region     = var.region
  size       = var.droplet_size
  image      = var.image
  ssh_keys   = [var.ssh_key_fingerprint]
  monitoring = true
  backups    = false
  tags       = ["portfolio", "rag", "vm"]
  #user_data = file("${path.module}/cloud-init.sh")
}