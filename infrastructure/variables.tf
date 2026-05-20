variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "europe-west1-b"
}

variable "name_prefix" {
  description = "Prefix for created resources"
  type        = string
  default     = "mctaxi-miniapp"
}

variable "machine_type" {
  description = "GCE instance machine type"
  type        = string
  default     = "e2-small"
}

variable "boot_disk_size_gb" {
  description = "Boot disk size in GB"
  type        = number
  default     = 20
}

variable "boot_disk_type" {
  description = "Boot disk type"
  type        = string
  default     = "pd-standard"
}

variable "ssh_public_key" {
  description = "Optional SSH public key content (e.g. 'user:ssh-ed25519 AAAA...')"
  type        = string
  default     = ""
}

variable "app_user" {
  description = "Linux user that owns and runs the app in their home directory"
  type        = string
  default     = "debian"
}

variable "allowed_ssh_cidrs" {
  description = "CIDRs allowed for SSH access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "allowed_app_cidrs" {
  description = "CIDRs allowed for HTTP/HTTPS and app port"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "app_port" {
  description = "App port for backend websocket/http"
  type        = number
  default     = 8000
}

variable "backend_repo_url" {
  description = "Git repository URL for the core backend"
  type        = string
  default     = ""
}

variable "backend_repo_ssh_private_key" {
  description = "SSH private key that has read access to the private backend repo"
  type        = string
  default     = ""
  sensitive   = true
}

variable "backend_repo_use_ssh_key" {
  description = "Set to true if you will provision an SSH private key on the VM at backend_repo_ssh_key_path (not recommended to put key in TF vars)."
  type        = bool
  default     = false
}

variable "backend_repo_ssh_key_path" {
  description = "Path where the SSH private key should be written on the VM"
  type        = string
  default     = "/root/.ssh/id_ed25519"
}

variable "backend_repo_branch" {
  description = "Git branch to deploy for the core backend"
  type        = string
  default     = "main"
}

variable "duckdns_subdomain" {
  description = "DuckDNS subdomain (without .duckdns.org). Leave empty to disable DuckDNS setup."
  type        = string
  default     = ""
}

variable "duckdns_token" {
  description = "DuckDNS token for updating dynamic DNS. Leave empty to disable DuckDNS setup."
  type        = string
  default     = ""
  sensitive   = true
}

variable "letsencrypt_email" {
  description = "Email for Let's Encrypt registration (used by Traefik)."
  type        = string
  default     = ""
}
