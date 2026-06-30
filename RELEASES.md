# 📦 Releases

This document provides information about project releases and how to create them.

## Release Process

### Creating a New Release

1. **Update version numbers** in:
   - `frontend/package.json` (version field)
   - `src/api/main.py` (version in FastAPI app config)
   - `CHANGELOG.md` (add new version section)

2. **Update CHANGELOG.md** with new features, fixes, and changes

3. **Commit changes**:
   ```bash
   git add .
   git commit -m "chore: bump version to X.Y.Z"
   git push origin main
   ```

4. **Create Git Tag**:
   ```bash
   git tag -a vX.Y.Z -m "Release version X.Y.Z"
   git push origin vX.Y.Z
   ```

5. **Create GitHub/GitLab Release**:
   - Go to repository → Releases → Create new release
   - Select the tag you just created
   - Add release notes (see template below)
   - Attach release assets (see below)

---

## Release Assets

### Backend Package

Create a distributable Python package:

```bash
# Build package
python -m build

# Files created:
# - dist/medical_extractor-X.Y.Z-py3-none-any.whl
# - dist/medical_extractor-X.Y.Z.tar.gz
```

Upload these files as release assets.

### Frontend Build

Create a production build:

```bash
cd frontend

# Install dependencies
npm ci --only=production

# Build for production
npm run build

# Create zip of dist folder
zip -r medical-extractor-frontend-X.Y.Z.zip dist/

# Upload zip as release asset
```

### Docker Images

Build and push Docker images:

```bash
# Build backend image
docker build -t medical-extractor-backend:X.Y.Z .

# Build frontend image
docker build -t medical-extractor-frontend:X.Y.Z ./frontend

# Tag for registry
docker tag medical-extractor-backend:X.Y.Z your-registry/medical-extractor-backend:X.Y.Z
docker tag medical-extractor-frontend:X.Y.Z your-registry/medical-extractor-frontend:X.Y.Z

# Push to registry
docker push your-registry/medical-extractor-backend:X.Y.Z
docker push your-registry/medical-extractor-frontend:X.Y.Z
```

---

## Release Notes Template

```markdown
# AI Medical Record Extractor vX.Y.Z

## 🎉 Release Date: YYYY-MM-DD

### ✨ New Features
- Feature 1 description
- Feature 2 description
- Feature 3 description

### 🐛 Bug Fixes
- Fixed issue with patient name extraction
- Resolved CORS configuration errors
- Fixed database connection pooling

### 🔧 Improvements
- Enhanced OCR accuracy for handwritten text
- Improved performance for large files
- Better error messages for users
- Updated dependencies to latest versions

### 📚 Documentation
- Added deployment guide
- Updated API documentation
- Added troubleshooting section

### ⚠️ Breaking Changes
- API endpoint `/old-endpoint` removed (use `/new-endpoint`)
- Database schema updated (automatic migration included)

### 🔒 Security
- Updated dependencies for security patches
- Added input validation for file uploads
- Implemented rate limiting

### 📦 Installation

#### Docker (Recommended)
```bash
docker pull your-registry/medical-extractor-backend:X.Y.Z
docker pull your-registry/medical-extractor-frontend:X.Y.Z
docker-compose up -d
```

#### Manual Installation
```bash
# Backend
pip install medical_extractor==X.Y.Z

# Frontend
npm install -g @medical-extractor/frontend@X.Y.Z
```

### 🔄 Upgrade from Previous Version

#### From vX.Y.Z-1
```bash
# Backup your data
./backup.sh

# Pull new images
docker-compose pull

# Restart with new version
docker-compose up -d
```

### ✅ Verification

After upgrading, verify:
- [ ] Application loads correctly
- [ ] File upload works
- [ ] Text extraction functions properly
- [ ] Database records are accessible
- [ ] Health check passes: `curl http://localhost:8000/health`

### 🐛 Known Issues
- Issue 1 description and workaround
- Issue 2 description (fix coming in next release)

### 🙏 Credits

Thanks to all contributors who made this release possible:
- Contributor 1
- Contributor 2

### 📄 Full Changelog
See [CHANGELOG.md](CHANGELOG.md) for complete list of changes.

---

**Download Links:**
- [Backend Wheel](link)
- [Backend Source](link)
- [Frontend Build](link)
- [Docker Compose](link)
```

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes, major rewrites
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible

### Examples:
- `v1.0.0` → `v1.0.1` (patch: bug fix)
- `v1.0.1` → `v1.1.0` (minor: new feature)
- `v1.1.0` → `v2.0.0` (major: breaking change)

---

## Release Checklist

Before creating a release:

- [ ] All tests pass: `pytest tests/ -v`
- [ ] No linting errors: `ruff check src/`
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated in all files
- [ ] Docker images build successfully
- [ ] Frontend builds without errors
- [ ] Manual testing completed
- [ ] Security review done
- [ ] Performance testing done (if applicable)

---

## Hotfix Releases

For critical bugs in production:

1. Create branch from production tag:
   ```bash
   git checkout -b hotfix/vX.Y.Z+1 vX.Y.Z
   ```

2. Fix the issue and commit

3. Merge to main and create new tag:
   ```bash
   git checkout main
   git merge hotfix/vX.Y.Z+1
   git tag -a vX.Y.Z+1 -m "Hotfix: description"
   git push origin main --tags
   ```

4. Create release immediately

---

## Rollback Procedure

If a release has critical issues:

### Docker Deployment
```bash
# Stop current version
docker-compose down

# Update docker-compose.yml to use previous version
# Example: change image tag from v1.2.0 to v1.1.0

# Start previous version
docker-compose up -d
```

### Manual Deployment
```bash
# Restore from backup
./restore.sh backup-YYYYMMDD-HHMMSS

# Or reinstall previous version
pip install medical_extractor==X.Y.Z-1
```

---

## Support Policy

- **Latest version**: Full support and bug fixes
- **Previous major version**: Security fixes only
- **Older versions**: No support (upgrade recommended)

### Supported Versions
| Version | Status | Support Until |
|---------|--------|---------------|
| v2.x.x  | Current | Next release + 3 months |
| v1.x.x  | Security only | 2024-12-31 |
| v0.x.x  | EOL | No longer supported |

---

## Automated Releases

### Using GitHub Actions

The `.github/workflows/release.yml` workflow automates releases:

```yaml
name: Create Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: |
            See CHANGELOG.md for changes
          draft: false
          prerelease: false
```

### Using GitLab CI

The `.gitlab-ci.yml` includes release automation:

```yaml
release:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/release-cli:latest
  rules:
    - if: $CI_COMMIT_TAG
  script:
    - |
      release-cli create \
        --name "Release $CI_COMMIT_TAG" \
        --description "$(cat CHANGELOG.md)" \
        --tag-name $CI_COMMIT_TAG
```

---

## Distribution Channels

### Package Managers

#### PyPI (Python Package)
```bash
# Build and publish
python -m build
twine upload dist/*

# Install from PyPI
pip install medical-extractor
```

#### npm (Frontend)
```bash
# Publish to npm
npm publish

# Install
npm install -g medical-extractor-frontend
```

### Docker Hub

```bash
# Login
docker login

# Push images
docker push username/medical-extractor-backend:X.Y.Z
docker push username/medical-extractor-frontend:X.Y.Z
```

---

## Post-Release Tasks

After creating a release:

- [ ] Announce on project website/blog
- [ ] Send email to mailing list
- [ ] Post on social media
- [ ] Update documentation site
- [ ] Notify users via application (if applicable)
- [ ] Monitor for issues (GitHub Issues, support tickets)
- [ ] Update hackathon submission (if applicable)

---

## License

All releases are under GNU General Public License v3.0