# Infrastructure Recreation Guide

This guide explains how to completely tear down your Google Cloud infrastructure and rebuild it using your CI/CD pipeline.

## 1. Destroy Infrastructure

**WARNING**: This will delete your Database, Cloud Run service, and all data within them. The Terraform State bucket and Artifact Registry images normally persist unless explicitly targeted, but `terraform destroy` attempts to remove all managed resources.

Run the following command in your terminal:

```bash
just destroy
```

This executes `terraform destroy -auto-approve`, determining what needs to be deleted from your state file.

## 2. Recreate Infrastructure

Once the destruction is complete, you can trigger a rebuild via GitHub Actions.

1.  **Navigate to GitHub Actions**: Go to the "Actions" tab in your repository.
2.  **Trigger Workflow**:
    -   Select the **Terraform** workflow.
    -   Click **Run workflow** (if `workflow_dispatch` is enabled).
    -   **OR**: Push a small change (like an empty commit) to the `main` branch:
        ```bash
        git commit --allow-empty -m "Trigger rebuild"
        git push
        ```
3.  **Monitor**: Watch the workflow. It will:
    -   `terraform plan` (detecting missing resources).
    -   `terraform apply` (creating new Database, Cloud Run, etc.).

## 3. Verify

After the workflow succeeds:
1.  Get the new **Cloud Run URL** from the workflow logs (Apply step outputs).
2.  Update your frontend configuration if the URL changed (it usually stays the same if the project/region is static, but dynamic names might change).
