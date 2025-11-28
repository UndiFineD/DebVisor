package main

# Require CPU and memory requests/limits on all containers
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  container := input.spec.template.spec.containers[_]
  not has_resources(container)
  msg := sprintf("Container missing resource requests/limits: %s", [container.name])
}

has_resources(c) {
  c.resources.requests.cpu
  c.resources.requests.memory
  c.resources.limits.cpu
  c.resources.limits.memory
}
