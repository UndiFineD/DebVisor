package main

# Require readinessProbe on all containers
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  container := input.spec.template.spec.containers[_]
  not container.readinessProbe
  msg := sprintf("Container missing readinessProbe: %s", [container.name])
}
