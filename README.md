# App de Presupuestos Web

Aplicación local para armar presupuestos de páginas web, apps y automatizaciones.

## Cómo usarla

1. Abrí una terminal en esta carpeta.
2. Ejecutá:

```powershell
python server.py
```

3. Entrá en el navegador a:

```text
http://127.0.0.1:8000
```

La base de datos se crea automáticamente en `presupuestos.db`.

## Qué permite hacer

- Guardar clientes y cotizaciones en SQLite.
- Armar presupuestos manualmente desde un catálogo de servicios.
- Armar presupuestos automáticamente según tipo de proyecto, páginas, base de datos, deploy/puesta en marcha, dominio, servidor/hosting, panel de gestión, mantenimiento e integraciones.
- Separar cargos únicos y cargos mensuales.
- Aclarar si el dominio lo compra el cliente, si ya existe o si se gestiona la compra/renovación como costo variable de proveedor.
- Editar cantidades, descripciones y precios.
- Aplicar descuento e IVA.
- Duplicar, cargar y eliminar cotizaciones.
- Exportar a PDF usando el botón `PDF` y la opción `Guardar como PDF` del navegador.
