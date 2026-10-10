# Infraestructura como Código (Conceptual)

## 1. Estructura de carpetas

    livetix-infra/
    ├── modules/                    # Módulos reutilizables
    │   ├── network/                # VPC, subnets, security groups
    │   ├── database/               # Aurora, DynamoDB
    │   ├── compute/                # ECS service, Lambda
    │   ├── queue/                  # SQS, SNS
    │   └── observability/          # CloudWatch, alarms
    ├── environments/
    │   ├── dev/
    │   ├── staging/
    │   └── prod/
    │       ├── us-east-1/
    │       ├── eu-west-1/
    │       └── sa-east-1/
    ├── global/                     # Route 53, CloudFront, IAM
    └── .github/
        └── workflows/
            ├── plan.yml
            └── apply.yml

## 2. Módulos: por qué y cómo

Cada módulo encapsula un recurso repetible. Ejemplo:

    # modules/compute/main.tf
    variable "service_name" { type = string }
    variable "region"       { type = string }
    variable "cpu"          { default = 512 }
    variable "memory"       { default = 1024 }

    resource "aws_ecs_service" "this" {
      name            = var.service_name
      cluster         = aws_ecs_cluster.this.id
      task_definition = aws_ecs_task_definition.this.arn
      desired_count   = 2
      launch_type     = "FARGATE"

      network_configuration {
        subnets         = var.private_subnets
        security_groups = [var.sg_id]
      }
    }

Uso en `environments/prod/us-east-1/main.tf`:

    module "checkout_service" {
      source       = "../../../modules/compute"
      service_name = "checkout"
      region       = "us-east-1"
      cpu          = 1024
      memory       = 2048
    }

## 3. Ambientes y versionado

- **dev:** un desarrollador, datos sintéticos, se puede romper.
- **staging:** espejo de prod con 10% de capacidad.
- **prod:** multi-región, datos reales, cambios con aprobación.

**Versionado:**

- Código en Git (monorepo).
- Estado de Terraform en S3 + DynamoDB lock (uno por ambiente).
- Tags en Git: `v1.2.3` → despliegue a prod.
- Módulos versionados con tags.

## 4. Secretos y credenciales

- **AWS Secrets Manager** para API keys de Stripe, DB passwords.
- **IAM Roles** para que los servicios accedan sin credenciales estáticas.
- **Nunca** secretos en el repo. `terraform.tfvars` va en `.gitignore`.
- Rotación automática de secretos cada 90 días.
- En CI/CD, usar **OIDC** para que GitHub Actions asuma rol de AWS sin access keys.

    resource "aws_secretsmanager_secret" "stripe_key" {
      name = "livetix/prod/stripe/api_key"
    }

    resource "aws_secretsmanager_secret_version" "stripe_key" {
      secret_id     = aws_secretsmanager_secret.stripe_key.id
      secret_string = var.stripe_api_key
    }

## 5. Pipeline CI/CD

    # .github/workflows/deploy.yml
    name: Deploy LiveTix

    on:
      push:
        branches: [main]
        paths: ['environments/prod/**']

    jobs:
      plan:
        runs-on: ubuntu-latest
        permissions:
          id-token: write
          contents: read
        steps:
          - uses: actions/checkout@v4
          - name: Configure AWS credentials (OIDC)
            uses: aws-actions/configure-aws-credentials@v4
            with:
              role-to-assume: arn:aws:iam::123456789:role/GitHubActionsDeploy
              aws-region: us-east-1
          - name: Terraform Init
            run: terraform -chdir=environments/prod/us-east-1 init
          - name: Terraform Plan
            run: terraform -chdir=environments/prod/us-east-1 plan -out=tfplan
          - name: Upload plan
            uses: actions/upload-artifact@v4
            with:
              name: tfplan
              path: environments/prod/us-east-1/tfplan

      apply:
        needs: plan
        runs-on: ubuntu-latest
        environment: production
        steps:
          - uses: actions/checkout@v4
          - name: Configure AWS credentials (OIDC)
            uses: aws-actions/configure-aws-credentials@v4
            with:
              role-to-assume: arn:aws:iam::123456789:role/GitHubActionsDeploy
              aws-region: us-east-1
          - uses: actions/download-artifact@v4
            with:
              name: tfplan
          - name: Terraform Apply
            run: terraform -chdir=environments/prod/us-east-1 apply -auto-approve tfplan

**Estrategia de despliegue:**

- **Blue/Green** en ECS: nueva versión al 5% de tráfico (canary), si métricas OK se cambia al 100%.
- **Rollback automático** si `error_rate > 1%` en 5 min.

## 6. Tradeoffs

- **Monorepo vs multi-repo:** elegí monorepo por simplicidad para 5 ingenieros. Multi-repo sería mejor si creciera a 20+.
- **Terraform vs CDK:** elegí Terraform por ser agnóstico y tener mejor ecosistema. CDK es más expresivo pero acopla a AWS.
- **Estado remoto en S3:** obligatorio para trabajo en equipo. Tradeoff: requiere bootstrap inicial (S3 + DynamoDB lock).
