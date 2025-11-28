package main

# Restrict dangerous Linux capabilities added to containers
DANGEROUS_CAPS := {"NET_ADMIN", "SYS_ADMIN", "SYS_MODULE", "SYS_PTRACE", "SYS_TIME", "SYS_RAWIO"}

violation[{
  "msg": msg,
  "resource": kind
}] {
  kind := input.kind
  kind == "Deployment" or kind == "StatefulSet" or kind == "DaemonSet" or kind == "Job" or kind == "CronJob"
  c := input.spec.template.spec.containers[_]
  caps := c.securityContext.capabilities.add
  cap := caps[_]
  cap_in_set := cap_in_list(cap)
  cap_in_set == true
  msg := sprintf("Disallowed capability added: %s in container %s", [cap, c.name])
}

cap_in_list(cap) {
  DANGEROUS_CAPS[cap]
}
