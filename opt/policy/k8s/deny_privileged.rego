package main

# Disallow privileged containers
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  c := input.spec.template.spec.containers[_]
  c.securityContext.privileged == true
  msg := sprintf("Privileged container not allowed: %s", [c.name])
}
