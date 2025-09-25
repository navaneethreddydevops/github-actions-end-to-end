# GitHub Actions Workflows Explained

This document provides detailed explanations of all the GitHub Actions workflows in this repository, helping you understand different patterns and techniques used in CI/CD automation.

## Table of Contents

- [Basic CI Workflow (`ci-basic.yml`)](#basic-ci-workflow)
- [Matrix Build Workflow (`ci-matrix.yml`)](#matrix-build-workflow)
- [Conditional Workflow (`conditional.yml`)](#conditional-workflow)
- [Manual Trigger Workflow (`manual.yml`)](#manual-trigger-workflow)
- [Artifacts Workflow (`artifacts.yml`)](#artifacts-workflow)
- [Scheduled Workflow (`scheduled.yml`)](#scheduled-workflow)

## Basic CI Workflow

**File:** `.github/workflows/ci-basic.yml`

### Purpose
Demonstrates the fundamentals of continuous integration with GitHub Actions, including code quality checks, testing, building, and security scanning.

### Triggers
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main` or `master` branches

### Key Learning Points

#### 1. Workflow Structure
```yaml
name: Basic CI Workflow
on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]
```

#### 2. Environment Variables
```yaml
env:
  PYTHON_VERSION: '3.9'
```
Global environment variables available to all jobs.

#### 3. Job Dependencies
```yaml
test:
  needs: lint  # This job waits for lint to complete
```
Controls job execution order using the `needs` keyword.

#### 4. Caching
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('src/requirements.txt') }}
```
Speeds up builds by caching dependencies between runs.

#### 5. Error Handling
```yaml
continue-on-error: true  # Allow step to fail without failing job
```

### Jobs Breakdown

1. **Lint Job**: Code quality checks with flake8 and black
2. **Test Job**: Unit tests with pytest and coverage reporting
3. **Build Job**: Application startup testing
4. **Security Job**: Vulnerability scanning with safety and bandit
5. **Summary Job**: Aggregates results and generates reports

### Best Practices Demonstrated
- Fail-fast approach (stop early on critical failures)
- Parallel job execution where possible
- Comprehensive error reporting
- Security-first mindset
- Proper dependency management

---

## Matrix Build Workflow

**File:** `.github/workflows/ci-matrix.yml`

### Purpose
Shows how to run the same job across multiple configurations (Python versions, operating systems, dependency versions).

### Key Learning Points

#### 1. Basic Matrix
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11']
```

#### 2. Multi-dimensional Matrix
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9']
    os: [ubuntu-latest, windows-latest, macos-latest]
```

#### 3. Matrix with Inclusions/Exclusions
```yaml
strategy:
  matrix:
    # ... base matrix
    include:
      - python-version: '3.11'
        os: ubuntu-latest
        experimental: true
    exclude:
      - python-version: '3.8'
        os: windows-latest
```

#### 4. Conditional Matrix Behavior
```yaml
continue-on-error: ${{ matrix.experimental }}
```

### Matrix Types Covered
1. **Python Versions**: Testing across Python 3.8-3.11
2. **Operating Systems**: Ubuntu, Windows, macOS
3. **Complex Matrix**: With inclusions, exclusions, and experimental configs
4. **Dependency Versions**: Testing with different Flask versions

### Use Cases
- Multi-platform support validation
- Version compatibility testing
- Performance comparison across environments
- Feature flag testing

---

## Conditional Workflow

**File:** `.github/workflows/conditional.yml`

### Purpose
Demonstrates various conditional execution patterns for jobs and steps.

### Key Learning Points

#### 1. Branch-based Conditions
```yaml
if: github.ref == 'refs/heads/main'
```

#### 2. Event-based Conditions
```yaml
if: github.event_name == 'push'
```

#### 3. Path-based Conditions
```yaml
- name: Get changed files
  uses: tj-actions/changed-files@v40
```

#### 4. Complex Conditions
```yaml
if: |
  (github.ref == 'refs/heads/main' && github.event_name == 'push') ||
  (github.event_name == 'pull_request' && contains(github.event.pull_request.labels.*.name, 'urgent'))
```

#### 5. Failure Handling
```yaml
if: steps.risky-step.outcome == 'failure'
```

### Condition Types
1. **Branch Conditions**: Different behavior per branch
2. **Event Conditions**: Response to different trigger types
3. **Path Conditions**: Run based on changed files
4. **Failure Conditions**: Handle step outcomes
5. **Job-level Conditions**: Entire jobs based on conditions

### Practical Applications
- Environment-specific deployments
- Skip unnecessary work
- Implement approval workflows
- Handle bot vs. human commits differently

---

## Manual Trigger Workflow

**File:** `.github/workflows/manual.yml`

### Purpose
Shows how to create interactive workflows that accept user input and can be triggered manually.

### Key Learning Points

#### 1. Workflow Dispatch Setup
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options: ['development', 'staging', 'production']
```

#### 2. Input Types
- `choice`: Dropdown selection
- `string`: Text input
- `boolean`: Checkbox
- `environment`: Environment selector

#### 3. Using Inputs
```yaml
run: echo "Deploying to ${{ github.event.inputs.environment }}"
```

#### 4. Conditional Logic Based on Inputs
```yaml
if: github.event.inputs.run_tests == 'true'
```

### Workflow Features
1. **Interactive Parameters**: User-friendly input forms
2. **Environment Selection**: Deploy to different environments
3. **Conditional Steps**: Based on user choices
4. **Deployment Strategies**: Blue-green, rolling, recreate
5. **Notification Options**: Team notifications
6. **Error Handling**: Rollback on failure

### Use Cases
- Production deployments
- Emergency hotfixes
- Data migration tasks
- Environment setup
- Maintenance operations

---

## Artifacts Workflow

**File:** `.github/workflows/artifacts.yml`

### Purpose
Comprehensive demonstration of artifact handling in GitHub Actions.

### Key Learning Points

#### 1. Creating Artifacts
```yaml
- name: Upload build artifacts
  uses: actions/upload-artifact@v3
  with:
    name: application-build
    path: build/
    retention-days: 30
```

#### 2. Downloading Artifacts
```yaml
- name: Download build artifacts
  uses: actions/download-artifact@v3
  with:
    name: application-build
    path: combined/build/
```

#### 3. Artifact Organization
- Logical grouping by purpose
- Appropriate retention periods
- Clear naming conventions
- Comprehensive metadata

### Artifact Types Created
1. **Build Artifacts**: Compiled binaries and build info
2. **Test Reports**: Test results, coverage, HTML reports
3. **Code Quality**: Linting, security, analysis reports
4. **Documentation**: API docs, user manuals, guides
5. **Combined Package**: All artifacts in one package

### Advanced Features
- Multi-format reports (JSON, HTML, XML)
- Comprehensive manifests
- Automated documentation generation
- Release packaging
- Long-term retention strategies

---

## Scheduled Workflow

**File:** `.github/workflows/scheduled.yml`

### Purpose
Demonstrates automated tasks that run on a schedule using cron syntax.

### Key Learning Points

#### 1. Cron Schedule Syntax
```yaml
schedule:
  - cron: '0 2 * * *'    # Daily at 2 AM UTC
  - cron: '0 8 * * 1'    # Weekly on Monday 8 AM UTC
  - cron: '0 6 1 * *'    # Monthly on 1st at 6 AM UTC
```

#### 2. Concurrency Control
```yaml
concurrency:
  group: scheduled-tasks
  cancel-in-progress: false
```

#### 3. Schedule-based Conditions
```yaml
if: github.event.schedule == '0 2 * * *'
```

### Scheduled Task Types
1. **Daily**: Health checks, log cleanup, security scans
2. **Weekly**: Comprehensive testing, dependency updates
3. **Monthly**: Security audits, performance baselines
4. **Emergency**: Manual maintenance tasks

### Automation Features
- Preventive maintenance
- Security monitoring
- Performance tracking
- Resource cleanup
- Compliance reporting

## Common Patterns and Best Practices

### 1. Security Best Practices
- Never hardcode secrets in workflows
- Use GitHub Secrets for sensitive data
- Regular security scanning
- Principle of least privilege

### 2. Performance Optimization
- Use caching for dependencies
- Parallel job execution
- Conditional execution to skip unnecessary work
- Appropriate runner selection

### 3. Error Handling
- Fail-fast for critical errors
- Continue-on-error for non-critical steps
- Comprehensive logging
- Meaningful error messages

### 4. Documentation and Reporting
- Clear job and step names
- Comprehensive summaries
- Artifact organization
- Progress reporting

### 5. Maintenance and Monitoring
- Regular dependency updates
- Security vulnerability monitoring
- Performance baseline tracking
- Automated cleanup tasks

## Advanced Techniques

### 1. Dynamic Matrices
Generate matrix configurations dynamically based on repository contents or external APIs.

### 2. Reusable Workflows
Create modular workflows that can be called by other workflows.

### 3. Custom Actions
Develop custom actions for repeated logic.

### 4. Environment Protection
Use environment protection rules for production deployments.

### 5. Approval Workflows
Implement human approval steps for critical operations.

## Testing Your Workflows

### 1. Start Small
Begin with the basic CI workflow and gradually add complexity.

### 2. Use Manual Triggers
Test workflows manually before relying on automatic triggers.

### 3. Monitor Resource Usage
Keep an eye on runner minutes and storage usage.

### 4. Test Error Scenarios
Intentionally break things to test error handling.

### 5. Review Logs Regularly
Check workflow logs to identify optimization opportunities.

## Conclusion

This repository provides a comprehensive foundation for learning GitHub Actions. Each workflow demonstrates specific concepts and can be adapted to your specific needs. The key to mastering GitHub Actions is to start simple and gradually build complexity as you become more comfortable with the platform.

Remember to always consider security, performance, and maintainability when designing your workflows. The examples here follow industry best practices and can serve as templates for your own projects.