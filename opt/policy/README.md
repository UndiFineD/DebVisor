# Policy (Conftest / OPA)\n\nThis folder provides starter Rego policies for Kubernetes

manifests

validated by Conftest in CI.\nPolicies focus on common reliability and security
checks:\n\n-
Disallow images with the `latest`tag.\n\n- Require CPU and memory resource
requests/limits
on
containers.\n\nPlace additional rules under`policy/k8s/` and they will be picked
up by the
combined
validator workflow.\nReferences:\n\n- Conftest:
\n\n->]([https://www.conftest.dev/>\n\n-]([https://www.conftest.dev/>\n\n]([https://www.conftest.dev/>\n\]([https://www.conftest.dev/>\n]([https://www.conftest.dev/>\]([https://www.conftest.dev/>]([https://www.conftest.dev/]([https://www.conftest.dev]([https://www.conftest.de]([https://www.conftest.d]([https://www.conftest.]([https://www.conftest]([https://www.conftes]([https://www.confte]([https://www.conft]([https://www.conf]([https://www.con]([https://www.co]([https://www.c]([https://www.]([https://www]([https://ww](https://ww)w).)c)o)n)f)t)e)s)t).)d)e)v)/)>)\)n)\)n)-)>)
OPA/Rego:
\n>\n]([https://www.openpolicyagent.org/docs/latest/policy-language/>\n>\]([https://www.openpolicyagent.org/docs/latest/policy-language/>\n>]([https://www.openpolicyagent.org/docs/latest/policy-language/>\n]([https://www.openpolicyagent.org/docs/latest/policy-language/>\]([https://www.openpolicyagent.org/docs/latest/policy-language/>]([https://www.openpolicyagent.org/docs/latest/policy-language/]([https://www.openpolicyagent.org/docs/latest/policy-language]([https://www.openpolicyagent.org/docs/latest/policy-languag]([https://www.openpolicyagent.org/docs/latest/policy-langua]([https://www.openpolicyagent.org/docs/latest/policy-langu]([https://www.openpolicyagent.org/docs/latest/policy-lang]([https://www.openpolicyagent.org/docs/latest/policy-lan]([https://www.openpolicyagent.org/docs/latest/policy-la]([https://www.openpolicyagent.org/docs/latest/policy-l]([https://www.openpolicyagent.org/docs/latest/policy-]([https://www.openpolicyagent.org/docs/latest/policy]([https://www.openpolicyagent.org/docs/latest/polic]([https://www.openpolicyagent.org/docs/latest/poli]([https://www.openpolicyagent.org/docs/latest/pol]([https://www.openpolicyagent.org/docs/latest/po]([https://www.openpolicyagent.org/docs/latest/p]([https://www.openpolicyagent.org/docs/latest/](https://www.openpolicyagent.org/docs/latest/)p)o)l)i)c)y)-)l)a)n)g)u)a)g)e)/)>)\)n)>)\)n)
