# CAVRA Product Site Deployment

`cavra.mind-ops.cloud` is the commercial product front door for CAVRA. It should
be hosted separately from the GitHub Pages sandbox so the buyer journey is not
mixed with the public demo console.

## Surface Map

| Surface | Role |
| --- | --- |
| `cavra.mind-ops.cloud` | Main commercial product website. |
| `huzefaaa2.github.io/cavra` | Public sandbox, demo console, and docs bridge. |
| GitHub repo | Source, README, installation, developer trust. |
| GitHub Wiki | Technical textbook and deep documentation. |
| `cavra-trial.mind-ops.cloud` | Trial intake and evaluator flow. |
| Private repos | Managed service, entitlement, trial ops, customer/private implementation. |

## Recommended Hosting

Use Azure Static Web Apps or another static hosting service that can deploy the
contents of `apps/product-site` plus `assets/brand`.

The static artifact layout must include:

```text
index.html
styles.css
site.js
video-script.html
assets/brand/*
```

## DNS

Create the DNS record for:

```text
cavra.mind-ops.cloud
```

Point it at the hosting provider target. Do not repoint the existing
`huzefaaa2.github.io/cavra` sandbox or `cavra-trial.mind-ops.cloud` trial
portal.

## Validation

Before publishing, run:

```bash
node --check apps/product-site/site.js
CAVRA_PRODUCT_SITE_URL=http://127.0.0.1:5175/ node scripts/validate-product-site.mjs
```

The validator checks:

- commercial product headline;
- CAVRA Managed and Enterprise Subscription sections;
- Trial Access CTA;
- textbook and Trial Field Guide links;
- runtime decision simulator;
- evidence explorer;
- AISPM cockpit;
- responsive rendering without console errors.

## Launch Checklist

- Product site validates locally.
- Brand assets are copied into the deployed artifact.
- Canonical URL is `https://cavra.mind-ops.cloud/`.
- Trial CTA points to `https://cavra-trial.mind-ops.cloud/`.
- Demo CTA points to `https://huzefaaa2.github.io/cavra/`.
- Textbook CTA points to `https://github.com/Huzefaaa2/cavra/wiki`.
- Contact CTA points to `hello@mind-ops.cloud`.
- Trial portal has been redeployed with `CAVRA Trial Access` copy.
