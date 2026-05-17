# PyPI Distribution & GitHub Publishing Guide

This guide walks through publishing CAVRA to PyPI and GitHub.

## Prerequisites

1. **GitHub account** with repository created
2. **PyPI account** (https://pypi.org/account/register/)
3. **PyPI API token** for authentication
4. Local git configuration (already done)

---

## Step 1: Push to GitHub

### 1a. Create GitHub repository

1. Go to https://github.com/new
2. Create repository: `cavra`
3. Choose:
   - ✓ Public
   - ✓ Initialize with nothing (we have our own .git)
4. Copy the HTTPS or SSH URL

### 1b. Add GitHub remote and push

```bash
# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/cavra.git

# Push to GitHub
git push -u origin main
```

### 1c. Set up GitHub branch protection (optional)

In GitHub Settings → Branches:
1. Add branch protection rule for `main`
2. ✓ Require status checks to pass (test.yml)
3. ✓ Require code review before merge (1 reviewer)
4. ✓ Dismiss stale reviews
5. ✓ Require branches be up to date

---

## Step 2: Build distribution package

### 2a. Install build tools

```bash
pip install --upgrade build twine
```

### 2b. Build package locally

```bash
cd /Users/huzefahusain/Projects/cavra
python -m build
```

This creates:
- `dist/cavra-0.1.0-py3-none-any.whl` (wheel)
- `dist/cavra-0.1.0.tar.gz` (source)

### 2c. Validate with twine

```bash
twine check dist/*
```

Should return:
```
Checking distribution dist/cavra-0.1.0-py3-none-any.whl: Passed
Checking distribution dist/cavra-0.1.0.tar.gz: Passed
```

---

## Step 3: Test PyPI (recommended first)

### 3a. Upload to TestPyPI

```bash
twine upload --repository testpypi dist/*
```

Enter username: `__token__`
Enter password: (your TestPyPI API token)

### 3b. Install from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ cavra
```

### 3c. Test the installation

```bash
cavra --version
cavra policy list
```

---

## Step 4: Publish to PyPI

### 4a. Upload to production PyPI

```bash
twine upload dist/*
```

Enter username: `__token__`
Enter password: (your PyPI API token from https://pypi.org/manage/account/tokens/)

### 4b. Install from PyPI

```bash
pip install cavra
```

### 4c. Verify installation

```bash
cavra --version
# Output: cavra, version 0.1.0
```

---

## Step 5: Create GitHub Release

### 5a. Create tag

```bash
git tag -a v0.1.0 -m "CAVRA MVP v0.1.0 - Initial release

Features:
- Core policy registry with YAML governance
- Runtime guard for file and command access control
- Session management and audit recording
- GitHub PR attestation generation
- 4 production policy packs
- Comprehensive documentation
- Full test suite (8/8 passing)
- GitHub Actions CI/CD workflows"

git push origin v0.1.0
```

### 5b. Create release on GitHub

1. Go to https://github.com/YOUR_USERNAME/cavra/releases
2. Click "Draft a new release"
3. Select tag: `v0.1.0`
4. Title: `CAVRA v0.1.0 - MVP Release`
5. Description:
   ```markdown
   # CAVRA v0.1.0

   Initial MVP release of runtime governance for AI coding agents.

   ## Features
   - ✓ Policy-as-code (YAML) with 4 baseline packs
   - ✓ Runtime file and command access control
   - ✓ Session management with audit trails
   - ✓ GitHub PR attestation generation
   - ✓ Webhook export for SIEM (Splunk, Datadog, Sentinel)
   - ✓ Full test suite (8/8 passing)
   - ✓ Comprehensive documentation

   ## Installation
   ```bash
   pip install cavra
   ```

   ## Quick Start
   ```bash
   # Start a governed session
   cavra agent start \
     --tool claude-code \
     --repo . \
     --policy-pack cavra-banking-baseline

   # Execute command under governance
   cavra agent exec "terraform plan"

   # List policies
   cavra policy list
   ```

   ## Documentation
   - [Vision](docs/vision.md)
   - [Architecture](docs/architecture.md)
   - [Policy Authoring](docs/policy-authoring.md)
   - [Implementation Guide](docs/implementation-guide.md)
   - [5-Year Roadmap](docs/roadmap.md)

   See [README.md](README.md) for complete documentation.

   ## License
   BUSL-1.1 (Business Source License with 4-year change deadline)
   ```
6. ✓ Set as latest release
7. Click "Publish release"

---

## Step 6: Announce publicly

### 6a. Social media

Post on:
- LinkedIn: Feature announcement, installation instructions
- Twitter/X: Brief announcement with link to release
- Reddit (r/devops, r/python): Community discussion

### 6b. Notify users

- Email to waitlist (if any)
- Post in relevant Slack communities
- Create discussion in GitHub Discussions

---

## Continuous update process

### For future versions

1. **Update version** in `pyproject.toml` and `setup.py`:
   ```
   version = "0.2.0"
   ```

2. **Update changelog** in `RELEASE_NOTES.md`:
   ```markdown
   ## v0.2.0 (Date)
   - Feature X
   - Feature Y
   - Bug fix Z
   ```

3. **Commit changes**:
   ```bash
   git add pyproject.toml setup.py RELEASE_NOTES.md
   git commit -m "Release v0.2.0"
   ```

4. **Build and test**:
   ```bash
   python -m build
   twine check dist/*
   ```

5. **Publish**:
   ```bash
   twine upload dist/*
   ```

6. **Tag and release**:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin main --tags
   ```

7. **GitHub Release**: Create release on GitHub (as above)

---

## Troubleshooting

### Issue: "401 Unauthorized" when uploading

**Solution**: Verify your PyPI API token
```bash
# Check stored credentials
cat ~/.pypirc
# Or re-authenticate
twine upload --skip-existing dist/*
```

### Issue: "File already exists on server"

**Solution**: Use `--skip-existing` flag
```bash
twine upload --skip-existing dist/*
```

### Issue: Test PyPI upload works but production fails

**Solution**: Ensure you're using the correct credentials
```bash
# Use explicit token
twine upload -u __token__ -p "pypi-your-token-here" dist/*
```

### Issue: Package can't be imported after install

**Solution**: Rebuild and check MANIFEST.in
```bash
python -m build --clean
twine check dist/*
```

---

## Security best practices

1. **Never commit API tokens** to git
2. **Use environment variables** for credentials:
   ```bash
   export TWINE_USERNAME="__token__"
   export TWINE_PASSWORD="pypi-your-token"
   twine upload dist/*
   ```

3. **Create repository-scoped tokens** on PyPI:
   - Go to PyPI → Account → API tokens
   - Create new token with `cavra` scope only

4. **Rotate tokens regularly** (quarterly)

5. **Sign releases with GPG** (future):
   ```bash
   git tag -s -a v0.1.0 -m "Release v0.1.0"
   ```

---

## Success checklist

- [ ] GitHub repository created and pushed
- [ ] PyPI package uploaded (TestPyPI first)
- [ ] Installation verified: `pip install cavra`
- [ ] CLI working: `cavra --version`
- [ ] GitHub release created with proper description
- [ ] Documentation linked in GitHub repo
- [ ] Public announcement made
- [ ] Repository starred and watched by team

---

## Next steps

After successful release:
1. Monitor GitHub issues and discussions
2. Gather customer feedback
3. Update policies based on real-world usage
4. Plan Phase 2: MCP governance and advanced features
5. Begin work on web UI for policy management

