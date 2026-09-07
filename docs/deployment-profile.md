# System Builder – Deploymentprofil

## Syfte

`.system-builder/deployment-profile.yaml` är canonical maskinläsbar källa för strukturerade deploymentval som behöver hållas konsekventa mellan arkitektur, implementation, CI, paketering och dokumentation.

Den ersätter inte:

- `docs/architecture.md`
- `docs/configuration.md`
- `docs/installation.md`
- `docs/operations.md`

utan ger dessa dokument en gemensam strukturerad profil att utgå från.

## Huvudområden

Profilen kan beskriva:

- packaging,
- image registry,
- target platform,
- runtime/statelessness,
- database och deploymentform,
- persistence,
- reverse proxy,
- TLS,
- health checks,
- environment variables,
- CI/publicering,
- deployment trigger.

## Canonical princip

Deploymentprofilen innehåller **val och maskinellt state**, inte fullständig vägledning.

Exempel:

- `deployment-profile.yaml`: `target.platform: coolify`
- `architecture.md`: varför Coolify passar lösningen
- `installation.md`: hur tjänsten installeras i Coolify
- `operations.md`: hur tjänsten drivs och felsöks

## Vanliga profiler

System Builder ska kunna representera minst:

1. local development,
2. Docker standalone,
3. Docker + external PostgreSQL,
4. Coolify + external PostgreSQL,
5. generic container platform,
6. basic Kubernetes.

De konkreta mönstren formaliseras vidare i senare utvecklingssteg.

## Coolify-regler

När `target.platform` är `coolify` gäller som baslinje:

- applikationen paketeras som Docker/OCI,
- PostgreSQL ska vara extern när PostgreSQL används,
- databasen får inte bakas in i app-imagen,
- reverse proxy hanteras av plattformen,
- TLS hanteras av plattformen,
- konfiguration och secrets tillförs externt,
- persistent volume används endast när applikationen faktiskt behöver persistent filstorage,
- health endpoint ska finnas när tjänsten kan stödja det.

## Databas

`database.type` och `database.deployment` hålls separata.

Exempel:

```yaml
database:
  type: postgresql
  deployment: external
```

Detta gör att samma applikation kan köras mot exempelvis:

- lokal Docker Compose-databas,
- Coolify database service,
- managed PostgreSQL,
- annan extern PostgreSQL.

## Statelessness

`runtime.stateless: true` betyder att applikationens instanser ska kunna ersättas utan att lokalt applikationsstate går förlorat.

En profil som samtidigt anger app-managed persistent files i lokal volume betraktas som inkonsekvent tills designen förtydligats.

## Health

När health checks är aktiverade ska minst en liveness/readiness/startup-endpoint definieras.

System Builder ska senare kunna använda detta för:

- Docker HEALTHCHECK,
- Coolify health checks,
- Kubernetes probes,
- operations documentation.

## Validering

Canonical profil:

```bash
python scripts/validate_deployment_profile.py \
  --file .system-builder/deployment-profile.yaml \
  --schema schemas/deployment-profile.schema.json
```

Exempel:

```bash
python scripts/validate_deployment_profile.py \
  --file examples/deployment-profile.coolify.example.yaml \
  --schema schemas/deployment-profile.schema.json
```

Negativ fixture:

```bash
python scripts/validate_deployment_profile.py \
  --file examples/deployment-profile.invalid.yaml \
  --schema schemas/deployment-profile.schema.json \
  --expect-invalid
```

## Small-project-regel

Deploymentprofilen behöver inte skapas för ett rent bibliotek eller projekt utan deploymentbehov.

För en körbar tjänst bör den däremot skapas så snart deploymentvalet materiellt påverkar:

- arkitektur,
- databas,
- filstorage,
- containerisering,
- CI,
- installation eller drift.
