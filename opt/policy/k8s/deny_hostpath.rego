package main

# Disallow hostPath volumes
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  vol := input.spec.template.spec.volumes[_]
  vol.hostPath
  msg := sprintf("hostPath volumes are not allowed: %v", [vol])
}
