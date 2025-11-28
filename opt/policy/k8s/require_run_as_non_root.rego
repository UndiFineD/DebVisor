package main

# Require runAsNonRoot at container or pod level
violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  spec := input.spec.template.spec
  c := spec.containers[_]
  not has_run_as_non_root(spec, c)
  msg := sprintf("Container must set runAsNonRoot: %s", [c.name])
}

has_run_as_non_root(spec, c) {
  c.securityContext.runAsNonRoot == true
}
has_run_as_non_root(spec, c) {
  spec.securityContext.runAsNonRoot == true
}
