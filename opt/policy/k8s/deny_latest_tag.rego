package main

# Fail if any container image uses the 'latest' tag
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  container := input.spec.template.spec.containers[_]
  endswith(lower(container.image), ":latest")
  msg := sprintf("Container image must not use 'latest': %s", [container.image])
}
