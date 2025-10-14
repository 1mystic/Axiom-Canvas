# Axiom Canvas - Deployment Checklist

Use this checklist to ensure a smooth deployment to Vercel.

## Pre-Deployment

### Code Quality
- [ ] All files created and in correct directories
- [ ] No syntax errors in Python code
- [ ] No console errors in JavaScript
- [ ] CSS renders correctly across browsers
- [ ] All imports and dependencies listed in requirements.txt

### Testing
- [ ] Tested locally with `python api/index.py`
- [ ] Tested basic plotting functionality
- [ ] Tested chat interface
- [ ] Tested PDF upload (if PyMuPDF installed)
- [ ] Tested on different browsers
- [ ] Tested responsive design on mobile

### Configuration Files
- [ ] `vercel.json` exists and is valid JSON
- [ ] `requirements.txt` has all dependencies
- [ ] `.gitignore` includes `.env` and `venv/`
- [ ] `.env.example` exists for reference
- [ ] README.md is complete and accurate

### API Keys
- [ ] Obtained Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Generated Flask secret key
- [ ] Never committed API keys to Git
- [ ] API keys stored securely

## Vercel Setup

### Account & CLI
- [ ] Created Vercel account at https://vercel.com/signup
- [ ] Installed Vercel CLI: `npm install -g vercel`
- [ ] Logged in: `vercel login`

### Environment Variables
- [ ] Added `GEMINI_API_KEY` to Vercel
  ```bash
  vercel env add GEMINI_API_KEY
  ```
- [ ] Added `FLASK_SECRET_KEY` to Vercel
  ```bash
  vercel env add FLASK_SECRET_KEY
  ```
- [ ] Set environment variables for all environments (Production, Preview, Development)

### Repository
- [ ] Code pushed to GitHub/GitLab/Bitbucket
- [ ] Repository is public or Vercel has access
- [ ] `.git` directory exists
- [ ] No large files (>100MB) in repo

## Deployment Methods

### Method 1: Vercel CLI (Recommended for First Deploy)

```bash
# Navigate to FLASK-APP directory
cd FLASK-APP

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

- [ ] Ran `vercel` command successfully
- [ ] Received deployment URL
- [ ] Tested preview deployment
- [ ] Ran `vercel --prod` for production
- [ ] Production URL received

### Method 2: GitHub Integration (Recommended for Continuous Deployment)

- [ ] Went to https://vercel.com/new
- [ ] Selected "Import Git Repository"
- [ ] Connected GitHub account
- [ ] Selected repository
- [ ] Configured build settings:
  - [ ] Root Directory: `FLASK-APP`
  - [ ] Framework Preset: `Other`
  - [ ] Build Command: (leave empty)
  - [ ] Output Directory: (leave empty)
- [ ] Added environment variables in Vercel dashboard
- [ ] Clicked "Deploy"
- [ ] Deployment succeeded

## Post-Deployment

### Verification
- [ ] Visited deployment URL
- [ ] Page loads without errors
- [ ] Desmos calculator renders
- [ ] Chat interface appears
- [ ] Tested sending a message
- [ ] Tested plotting a function
- [ ] Tested PDF upload
- [ ] Checked browser console for errors
- [ ] Tested on mobile device

### Performance
- [ ] Page loads in < 3 seconds
- [ ] Chat responses in < 5 seconds
- [ ] Graph renders smoothly
- [ ] No memory leaks in long sessions

### Monitoring
- [ ] Set up Vercel Analytics (optional)
- [ ] Configured error tracking
- [ ] Checked deployment logs
- [ ] Set up uptime monitoring (optional)

## Troubleshooting

### Common Deployment Errors

#### Build Fails
```
Error: No module named 'google.generativeai'
```
**Fix:** Ensure `google-generativeai` is in `requirements.txt`

#### Runtime Error
```
Error: GEMINI_API_KEY not set
```
**Fix:** Add environment variable in Vercel dashboard

#### Import Error
```
ModuleNotFoundError: No module named 'fitz'
```
**Fix:** Ensure `PyMuPDF` is in `requirements.txt`

#### Function Timeout
```
Error: Function execution timed out
```
**Fix:** Optimize PDF processing or increase timeout in `vercel.json`

### Verification Commands

Check deployment status:
```bash
vercel list
```

View logs:
```bash
vercel logs [deployment-url]
```

Check environment variables:
```bash
vercel env ls
```

Remove deployment:
```bash
vercel remove [deployment-name]
```

## Domain Configuration (Optional)

### Custom Domain
- [ ] Purchased domain
- [ ] Added domain in Vercel dashboard
- [ ] Configured DNS records
- [ ] SSL certificate issued
- [ ] Domain accessible via HTTPS

### Subdomain
- [ ] Created subdomain
- [ ] Added to Vercel project
- [ ] DNS propagated
- [ ] Tested subdomain access

## Security Review

### Pre-Launch Security
- [ ] No API keys in source code
- [ ] `.env` file in `.gitignore`
- [ ] HTTPS enabled (automatic on Vercel)
- [ ] Input validation implemented
- [ ] File upload size limits set
- [ ] Rate limiting considered

### Post-Launch Monitoring
- [ ] Monitor for unusual API usage
- [ ] Check for errors in logs
- [ ] Watch for abuse patterns
- [ ] Set up alerts for high usage

## Performance Optimization

### Vercel Configuration
- [ ] Enabled Edge Network
- [ ] Configured caching headers
- [ ] Set appropriate timeout values
- [ ] Optimized function size

### Code Optimization
- [ ] Minimized dependencies
- [ ] Implemented lazy loading
- [ ] Optimized images (if any)
- [ ] Reduced API calls

## Documentation

### User-Facing
- [ ] README.md complete
- [ ] Usage examples provided
- [ ] Troubleshooting guide available
- [ ] API documentation (if exposing APIs)

### Developer-Facing
- [ ] IMPLEMENTATION_GUIDE.md complete
- [ ] Code comments added
- [ ] Architecture documented
- [ ] Contribution guidelines (if open source)

## Rollback Plan

### If Deployment Fails
1. Check Vercel deployment logs
2. Review error messages
3. Test locally to reproduce
4. Fix issues and redeploy
5. If critical, rollback to previous deployment:
   ```bash
   vercel rollback [previous-deployment-url]
   ```

### Emergency Contacts
- Vercel Support: https://vercel.com/support
- Gemini API Support: https://ai.google.dev/support

## Launch Checklist

### Final Review
- [ ] All features working
- [ ] No critical bugs
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] Team notified of launch

### Launch Steps
1. [ ] Final test on production URL
2. [ ] Announce launch (if applicable)
3. [ ] Monitor logs for first hour
4. [ ] Check error rates
5. [ ] Gather initial user feedback

### Post-Launch
- [ ] Monitor daily for first week
- [ ] Respond to user feedback
- [ ] Fix any issues promptly
- [ ] Plan next features/improvements

## Maintenance Schedule

### Daily
- [ ] Check error logs
- [ ] Monitor API usage
- [ ] Respond to issues

### Weekly
- [ ] Review performance metrics
- [ ] Check dependency updates
- [ ] Test critical features

### Monthly
- [ ] Update dependencies
- [ ] Review security
- [ ] Optimize performance
- [ ] Backup data (if applicable)

## Success Metrics

Track these metrics to measure success:

- [ ] Deployment uptime: > 99.9%
- [ ] Average response time: < 3s
- [ ] Error rate: < 1%
- [ ] User satisfaction: Monitor feedback
- [ ] API usage: Within free tier limits

---

## Quick Reference

### Essential Commands

```bash
# Deploy to production
vercel --prod

# View logs
vercel logs

# List deployments
vercel list

# Add environment variable
vercel env add VARIABLE_NAME

# Remove deployment
vercel remove [deployment-name]
```

### Essential URLs

- Vercel Dashboard: https://vercel.com/dashboard
- Deployment Logs: https://vercel.com/[username]/[project]/[deployment]
- Gemini API Console: https://makersuite.google.com/
- Project Repository: [Your GitHub URL]

---

**Congratulations on deploying Axiom Canvas! 🎉**

Remember to:
- Monitor your Gemini API usage to stay within free tier limits
- Check Vercel analytics for deployment health
- Keep dependencies updated for security
- Gather user feedback for improvements

For support, refer to:
- README.md for user documentation
- IMPLEMENTATION_GUIDE.md for technical details
- TEST_PROMPTS.md for testing scenarios
