# Open-Core Security Model

The Community repository is public and must be treated as untrusted for secrets
or proprietary material. Public code can define interfaces, but private
implementation and commercial entitlement checks must be external.

## Public Controls

- boundary validation scans public source paths for risky private terms;
- Enterprise source is represented by dynamic imports only;
- license validation is a local placeholder only;
- trial validation delegates real checks to future private services;
- connector evidence redacts credentials.

## Private Controls

Enterprise repositories should enforce:

- branch protection and required review;
- CodeQL and dependency scanning;
- secret scanning and push protection;
- signed release provenance;
- license service signing keys in KMS or HSM;
- customer data isolation.
