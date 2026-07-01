# CAVRA Product Site

This static site is the source for the commercial CAVRA product front door:

```text
https://cavra.mind-ops.cloud
```

It is intentionally separate from `apps/sandbox-ui`, which remains the public
demo console and documentation bridge at `https://huzefaaa2.github.io/cavra/`.

## Role

- Explain CAVRA as the runtime authority layer for AI agents.
- Present CAVRA Community, CAVRA Managed, Enterprise Subscription, and Trial
  Access as the product paths.
- Showcase the runtime decision simulator, evidence explorer, AISPM cockpit,
  Managed operating model, Enterprise Subscription packages, Trust Center
  preview, and buyer resources.
- Link to the GitHub Wiki textbook, Trial Field Guide, public sandbox, GitHub
  repo, and trial portal.

## Local Preview

From the repository root:

```bash
rm -rf /tmp/cavra-product-site
mkdir -p /tmp/cavra-product-site/assets
cp -R apps/product-site/. /tmp/cavra-product-site/
cp -R assets/brand /tmp/cavra-product-site/assets/
python3 -m http.server 5175 --directory /tmp/cavra-product-site
```

In another terminal, validate:

```bash
CAVRA_PRODUCT_SITE_URL=http://127.0.0.1:5175/ node scripts/validate-product-site.mjs
```
