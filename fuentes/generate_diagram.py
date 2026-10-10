#!/usr/bin/env python3
"""Genera LiveTix-Arquitectura.drawio (version final, sin lineas cruzadas)"""

from xml.dom import minidom

PAGE_WIDTH = 2600
PAGE_HEIGHT = 2000

COLOR_GLOBAL_FILL = "#DAE8FC"
COLOR_GLOBAL_STROKE = "#6C8EBF"
COLOR_US_FILL = "#D5E8D4"
COLOR_US_STROKE = "#82B366"
COLOR_EU_FILL = "#FFF2CC"
COLOR_EU_STROKE = "#D6B656"
COLOR_SA_FILL = "#FFE6CC"
COLOR_SA_STROKE = "#D79B00"

_counter = [0]


def new_id():
    _counter[0] += 1
    return f"cell_{_counter[0]}"


def box(cells, x, y, w, h, label, fill, stroke, dashed=True,
        font_size=14, font_style=1):
    cid = new_id()
    style = (
        f"rounded=0;whiteSpace=wrap;html=1;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth=2;"
        f"{'dashed=1;dashPattern=8 8;' if dashed else ''}"
        f"verticalAlign=top;align=left;spacingTop=10;spacingLeft=15;"
        f"fontSize={font_size};fontStyle={font_style};fontColor=#333333;"
    )
    cells.append(
        f'<mxCell id="{cid}" value="{label}" style="{style}" '
        f'vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
        f'</mxCell>'
    )
    return cid


def aws_icon(cells, x, y, w, h, label, shape):
    cid = new_id()
    style = (
        f"sketch=0;outlineConnect=0;fontColor=#232F3E;"
        f"gradientColor=none;fillColor=#232F3E;strokeColor=none;"
        f"dashed=0;verticalLabelPosition=bottom;verticalAlign=top;"
        f"align=center;html=1;fontSize=11;fontStyle=0;"
        f"aspect=fixed;shape=mxgraph.aws4.{shape};"
    )
    cells.append(
        f'<mxCell id="{cid}" value="{label}" style="{style}" '
        f'vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
        f'</mxCell>'
    )
    return cid


def generic_icon(cells, x, y, w, h, label, fill="#FFFFFF", stroke="#000000",
                 shape="ellipse", font_size=12):
    cid = new_id()
    style = (
        f"{shape};whiteSpace=wrap;html=1;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth=2;"
        f"fontSize={font_size};fontStyle=1;"
    )
    cells.append(
        f'<mxCell id="{cid}" value="{label}" style="{style}" '
        f'vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
        f'</mxCell>'
    )
    return cid


def text(cells, x, y, w, h, label, font_size=14, font_style=1,
         align="left", color="#000000"):
    cid = new_id()
    style = (
        f"text;html=1;strokeColor=none;fillColor=none;"
        f"align={align};verticalAlign=middle;whiteSpace=wrap;rounded=0;"
        f"fontSize={font_size};fontStyle={font_style};fontColor={color};"
    )
    cells.append(
        f'<mxCell id="{cid}" value="{label}" style="{style}" '
        f'vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
        f'</mxCell>'
    )
    return cid


def edge(cells, source, target, label="", dashed=False, color="#000000",
         width=2, exit_x=None, exit_y=None, entry_x=None, entry_y=None,
         curved=False):
    cid = new_id()
    base_style = (
        f"rounded=0;html=1;"
        f"strokeColor={color};strokeWidth={width};"
        f"fontSize=9;fontColor=#333333;"
        f"{'dashed=1;dashPattern=6 4;' if dashed else ''}"
    )
    if curved:
        style = base_style + "edgeStyle=orthogonalEdgeStyle;curved=1;"
    else:
        style = base_style + "edgeStyle=orthogonalEdgeStyle;jettySize=auto;orthogonalLoop=1;"
    if exit_x is not None:
        style += f"exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;"
    if entry_x is not None:
        style += f"entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;"
    cells.append(
        f'<mxCell id="{cid}" value="{label}" style="{style}" '
        f'edge="1" parent="1" source="{source}" target="{target}">'
        f'<mxGeometry relative="1" as="geometry"/>'
        f'</mxCell>'
    )
    return cid


def build():
    cells = []
    background_cells = []

    text(cells, 60, 20, 1600, 50,
         "LiveTix - Arquitectura Global",
         font_size=24, font_style=1, color="#0B3D91")
    text(cells, 60, 70, 1600, 30,
         "Autor: Bruno Moutinho  |  Nube: AWS  |  3 regiones",
         font_size=12, font_style=0, color="#555555")

    gx, gy, gw, gh = 60, 130, 2280, 260
    box(background_cells, gx, gy, gw, gh,
        "PLANO GLOBAL (una sola vez en el mundo)",
        COLOR_GLOBAL_FILL, COLOR_GLOBAL_STROKE, dashed=True, font_size=16)

    region_y = gy + gh + 60
    region_h = 900
    region_w = 680
    gap = 40

    region_specs = [
        ("REGION us-east-1", COLOR_US_FILL, COLOR_US_STROKE),
        ("REGION eu-west-1", COLOR_EU_FILL, COLOR_EU_STROKE),
        ("REGION sa-east-1", COLOR_SA_FILL, COLOR_SA_STROKE),
    ]

    region_positions = []
    for i, (name, fill, stroke) in enumerate(region_specs):
        rx = gx + i * (region_w + gap)
        box(background_cells, rx, region_y, region_w, region_h,
            name, fill, stroke, dashed=True, font_size=15)
        region_positions.append((rx, region_y))

    icon_y = gy + 70
    icon_size = 78

    aws_icon(cells, gx + 80, icon_y, icon_size, icon_size,
             "Route 53", "route_53")
    aws_icon(cells, gx + 280, icon_y, icon_size, icon_size,
             "WAF + Shield", "waf")
    cdn = aws_icon(cells, gx + 480, icon_y, icon_size, icon_size,
                   "CloudFront", "cloudfront")
    aws_icon(cells, gx + 680, icon_y, icon_size, icon_size,
             "Cognito", "cognito")
    catalog = aws_icon(cells, gx + 880, icon_y, icon_size, icon_size,
                       "DynamoDB Global", "dynamodb")

    def build_region(rx, ry):
        s = 60
        c1 = rx + 40
        api = aws_icon(cells, c1, ry + 90, s, s, "API Gateway", "api_gateway")
        aws_icon(cells, c1, ry + 230, s, s, "ALB", "elastic_load_balancing")

        c2 = rx + 240
        checkout = aws_icon(cells, c2, ry + 90, s, s, "Checkout", "fargate")
        inventory = aws_icon(cells, c2, ry + 230, s, s, "Inventario", "fargate")
        payment_w = aws_icon(cells, c2, ry + 380, s, s, "Payment Worker", "fargate")
        issue_w = aws_icon(cells, c2, ry + 530, s, s, "Ticket Issue", "fargate")
        reconciler = aws_icon(cells, c2, ry + 760, s, s, "Reconciliador", "lambda")

        c3 = rx + 460
        orders_db = aws_icon(cells, c3, ry + 90, s, s, "Orders DB", "aurora")
        inv_db = aws_icon(cells, c3, ry + 230, s, s, "Inventario DB", "dynamodb")
        queue = aws_icon(cells, c3, ry + 380, s, s, "SQS FIFO", "sqs")
        outbox = aws_icon(cells, c3, ry + 530, s, s, "Outbox", "dynamodb")
        sns = aws_icon(cells, c3, ry + 680, s, s, "SNS", "sns")
        aws_icon(cells, c3, ry + 820, s, s, "Boletos S3", "s3")

        aws_icon(cells, c1, ry + 760, s, s, "Secrets", "secrets_manager")
        aws_icon(cells, c1, ry + 860, s, s, "CloudWatch", "cloudwatch")

        edge(cells, api, checkout, "")
        edge(cells, checkout, inventory, "", color="#B85450")
        edge(cells, inventory, inv_db, "", color="#B85450")
        edge(cells, checkout, orders_db, "")
        edge(cells, checkout, queue, "")
        edge(cells, queue, payment_w, "")
        edge(cells, payment_w, orders_db, "", color="#82B366")
        edge(cells, payment_w, outbox, "")
        edge(cells, outbox, sns, "")
        edge(cells, sns, issue_w, "")
        edge(cells, issue_w, orders_db, "", color="#82B366")
        edge(cells, reconciler, orders_db, "",
             dashed=True, color="#D79B00")

        return {"api": api, "payment_w": payment_w}

    comps_list = []
    for rx, ry in region_positions:
        comps_list.append(build_region(rx, ry))

    # Global -> regiones
    for comps in comps_list:
        edge(cells, cdn, comps["api"], "tráfico", dashed=True, color="#6C8EBF",
             exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0)
        edge(cells, catalog, comps["api"], "réplica catálogo",
             dashed=True, color="#6C8EBF", width=1,
             exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0)

    # Stripe: una elipse por region, justo debajo de cada una
    stripe_y = region_y + region_h + 60
    for i, comps in enumerate(comps_list):
        rx = region_positions[i][0]
        stripe = generic_icon(cells, rx + 220, stripe_y, 240, 90,
                              "Stripe / PayPal",
                              fill="#F5F5F5", stroke="#666666",
                              shape="ellipse", font_size=13)
        edge(cells, comps["payment_w"], stripe, "pago",
             dashed=True, color="#B85450", curved=True,
             exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0)

    # Leyenda a la derecha, alineada con Stripe
    legend_x = gx + 2100
    legend_y = region_y
    box(cells, legend_x, legend_y, 440, 240,
        "LEYENDA", "#FFFFFF", "#333333", dashed=False, font_size=14)
    items = [
        "Azul: Plano Global",
        "Colores: Regiones",
        "Seta solida: flujo critico",
        "Seta tracejada: asincrono",
        "Orders/Inventario: ACID",
        "Catalogo/Boletos: eventual",
    ]
    for i, t in enumerate(items):
        text(cells, legend_x + 15, legend_y + 50 + i * 28,
             410, 25, t, font_size=11, font_style=0, align="left")

    all_cells = background_cells + cells

    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<mxfile host="app.diagrams.net">',
        '  <diagram name="LiveTix" id="p1">',
        f'    <mxGraphModel pageWidth="{PAGE_WIDTH}" pageHeight="{PAGE_HEIGHT}" '
        f'grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
        f'arrows="1" fold="1" page="1" pageScale="1" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>',
    ]
    xml_parts.extend(all_cells)
    xml_parts.extend([
        '      </root>',
        '    </mxGraphModel>',
        '  </diagram>',
        '</mxfile>',
    ])

    xml_str = "\n".join(xml_parts)
    parsed = minidom.parseString(xml_str)
    pretty = parsed.toprettyxml(indent="  ", encoding="UTF-8").decode("utf-8")
    lines = [l for l in pretty.split("\n") if not l.startswith("<?xml")]
    final = '<?xml version="1.0" encoding="UTF-8"?>\n' + "\n".join(lines)

    with open("LiveTix-Arquitectura.drawio", "w", encoding="utf-8") as f:
        f.write(final)

    print("OK: LiveTix-Arquitectura.drawio")
    print(f"Celdas: {_counter[0]}")
    print(f"Bytes: {len(final)}")


if __name__ == "__main__":
    build()
