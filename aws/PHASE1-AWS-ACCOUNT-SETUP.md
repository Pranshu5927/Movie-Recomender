# Phase 1: AWS Account Setup & IAM Configuration

**Goal**: Create an AWS account, enable billing alerts, create an IAM user for deployments, and generate access keys for GitHub Actions.

**Time**: ~30 minutes

**What You'll Have at the End**:
- Active AWS account with free tier enabled
- IAM user `github-actions-deployer`
- AWS access keys stored in GitHub Secrets
- Billing alert set to $50 (twice your budget, so you know if something's wrong)

---

## Step 1: Create AWS Account

### 1.1 Go to AWS Homepage
- Open your browser and go to: https://aws.amazon.com
- Click **"Create an AWS account"** (top right, or "Create a Free Account")

### 1.2 Fill in Account Information
- **Email Address**: Use any email (they'll send confirmations)
- **Account Name**: Something like `movie-recommender-prod`
- **Password**: Make it strong (AWS is a big target)
- Click **"Create"**

### 1.3 Add Billing Information
- On the next page, choose **Personal** (not Business)
- Fill in your address
- Add a valid credit card (required even for free tier; AWS won't charge without permission)
- Click **"Verify and Create Account"**

### 1.4 Verify Your Email
- AWS sends you a confirmation email
- Click the link in the email within 24 hours
- This activates your account

### 1.5 Confirm Free Tier Eligibility
- After email verification, go back to AWS Console: https://console.aws.amazon.com
- You should see **"Free Tier"** badge in the top-right corner
- If not, contact AWS support (rare issue)

**✅ You now have an AWS account with free tier enabled.**

---

## Step 2: Enable Billing Alerts

### 2.1 Open Billing Dashboard
- Click your **account name** (top-right corner)
- Select **"Billing and Cost Management"**

### 2.2 Enable Cost Anomaly Detection (Optional but Recommended)
- In the left sidebar, click **"Billing Preferences"**
- Check ✅ **"Receive Free Tier Usage Alerts"**
- Check ✅ **"Receive Billing Alerts"**
- Click **"Save Preferences"**

### 2.3 Set Up Budget Alert
- In the left sidebar, click **"Budgets"** (under "Cost Management")
- Click **"Create a budget"**
- Choose **"Simplified budgets"**
- Set budget amount: **$50** (double your target, so you get warned early)
- Email to notify: **your email**
- Click **"Create budget"**

**✅ Now AWS will email you if spending approaches $50/month.**

---

## Step 3: Create IAM User for GitHub Actions

### 3.1 Go to IAM Dashboard
- In the AWS Console, search for **"IAM"** (top search bar)
- Click **"IAM"** from results
- You're now in the IAM dashboard

### 3.2 Create New User
- In the left sidebar, click **"Users"**
- Click **"Create user"** (top right, orange button)
- Username: `github-actions-deployer`
- Check ✅ **"Provide user access to AWS Management Console"** (optional, but good for learning)
- Check ✅ **"I want to create an IAM user"**
- Click **"Next"**

### 3.3 Set Permissions
- You'll see "Permissions options"
- Choose **"Attach policies directly"**
- Search for and check ✅ these policies:
  - `AmazonEC2ContainerRegistryPowerUser` (for ECR)
  - `AmazonECS_FullAccess` (for ECS)
  - `AmazonRDSFullAccess` (for RDS)
  - `AmazonVPCFullAccess` (for networking)
  - `CloudFormationFullAccess` (for infrastructure as code)
  - `IAMReadOnlyAccess` (to read existing IAM configs)
  - `CloudWatchLogsFullAccess` (for logs)
  
**Note**: These are broader than strictly necessary (security best practice is least privilege, but this is for learning)

- Click **"Next"**

### 3.4 Review and Create
- Review the user details
- Click **"Create user"**
- You'll see a success page

**✅ IAM user created.**

---

## Step 4: Generate Access Keys

### 4.1 Get Access Keys for GitHub Actions
- You're on the user confirmation page after creating the user
- You'll see tabs: "Security credentials" — click it
- Scroll down to **"Access keys"**
- Click **"Create access key"**

### 4.2 Choose Use Case
- Select **"Application running on an AWS compute service"** (closest match for GitHub Actions)
- Check ✅ **"I understand the above recommendation..."**
- Click **"Next"**

### 4.3 Copy Your Keys
- You'll see:
  - **Access key ID** (looks like: `AKIA...`)
  - **Secret access key** (looks like: `wJal...`)
- **IMPORTANT**: Copy both and save in a **temporary text file** on your computer
  - Do NOT push this to GitHub or share it
  - After adding to GitHub Secrets, delete the text file

### 4.4 Click "Done"
- AWS will show the keys one more time on this page
- After you leave this page, you **cannot** see the secret key again
- If you lose it, you'll need to delete and create a new access key pair

---

## Step 5: Store Keys in GitHub Secrets

### 5.1 Go to GitHub
- Open your Movie Recommender repo on GitHub
- Click **"Settings"** (top right)
- In the left sidebar, click **"Secrets and variables"** → **"Actions"**

### 5.2 Add AWS_ACCESS_KEY_ID
- Click **"New repository secret"** (green button)
- Name: `AWS_ACCESS_KEY_ID`
- Secret: Paste the **Access key ID** from Step 4.3
- Click **"Add secret"**

### 5.3 Add AWS_SECRET_ACCESS_KEY
- Click **"New repository secret"** again
- Name: `AWS_SECRET_ACCESS_KEY`
- Secret: Paste the **Secret access key** from Step 4.3
- Click **"Add secret"**

### 5.4 Add AWS_REGION
- Click **"New repository secret"** again
- Name: `AWS_REGION`
- Secret: `us-east-1` (default region, good for learning)
- Click **"Add secret"**

**✅ GitHub Secrets are now configured.**

---

## Step 6: Verify Everything Works

### 6.1 Test IAM User (Optional)
- In AWS Console, go back to **IAM** → **Users**
- Click on `github-actions-deployer`
- Verify you see the policies you attached in Step 3.3

### 6.2 Test GitHub Secrets
- In your GitHub repo, click **"Settings"** → **"Secrets and variables"** → **"Actions"**
- You should see:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`

---

## Security Best Practices Checklist

- ✅ Never commit AWS credentials to GitHub (they're in GitHub Secrets, not code)
- ✅ Delete the temporary text file with your keys
- ✅ Budget alert is set (you'll know if something's wrong)
- ✅ IAM user has limited permissions (not using root account)
- ✅ Free tier is enabled

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Billing and Cost Management" not showing | You may need to verify email first. Check your inbox. |
| Can't find IAM in AWS Console | Try searching in the top search bar for "IAM" |
| Lost secret access key | Delete the key in IAM → Users → Security Credentials, and create a new one |
| Budget alert not working | Check that billing alerts are enabled in Billing Preferences |

---

## What's Next?

You now have:
1. ✅ AWS account with free tier
2. ✅ Billing alerts set
3. ✅ IAM user with deployment permissions
4. ✅ GitHub Secrets configured

**Next Phase**: Phase 2 — Containerization (Docker)
- Create `backend/Dockerfile`
- Create `frontend-react/Dockerfile`
- Create `docker-compose.yml`
- Test locally

---

## Quick Reference

| Item | Value |
|------|-------|
| AWS Region | `us-east-1` |
| IAM User | `github-actions-deployer` |
| Budget Alert | $50/month |
| Free Tier Limit | $0 (with alerts) |
| GitHub Secrets Needed | 3 (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION) |
