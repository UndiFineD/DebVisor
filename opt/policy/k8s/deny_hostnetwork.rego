package main

# Disallow use of hostNetwork for pods
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  spec := input.spec.template.spec
  spec.hostNetwork == true
  msg := "hostNetwork is not allowed"
}
