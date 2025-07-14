#!/bin/bash

echo "🚀 AI Social Media Post Generator - Vercel Deployment Script"
echo "============================================================"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Make sure to set your OPENAI_API_KEY in Vercel dashboard after deployment"
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Post-deployment checklist:"
echo "1. Go to your Vercel dashboard"
echo "2. Navigate to your project settings"
echo "3. Add environment variable: OPENAI_API_KEY"
echo "4. Redeploy if needed"
echo ""
echo "🌐 Your app should be live at the URL provided above!" 