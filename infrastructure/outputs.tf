output "server_name" {
  description = "Created VM name"
  value       = google_compute_instance.miniapp_server.name
}

output "server_external_ip" {
  description = "Static external IP of VM"
  value       = google_compute_address.vm_ip.address
}

output "http_url" {
  description = "HTTP URL for quick check"
  value       = "http://${google_compute_address.vm_ip.address}"
}

output "ws_url_example" {
  description = "WebSocket URL example for Telegram Mini App"
  value       = "ws://${google_compute_address.vm_ip.address}:${var.app_port}/ws"
}
