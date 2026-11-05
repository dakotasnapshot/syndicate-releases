# Syndicate Releases

Maintained personally by [Dakota Cole (@dakotasnapshot)](https://github.com/dakotasnapshot).

Official downloadable Syndicate packages are hosted as [GitHub Release assets](https://github.com/dakotasnapshot/syndicate-releases/releases). The product/download front end remains [synmessenger.com](https://synmessenger.com/downloads/).

- `desktop-vVERSION`: desktop installers and native updater packages.
- `loader-vVERSION`: Syndicate Loader for macOS.
- `ios-VERSION-buildBUILD`: iPhone/iPad IPA packages.

Each release includes `SHA256SUMS.txt` and `release-manifest.json` with artifact filenames, sizes, SHA-256 digests and recorded source/build provenance. Assets are versioned: never replace published bytes. Publish a new version for changed contents. Existing Apple signatures/notarization and signed desktop update metadata remain authoritative; moving a file does not sign or notarize it. Windows previews remain unsigned unless a release explicitly states otherwise.

## Sources and licensing

- [Desktop / web source](https://github.com/dakotasnapshot/syn-messenger-desktop)
- [iOS / Watch source](https://github.com/dakotasnapshot/syn-messenger-ios)
- [Android source](https://github.com/dakotasnapshot/syn-messenger-android)
- Source/build provenance recorded in release manifests where verified. Historical entries without verified provenance are identified as such, never presented as newly reproducible or attested builds.
- Syndicate is an independent Matrix client based on Element. Upstream copyright/license notices remain with corresponding source and packages; applicable AGPL/GPL source obligations are unchanged.

Release tags identify delivery records, not application source commits; consult each manifest for verified source provenance.

The initial archive migration preserves exact existing public package bytes. It is not a rebuild or new build-provenance attestation. Public assets exclude credentials, signing private keys, provisioning material outside previously published signed application packages, private backups and rejected/staging builds.

## Delivery contract

The website links directly to immutable release asset URLs; large downloads are delivered by GitHub's release infrastructure. Checksums and the complete release manifest remain public alongside them. Verified recovery copies are maintained separately; private backup locations and credentials are not part of this repository.

Existing desktop updater endpoints remain compatible during migration. Older MSI/Linux clients enforce same-origin installer URLs and reject redirects: do not replace their feed URLs with GitHub links. A newer compatible signed-manifest client must be shipped before those feeds can move off origin. Keep the same update signing key and profile/crypto-store identity.

## Release verification

Run `python3 scripts/verify-release.py TAG`. The verifier streams every manifest-listed public asset and checks its exact size/SHA-256. It never installs packages or uses account data. GitHub Actions repeats this verification for published releases and manual checks. This verifies delivered bytes, not application security, OS signing or build reproducibility.

## Signed update channels

`channels/stable/` publishes authenticated MSI/Linux envelopes for the next compatible desktop client. The public verification key is `RELEASE_PUBLIC_KEY.pem`; its private counterpart never belongs in this repository. Website-era0.1.10 clients must retain direct same-origin bridge installers before they can adopt GitHub-backed channels. Channel changes are mutable discovery metadata; package URLs, bytes and checksums are versioned and immutable by release policy.
