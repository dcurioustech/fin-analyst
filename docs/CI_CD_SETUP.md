# CI/CD Setup Guide

This document explains the Continuous Integration and Continuous Deployment setup for the Financial Analysis Assistant.

## GitHub Actions Workflows

### 1. Test Suite (`test.yml`)
**Triggers:** Push to main/develop/feature branches, Pull Requests
**Purpose:** Run comprehensive tests on every code change

**Jobs:**
- **test**: Runs unit and integration tests with coverage reporting
- **lint**: Code quality checks with flake8, black, and isort

### 2. Pull Request Checks (`pr-check.yml`)
**Triggers:** Pull Request events
**Purpose:** Fast feedback for pull requests

**Jobs:**
- **quick-test**: Fast test execution for immediate feedback
- **test-coverage**: Full coverage analysis with PR comments

### 3. CI/CD Pipeline (`ci.yml`)
**Triggers:** Push to main/develop, Pull Requests
**Purpose:** Comprehensive quality assurance

**Jobs:**
- **test**: Multi-version Python testing (3.9-3.12)
- **security-scan**: Security vulnerability scanning
- **type-check**: Static type checking with mypy
- **integration-test**: Full integration testing

### 4. Release and Deploy (`release.yml`)
**Triggers:** Release published, Manual workflow dispatch
**Purpose:** Automated deployment to production

**Jobs:**
- **test-before-release**: Pre-deployment testing
- **build-and-deploy**: Docker build and Cloud Run deployment

## Required GitHub Secrets

To enable full CI/CD functionality, configure these secrets in your GitHub repository:

### Google Cloud Platform
```
GCP_SA_KEY          # Service account key JSON
GCP_PROJECT_ID      # Your GCP project ID
```

### Optional
```
CODECOV_TOKEN       # For coverage reporting (if using Codecov)
```

## Setting Up Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each required secret

### GCP Service Account Setup
```bash
# Create service account
gcloud iam service-accounts create github-actions \
    --description="GitHub Actions CI/CD" \
    --display-name="GitHub Actions"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Create and download key
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## Local Development Commands

### Testing
```bash
# Run tests as they run in CI
make ci-test

# Run linting as in CI
make ci-lint

# Run security checks
make ci-security

# Run all tests with coverage
make test-coverage
```

### Docker
```bash
# Build Docker image
make docker-build

# Run container locally
make docker-run

# Test Docker container
make docker-test
```

## Workflow Status Badges

Add these badges to your README.md:

```markdown
![Test Suite](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Test%20Suite/badge.svg)
![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI%2FCD%20Pipeline/badge.svg)
```

## Branch Protection Rules

Recommended branch protection settings for `main`:

1. **Require pull request reviews before merging**
2. **Require status checks to pass before merging**
   - Test Suite / test
   - Test Suite / lint
   - CI/CD Pipeline / test
3. **Require branches to be up to date before merging**
4. **Require linear history**
5. **Include administrators**

## Deployment Process

### Automatic Deployment
1. Create a release on GitHub
2. Workflows automatically run tests
3. If tests pass, builds and deploys to Cloud Run

### Manual Deployment
1. Go to Actions tab in GitHub
2. Select "Release and Deploy" workflow
3. Click "Run workflow"
4. Choose environment (staging/production)

## Monitoring and Alerts

### Test Failures
- Failed workflows send notifications to repository watchers
- Check the Actions tab for detailed logs
- Failed tests block merging (if branch protection is enabled)

### Deployment Status
- Monitor Cloud Run service health
- Check application logs in Google Cloud Console
- Use the `/health` endpoint for monitoring

## Troubleshooting

### Common Issues

**Tests fail in CI but pass locally:**
- Check Python version differences
- Verify environment variables
- Check for missing dependencies

**Docker build fails:**
- Check Dockerfile syntax
- Verify all required files are included
- Check .dockerignore exclusions

**Deployment fails:**
- Verify GCP credentials
- Check service account permissions
- Verify Cloud Run configuration

### Getting Help

1. Check workflow logs in GitHub Actions
2. Review this documentation
3. Check Google Cloud Console for deployment issues
4. Create an issue using the bug report template