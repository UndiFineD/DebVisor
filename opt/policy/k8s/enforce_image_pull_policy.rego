package main

# Enforce imagePullPolicy: Always when using 'latest' tag
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  c := input.spec.template.spec.containers[_]
  endswith(lower(c.image), ":latest")
  not c.imagePullPolicy
  msg := sprintf("imagePullPolicy must be set to Always for latest: %s", [c.name])
}
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  c := input.spec.template.spec.containers[_]
  endswith(lower(c.image), ":latest")
  lower(c.imagePullPolicy) != "always"
  msg := sprintf("imagePullPolicy must be Always when using latest: %s", [c.name])
}
