---
name: k3s-cluster-ops
description: Install, configure, upgrade, back up, and troubleshoot K3s lightweight Kubernetes clusters, including joining nodes, ingress, storage, and registries. Use when working on a K3s cluster, a home lab or edge Kubernetes setup, or when a K3s node or workload will not start.
---

# K3s Cluster Operations

## When to use

- Standing up a new single-node or multi-node K3s cluster.
- Joining or removing nodes, upgrading K3s, or taking and restoring backups.
- A K3s service, node, or workload is unhealthy and needs diagnosing.
- Do NOT use for general Kubernetes questions that are not specific to K3s defaults and tooling.

## Key facts

- K3s runs as the `k3s` systemd unit on servers and `k3s-agent` on agents. Logs: `journalctl -u k3s` (or `-u k3s-agent`).
- The admin kubeconfig is `/etc/rancher/k3s/k3s.yaml`. Copy it elsewhere and change the server address from `127.0.0.1` to the node's address before using it remotely.
- The join token is at `/var/lib/rancher/k3s/server/node-token`. Agents join with `K3S_URL` and `K3S_TOKEN` set at install time.
- Defaults bundle Traefik (ingress), ServiceLB (load balancer), CoreDNS, metrics-server, and the local-path storage provisioner. Disable any of them with `--disable` flags when you bring your own.
- Manifests dropped into `/var/lib/rancher/k3s/server/manifests/` are applied automatically.
- Private registry mirrors and credentials go in `/etc/rancher/k3s/registries.yaml`; restart the service after editing.
- Configuration can live in `/etc/rancher/k3s/config.yaml` instead of long command-line flags, which keeps installs reproducible.

## Steps

1. Pick the datastore. A single server uses embedded SQLite by default. For high availability use embedded etcd by starting the first server with `--cluster-init` and joining further servers (an odd number, three or more) with the same token.
2. Install with the official script, pinning the version with `INSTALL_K3S_VERSION` so nodes do not drift.
3. Verify with `kubectl get nodes -o wide` and `kubectl get pods -A`. Every system pod should reach Running before deploying workloads.
4. Upgrade servers one at a time, then agents, by re-running the install script with the new pinned version, or use the system-upgrade-controller for rolling upgrades. Do not skip minor versions.
5. Back up before any upgrade. With embedded etcd use `k3s etcd-snapshot save`, and copy snapshots off the node; scheduled snapshots are configured through `etcd-snapshot-schedule-cron` and `etcd-snapshot-retention`. With SQLite, copy the datastore files under `/var/lib/rancher/k3s/server/db/` while the service is stopped.
6. To remove a node, drain it with `kubectl drain`, delete it with `kubectl delete node`, then run `k3s-uninstall.sh` (server) or `k3s-agent-uninstall.sh` (agent) on the machine.

## Troubleshooting

- **Node NotReady:** check `systemctl status k3s-agent`, then the journal for certificate, clock, or connectivity errors. Confirm the agent can reach port 6443 on the server.
- **Pods stuck Pending:** `kubectl describe pod` and read events; the usual causes are insufficient resources, taints, or an unbound PVC.
- **Image pull failures:** check `registries.yaml`, DNS from the node, and registry credentials.
- **Ingress not responding:** confirm Traefik pods are running and the Ingress class matches, and check that nothing else already binds ports 80 and 443 on the node.
- **Time skew:** clock drift breaks certificate validation; make sure NTP is running on every node.
- Firewall rules must allow 6443 (API), 8472/udp (flannel VXLAN), and 10250 (kubelet) between nodes.

## Output

The commands or config to apply, the expected result of each, and any rollback step. Flag every step that restarts the cluster or loses data.

## Notes

- Treat the node token and kubeconfig as secrets; never commit them.
- Prefer config files and pinned versions over ad hoc flags so a rebuilt node matches the others.
