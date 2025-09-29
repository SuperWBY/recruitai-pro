#!/bin/bash

# RecruitAI Pro - GitHub Upload Script
echo "🚀 RecruitAI Pro - GitHub Upload Script"
echo "======================================"

# Check if GitHub username is provided
if [ -z "$1" ]; then
    echo "❌ Please provide your GitHub username as an argument"
    echo "Usage: ./upload-to-github.sh YOUR_GITHUB_USERNAME"
    echo "Example: ./upload-to-github.sh john-doe"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="recruitai-pro"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "📋 Repository Information:"
echo "   GitHub Username: $GITHUB_USERNAME"
echo "   Repository Name: $REPO_NAME"
echo "   Repository URL: $REPO_URL"
echo ""

# Check if remote already exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "⚠️  Remote 'origin' already exists"
    echo "   Current URL: $(git remote get-url origin)"
    read -p "Do you want to update it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin $REPO_URL
        echo "✅ Remote URL updated"
    else
        echo "❌ Upload cancelled"
        exit 1
    fi
else
    echo "➕ Adding remote repository..."
    git remote add origin $REPO_URL
    echo "✅ Remote repository added"
fi

echo ""
echo "🔍 Current repository status:"
git remote -v
echo ""

echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Success! Your RecruitAI Pro project has been uploaded to GitHub!"
    echo "🌐 Repository URL: $REPO_URL"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Visit your repository: $REPO_URL"
    echo "   2. Add a description and topics to your repository"
    echo "   3. Consider adding a LICENSE file"
    echo "   4. Set up GitHub Pages if needed"
    echo "   5. Share your amazing project with the world! 🚀"
else
    echo ""
    echo "❌ Upload failed. Please check:"
    echo "   1. GitHub repository exists: $REPO_URL"
    echo "   2. You have write access to the repository"
    echo "   3. Your GitHub credentials are configured"
    echo "   4. Network connection is working"
fi
