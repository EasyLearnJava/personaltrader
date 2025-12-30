# 🔑 Render.com API Key Setup for Augment Code

This guide shows you how to get your Render.com API key and connect it to Augment Code settings.

---

## 📋 Step 1: Get Render.com API Key

### 1.1 Log into Render.com

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Sign in with your account

### 1.2 Navigate to Account Settings

1. Click on your **profile picture** (top right corner)
2. Select **Account Settings** from the dropdown menu

### 1.3 Generate API Key

1. In the left sidebar, click **API Keys**
2. Click **Create API Key** button
3. Give it a name (e.g., "Augment Code Integration")
4. Click **Create**
5. **Copy the API key immediately** - you won't be able to see it again!

**Example API Key format:**
```
rnd_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890
```

⚠️ **Important:** Store this key securely. If you lose it, you'll need to generate a new one.

---

## 🔧 Step 2: Add API Key to Augment Code Settings

### Option A: Using VS Code Settings UI

1. **Open VS Code Settings**
   - Press `Ctrl + ,` (Windows/Linux) or `Cmd + ,` (Mac)
   - Or: File → Preferences → Settings

2. **Search for Render**
   - Type "render" in the search bar
   - Look for "Augment: Render API Key" or similar

3. **Add Your API Key**
   - Paste your Render.com API key
   - Click outside the field to save

### Option B: Using settings.json (Recommended)

1. **Open Command Palette**
   - Press `Ctrl + Shift + P` (Windows/Linux)
   - Press `Cmd + Shift + P` (Mac)

2. **Open Settings JSON**
   - Type: `Preferences: Open User Settings (JSON)`
   - Press Enter

3. **Add Render API Key**
   
   Add this line to your `settings.json`:
   
   ```json
   {
     "augment.renderApiKey": "rnd_YOUR_API_KEY_HERE"
   }
   ```

4. **Save the file** (`Ctrl + S` or `Cmd + S`)

### Option C: Using Environment Variables

1. **Create/Edit `.env` file** in your project root:
   
   ```bash
   RENDER_API_KEY=rnd_YOUR_API_KEY_HERE
   ```

2. **Add to VS Code settings.json**:
   
   ```json
   {
     "augment.renderApiKey": "${env:RENDER_API_KEY}"
   }
   ```

---

## ✅ Step 3: Verify Connection

### Test the Connection

1. **Open Command Palette** (`Ctrl/Cmd + Shift + P`)
2. Type: `Augment: Test Render Connection`
3. You should see: ✅ "Connected to Render.com successfully"

### Alternative: Check in Augment Panel

1. Open Augment panel in VS Code
2. Look for Render.com integration status
3. Should show: 🟢 Connected

---

## 🔒 Security Best Practices

### ✅ DO:
- Store API key in VS Code settings (encrypted)
- Use environment variables for team projects
- Rotate API keys periodically
- Use different keys for different environments

### ❌ DON'T:
- Commit API keys to Git
- Share API keys in chat/email
- Use the same key across multiple tools
- Store in plain text files

---

## 🛠️ Troubleshooting

### Issue: "Invalid API Key"

**Solution:**
1. Verify you copied the entire key (starts with `rnd_`)
2. Check for extra spaces before/after the key
3. Generate a new API key if needed

### Issue: "Connection Failed"

**Solution:**
1. Check your internet connection
2. Verify Render.com is accessible: [https://status.render.com](https://status.render.com)
3. Try regenerating the API key

### Issue: "Permission Denied"

**Solution:**
1. Make sure you're the account owner or have API access
2. Check if your Render.com plan supports API access
3. Verify the API key hasn't been revoked

---

## 📚 What You Can Do with Render API in Augment

Once connected, Augment can:

- ✅ Deploy your app directly from VS Code
- ✅ View deployment logs in real-time
- ✅ Check service status
- ✅ Manage environment variables
- ✅ Trigger manual deployments
- ✅ View build history

---

## 🔄 Rotating API Keys

### When to Rotate:
- Every 90 days (recommended)
- If key is compromised
- When team member leaves
- After security incident

### How to Rotate:

1. **Generate new key** in Render.com
2. **Update Augment settings** with new key
3. **Test connection** to verify
4. **Delete old key** from Render.com

---

## 📞 Need Help?

- **Render.com Docs:** [https://render.com/docs/api](https://render.com/docs/api)
- **Augment Docs:** Check Augment Code documentation
- **Render Support:** [https://render.com/support](https://render.com/support)

---

**🎉 You're all set! Augment Code can now interact with your Render.com deployments.**

