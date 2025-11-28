package main

# Require both readinessProbe and livenessProbe on all containers
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  c := input.spec.template.spec.containers[_]
  not has_both_probes(c)
  msg := sprintf("Container missing required probes (readiness + liveness): %s", [c.name])
}

has_both_probes(c) {
  c.readinessProbe
  c.livenessProbe
}
