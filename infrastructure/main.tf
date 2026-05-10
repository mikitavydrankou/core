resource "random_id" "suffix" {
  byte_length = 2
}

locals {
  base_name = "${var.name_prefix}-${random_id.suffix.hex}"
  docker_compose = templatefile("${path.module}/docker-compose.yml.tftpl", {
    duckdns_subdomain = var.duckdns_subdomain
    letsencrypt_email = var.letsencrypt_email
    app_dir = "/opt/core/core"
    app_root = "/opt/mctaxi"
    app_port = var.app_port
  })
  startup_script = templatefile("${path.module}/startup.sh.tftpl", {
    backend_repo_url          = var.backend_repo_url
    backend_repo_branch       = var.backend_repo_branch
    backend_repo_ssh_key      = var.backend_repo_ssh_private_key
    backend_repo_ssh_key_path = var.backend_repo_ssh_key_path
    backend_repo_use_ssh_key  = var.backend_repo_use_ssh_key
    app_port                  = var.app_port
    duckdns_subdomain         = var.duckdns_subdomain
    duckdns_token             = var.duckdns_token
    letsencrypt_email         = var.letsencrypt_email
    docker_compose            = local.docker_compose
  })
}

resource "google_compute_network" "vpc" {
  name                    = "${local.base_name}-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${local.base_name}-subnet"
  region        = var.region
  network       = google_compute_network.vpc.id
  ip_cidr_range = "10.20.0.0/24"
}

resource "google_compute_address" "vm_ip" {
  name   = "${local.base_name}-ip"
  region = var.region
}

resource "google_compute_firewall" "allow_ssh" {
  name    = "${local.base_name}-allow-ssh"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = var.allowed_ssh_cidrs
  target_tags   = ["miniapp-server"]
}

resource "google_compute_firewall" "allow_web_and_app" {
  name    = "${local.base_name}-allow-web-app"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443", tostring(var.app_port)]
  }

  source_ranges = var.allowed_app_cidrs
  target_tags   = ["miniapp-server"]
}

resource "google_compute_instance" "miniapp_server" {
  name         = "${local.base_name}-vm"
  machine_type = var.machine_type
  zone         = var.zone
  tags         = ["miniapp-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = var.boot_disk_size_gb
      type  = var.boot_disk_type
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.subnet.id
    access_config {
      nat_ip = google_compute_address.vm_ip.address
    }
  }

  metadata = var.ssh_public_key == "" ? {} : {
    "ssh-keys" = var.ssh_public_key
  }

  metadata_startup_script = local.startup_script
}
