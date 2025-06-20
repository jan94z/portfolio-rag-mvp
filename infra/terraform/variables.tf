variable "droplet_name" {
  description = "Name of the droplet to point the domain to"
  type        = string
}

variable "do_token" {
  description = "DigitalOcean access token"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "DigitalOcean region"
  type        = string
  default     = "fra1"
}

variable "droplet_size" {
  description = "Droplet size"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "image" {
  description = "Droplet base image"
  type        = string
  default     = "ubuntu-22-04-x64"
}

variable "ssh_key_fingerprint" {
  description = "SSH key fingerprint"
  type        = string
}

variable "my_ip" {
  type        = string
  description = "Your current public IP to allow SSH access"
}


