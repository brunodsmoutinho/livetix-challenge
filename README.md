# LiveTix - System Design Challenge

Diseno de arquitectura para una plataforma global de venta de boletos
para eventos en vivo, operando en 4 paises sobre 3 continentes.

**Autor:** Bruno Moutinho
**Rol:** Cloud Engineer Senior
**Fecha:** Octubre 2025
**Nube elegida:** AWS

---

## Contenido del entregable

### Documento unificado (recomendado)
- documentos/LiveTix-Entrega.pdf - Documento completo con capa,
  decisiones arquitectonicas, IaC y diagrama embutido.

### Documentos por separado
- documentos/01-decisiones.md - Documento de decisiones arquitectonicas
- documentos/02-iac.md - Infraestructura como Codigo (conceptual)

### Diagramas
- diagramas/LiveTix-Arquitectura.png - Diagrama principal (imagen)
- diagramas/LiveTix-Arquitectura.svg - Vectorial
- diagramas/LiveTix-Arquitectura.pdf - PDF del diagrama
- diagramas/LiveTix-Arquitectura.drawio - Fuente editable (draw.io)

### Fuentes (codigo)
- fuentes/generate_diagram.py - Script Python que genera el .drawio
- fuentes/build_pdf.py - Script Python que genera el PDF unificado

---

## Resumen ejecutivo

LiveTix debe soportar picos de 10-20x en segundos sin vender el mismo
asiento dos veces y sin cobrar sin entregar boleto.

Decisiones clave:

| Decision | Eleccion | Tradeoff |
|---|---|---|
| Nube | AWS | Vendor lock-in |
| Regiones | 3 (us-east-1, eu-west-1, sa-east-1) | Costo 3x |
| Computo | Fargate + Lambda (serverless gestionado) | Menos control que K8s |
| Inventario | Aurora PG con conditional writes | Escala vertical limitada |
| Consistencia pago | Saga + Outbox + Reconciliador | Latencia +1-2s |
| Picos | Sala de espera + SQS FIFO | Friccion al usuario |

---

## Como regenerar los artefactos

### Regenerar el diagrama

    cd fuentes/
    python3 generate_diagram.py

Esto genera LiveTix-Arquitectura.drawio.

### Regenerar el PDF unificado

    cd fuentes/
    python3 build_pdf.py

Requiere markdown y weasyprint:

    pip install markdown weasyprint

---

## Contacto

Bruno Moutinho
