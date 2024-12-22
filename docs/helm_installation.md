# Helm Installatie Handleiding

Deze handleiding beschrijft hoe je de Presidio-NL API kunt installeren en configureren met Helm in een Kubernetes omgeving.

## Inhoudsopgave
- [Vereisten](#vereisten)
- [Basis Installatie](#basis-installatie)
- [Configuratie Opties](#configuratie-opties)
- [Voorbeelden](#voorbeelden)
- [Troubleshooting](#troubleshooting)

## Vereisten

- Kubernetes cluster (1.16+)
- Helm 3.0+
- Ingress controller (bijv. nginx-ingress)
- (Optioneel) cert-manager voor TLS

## Basis Installatie

1. Voeg de repository toe (indien van toepassing):
```bash
helm repo add presidio-nl https://[your-repo-url]
helm repo update
```

2. Installeer de chart:
```bash
helm install presidio-nl ./charts/presidio-nl
```

## Configuratie Opties

### API Endpoint Configuratie

De belangrijkste configuratie opties voor de API endpoint bevinden zich in de `values.yaml`:

```yaml
ingress:
  enabled: true
  className: "nginx"  # Of een andere ingress controller
  annotations:
    kubernetes.io/ingress.class: nginx
    # cert-manager.io/cluster-issuer: letsencrypt-prod  # Voor SSL
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: presidio-nl-tls
      hosts:
        - api.example.com

app:
  api:
    rootPath: "/api/v1"
    cors:
      enabled: true
      allowOrigins: ["*"]
```

### Verschillende Omgevingen

#### 1. Development (intern gebruik)
```yaml
ingress:
  enabled: true
  hosts:
    - host: presidio-api.dev.internal
      paths:
        - path: /
          pathType: Prefix
  tls: []  # Geen TLS voor interne dev

app:
  debug: true
  api:
    cors:
      enabled: true
      allowOrigins: ["*"]
```

#### 2. Staging (beperkte toegang)
```yaml
ingress:
  enabled: true
  annotations:
    nginx.ingress.kubernetes.io/whitelist-source-range: "10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
  hosts:
    - host: presidio-api.staging.company.nl
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: staging-tls
      hosts:
        - presidio-api.staging.company.nl

app:
  debug: false
  api:
    cors:
      enabled: true
      allowOrigins: ["https://*.company.nl"]
```

#### 3. Production (publieke toegang met SSL)
```yaml
ingress:
  enabled: true
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: api.presidio.company.nl
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: presidio-prod-tls
      hosts:
        - api.presidio.company.nl

app:
  debug: false
  api:
    cors:
      enabled: true
      allowOrigins: ["https://presidio.company.nl"]
```

## Voorbeelden

### 1. Installatie in Development Namespace

```bash
helm install presidio-nl ./charts/presidio-nl \
  --namespace development \
  --create-namespace \
  --values ./values-dev.yaml
```

### 2. Installatie in Production met Custom Domain

```bash
helm install presidio-nl ./charts/presidio-nl \
  --namespace production \
  --create-namespace \
  --set ingress.hosts[0].host=api.mijnbedrijf.nl \
  --set ingress.tls[0].hosts[0]=api.mijnbedrijf.nl \
  --set ingress.tls[0].secretName=mijnbedrijf-tls
```

### 3. ArgoCD Application Voorbeeld

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: presidio-nl
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/presidio-nl.git
    targetRevision: HEAD
    path: charts/presidio-nl
    helm:
      values: |
        ingress:
          enabled: true
          hosts:
            - host: api.presidio.company.nl
              paths:
                - path: /
                  pathType: Prefix
          tls:
            - secretName: presidio-tls
              hosts:
                - api.presidio.company.nl
  destination:
    server: https://kubernetes.default.svc
    namespace: presidio-nl
```

## Troubleshooting

### Veelvoorkomende Problemen

1. **Ingress niet bereikbaar**
   - Controleer of de ingress controller correct is geïnstalleerd
   - Verifieer de ingress configuratie: `kubectl get ingress -n <namespace>`
   - Check de ingress logs: `kubectl logs -n ingress-nginx deploy/ingress-nginx-controller`

2. **TLS/SSL Problemen**
   - Controleer of cert-manager correct is geconfigureerd
   - Verifieer de status van het certificaat: `kubectl get certificate -n <namespace>`
   - Check cert-manager logs: `kubectl logs -n cert-manager deploy/cert-manager`

3. **API niet bereikbaar vanuit andere namespaces**
   - Controleer network policies
   - Verifieer service endpoints: `kubectl get endpoints -n <namespace>`
   - Test connectiviteit vanuit een debug pod 